# Product Requirements Document (PRD)

**Project Name:** Civitai Archive Bridge (Working Title)

**Platform:** Chromium-based Browsers (Chrome, Edge, Brave, etc.)

**Extension Version:** Manifest V3

## 1. Overview and Objective

The Civitai Archive Bridge is a browser extension designed to streamline the workflow for users browsing `civitai.com` and `civitai.red`. Its primary function is to extract the unique model ID from the currently viewed model page and instantly open the corresponding model pages on designated archive sites (Civarchive, Civitaiarchive, and Civitai.red).

## 2. Target Workflows & URL Logic

When activated, the extension must parse the active tab's URL, extract the model ID, and construct new target URLs, discarding sub-model names and query parameters.

**Example Input URL:**

```
https://civitai.com/models/2025388/augmentedcore-by-stx?modelVersionId=2292261
```

**Extraction Logic:**

1. Identify the base path `/models/`.
2. Extract the numeric ID immediately following `/models/` (`2025388`).
3. Discard everything after the ID (e.g., `/augmentedcore-by-stx` and `?modelVersionId=...`).

**Resulting Target URLs (based on user settings):**

- `https://civarchive.com/models/2025388`
- `https://civitaiarchive.com/models/2025388`
- `https://civitai.red/models/2025388`

## 3. User Interface & User Experience (UX)

### 3.1. Extension Icon States

- **Active State:** The icon appears in full color only when the user is on a valid model page (e.g., `*://civitai.com/models/*` or `*://civitai.red/models/*`).
- **Inactive/Disabled State:** The icon is grayed out on unsupported domains and unsupported sub-pages of Civitai (e.g., user profiles, image posts, articles, or the homepage).

### 3.2. Activation Methods

- **Left-Click:** Clicking the active extension icon in the toolbar triggers the URL extraction and opens the new tabs.
- **Keyboard Shortcut:** A customizable keyboard shortcut (e.g., `Alt+C` or `Ctrl+Shift+C`) triggers the same action. This shortcut will be registered in the manifest so users can change it via `chrome://extensions/shortcuts`.

### 3.3. Context Menu (Right-Click)

Right-clicking the extension icon will display a native context menu with checkboxes for the target destinations:

- [✓] Open in Civarchive.com

- [✓] Open in Civitaiarchive.com

- [✓] Open in Civitai.red

  Users can toggle these directly from the menu without needing to open a separate settings page.

### 3.4. Options / Settings Page

A dedicated settings page (accessible via the extension management menu) will mirror the context menu options.

- It will contain the same three checkboxes.
- Changes made here will instantly sync with the context menu (and vice versa) using `chrome.storage.sync`.

### 3.5. Tab Management

- **Placement:** Newly generated archive tabs will open immediately to the right of the currently active tab, rather than at the far end of the tab strip.
- **Focus:** The browser will instantly switch focus to the newly opened tab(s). *(Note: If multiple archives are selected, focus will naturally land on the last one opened in the sequence).*

## 4. Edge Cases and Error Handling

### 4.1. The "Current Domain" Paradox

- **Condition:** The user is currently browsing `civitai.red/models/12345` and has the `civitai.red` checkbox enabled.
- **Resolution:** The extension will check the origin domain. It will **not** open a new `civitai.red` tab if the user is already on `civitai.red`, ensuring redundant tabs are not created.

### 4.2. Shortcut Triggered on Invalid Page

- **Condition:** The user presses the keyboard shortcut while on an invalid page (e.g., `civitai.com/images/...`) where the icon is otherwise grayed out.
- **Resolution:** The extension will fail gracefully. It will not attempt to open broken URLs. It will display a brief, unobtrusive Chrome notification or an extension badge stating "Not a model page" or simply do nothing.

## 5. Technical Requirements

### 5.1. Chromium API Permissions

- `activeTab`: To read the current URL when the user invokes the extension.
- `tabs`: To create new tabs and control their placement/index.
- `storage`: Specifically `storage.sync`, to save user preferences for the target checkboxes.
- `contextMenus`: To create the checkbox toggles when right-clicking the icon.
- `declarativeContent` (or equivalent MV3 logic): To handle the graying out/activation of the extension icon based on page URL matching.

### 5.2. File Structure Outline

- `manifest.json`: Configuration, permissions, and background script definitions.
- `background.js`: Service worker handling context menus, shortcuts, and tab creation logic.
- `options.html` & `options.js`: The settings page UI and logic.
- Icons (16x16, 48x48, 128x128).