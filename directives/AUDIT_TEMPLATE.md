# Directive: Documentation Audit & State Sync
**Date**: [YYYY-MM-DD]
**Status**: Final Review Phase

## 1. Objective
To verify that the project's architectural integrity has been maintained throughout the current feature branch and to ensure all documentation is synchronized before merging to `main`.

## 2. Context-First Research
- **Current Branch**: [Insert Branch Name]
- **Associated GitHub Issue**: [e.g., #123]
- **Primary Directive**: [e.g., 2026-02-02_feature_x.md]

## 3. The 3-Layer Audit Checklist

### Layer 1: Environment & Hygiene
- [ ] **.gitignore Check**: Confirm that `.tmp/` is not being tracked.
- [ ] **.gitattributes Check**: Ensure no line-ending conflicts were introduced.

### Layer 2: Orchestration & Directives
- [ ] **Directive Presence**: Is there a unique, date-stamped directive for every non-trivial task performed in this branch?
- [ ] **Non-Trivial Compliance**: Did all multi-file modifications or dependency changes have an approved Execution Plan?
- [ ] **Naming Convention**: Do all files in `directives/` follow the `YYYY-MM-DD_description.md` format?

### Layer 3: Execution & Self-Annealing
- [ ] **Execution Logs**: Verify that `.tmp/logs/` contains a timestamped log for every script run from the `execution/` folder.
- [ ] **Idempotent Writes**: Confirm that no files in `src/` were reformatted or broadly refactored outside the scope of the directive.

## 4. Operational Maintenance
- [ ] **Documentation Standard**: Do all new functions in `src/` have Google/NumPy style docstrings?
- [ ] **README Update**: Does the `README.md` accurately reflect the new features and updated usage guidelines?
- [ ] **State Sync**: Is `.tmp/project_state.json` updated with the final completion status and the PR link?

## 5. GitHub Synchronization
- [ ] **PR Summary**: Has a Pull Request been created via MCP with a bulleted summary of changes?
- [ ] **Issue Linking**: Does the PR body explicitly reference the GitHub issue number?

## 6. Validation Standard
- [ ] Run the final validation script or entry point to ensure zero regressions in the main branch logic.

## 7. Deliverables
- [ ] Updated `README.md`.
- [ ] Finalized `.tmp/project_state.json`.
- [ ] Merged/Draft PR link.
