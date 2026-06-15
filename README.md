# ThousandEyes AgenticOps Tools

Small Node.js scripts for working with ThousandEyes browser transaction tests and agent cleanup.

## Contents

- `create-thousandeyes-blog-test.mjs`: creates a ThousandEyes web transaction test for the ThousandEyes blog article.
- `thousandeyes-blog-transaction.js`: browser transaction script uploaded into the ThousandEyes test.
- `delete-thousandeyes-agent-safely.mjs`: deletes a named agent only after an explicit confirmation environment variable is set, and writes local snapshots before and after the delete.
- `projects/01-network-automation-node/`: small Node.js network automation examples.
- `projects/02-terraform-provider/`: ThousandEyes Terraform provider starter project.
- `projects/03-mcp-assisted-workflows/`: MCP-assisted ThousandEyes workflow notes.

## Requirements

- Node.js 20 or newer.
- A ThousandEyes bearer token with the required API permissions.
- A ThousandEyes account group ID if your token has access to more than one account group.

## Setup

Copy the example environment file and fill in your local values:

```bash
cp .env.example .env
```

Required values:

```bash
TE_TOKEN=your-token
TE_AID=your-account-group-id
```

Never commit `.env` or bearer tokens to GitHub.

## Commands

Check syntax:

```bash
npm run check
```

List cloud agents from the API:

```bash
npm run agents:list
```

Generate an agent-to-server payload without creating a test:

```bash
npm run payload:agent-to-server
```

Create the blog transaction test:

```bash
npm run create:blog-test
```

Delete an agent safely:

```bash
npm run delete:agent
```

For delete runs, set `AGENT_NAME` and `CONFIRM_DELETE_AGENT` in `.env` to the same exact agent name. The npm scripts load `.env` automatically with Node's `--env-file` flag.

The delete script writes snapshot files under `thousandeyes-delete-agent-snapshots/`. Those files are ignored by Git because they can contain account-specific data.

## GitHub Setup

This folder is intended to be its own Git repository. After reviewing the files:

```bash
git add .
git commit -m "Initial project setup"
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO.git
git push -u origin main
```

If you use GitHub Desktop or VS Code/Copilot, open this folder directly:

```bash
/Users/ssudarsi/Documents/Codex
```
