# ThousandEyes Transaction Tests Debugging Guide

Transaction Tests simulate real user workflows using JavaScript and Selenium WebDriver in Browser Synthetics.

Use this document when customers ask for help with transaction test failures, Selenium JavaScript errors, browser automation issues, element not found errors, timeout errors, login workflow failures, Chromium version behavior changes, HAR, waterfall investigation, XPath, selectors, and scripting assistance.

Important troubleshooting topics:

- Chromium 148 common issues
- Dual Chromium behavior
- Selenium JavaScript waits
- CSS selectors
- XPath helpers
- HAR and waterfall debugging
- Page elements
- Browser console errors
- Network dependency failures
- Login redirects
- Credential repository issues

Official references:

- ThousandEyes Chromium v148 Common Issues: https://docs.thousandeyes.com/product-documentation/browser-synthetics/dual-chromium-option/chromium-148-common-issues
- ThousandEyes Dual Chromium Option: https://docs.thousandeyes.com/product-documentation/browser-synthetics/dual-chromium-option
- ThousandEyes Transaction Scripting Reference: https://docs.thousandeyes.com/product-documentation/browser-synthetics/transaction-tests/transaction-scripting-reference
- Selenium WebDriver: https://www.selenium.dev/documentation/webdriver/
- Selenium Locators: https://www.selenium.dev/documentation/webdriver/elements/locators/
- Selenium Waits: https://www.selenium.dev/documentation/webdriver/waits/
- MDN document.evaluate XPath: https://developer.mozilla.org/en-US/docs/Web/API/Document/evaluate

## HAR and Waterfall Debugging

Use HAR and waterfall data to check slow DNS, TCP connect, TLS, wait, receive time, blocked requests, redirects, 4xx/5xx responses, third-party script failures, JavaScript bundles, API calls required for rendering, login redirects, and authentication/session endpoints.

## XPath and Selector Help

Prefer stable IDs, data-testid attributes, name attributes, and stable CSS selectors. Use XPath carefully when CSS cannot target the element reliably.

Example XPath:

By.xpath("//button[contains(normalize-space(), 'Sign in')]")

Browser console XPath helper:

$x("//button[contains(normalize-space(), 'Sign in')]")

## Selenium JavaScript Best Practices

Use async/await consistently. Use explicit waits. Wait for elements to be located, visible, and interactable before clicking or typing. Avoid fixed sleeps unless no reliable page condition exists.

## Chromium 148 Investigation

Use Chromium 148 or Dual Chromium guidance when failures start after browser runtime changes. Review screenshots, HAR/waterfall, failing step timing, console/script errors, browser option, agent type, and successful-vs-failed runs.
