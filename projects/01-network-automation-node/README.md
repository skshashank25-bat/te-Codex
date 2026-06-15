# Network Automation with Node.js

This mini-project keeps network automation small and inspectable. The scripts use Node.js built-in `fetch`, read `.env` through the root npm scripts, and avoid dependencies.

## Commands

From the repository root:

```bash
npm run agents:list
npm run payload:agent-to-server
```

## Environment

Set these values in the root `.env` file:

```bash
TE_TOKEN=your-token
TE_AID=your-account-group-id
AGENT_LOCATION=Melbourne
TARGET_SERVER=www.thousandeyes.com
TARGET_PORT=443
CREATE_TEST=false
```

`payload:agent-to-server` prints the JSON payload by default. It creates a real ThousandEyes test only when `CREATE_TEST=true`.

## Safety

- Keep `CREATE_TEST=false` while learning.
- Review the printed payload before changing anything in ThousandEyes.
- Do not commit `.env` or API output containing account-specific data.
