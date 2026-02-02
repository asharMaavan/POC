# Boards QA (BDD Automation + QA Artifacts)

This repository contains QA artifacts and BDD automation for a multi-tenant "Boards" module, including API/UI tests, performance smoke plan, and manual documentation.

## Audience
- **Non-technical reviewers:** Use the ?Quick Start? and ?What?s Included? sections.
- **Technical reviewers:** Use the ?Setup?, ?Configuration?, and ?Run Commands? sections.

---

## What?s Included (Non-Technical Overview)
- **Manual QA artifacts:** Test plan, exploratory charters, test cases, defect reports, traceability, and summary.
- **Automated tests:** BDD scenarios for API and UI using pytest-bdd + Playwright.
- **Performance smoke:** JMeter test plan and instructions.
- **Reports:** HTML reports can be generated using pytest-html.

---

## Repository Structure (Technical)
- `features/` ? BDD feature files (auth, boards, cards, RBAC, tenant isolation)
- `tests/` ? Step definitions, helpers, and test entry points
- `docs/` ? TestPlan, Charters, TestCases, CrossBrowserMatrix, Defects, Traceability, Summary
- `perf/` ? JMeter plan (`boards_smoke.jmx`) and instructions
- `reports/` ? Output reports (gitignored)
- `pyproject.toml`, `pytest.ini` ? Python dependencies and test configuration

---

## Prerequisites
- **Python:** 3.10+ (recommended 3.12)
- **Node:** Not required
- **Java:** Required only for JMeter (Java 8+)
- **Browsers:** Chromium/Firefox/WebKit installed by Playwright

### Optional Tools
- **JMeter:** for performance smoke (Apache JMeter 5.6+)
- **pytest-html:** HTML report generator for pytest (used instead of Allure)

---

## Setup (Windows PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -U pip
pip install -e .
python -m playwright install
pip install pytest-html
```

## Setup (macOS/Linux)
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -U pip
pip install -e .
python -m playwright install
pip install pytest-html
```

---

## Run Commands (BDD Automation)

### BDD API tests
```bash
pytest -m api
```

### BDD UI tests (per browser)
```bash
pytest -m e2e --browser chromium
pytest -m e2e --browser firefox
pytest -m e2e --browser webkit
```

### Smoke suite
```bash
pytest -m smoke
```

---

## HTML Reports (pytest-html)

pytest-html generates a single, self-contained HTML file per run.

Generate reports:
```bash
pytest -m e2e --browser chromium --html reports/pytest-e2e-report.html --self-contained-html
pytest -m api --html reports/pytest-api-report.html --self-contained-html
```

Reports will be saved in `reports/`.

---

## Performance Smoke (JMeter)

Plan:
- `perf/boards_smoke.jmx`
- Scenario: 20 VUs, 2-min ramp, 3-min steady
- Flow: login ? create board ? create 2 cards ? move a card ? GET /boards

Run (non-GUI):
```bash
jmeter -n -t perf/boards_smoke.jmx -l reports/boards_smoke.jtl
```

Generate HTML report:
```bash
jmeter -g reports/boards_smoke.jtl -o reports/boards_smoke_html
```

If output folder exists, delete it first:
```powershell
Remove-Item -Recurse -Force reports\boards_smoke_html
```

---

## Manual QA Artifacts
Located in `docs/`:
- `TestPlan.md`
- `Charters.md`
- `TestCases.md`
- `CrossBrowserMatrix.md`
- `Defects.md`
- `Traceability.md`
- `Summary.md`

---

## Notes and Assumptions
- The system under test must provide `/api/v1` endpoints as described in the acceptance criteria and examples.
- The UI must expose `data-testid` attributes referenced in the feature files and step definitions.
- Set target endpoints before running tests:
  - PowerShell:
    ```powershell
    $env:API_BASE_URL="http://localhost:8000/api/v1"
    $env:UI_BASE_URL="http://localhost:5173"
    ```
  - Bash:
    ```bash
    export API_BASE_URL="http://localhost:8000/api/v1"
    export UI_BASE_URL="http://localhost:5173"
    ```
- Reports and test artifacts are not committed (gitignored).

---

## Troubleshooting
- **Missing pytest arguments (e.g. --html):** install the plugin: `pip install pytest-html`
- **Playwright browser errors:** run `python -m playwright install`
- **JMeter not found:** add `jmeter.bat` to PATH or use full path

---

## CI (GitHub Actions)

This repo includes `.github/workflows/qa.yml` with two jobs:
- **e2e**: runs pytest BDD UI tests on Chromium and uploads the HTML report.
- **api**: runs pytest BDD API tests and uploads the HTML report.

Set these GitHub Secrets before running CI:
- `API_BASE_URL` (e.g., `http://your-api/api/v1`)
- `UI_BASE_URL` (e.g., `http://your-ui`)

---

## Contact / Ownership
Adapt endpoints and environment variables to your target system.
