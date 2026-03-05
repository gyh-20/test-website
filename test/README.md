# Automated Test Suite

This directory contains automated tests for the Login/Registration application, including both backend API tests and frontend UI tests with AI vision analysis.

## Test Structure

```
test/
├── backend_api_test.py      # Backend API tests using pytest
├── frontend_ui_test.py       # Frontend UI tests using Playwright
├── requirements.txt         # Test dependencies
├── run_tests.sh            # Linux/Mac test runner
├── run_tests.bat           # Windows test runner
├── screenshots/            # Screenshot storage (generated)
└── README.md              # This file
```

## Prerequisites

1. **Python 3.8+**
2. **ANTHROPIC API Key** (for AI vision analysis) - Optional but recommended

   Get your API key from https://console.anthropic.com/

   Set it as environment variable:
   ```bash
   # Linux/Mac
   export ANTHROPIC_API_KEY=your_api_key_here

   # Windows CMD
   set ANTHROPIC_API_KEY=your_api_key_here

   # Windows PowerShell
   $env:ANTHROPIC_API_KEY="your_api_key_here"
   ```

## Running Tests

### Windows

```bash
# Open PowerShell or CMD in the project root
cd test
run_tests.bat
```

### Linux/Mac

```bash
# Make the script executable
chmod +x test/run_tests.sh

# Run tests
cd test
./run_tests.sh
```

### Run Specific Test Suites

#### Backend Tests Only

```bash
cd test
pip install -r requirements.txt
cd ../backend
pip install -r requirements.txt
python ../test/backend_api_test.py
```

#### Frontend Tests Only

First start the servers manually:
```bash
# Terminal 1 - Backend
cd backend
python app.py

# Terminal 2 - Frontend
cd frontend
python -m http.server 8000

# Terminal 3 - Tests
cd test
python frontend_ui_test.py
```

## Test Coverage

### Backend Tests (`backend_api_test.py`)

| Test | Description | Endpoint |
|------|-------------|----------|
| 1 | Unregistered user login | POST /login |
| 2 | Register new user | POST /register |
| 3 | Login with correct credentials | POST /login |
| 4 | Login with incorrect password | POST /login |
| 5 | Register existing username | POST /register |

### Frontend Tests (`frontend_ui_test.py`)

| Test | Description | AI Vision Check |
|------|-------------|-----------------|
| 1 | Login form display | ✓ No errors |
| 2 | Unregistered user login | ✓ "User not found" error |
| 3 | Switch to registration | ✓ No errors |
| 4 | Register new user | ✓ Success state |
| 5 | Login with correct credentials | ✓ Success state |
| 6 | Welcome screen | ✓ "Welcome" message |
| 7 | Login with incorrect password | ✓ "Incorrect password" error |

## AI Vision Analysis

The frontend tests use Claude Vision (via Anthropic API) to analyze screenshots for:

- **Error messages** - Detects red error text, error banners, and validation messages
- **Success states** - Identifies welcome messages, green success indicators
- **Page state** - Determines if on login, registration, or welcome screen

### How It Works

1. Playwright captures screenshots at each test step
2. Screenshots are sent to Claude Vision API
3. AI analyzes the image for specific UI elements
4. Test assertions verify expected error/success messages

### Without API Key

If `ANTHROPIC_API_KEY` is not set, tests will still run but skip AI analysis:
- Screenshots are still captured
- Tests check DOM elements directly (text content, element visibility)
- Warnings are displayed in output

## Test Output

### Console Output

```
============================================================
   Login/Registration App Test Suite
============================================================

[1/5] Installing test dependencies...
✓ Dependencies installed

[2/5] Installing backend dependencies...
✓ Backend dependencies installed

[3/5] Starting backend server...
✓ Backend server is running (PID: 12345)

[4/5] Starting frontend server...
✓ Frontend server is running (PID: 12346)

[5/5] Running tests...

============================================================
   Backend API Tests
============================================================
...
test_backend_api.py::TestBackendAPI::test_1_unregistered_user_login PASSED
...

============================================================
   Frontend UI Tests
============================================================
...
============================================================
   Test Summary
============================================================
✓ Backend tests: PASSED
✓ Frontend tests: PASSED

Screenshots saved to: /path/to/test/screenshots/
```

### Screenshots

All screenshots are saved to `test/screenshots/` with timestamps:
- `01_login_form_20240101_120000.png`
- `02_unregistered_login_20240101_120001.png`
- etc.

### Log Files

- `test/backend.log` - Backend server output
- `test/frontend.log` - Frontend server output

## Troubleshooting

### Port Already in Use

```
Error: Address already in use
```

**Solution:** Kill processes using ports 5000 or 8000:
```bash
# Windows
netstat -ano | findstr :5000
taskkill /F /PID <PID>

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Playwright Browser Issues

```
Error: Executable doesn't exist at /path/to/chromium
```

**Solution:** Reinstall Playwright browsers:
```bash
playwright install chromium
```

### Anthropic API Errors

```
Error: 401 Unauthorized
```

**Solution:** Verify your API key:
```bash
echo $ANTHROPIC_API_KEY  # Check if set
export ANTHROPIC_API_KEY=sk-ant-xxxxx  # Set correct key
```

### Frontend Tests Time Out

```
TimeoutError: page.goto: Timeout 30000ms exceeded
```

**Solution:** Ensure servers are running:
```bash
# Check backend
curl http://localhost:5000

# Check frontend
curl http://localhost:8000
```

## Adding New Tests

### Backend Tests

Add new test methods to `backend_api_test.py`:

```python
def test_new_feature(self):
    response = requests.post(
        f"{BASE_URL}/endpoint",
        json={"key": "value"}
    )
    assert response.status_code == 200
    assert response.json()["success"] is True
```

### Frontend Tests

Add new test steps to `test_frontend_ui()` in `frontend_ui_test.py`:

```python
# Navigate to page
await page.goto(FRONTEND_URL)

# Perform action
await page.click('#some-button')

# Wait for result
await page.wait_for_timeout(1000)

# Take screenshot
screenshot_path = take_screenshot(page, "new_test")

# Analyze with AI
has_error, error_msg = analyze_screenshot_with_ai(screenshot_path)

# Assert result
assert not has_error, f"Unexpected error: {error_msg}"
```

## Dependencies

```
requests==2.31.0       # HTTP client for backend tests
pytest==7.4.3           # Test framework
pytest-asyncio==0.21.1  # Async support for pytest
playwright==1.40.0      # Browser automation
anthropic==0.18.0       # Anthropic API for AI vision
```

## Security Notes

- The `/reset_users` endpoint is only for testing and should be removed in production
- API keys should never be committed to version control
- Use environment variables for all sensitive data

## License

Same as the main project.
