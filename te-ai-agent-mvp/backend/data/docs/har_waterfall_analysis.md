# HAR and Waterfall Analysis Guide

Use this document when customers ask about HAR files, waterfall charts, page elements, page load timing, slow resources, blocked resources, redirects, or why a Transaction or Page Load test failed during page rendering.

## Common Support Requests

- Review HAR or waterfall data.
- Identify slow page elements.
- Find which request delayed page load.
- Troubleshoot page timeout.
- Troubleshoot missing UI elements.
- Compare successful and failed runs.
- Understand DNS, connect, SSL, wait, receive, and content download timing.
- Find failed HTTP requests such as 401, 403, 404, 429, 500, or 503.
- Identify third-party dependency issues.
- Investigate login redirects or session calls.

## What HAR and Waterfall Data Can Show

HAR and waterfall data can help identify:

- Slow DNS lookup.
- Slow TCP connection.
- Slow TLS/SSL negotiation.
- High time to first byte.
- Slow content download.
- Redirect chains.
- Blocked or stalled requests.
- HTTP 4xx and 5xx responses.
- Missing JavaScript bundles.
- Failed CSS, image, font, or API resources.
- Third-party scripts delaying rendering.
- Authentication or session endpoints failing.
- API calls required before the DOM renders.
- Resources loaded after the script tried to click or type.

## Timing Fields to Review

DNS time:

- High DNS time may indicate DNS resolver, geography, or network path issue.

Connect time:

- High connect time may indicate network latency, routing, firewall, or server reachability issue.

SSL/TLS time:

- High SSL time may indicate certificate, TLS negotiation, inspection, or network delay.

Wait / TTFB:

- High wait time may indicate backend application or origin server slowness.

Receive / Content Download:

- High receive time may indicate large asset size, bandwidth, or transfer issue.

Blocked / Stalled:

- May indicate browser connection limits, prioritization, proxy behavior, or resource contention.

## Transaction Test Debugging Workflow

1. Identify the failing transaction step.
2. Review the screenshot for that step.
3. Open HAR or waterfall data.
4. Look for red or failed requests.
5. Check whether required JavaScript bundles loaded.
6. Check whether API calls needed for rendering succeeded.
7. Check login redirect chain.
8. Compare the same step in a successful run.
9. Identify whether the missing element depends on a delayed or failed resource.
10. Adjust Selenium waits to wait for the actual UI condition.

## Common Findings

### JavaScript Bundle Failed

Symptoms:

- Blank page.
- Spinner never disappears.
- UI element never appears.
- Console error may be present.

Action:

- Find failed JS request.
- Check response code.
- Check CDN or third-party dependency.
- Compare successful run.

### API Call Failed

Symptoms:

- Page shell loads but data is missing.
- Button, table, or dashboard does not appear.
- Application shows error state.

Action:

- Identify failed XHR/fetch request.
- Check status code.
- Check authentication/session behavior.
- Check account or permission context.

### Redirect Chain Problem

Symptoms:

- Login page loops.
- Session not established.
- Final page never loads.

Action:

- Review redirect sequence.
- Check 302/301 responses.
- Check cookies/session requests.
- Check identity provider behavior.

### Third-Party Dependency Slow or Failed

Symptoms:

- Page renders slowly.
- Script times out.
- Specific widget or login component missing.

Action:

- Identify third-party domain.
- Check timing and status code.
- Compare affected and unaffected agents.
- Check if domain is blocked by network policy.

## HAR and Selenium Wait Relationship

If HAR shows a required API call or JS bundle finishing late, the script should wait for the resulting UI condition, not just page navigation.

Better:

```javascript
const element = await driver.wait(
  until.elementLocated(By.css('[data-testid="ready-state"]')),
  15000
);
await driver.wait(until.elementIsVisible(element), 15000);

Avoid:

await driver.sleep(15000);
Evidence to Collect
Test ID.
Agent name and type.
Timestamp.
Step name.
Screenshot.
HAR file or waterfall screenshot.
Failed request URL/domain.
Failed request status code.
Timing fields for slow request.
Successful comparison run.
Script snippet around failing step.
Account group / aid.
