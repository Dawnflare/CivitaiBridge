/**
 * CivitaiBridge — Options Page Script
 *
 * Manages the settings page checkboxes. Reads initial state from
 * chrome.storage.sync and writes changes back on toggle.
 * Listens for external storage changes (e.g., from context menu toggles)
 * to keep the UI in sync.
 *
 * Reference: GitHub Issue #3
 */

/**
 * Destination keys — must match the keys used in background.js.
 */
const DESTINATION_KEYS = ["civarchive", "civitaiarchive", "civitaired"];

/**
 * References to the checkbox DOM elements.
 * @type {Object.<string, HTMLInputElement>}
 */
const checkboxes = {};

/**
 * Reference to the status message element for save feedback.
 * @type {HTMLElement}
 */
const statusEl = document.getElementById("status");

/**
 * Timer ID for hiding the status message after a brief delay.
 * @type {number|null}
 */
let statusTimer = null;

// ---------------------------------------------------------------------------
// Initialization
// ---------------------------------------------------------------------------

/**
 * On page load, cache checkbox references and set their initial state
 * from storage.
 */
document.addEventListener("DOMContentLoaded", async () => {
  // Cache checkbox elements
  for (const key of DESTINATION_KEYS) {
    checkboxes[key] = document.getElementById(key);
  }

  // Load current preferences from storage
  const prefs = await chrome.storage.sync.get(DESTINATION_KEYS);

  // Set checkbox states (default to true if key is missing)
  for (const key of DESTINATION_KEYS) {
    checkboxes[key].checked = prefs[key] !== undefined ? prefs[key] : true;
  }

  // Attach change listeners
  for (const key of DESTINATION_KEYS) {
    checkboxes[key].addEventListener("change", () => onCheckboxChange(key));
  }
});

// ---------------------------------------------------------------------------
// Event Handlers
// ---------------------------------------------------------------------------

/**
 * Handles a checkbox change event. Persists the new value to storage
 * and shows a brief "saved" confirmation.
 *
 * @param {string} key - The destination key that was toggled.
 */
async function onCheckboxChange(key) {
  const newValue = checkboxes[key].checked;
  await chrome.storage.sync.set({ [key]: newValue });
  showStatus();
}

/**
 * Listens for storage changes made externally (e.g., context menu toggles
 * in the background service worker). Updates checkbox states to stay in sync.
 */
chrome.storage.onChanged.addListener((changes, areaName) => {
  if (areaName !== "sync") return;

  for (const key of DESTINATION_KEYS) {
    if (changes[key] !== undefined) {
      checkboxes[key].checked = changes[key].newValue;
    }
  }
});

// ---------------------------------------------------------------------------
// UI Helpers
// ---------------------------------------------------------------------------

/**
 * Briefly shows a "Settings saved" status message, then fades it out.
 */
function showStatus() {
  // Clear any existing timer
  if (statusTimer) clearTimeout(statusTimer);

  statusEl.classList.add("visible");

  statusTimer = setTimeout(() => {
    statusEl.classList.remove("visible");
    statusTimer = null;
  }, 1500);
}
