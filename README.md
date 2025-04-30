# Playwright Automated Test

This project contains automated tests for web form using Playwright and Python. The framework is built using the Page Object Model (POM) pattern for better maintainability and reusability.

## Features

- Cross-browser testing support (Chromium, Firefox, Safari)
- Page Object Model implementation
- Parameterized test cases
- Happy path and negative test scenarios
- Configurable test execution

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd playwright_test
```

2. Create and activate a virtual environment (optional but recommended):
```bash
python -m venv venv
source venv/bin/activate 
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install Playwright browsers:
```bash
playwright install
```

## Running Tests

### Running Happy Path Tests for Home Page

To run the happy path tests for the home page form:

```bash
pytest -n auto -m happy_path_home -v
```

### Running Negative Tests for Home Page

- Run Negative tests:
```bash
pytest -n auto -m negative -v
```

### Additional Test Running OPtions

- Run all tests with detailed output:
```bash
pytest -v
```

## Test Structure

- `tests/`: Contains test files
  - `test_request_form_home.py`: Tests for the home page form
  - `test_request_form_quote.py`: Tests for the quote page form
- `pages/`: Contains page object classes
  - `base_page.py`: Base page class with common functionality
  - `home_page.py`: Home page specific implementations
  - `quote_page.py`: Quote page specific implementations
