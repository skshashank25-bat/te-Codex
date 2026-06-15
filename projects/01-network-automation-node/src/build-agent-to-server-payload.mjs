const API_BASE_URL =
  process.env.THOUSANDEYES_API_BASE_URL ||
  process.env.THOU_SANDEYES_API_BASE_URL ||
  'https://api.thousandeyes.com/v7';
const BEARER_TOKEN =
  process.env.TE_TOKEN ||
  process.env.THOU_SANDEYES_TOKEN ||
  process.env.THOUSANDEYES_TOKEN ||
  process.env.TE_BEARER_TOKEN ||
  process.env.BEARER_TOKEN;
const ACCOUNT_GROUP_ID =
  process.env.TE_AID ||
  process.env.THOUSANDEYES_AID ||
  process.env.THOU_SANDEYES_AID;

const TEST_NAME = process.env.TEST_NAME || 'GitHub Playground - Agent to Server';
const TARGET_SERVER = process.env.TARGET_SERVER || 'www.thousandeyes.com';
const TARGET_PORT = Number(process.env.TARGET_PORT || 443);
const AGENT_ID = process.env.AGENT_ID;
const AGENT_LOCATION = process.env.AGENT_LOCATION || 'Melbourne';
const CREATE_TEST = String(process.env.CREATE_TEST || 'false').toLowerCase() === 'true';

if (!BEARER_TOKEN) {
  throw new Error('Set TE_TOKEN or THOUSANDEYES_TOKEN in .env before running this script.');
}

const agentId = AGENT_ID || await findFirstCloudAgentId(AGENT_LOCATION);
const payload = {
  testName: TEST_NAME,
  interval: 300,
  agents: [{ agentId: String(agentId) }],
  server: TARGET_SERVER,
  port: TARGET_PORT,
  protocol: 'tcp',
  networkMeasurements: true,
  alertsEnabled: false,
  enabled: true
};

if (!CREATE_TEST) {
  console.log(formatJson({
    dryRun: true,
    message: 'Set CREATE_TEST=true to create this ThousandEyes test.',
    payload
  }));
} else {
  const response = await teFetch(apiUrl('/tests/agent-to-server'), {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(payload)
  });
  const body = await parseResponse(response);

  if (!response.ok) {
    throw new Error(`Failed to create agent-to-server test: HTTP ${response.status}\n${formatJson(body)}`);
  }

  console.log(formatJson({
    created: true,
    testId: body.testId,
    testName: body.testName || TEST_NAME
  }));
}

async function findFirstCloudAgentId(locationFilter) {
  const response = await teFetch(apiUrl('/agents', { agentTypes: 'cloud' }));
  const data = await parseResponse(response);

  if (!response.ok) {
    throw new Error(`Failed to list agents: HTTP ${response.status}\n${formatJson(data)}`);
  }

  const agents = Array.isArray(data.agents) ? data.agents : [];
  const match = agents.find((agent) => {
    const location = String(agent.location || agent.agentName || '').toLowerCase();
    return location.includes(locationFilter.toLowerCase());
  });

  if (!match) {
    throw new Error(`No cloud agent matched AGENT_LOCATION="${locationFilter}". Set AGENT_ID explicitly.`);
  }

  return match.agentId;
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
