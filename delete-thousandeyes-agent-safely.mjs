import { mkdir, writeFile } from 'node:fs/promises';

const API_BASE_URL =
  process.env.THOUSANDEYES_API_BASE_URL ||
  process.env.THOU_SANDEYES_API_BASE_URL ||
  'https://api.thousandeyes.com/v7';
const BEARER_TOKEN =
  process.env.THOU_SANDEYES_TOKEN ||
  process.env.THOUSANDEYES_TOKEN ||
  process.env.TE_BEARER_TOKEN ||
  process.env.BEARER_TOKEN;
const ACCOUNT_GROUP_ID =
  process.env.THOUSANDEYES_AID ||
  process.env.THOU_SANDEYES_AID ||
  process.env.TE_AID;

const AGENT_NAME = process.env.AGENT_NAME || 'thousandeyes-va-907056';
const AGENT_ID = process.env.AGENT_ID;
const TEST_NAME =
  process.env.TEST_NAME ||
  'API agent-to-server test addition for www.thousandeyes.com';
const TEST_TYPES = [
  'agent-to-server',
  'agent-to-agent',
  'http-server',
  'page-load',
  'web-transactions',
  'api',
  'dns-server',
  'dns-trace',
  'dnssec',
  'ftp-server',
  'sip-server',
  'voice'
];
const CONFIRM_DELETE_AGENT = process.env.CONFIRM_DELETE_AGENT;

if (!BEARER_TOKEN) {
  throw new Error(
    'Set THOUSANDEYES_TOKEN, THOU_SANDEYES_TOKEN, TE_BEARER_TOKEN, or BEARER_TOKEN before running this script.'
  );
}

if (CONFIRM_DELETE_AGENT !== AGENT_NAME) {
  throw new Error(
    `Refusing to delete. Set CONFIRM_DELETE_AGENT="${AGENT_NAME}" to confirm the exact agent name.`
  );
}

const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
const snapshotDir = new URL(`./thousandeyes-delete-agent-snapshots/${timestamp}/`, import.meta.url);

await mkdir(snapshotDir, { recursive: true });

const agent = AGENT_ID ? await getAgentById(AGENT_ID) : await findAgentByName(AGENT_NAME);
const beforeAgent = await getAgentExpanded(agent.agentId);
const beforeTest = await findAgentToServerTest(TEST_NAME);

await writeSnapshot('before-agent.json', beforeAgent);
await writeSnapshot('before-test.json', beforeTest);

assertTargetAgent(beforeAgent, AGENT_NAME);

console.log(`Deleting agent ${beforeAgent.agentName} (${beforeAgent.agentId}) from ${accountGroupDescription()}...`);

const deleteResponse = await teFetch(apiUrl(`/agents/${beforeAgent.agentId}`), {
  method: 'DELETE'
});
const deleteBody = await parseResponse(deleteResponse);

await writeSnapshot('delete-response.json', deleteBody);

if (!deleteResponse.ok) {
  throw new Error(`Failed to delete agent: HTTP ${deleteResponse.status}\n${formatJson(deleteBody)}`);
}

const afterAgent = await getAgentAfterDelete(beforeAgent.agentId);
const afterTest = await findAgentToServerTest(TEST_NAME);
const activityLog = await getRecentActivityLog();

await writeSnapshot('after-agent.json', afterAgent);
await writeSnapshot('after-test.json', afterTest);
await writeSnapshot('activity-log-24h.json', activityLog);

console.log('Delete completed.');
console.log(`Snapshots: ${snapshotDir.pathname}`);
console.log(`Deleted agent: ${beforeAgent.agentName} (${beforeAgent.agentId})`);
console.log(`Test checked: ${TEST_NAME}`);
console.log(`Agent endpoint after delete: HTTP ${afterAgent.status}`);

async function findAgentByName(agentName) {
  const data = await teGet('/agents');
  const agents = Array.isArray(data.agents) ? data.agents : [];
  const matches = agents.filter((candidate) => candidate.agentName === agentName);

  if (matches.length === 0) {
    throw new Error(`No agent named "${agentName}" was found in ${accountGroupDescription()}.`);
  }

  if (matches.length > 1) {
    throw new Error(
      `Found ${matches.length} agents named "${agentName}". Re-run with AGENT_ID set to the intended agentId.`
    );
  }

  return matches[0];
}

