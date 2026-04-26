import os
import subprocess
import datetime
import sys

def setup_agent_workspace():
    """
    Initializes a professional agentic development environment.
    Sets up folders, git rules, agent instructions, and GitHub synchronization.
    Handles encoding issues for Windows environments.
    """
    
    # Helper for robust printing in different terminal encodings
    def log(message):
        try:
            print(message)
        except UnicodeEncodeError:
            # Fallback for terminals that don't support emojis/unicode
            print(message.encode('ascii', 'ignore').decode('ascii'))

    log("🚀 Starting Professional Agentic Workspace Initialization...")

    # 1. Define and create the 3-Layer directory structure
    folders = [
        'directives', 
        'execution', 
        'src', 
        '.tmp', 
        '.tmp/logs'
    ]
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        log(f"  [OK] Created folder: {folder}")

    # 2. Generate the .gitattributes (Handles LF/CRLF for cross-platform safety)
    gitattributes_content = """# Keep LF in the repo for web files, but CRLF for Windows scripts
* text=auto eol=lf
*.bat text eol=crlf
*.cmd text eol=crlf
*.ps1 text eol=crlf
"""
    with open('.gitattributes', 'w', encoding='utf-8') as f:
        f.write(gitattributes_content)
    log("  [OK] Created .gitattributes")

    # 3. Generate the comprehensive .gitignore
    gitignore_content = """# --- Python / venv ---
.venv/
env/
venv/
__pycache__/
*.py[cod]
*.pyo
*.pyd

# --- Node.js ---
node_modules/

# --- Packaging / build artifacts ---
build/
dist/
*.egg-info/
.eggs/
pip-wheel-metadata/

# --- Compressed Archives ---
*.zip
*.rar
*.tar.gz
*.7z

# --- Tests / coverage ---
.pytest_cache/
.coverage
.coverage.*

# --- Type checkers / linters ---
.mypy_cache/
.pytype/
.pyright/
.ruff_cache/
.pyre/

# --- Logs ---
logs/
*.log

# --- Env / secrets ---
.env
.env.*
*.pem
*.key
token.json
credentials.json

# --- Editors / IDEs ---
.vscode/
.idea/
*.code-workspace

# --- OS junk (Windows/macOS) ---
Thumbs.db
desktop.ini
.DS_Store
.AppleDouble
.LSOverride

# --- Linux ---
*~
.cache/
*.swp

# --- Temporary / Agent artifacts ---
gemini.md
agent.md
.agent/
.tmp/
*.orig
*.bak
*.old

# --- Misc ---
*.sln.cache
"""
    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    log("  [OK] Created comprehensive .gitignore")

    # 4. Generate Initial README.md
    repo_name = os.path.basename(os.getcwd())
    readme_content = f"""# {repo_name}

## Description
Professional coding project managed with a 3-Layer Agentic Architecture.

## Features
- Modular 3-layer architecture (Directives, Orchestration, Execution).
- Automated workflow via Agent.
- Integrated GitHub synchronization.

## Usage Guidelines
- All logic changes must be proposed via a Directive in the `directives/` folder.
- Deterministic tasks are handled by scripts in `execution/`.
- Intermediate data is stored in `.tmp/`.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
"""
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    log("  [OK] Created initial README.md")

    # 5. Generate MIT LICENSE.md
    current_year = datetime.datetime.now().year
    license_content = f"""MIT License

Copyright (c) {current_year} [NAME]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
    with open('LICENSE.md', 'w', encoding='utf-8') as f:
        f.write(license_content)
    log("  [OK] Created LICENSE.md (MIT)")

    # 6. Generate Gemini.md (Architect Edition v14)
    gemini_md_content = """# Role & Identity
You are a Senior Project Architect. You operate under a 3-Layer Architecture (Directive → Orchestration → Execution) to separate high-level intent from deterministic execution.

# Layer 1: Environment & Git Initialization
Before any work begins, initialize the workspace:
1. **Environments**: Python (venv) or Node.js isolation required. 
   - **Action**: Run `python -m venv .venv`. 
   - **Path**: Use `./.venv/bin/python` (or `Scripts/python.exe` on Windows).
2. **Git Hygiene**: Create a comprehensive `.gitignore` and a `.gitattributes` (handling LF/CRLF for cross-platform safety).
3. **Structure**: Create `directives/`, `execution/`, and `.tmp/` folders immediately.

# Layer 2: The Orchestration Workflow
You are the **Orchestrator**. Leverage connected MCP servers (GitHub) to maintain project synchronicity.

- **Context First**: Before planning, inspect the repository structure and use the GitHub MCP to search related issues or PRs.
- **GitHub as Source of Truth**: For every non-trivial task, ensure a corresponding GitHub issue exists. Reference the issue number (e.g., `#123`) in the directive.
- **Non-Trivial Definition**: A task is non-trivial if it:
  - Modifies more than one file.
  - Introduces new logic, data structures, or schemas.
  - Adds or upgrades dependencies.
