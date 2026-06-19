# ThousandEyes Endpoint Agents Support Guide

Endpoint Agents provide visibility from user devices and help measure endpoint, network, VPN, proxy, DNS, and real-user experience.

Use this document when customers ask about:

- Retrieving Endpoint Agents.
- Endpoint Agent offline status.
- Missing endpoint data.
- Endpoint Agent assignment.
- Endpoint Agent permissions.
- Endpoint Agent installation or upgrade issues.
- Endpoint Agent visibility in account groups.

## Common Symptoms

- Endpoint Agent is not visible.
- Endpoint Agent appears offline.
- Endpoint data is missing.
- Endpoint Agent data is visible to one user but not another.
- API returns 403 when retrieving Endpoint Agents.
- API returns empty results.
- Device is installed but not reporting.

## Common Causes

- Agent is not installed or not running.
- Device is assigned to a different account group.
- User lacks permission to view endpoint data.
- Endpoint Agent has not checked in recently.
- Network connectivity to ThousandEyes cloud services is blocked.
- Proxy, VPN, DNS, or firewall settings prevent reporting.
- Endpoint Agent version is outdated.
- Data is filtered by account group or query parameter.

## Troubleshooting Checklist

1. Confirm the Endpoint Agent is installed.
2. Confirm the Endpoint Agent service/process is running.
3. Confirm the device has network connectivity.
4. Confirm proxy, VPN, DNS, and firewall behavior.
5. Confirm the user has permission to view Endpoint Agent data.
6. Confirm the account group / aid context.
7. Check whether other users can see the agent.
8. Check whether the device recently changed network, VPN, or policy.
9. Check whether Endpoint Agent was recently upgraded.
10. Compare API output with UI visibility.

## API Troubleshooting Notes

For API requests:

- Confirm the request uses https://api.thousandeyes.com/v7.
- Confirm Authorization: Bearer <TOKEN>.
- Confirm the token belongs to a user with Endpoint Agent visibility.
- Confirm the correct account group / aid context.
- If response is empty, check filters and account group visibility.
- If response is 403, check role, scope, and account group access.
- If response is 404, check endpoint path and object identifier.

## Evidence to Collect

- Endpoint Agent hostname or device identifier.
- User account and account group / aid.
- API method and sanitized URL.
- Response status and response body.
- Timestamp of the request.
- Whether the agent is visible in UI.
- Whether other users can view the agent.
- Endpoint Agent version.
- OS version.
- Network, VPN, proxy, and DNS context.

## Official References

- Endpoint Agents documentation:
  https://docs.thousandeyes.com/product-documentation/global-vantage-points/endpoint-agents

- Endpoint Agents API v7:
  https://developer.cisco.com/docs/thousandeyes/endpoint-agents/
