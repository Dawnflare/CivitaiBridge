# CivitaiBridge

A lightweight Chromium browser extension that instantly opens Civitai model pages on archive sites.

## What It Does

When browsing a model page on **civitai.com** or **civitai.red**, click the extension icon (or press `Alt+C`) to instantly open that model on:

- [Civarchive.com](https://civarchive.com)
- [Civitaiarchive.com](https://civitaiarchive.com)
- [Civitai.red](https://civitai.red)

The extension extracts the model ID from the current URL and constructs clean archive URLs — no slug names, no query parameters.

## Features

- **One-Click Access** — Click the icon or press `Alt+C` to open archive tabs.
- **Smart Icon State** — Icon activates only on valid model pages; grayed out everywhere else.
- **Context Menu Toggles** — Right-click the icon to enable/disable individual archive destinations.
- **Options Page** — Full settings page synced with context menu preferences.
- **Tab Placement** — Archive tabs open immediately right of your current tab, with focus on the last opened.
- **Duplicate Prevention** — Won't open a redundant tab for the site you're already on.

## Installation

1. Clone or download this repository.
2. Open your Chromium browser and navigate to `chrome://extensions/`.
3. Enable **Developer mode** (top-right toggle).
4. Click **Load unpacked** and select the `src/` folder.
5. The CivitaiBridge icon will appear in your toolbar.

## Keyboard Shortcut

The default shortcut is **Alt+C**. To customize:
1. Go to `chrome://extensions/shortcuts`.
2. Find **CivitaiBridge** → "Open model on archive sites".
3. Set your preferred key combination.

## Development

### Project Structure

```
src/
├── manifest.json     # Extension manifest (MV3)
├── background.js     # Service worker — core logic
├── options.html      # Settings page UI
├── options.js        # Settings page script
└── icons/
    ├── icon-16.png
    ├── icon-48.png
    └── icon-128.png
```

### Architecture

This project follows a **3-Layer Architecture** (Directive → Orchestration → Execution):
- **Directives**: Task specifications in `directives/`
- **Orchestration**: Managed via GitHub Issues and PRs
- **Execution**: Deterministic scripts and code in `src/`

All non-trivial changes require an approved directive before implementation.

## License

This project is licensed under the MIT License — see the [LICENSE.md](LICENSE.md) file for details.
