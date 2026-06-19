# ThousandEyes Dual Chromium and Chromium 148 Troubleshooting Guide

Use this document when customers report Browser Synthetics or Transaction test failures after Chromium runtime changes, Chromium 148 rollout, or Dual Chromium option changes.

## Common Support Requests

- Transaction test broke after Chromium upgrade.
- Page Load test behaves differently in Chromium 148.
- Script works in one Chromium version but fails in another.
- Click behavior changed.
- Element visibility changed.
- Download, popup, or dialog behavior changed.
- Timing-sensitive script started failing.
- Dual Chromium testing results differ.

## Common Symptoms

- Element not found after browser upgrade.
- Element found but not clickable.
- Page screenshot looks different.
- Login page behaves differently.
- JavaScript execution fails.
- Browser security behavior changed.
- Cross-origin behavior changed.
- Rendering or layout changed.
- Selenium wait no longer works reliably.
- Test passes with one Chromium option and fails with another.

## Common Causes

- Application behavior changed under newer Chromium.
- Browser security policy changed.
- Timing changed due to rendering/runtime differences.
- DOM structure changed because of responsive layout.
- Third-party script behaves differently.
- Test relies on brittle selectors.
- Test relies on fixed sleeps.
- Test uses deprecated browser behavior.
- Test depends on popups, downloads, or dialogs.

## Troubleshooting Checklist

1. Confirm when the failure started.
2. Confirm whether it aligns with Chromium 148 or browser runtime rollout.
3. Compare screenshots from passing and failing runs.
4. Compare HAR and waterfall data.
5. Compare console or script errors if available.
6. Identify the failing step.
7. Check whether the element still exists in the DOM.
8. Check whether the element is visible and clickable.
9. Replace fixed sleeps with explicit waits.
10. Test with the alternate Chromium option if available.
11. Check whether selectors are brittle or layout-dependent.
12. Review ThousandEyes Chromium 148 common issues documentation.

## Recommended Script Adjustments

- Prefer explicit waits.
- Wait for element location, visibility, and clickability.
- Avoid absolute XPath.
- Prefer data-testid or stable CSS selectors.
- Avoid fixed sleeps for page readiness.
- Handle overlays, modals, and cookie banners.
- Verify iframe and shadow DOM behavior.
- Avoid relying on browser-specific timing.

## Evidence to Collect

- Test ID.
- Agent type and location.
- Timestamp of failing run.
- Browser runtime or Dual Chromium option.
- Screenshot from passing and failing run.
- HAR and waterfall data.
- Failing step name.
- Script snippet around failing step.
- Console/script error.
- Whether issue reproduces in another Chromium option.
- Whether issue started after application or browser change.

## Official References

- Chromium v148 Common Issues:
  https://docs.thousandeyes.com/product-documentation/browser-synthetics/dual-chromium-option/chromium-148-common-issues

- Dual Chromium Option:
  https://docs.thousandeyes.com/product-documentation/browser-synthetics/dual-chromium-option

- Working With Dual Chromium:
  https://docs.thousandeyes.com/product-documentation/browser-synthetics/dual-chromium-option/working-with-dual-chromium