- **Directive Requirement**: All non-trivial tasks map to a unique directive.
  - **Action**: Create a new file in `directives/` by duplicating `directives/TEMPLATE.md`.
  - **Naming Convention**: Use `YYYY-MM-DD_short_description.md` (e.g., `2026-02-02_api_auth.md`).
- **Planning Gate**: For MEDIUM/HIGH risk tasks, produce an **Execution Plan** and a **Draft PR Summary** for user confirmation.
- **Risk Classification**: LOW (Single-file), MEDIUM (Multi-file), HIGH (Auth/Infra/Dependencies).
- **File Scope Rule**: New files may only be created inside `directives/`, `execution/`, `src/`, or `.tmp/` unless they are standard project files (e.g., README.md, LICENSE.md).

# Layer 3: Execution & Self-Annealing
1. **Idempotent Writes**: Read files before writing; only modify if content differs.
2. **Logging**: Log actions, timestamps, and script names to `.tmp/logs/`.
3. **Validation**: Prefer automated tests. If none exist, verify via entry point or log check.
4. **Self-Anneal Limits**: Attempt up to **five** autonomous fixes with 'Context First' re-inspection between attempts.

# Operational Constraints
- **Documentation Standard**: Maintain careful descriptive documentation within all code files.
  - **Functions**: Every function MUST have a docstring (Google or NumPy style) describing its purpose, arguments, and return values.
  - **Logic Blocks**: Use comments to explain the "why" behind complex code blocks.
- **README & License Maintenance**: 
  - Always update the `README.md` when significant changes are made or new features are added.
  - Ensure the `LICENSE.md` remains present and correctly identifies the project's open-source status.
- **Minimal Change Principle**: Avoid broad refactors or reformatting unrelated code.
- **State Management**: Update `.tmp/project_state.json` after major steps. Include active GitHub issue/PR links.
- **Commit & PR Strategy**: 
  - For LOW-risk edits, commit with descriptive messages referencing issues.
  - Upon validation, use GitHub MCP to create a PR with a bulleted summary of changes.
- **Completion**: Summarize actions, update the state file, and stop upon validation.
"""
    with open('Gemini.md', 'w', encoding='utf-8') as f:
        f.write(gemini_md_content)
    log("  [OK] Created Gemini.md (v14)")

    # 7. Generate Directive TEMPLATE.md
    directive_template = """# Directive: [Task Name]

## 1. Objective
<!-- Define the goal -->

## 2. Context & Research (Context-First)
<!-- Findings from repository inspection and GitHub MCP search -->

## 3. Planning & Risk Assessment
<!-- Risk Level: LOW / MEDIUM / HIGH -->

## 4. Execution Steps (Scripts)
<!-- Scripts to call in execution/ -->

## 5. Validation Standard
<!-- How to verify success -->

## 6. Expected Deliverables
<!-- Final Code, GitHub PR Link, State Update, README updated -->

## 7. Failure Handling
<!-- Notes on rate limits or "Self-Anneal" failure points -->
"""
    with open('directives/TEMPLATE.md', 'w', encoding='utf-8') as f:
        f.write(directive_template)
    log("  [OK] Created directives/TEMPLATE.md")

    # 7.1 Generate AUDIT_TEMPLATE.md
    audit_template = """# Directive: Documentation Audit & State Sync
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
"""
    with open('directives/AUDIT_TEMPLATE.md', 'w', encoding='utf-8') as f:
        f.write(audit_template)
    log("  [OK] Created directives/AUDIT_TEMPLATE.md")

    # 8. Git and GitHub CLI Initialization
    try:
        if not os.path.exists('.git'):
            subprocess.run(["git", "init"], check=True, capture_output=True)
            log("  [OK] Initialized local Git repository.")

        gh_check = subprocess.run(["gh", "--version"], capture_output=True)
        if gh_check.returncode == 0:
            log(f"  [..] Attempting to create GitHub repository: {repo_name}")
            
            subprocess.run([
                "gh", "repo", "create", repo_name, 
                "--public", "--source=.", "--remote=origin"
            ], check=True, capture_output=True)
            
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", "chore: initial project structure with 3-Layer Architecture"], check=True)
            subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
            
            log(f"  [OK] Successfully linked and pushed to GitHub: {repo_name}")
        else:
            log("  [!] GitHub CLI (gh) not found. Skipping remote repo creation.")

    except subprocess.CalledProcessError as e:
        log(f"  [!] GitHub/Git Error: {e.stderr.decode() if e.stderr else e}")
    except Exception as e:
        log(f"  [!] An unexpected error occurred during Git setup: {e}")

    log("\n✅ Workspace successfully initialized for Professional Agentic Workflows!")
    log("Next step: Ask the agent to 'Read Gemini.md and begin the first task.'")

if __name__ == "__main__":
    setup_agent_workspace()