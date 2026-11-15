# Sauce Demo Playwright Automation

## Setup

Install the dependencies:

```bash
python -m pip install -r requirements.txt
python -m playwright install
```

## Run the tests

Run the full suite:

```powershell
.\run_tests.ps1
```

Run one test:

```bash
python -m pytest tests/test_login.py -v
```

Run smoke tests:

```bash
python -m pytest -m smoke -v
```

Run regression tests:

```bash
python -m pytest -m regression -v
```

## Framework design

The project uses Page Object Model. Each main page has its own file under `pages`. The test files contain the test flow and assertions.

Fixtures in `conftest.py` create the page objects and provide a logged-in browser page for tests that do not test login.

Base URL, username, password and browser can be changed with command line options or environment variables.

The suite uses Playwright auto-waiting and `expect` assertions. There are no fixed waits.

## Reports and failed test files

`run_tests.ps1` runs tests in parallel and creates:

- `reports/junit.xml`
- `reports/report.html`

Playwright failure files can be kept under `test-results/`.

## Azure Pipeline

The pipeline installs Python dependencies and Playwright browsers, runs the tests, publishes JUnit results, and uploads reports and test artifacts. The pool value is a parameter so the YAML can be changed for a Microsoft-hosted or self-hosted agent.

## Assumptions

The Sauce Demo test application is available and the standard test users remain available.

## With more time

I would add stronger test data handling, cross-browser pipeline jobs, and Allure reporting.

## AI usage

AI was used to help understand the assignment structure and to review the initial project setup. The code was reviewed and understood before use.