async function getAgentById(agentId) {
  const data = await teGet(`/agents/${agentId}`);
  return normalizeSingleResource(data, 'agent');
}

async function getAgentExpanded(agentId) {
  const expanded = await teGet(`/agents/${agentId}`, { expand: 'test' });
  return normalizeSingleResource(expanded, 'agent');
}

async function getAgentAfterDelete(agentId) {
  const response = await teFetch(apiUrl(`/agents/${agentId}`, { expand: 'test' }));
  const body = await parseResponse(response);

  return {
    status: response.status,
    ok: response.ok,
    body
  };
}

async function findAgentToServerTest(testName) {
  const results = [];
  const errors = [];

  for (const testType of TEST_TYPES) {
    try {
      const data = await teGet(`/tests/${testType}`);
      const tests = Array.isArray(data.tests) ? data.tests : [];

      for (const test of tests) {
        if (test.testName === testName) {
          return {
            found: true,
            searchedTypes: TEST_TYPES,
            matchedType: testType,
            ...test
          };
        }

        if (String(test.testName || '').toLowerCase().includes('www.thousandeyes.com')) {
          results.push({
            matchedType: testType,
            ...pick(test, ['testId', 'testName', 'type', 'agents', 'server'])
          });
        }
      }
    } catch (error) {
      errors.push({
        testType,
        error: error.message
      });
    }
  }

  return {
    found: false,
    testName,
    searchedTypes: TEST_TYPES,
    testsWithSimilarNames: results,
    errors
  };
}

async function getRecentActivityLog() {
  try {
    return await teGet('/audit-user-events', { window: '24h' });
  } catch (error) {
    return {
      warning: 'Could not retrieve activity log. The token may not have activity log permission.',
      error: error.message
    };
  }
}

async function teGet(path, params = {}) {
  const response = await teFetch(apiUrl(path, params));
  const body = await parseResponse(response);

  if (!response.ok) {
    throw new Error(`GET ${path} failed: HTTP ${response.status}\n${formatJson(body)}`);
  }

  return body;
}

async function teFetch(url, options = {}) {
  return fetch(url, {
    ...options,
    headers: {
      accept: 'application/hal+json, application/json',
      authorization: `Bearer ${BEARER_TOKEN}`,
      ...(options.headers || {})
    }
  });
}

function apiUrl(path, params = {}) {
  const url = new URL(path.replace(/^\//, ''), API_BASE_URL.endsWith('/') ? API_BASE_URL : `${API_BASE_URL}/`);

  if (ACCOUNT_GROUP_ID) {
    url.searchParams.set('aid', ACCOUNT_GROUP_ID);
  }

  for (const [key, value] of Object.entries(params)) {
    url.searchParams.set(key, value);
  }

  return url;
}

async function parseResponse(response) {
  const text = await response.text();

  if (!text) {
    return {};
  }

  try {
    return JSON.parse(text);
  } catch (_error) {
    return text;
  }
}

function normalizeSingleResource(data, resourceName) {
  if (Array.isArray(data.agents) && data.agents.length === 1) {
    return data.agents[0];
  }

  if (data && typeof data === 'object' && !Array.isArray(data)) {
    return data;
  }

  throw new Error(`Unexpected ${resourceName} response shape:\n${formatJson(data)}`);
}

function assertTargetAgent(agent, expectedName) {
  if (agent.agentName !== expectedName) {
    throw new Error(`Refusing to delete agent "${agent.agentName}". Expected "${expectedName}".`);
  }

  const state = String(agent.agentState || '').toLowerCase();
  if (state && state !== 'offline' && state !== 'disabled') {
    console.warn(`Warning: agent state is "${agent.agentState}", not offline/disabled.`);
  }
}

async function writeSnapshot(filename, data) {
  await writeFile(new URL(filename, snapshotDir), `${formatJson(data)}\n`);
}

function accountGroupDescription() {
  return ACCOUNT_GROUP_ID ? `AID ${ACCOUNT_GROUP_ID}` : 'the token default account group';
}

function formatJson(value) {
  return typeof value === 'string' ? value : JSON.stringify(value, null, 2);
}

function pick(object, keys) {
  return Object.fromEntries(keys.map((key) => [key, object?.[key]]));
}
