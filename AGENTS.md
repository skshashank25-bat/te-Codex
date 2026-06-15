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
- `npm run terraform:fmt:check`: check Terraform formatting.
- `npm run create:blog-test`: create the blog transaction test.
- `npm run delete:agent`: run the guarded delete flow.
- `npm run agents:list`: list cloud agents by location.
- `npm run payload:agent-to-server`: generate a dry-run agent-to-server payload.

## Style

- Keep scripts dependency-light and readable.
- Prefer explicit environment variables over hard-coded account-specific values.
- Keep Terraform state, `.terraform/`, and local `*.tfvars` files out of Git.
- Add comments only for behavior that is not obvious from the code.
