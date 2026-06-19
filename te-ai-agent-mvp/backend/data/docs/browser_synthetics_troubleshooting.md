# ThousandEyes Browser Synthetics Troubleshooting Guide

Use this document when customers report Browser Synthetics issues involving Page Load tests, Transaction tests, browser rendering, screenshots, DOM behavior, page timing, or failed user journeys.

## Common Support Requests

- Page Load test failures.
- Transaction test failures.
- Browser page did not render correctly.
- Screenshot does not match expected page.
- Page timed out.
- Element was not visible.
- JavaScript application did not finish rendering.
- Browser Synthetics result differs from manual browser test.

## Common Causes

- Page loaded slowly from selected agent.
- JavaScript bundle failed to load.
- API call required for rendering failed.
- Third-party resource delayed or blocked rendering.
- Login or redirect flow changed.
- Cookie banner, modal, or overlay blocked interaction.
- Browser runtime changed.
- Application changed DOM structure.
- Enterprise Agent network path differs from user machine.
- Cloud Agent location has different latency or routing.

## Troubleshooting Checklist

1. Compare successful and failed runs.
2. Review screenshots for each step.
3. Review page timing.
4. Review HAR and waterfall data.
5. Check DNS, connect, SSL, wait, and receive timing.
6. Look for HTTP 4xx or 5xx responses.
7. Check JavaScript bundle loading.
8. Check API calls required for rendering.
9. Check login redirects.
10. Check third-party dependencies.
11. Confirm whether issue is agent-specific.
12. Confirm whether issue started after browser/runtime change.

## Screenshot Analysis

Screenshots can show:

- Page did not load.
- Page loaded partially.
- Login prompt appeared.
- Captcha or MFA appeared.
- Cookie banner blocked action.
- Spinner stayed on screen.
- Error page appeared.
- Application route changed.

## DOM and Rendering Issues

If the page appears blank or incomplete:

- Check whether JavaScript bundle loaded.
- Check whether required API calls succeeded.
- Check whether CORS, auth, or session issues occurred.
- Check whether third-party scripts failed.
- Check whether SPA route changed.
- Check HAR/waterfall for blocked resources.

## Agent-Specific Investigation

If issue occurs only on some agents:

- Compare Cloud Agent and Enterprise Agent runs.
- Compare geographic locations.
- Check DNS resolution.
- Check proxy, firewall, VPN, and routing.
- Check whether the application blocks certain regions or IP ranges.
- Check TLS/SSL negotiation behavior.

## Evidence to Collect

- Test ID.
- Agent name and type.
- Timestamp.
- Failing step.
- Screenshot.
- HAR or waterfall data.
- Console or script error if available.
- Successful comparison run.
- Browser runtime or Dual Chromium option.
- Account group / aid.
