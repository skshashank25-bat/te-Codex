import assert from 'assert';
import { By, until } from 'selenium-webdriver';
import { driver, markers, test, transaction } from 'thousandeyes';

const BLOG_URL = 'https://www.thousandeyes.com/blog/';
const ARTICLE_PATH = '/blog/agentic-ops-when-ai-monitors-ai-via-mcp';
const ARTICLE_URL = `https://www.thousandeyes.com${ARTICLE_PATH}`;
const ARTICLE_TITLE = 'Cisco ThousandEyes AgenticOps: When AI Monitors AI via MCP';

runScript();

async function runScript() {
  await configureDriver();
  transaction.start();

  const settings = test.getSettings();
  const startUrl = normalizeUrl(settings.url || BLOG_URL);

  markers.start('Load blog landing page');
  await driver.get(startUrl);
  await waitForDocumentReady();
  await dismissOptionalOverlays();
  await driver.wait(until.urlContains('/blog'), 30000, 'Blog landing page did not load');
  await driver.takeScreenshot();
  markers.stop('Load blog landing page');

  markers.start('Navigate to AgenticOps MCP article');
  const clickedArticleLink = await clickArticleLinkIfPresent();

  if (!clickedArticleLink) {
    await driver.get(ARTICLE_URL);
  }

  await waitForDocumentReady();
  await driver.wait(
    until.urlContains(ARTICLE_PATH),
    30000,
    `Browser did not navigate to ${ARTICLE_PATH}`
  );

  const heading = await driver.wait(
    until.elementLocated(By.xpath("//h1[contains(normalize-space(.), 'Cisco ThousandEyes AgenticOps')]")),
    30000,
    'Article heading was not found'
  );
  await driver.wait(until.elementIsVisible(heading), 30000);

  const headingText = await heading.getText();
  assert(
    headingText.includes(ARTICLE_TITLE),
    `Unexpected article heading: ${headingText}`
  );

  await driver.takeScreenshot();
  markers.stop('Navigate to AgenticOps MCP article');
  transaction.stop();
}

async function configureDriver() {
  const settings = test.getSettings();
  const timeoutMs = Math.max((settings.timeout || 30) * 1000, 30000);

  await driver.manage().setTimeouts({
    implicit: Math.min(timeoutMs / 2, 15000),
    pageLoad: timeoutMs,
    script: 30000
  });
}

function normalizeUrl(url) {
  const value = String(url || BLOG_URL).trim();
  return /^https?:\/\//i.test(value) ? value : `https://${value}`;
}

async function waitForDocumentReady(timeoutMs = 30000) {
  await driver.wait(async () => {
    const readyState = await driver.executeScript('return document.readyState');
    return readyState === 'interactive' || readyState === 'complete';
  }, timeoutMs, 'Document did not become ready');
}

async function dismissOptionalOverlays() {
  const selectors = [
    '#onetrust-accept-btn-handler',
    'button[aria-label="Close"]',
    'button[title="Close"]',
    '[aria-label="Close"]'
  ];

  for (const selector of selectors) {
    const elements = await driver.findElements(By.css(selector));

    for (const element of elements) {
      try {
        if (await element.isDisplayed()) {
          await element.click();
          await driver.sleep(500);
          return;
        }
      } catch (_error) {
        // Overlay controls can disappear while the page finishes rendering.
      }
    }
  }

  const clicked = await driver.executeScript(() => {
    const labels = ['accept all', 'accept cookies', 'agree', 'got it'];
    const controls = Array.from(document.querySelectorAll('button, a'));
    const control = controls.find((candidate) => {
      const text = (candidate.textContent || '').trim().toLowerCase();
      return labels.includes(text);
    });

    if (!control) {
      return false;
    }

    control.click();
    return true;
  });

  if (clicked) {
    await driver.sleep(500);
  }
}

async function clickArticleLinkIfPresent() {
  for (let attempt = 0; attempt < 8; attempt++) {
    const link = await findDisplayedArticleLink();

    if (link) {
      await driver.executeScript(
        'arguments[0].scrollIntoView({ block: "center", inline: "center" });',
        link
      );
      await driver.sleep(300);

      try {
        await link.click();
      } catch (_error) {
        await driver.executeScript('arguments[0].click();', link);
      }

      return true;
    }

    await driver.executeScript('window.scrollBy(0, Math.max(window.innerHeight * 0.8, 600));');
    await driver.sleep(1000);
  }

  return false;
}

async function findDisplayedArticleLink() {
  const selectors = [
    By.css(`a[href*="${ARTICLE_PATH}"]`),
    By.xpath("//a[contains(normalize-space(.), 'Cisco ThousandEyes AgenticOps')]")
  ];

  for (const selector of selectors) {
    const links = await driver.findElements(selector);

    for (const link of links) {
      try {
        if (await link.isDisplayed()) {
          return link;
        }
      } catch (_error) {
        // Ignore stale or detached links while dynamic cards are loading.
      }
    }
  }

  return null;
}
