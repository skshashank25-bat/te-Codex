# MCP-Assisted ThousandEyes Workflows

This project folder documents how to use the ThousandEyes MCP server as a discovery and validation assistant while keeping durable infrastructure in Git.

## Read-Only Discovery Flow

Use MCP tools to inspect current ThousandEyes state before writing Terraform or scripts:

1. `get_account_groups`: choose the account group scope.
2. `list_cloud_enterprise_agents`: find source agents by location, type, and enabled state.
3. `list_network_app_synthetics_tests`: check whether a similar test already exists.
4. `get_network_app_synthetics_test`: inspect a known test before modeling it in code.
5. `get_network_app_synthetics_metrics`: inspect recent performance data before changing monitoring.
6. `get_full_path_visualization`: troubleshoot path-level details for network tests.

Do not commit live MCP output unless it has been reviewed and sanitized.

## Write Flow

For persistent monitoring, prefer this order:

1. Discover agents and existing tests with MCP.
2. Prototype in Node.js with dry-run payloads.
3. Move durable tests into Terraform.
4. Run `terraform plan`.
5. Apply only after reviewing the plan.
6. Commit the Terraform code, not local state or secrets.

MCP write tools such as `create_synthetic_test`, `update_synthetic_test`, `delete_synthetic_test`, and `deploy_template` should be treated as live changes. Use them only after an explicit confirmation step.

## Example Prompts

```text
List enabled Melbourne cloud agents and summarize the IDs without committing them.
```

```text
Find existing HTTP server tests targeting www.thousandeyes.com and tell me whether a Terraform resource would duplicate anything.
```

```text
Inspect test 12345 as type agent-to-server and suggest Terraform variables to model it.
```

```text
Run an instant agent-to-server check from agent <agent-id> to www.thousandeyes.com:443, then summarize latency and loss.
```

For instant tests, confirm the target and agents first because the test executes immediately.
