# Directive: UX Enhancements (Shortcut, Context Menu, Clipboard)

## 1. Objective
Implement user-requested UX enhancements: change default shortcut to Alt+L, display the shortcut in the context menu, and copy the opened archive URLs to the clipboard. Reference GitHub Issue #6.

## 2. Context & Research (Context-First)
- Current shortcut is Alt+C. User requested Alt+L.
- The context menu can show informational items by setting `enabled: false`. We can retrieve the current shortcut using `chrome.commands.getAll()`.
- Copying to the clipboard in MV3 service workers requires injecting a script into the active tab via `chrome.scripting.executeScript`.

## 3. Planning & Risk Assessment
- **Risk Level: LOW** (Minor logic additions, no major structural changes)

## 4. Execution Steps
1. Create feature branch `feature/ux-enhancements`.
2. Update `manifest.json` with `Alt+L` and `scripting` permission.
3. Update `README.md` documentation to reflect the new shortcut.
4. Update `background.js` to:
   - Query `chrome.commands.getAll()` in `createContextMenus` and add a separator + shortcut display item.
   - Inject script in `action.onClicked` to copy generated URLs to the clipboard.
5. Create PR.

## 5. Validation Standard
- Check `chrome://extensions/shortcuts` for Alt+L.
- Right-click icon shows "Shortcut: Alt+L".
- Clicking icon copies URLs to clipboard.

## 6. Expected Deliverables
- Modified `manifest.json`, `README.md`, `background.js`.
- PR linking to Issue #6.
- Updated project state.

## 7. Failure Handling
- If `chrome.scripting` fails due to permissions on certain pages, catch the error gracefully without breaking tab opening.
