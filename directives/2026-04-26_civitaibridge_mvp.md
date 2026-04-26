# Directive: CivitaiBridge MVP Implementation

## 1. Objective
Implement the complete CivitaiBridge Chrome extension per the PRD. This directive covers all four phases (Issues #1–#4) as a cohesive MVP delivery.

## 2. Context & Research (Context-First)
- Repository: Dawnflare/CivitaiBridge (freshly initialized, no source files yet)
- PRD reviewed: `CivitaiBridge_PRD.md`
- Chrome MV3 APIs researched: `declarativeContent`, `contextMenus`, `storage.sync`, `tabs.create`
- No prior issues or PRs exist

## 3. Planning & Risk Assessment
- **Risk Level: HIGH** (multi-file, new extension architecture, multiple Chrome APIs)
- Implementation plan approved by user (auto-approved via review policy)
- GitHub Issues created: #1 (manifest/icons), #2 (background.js), #3 (options page), #4 (docs)

## 4. Execution Steps
1. Create feature branch `feature/mvp-extension`
2. Generate extension icons
3. Write `src/manifest.json`
4. Write `src/background.js`
5. Write `src/options.html` and `src/options.js`
6. Rewrite `README.md`
7. Push all changes and create PR

## 5. Validation Standard
- Load unpacked extension in Chrome
- Verify icon state changes on valid/invalid pages
- Verify archive tabs open with correct URLs
- Verify context menu checkboxes and options page sync
- Verify tab placement and focus behavior

## 6. Expected Deliverables
- Complete extension source in `src/`
- Updated README.md
- GitHub PR with bulleted summary referencing issues #1–#4
- Updated `.tmp/project_state.json`

## 7. Failure Handling
- Self-anneal up to 5 attempts on manifest schema or API usage errors
- If icon generation fails, use placeholder colored squares and note in PR
