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
const AGENT_LOCATION = process.env.AGENT_LOCATION || 'Melbourne';

if (!BEARER_TOKEN) {
  throw new Error('Set TE_TOKEN or THOUSANDEYES_TOKEN in .env before running this script.');
}

const response = await teFetch(apiUrl('/agents', { agentTypes: 'cloud' }));
const data = await parseResponse(response);

if (!response.ok) {
  throw new Error(`Failed to list agents: HTTP ${response.status}\n${formatJson(data)}`);
}

const agents = (Array.isArray(data.agents) ? data.agents : [])
  .filter((agent) => {
    const location = String(agent.location || agent.agentName || '').toLowerCase();
    return location.includes(AGENT_LOCATION.toLowerCase());
  })
  .map((agent) => ({
    agentId: String(agent.agentId),
    agentName: agent.agentName,
    location: agent.location,
    countryId: agent.countryId,
    enabled: agent.enabled
  }));

console.log(formatJson({
  accountGroup: ACCOUNT_GROUP_ID || 'token default',
  locationFilter: AGENT_LOCATION,
  count: agents.length,
  agents
}));

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
