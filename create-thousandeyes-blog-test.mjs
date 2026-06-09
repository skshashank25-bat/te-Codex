import { readFile } from 'node:fs/promises';

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

const TEST_NAME =
  process.env.TEST_NAME ||
  'Blog Transaction - AgenticOps MCP';
const TEST_URL = 'https://www.thousandeyes.com/blog/';
const TRANSACTION_SCRIPT_PATH = new URL('./thousandeyes-blog-transaction.js', import.meta.url);

if (!BEARER_TOKEN) {
  throw new Error(
    'Set THOUSANDEYES_TOKEN, THOU_SANDEYES_TOKEN, TE_BEARER_TOKEN, or BEARER_TOKEN before running this script.'
  );
}

const melbourneAgent = await findMelbourneCloudAgent();
const transactionScript = await readFile(TRANSACTION_SCRIPT_PATH, 'utf8');

const payload = {
  testName: TEST_NAME,
  description: 'Starts on the ThousandEyes blog landing page and navigates to the AgenticOps MCP article.',
  url: TEST_URL,
  interval: 300,
  agents: [{ agentId: String(melbourneAgent.agentId) }],
  enabled: true,
  alertsEnabled: false,
  bandwidthMeasurements: false,
  networkMeasurements: true,
  protocol: 'tcp',
  targetTime: 30,
  timeLimit: 90,
  pageLoadingStrategy: 'normal',
  transactionScript
};

const createUrl = apiUrl('/tests/web-transactions');
const response = await teFetch(createUrl, {
  method: 'POST',
  headers: { 'content-type': 'application/json' },
  body: JSON.stringify(payload)
});

const createdTest = await parseResponse(response);

if (!response.ok) {
  throw new Error(`Failed to create transaction test: HTTP ${response.status}\n${formatJson(createdTest)}`);
}

console.log(`Created ThousandEyes transaction test: ${createdTest.testName || TEST_NAME}`);
console.log(`Test ID: ${createdTest.testId}`);
console.log(`Agent: ${melbourneAgent.agentName} (${melbourneAgent.agentId})`);
console.log(`Location: ${melbourneAgent.location || 'unknown'}`);

async function findMelbourneCloudAgent() {
  const response = await teFetch(apiUrl('/agents', { agentTypes: 'cloud' }));
  const data = await parseResponse(response);

  if (!response.ok) {
    throw new Error(`Failed to list agents: HTTP ${response.status}\n${formatJson(data)}`);
  }

  const agents = Array.isArray(data.agents) ? data.agents : [];
  const matches = agents.filter((agent) => {
    const name = String(agent.agentName || '').toLowerCase();
    const location = String(agent.location || '').toLowerCase();
    const type = String(agent.agentType || '').toLowerCase();

    return type === 'cloud' && (name.includes('melbourne') || location.includes('melbourne'));
  });

  if (matches.length === 0) {
    throw new Error('No Melbourne cloud agent was returned by /v7/agents for the configured account group.');
  }

  const exactMatch = matches.find((agent) => {
    const name = String(agent.agentName || '').toLowerCase();
    const location = String(agent.location || '').toLowerCase();
    return name === 'melbourne' || location === 'melbourne';
  });

  return exactMatch || matches[0];
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

function formatJson(value) {
  return typeof value === 'string' ? value : JSON.stringify(value, null, 2);
}
