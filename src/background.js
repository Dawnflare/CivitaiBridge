/**
 * CivitaiBridge — Background Service Worker
 *
 * Core logic for the CivitaiBridge Chrome extension.
 * Handles initialization, declarativeContent rules, context menus,
 * URL parsing, and tab management.
 *
 * References: GitHub Issues #1, #2
 */

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

/**
 * Archive destination definitions.
 * Each entry maps a storage key to its display label and base URL.
 */
const DESTINATIONS = [
  { key: "civarchive",      label: "Open in Civarchive.com",      baseUrl: "https://civarchive.com/models/" },
  { key: "civitaiarchive",  label: "Open in Civitaiarchive.com",  baseUrl: "https://civitaiarchive.com/models/" },
  { key: "civitaired",      label: "Open in Civitai.red",         baseUrl: "https://civitai.red/models/" },
];

/**
 * Default user preferences — all destinations enabled by default.
 */
const DEFAULT_PREFS = Object.fromEntries(
  DESTINATIONS.map((d) => [d.key, true])
);

/**
 * Regex to extract a numeric model ID from a Civitai URL path.
 * Matches "/models/<digits>" and captures the digits.
 */
const MODEL_ID_REGEX = /\/models\/(\d+)/;

/**
 * Valid source domains that the extension activates on.
 */
const SOURCE_HOSTS = ["civitai.com", "civitai.red"];

// ---------------------------------------------------------------------------
// Initialization — runs once on install or update
// ---------------------------------------------------------------------------

chrome.runtime.onInstalled.addListener(async () => {
  // Seed default preferences (only sets keys that don't already exist)
  const existing = await chrome.storage.sync.get(Object.keys(DEFAULT_PREFS));
  const merged = { ...DEFAULT_PREFS, ...existing };
  await chrome.storage.sync.set(merged);

  // Register declarativeContent rules to enable the action icon
  // only on valid Civitai model pages.
  await registerDeclarativeContentRules();

  // Build the right-click context menu checkboxes
  await createContextMenus(merged);
});

// ---------------------------------------------------------------------------
// DeclarativeContent — icon activation on matching pages
// ---------------------------------------------------------------------------

/**
 * Registers page-matching rules that enable the extension action icon
 * when the user navigates to a model page on civitai.com or civitai.red.
 *
 * Called once during onInstalled. Rules persist across service worker restarts.
 */
function registerDeclarativeContentRules() {
  return new Promise((resolve) => {
    // Clear any stale rules before adding fresh ones.
    // Note: removeRules does not return a Promise in MV3, so we must use the callback.
    chrome.declarativeContent.onPageChanged.removeRules(undefined, () => {
      const conditions = SOURCE_HOSTS.map(
        (host) =>
          new chrome.declarativeContent.PageStateMatcher({
            pageUrl: { hostEquals: host, pathPrefix: "/models/" },
          })
      );

      chrome.declarativeContent.onPageChanged.addRules(
        [
          {
            conditions,
            actions: [new chrome.declarativeContent.ShowAction()],
          },
        ],
        () => resolve()
      );
    });
  });
}

// ---------------------------------------------------------------------------
// Context Menus — right-click checkbox toggles
// ---------------------------------------------------------------------------

/**
 * Creates the three checkbox context menu items under the extension icon,
 * plus a disabled item displaying the current keyboard shortcut.
 * Reads current preference state to set the initial checked values.
 *
 * @param {Object} prefs - Current preference values keyed by destination key.
 */
function createContextMenus(prefs) {
  return new Promise((resolve) => {
    // Remove existing items first (idempotent re-creation)
    chrome.contextMenus.removeAll(async () => {
      for (const dest of DESTINATIONS) {
        chrome.contextMenus.create({
          id: dest.key,
          title: dest.label,
          type: "checkbox",
          checked: !!prefs[dest.key],
          contexts: ["action"],
        });
      }

      // Retrieve the current shortcut for the action
      const commands = await chrome.commands.getAll();
      const actionCommand = commands.find(cmd => cmd.name === "_execute_action");
      const shortcutText = actionCommand && actionCommand.shortcut ? actionCommand.shortcut : "Not set";

      // Add a separator and the shortcut info
      chrome.contextMenus.create({
        id: "separator",
        type: "separator",
        contexts: ["action"]
      });

      chrome.contextMenus.create({
        id: "shortcut-info",
        title: `Shortcut: ${shortcutText}`,
        enabled: false,
        contexts: ["action"]
      }, () => resolve());
    });
  });
}

