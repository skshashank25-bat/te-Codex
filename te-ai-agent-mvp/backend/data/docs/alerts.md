# ThousandEyes Alerts Support Guide

ThousandEyes alerts notify users when test or network conditions match configured alert rules.

Use this document when customers ask about:

- Retrieving alerts.
- Retrieving alert rules.
- Alert not triggering.
- Alert triggered but notification not delivered.
- Alert rule thresholds.
- Alert history.
- Alert API errors.
- Account group visibility for alerts.

## Common Symptoms

- Alert did not trigger.
- Alert triggered late.
- Alert notification was not delivered.
- Alert appears in UI but not API.
- API returns 403 when retrieving alerts or alert rules.
- API returns empty alert list.
- Alert rule exists but does not apply to expected test.

## Common Causes

- Test results did not meet alert rule criteria.
- Alert rule is disabled.
- Alert rule is assigned to a different test.
- Notification channel is misconfigured.
- User lacks access to the account group.
- Alert rule threshold is too strict or too loose.
- Alert suppression or maintenance window is active.
- API query uses wrong account group / aid.
- Alert already cleared before the customer checked.

## Troubleshooting Checklist

1. Confirm the alert rule is enabled.
2. Confirm the alert rule is assigned to the expected test.
3. Confirm the test result actually crossed the threshold.
4. Review alert history.
5. Verify notification channel configuration.
6. Confirm recipients, webhook, email, or integration settings.
7. Check for maintenance windows or suppression.
8. Confirm account group / aid context.
9. Compare UI alert visibility with API output.
10. Check customer role and permissions.

## API Troubleshooting Notes

For alert-related API requests:

- Confirm the request uses https://api.thousandeyes.com/v7.
- Confirm Authorization: Bearer <TOKEN>.
- Confirm the correct endpoint for alerts or alert rules.
- Confirm account group / aid context.
- If response is 403, check role, scope, and account group access.
- If response is empty, check account group and query filters.
- If response is 404, check object ID and endpoint path.
- If response is 429, honor Retry-After and add backoff.

## Evidence to Collect

- Alert rule ID.
- Test ID.
- Account group / aid.
- Alert start and clear timestamp.
- API method and sanitized URL.
- Response status and response body.
- UI screenshot of alert history if available.
- Notification channel configuration.
- Expected threshold and observed test result.
- Whether maintenance or suppression was active.

## Official References

- Alerts API v7:
  https://developer.cisco.com/docs/thousandeyes/alert/

- Alert Rules API v7:
  https://developer.cisco.com/docs/thousandeyes/alert-rules/
