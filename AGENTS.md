# AGENTS.md

## Project

This repository contains Node.js scripts for ThousandEyes API workflows and browser transaction tests.

## Safety

- Do not commit `.env`, bearer tokens, account-specific snapshots, or other credentials.
- Keep account group IDs and API tokens in environment variables.
- Treat `delete-thousandeyes-agent-safely.mjs` as destructive. Preserve its exact-name confirmation check.
- Snapshot files under `thousandeyes-delete-agent-snapshots/` are local evidence and should remain ignored by Git.

## Commands

- `npm run check`: syntax-check the scripts.
- `npm run create:blog-test`: create the blog transaction test.
- `npm run delete:agent`: run the guarded delete flow.

## Style

- Keep scripts dependency-light and readable.
- Prefer explicit environment variables over hard-coded account-specific values.
- Add comments only for behavior that is not obvious from the code.