/**
 * Handles context menu checkbox clicks.
 * Toggles the corresponding preference in storage and updates the menu item.
 */
chrome.contextMenus.onClicked.addListener(async (info) => {
  const dest = DESTINATIONS.find((d) => d.key === info.menuItemId);
  if (!dest) return;

  // info.checked already reflects the NEW state after the user clicked
  const newValue = info.checked;

  // Persist to storage
  await chrome.storage.sync.set({ [dest.key]: newValue });

  // Explicitly update the menu item to stay in sync
  chrome.contextMenus.update(dest.key, { checked: newValue });
});

/**
 * When the service worker restarts (e.g., after being idle), context menus
 * are lost. We re-create them using the latest stored preferences.
 *
 * NOTE: chrome.runtime.onStartup fires when the browser profile starts,
 * which covers cold starts. For warm restarts of the service worker itself,
 * context menus registered via onInstalled persist until the browser closes.
 */
chrome.runtime.onStartup.addListener(async () => {
  const prefs = await chrome.storage.sync.get(Object.keys(DEFAULT_PREFS));
  await createContextMenus(prefs);
});

// ---------------------------------------------------------------------------
// Core Action — URL parsing and tab opening
// ---------------------------------------------------------------------------

/**
 * Handles the primary extension action: extracts the model ID from the
 * active tab's URL and opens corresponding archive tabs.
 *
 * Triggered by either:
 *  - Clicking the extension icon (when enabled)
 *  - Pressing the keyboard shortcut (Alt+C by default)
 *
 * Because we use `_execute_action` for the command and `declarativeContent`
 * to disable the action on non-model pages, the keyboard shortcut naturally
 * does nothing on invalid pages — no extra guard needed.
 */
chrome.action.onClicked.addListener(async (tab) => {
  // Extract the model ID from the current tab's URL
  const modelId = extractModelId(tab.url);
  if (!modelId) {
    // Shouldn't happen since the action is disabled on non-model pages,
    // but guard defensively anyway.
    return;
  }

  // Read user preferences
  const prefs = await chrome.storage.sync.get(Object.keys(DEFAULT_PREFS));

  // Determine which destinations to open
  const currentOrigin = new URL(tab.url).origin;
  const urlsToOpen = [];

  for (const dest of DESTINATIONS) {
    if (!prefs[dest.key]) continue;

    const targetUrl = dest.baseUrl + modelId;
    const targetOrigin = new URL(targetUrl).origin;

    // Current Domain Paradox: skip if user is already on this domain
    if (targetOrigin === currentOrigin) continue;

    urlsToOpen.push(targetUrl);
  }

  if (urlsToOpen.length === 0) return;

  // Copy ONLY the first opened URL to the clipboard
  const urlToCopy = urlsToOpen[0];
  try {
    await chrome.scripting.executeScript({
      target: { tabId: tab.id },
      func: (text) => {
        navigator.clipboard.writeText(text).catch(err => console.error("Clipboard copy failed:", err));
      },
      args: [urlToCopy]
    });
  } catch (err) {
    console.error("Scripting injection failed:", err);
  }

  // Open tabs sequentially to the right of the active tab.
  // Each subsequent tab gets index + 1 so they appear in order.
  for (let i = 0; i < urlsToOpen.length; i++) {
    const isLast = i === urlsToOpen.length - 1;
    await chrome.tabs.create({
      url: urlsToOpen[i],
      index: tab.index + 1 + i,
      active: isLast, // Focus lands on the last opened tab
    });
  }
});

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/**
 * Extracts the numeric model ID from a Civitai URL.
 *
 * @param {string} url - The full URL to parse.
 * @returns {string|null} The numeric model ID, or null if not found.
 *
 * @example
 *   extractModelId("https://civitai.com/models/2025388/some-name?v=123")
 *   // => "2025388"
 *
 *   extractModelId("https://civitai.com/images/456")
 *   // => null
 */
function extractModelId(url) {
  if (!url) return null;
  const match = url.match(MODEL_ID_REGEX);
  return match ? match[1] : null;
}
