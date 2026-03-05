# Automated Test Suite

This directory contains automated tests for Login/Registration application, including both backend API tests and frontend UI tests with AI vision analysis.

## Test Structure

```
test/
├── backend_api_test.py      # Backend API tests using pytest
├── frontend_ui_test.py       # Frontend UI tests using Playwright
├── requirements.txt         # Test dependencies
├── run_tests.sh            # Linux/Mac test runner
├── run_tests.bat           # Windows test runner
├── screenshots/            # Screenshot storage (generated)
├── README.md              # This file
└── TROUBLESHOOTING.md    # Troubleshooting guide
```

## Prerequisites

1. **Python 3.8+**
2. **AI API Key** (for AI vision analysis) - Built-in, no configuration needed

   The tests use built-in AI API (https://llmapi.paratera.com) with Qwen2.5-VL-72B-Instruct model for vision analysis.

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
| 6 | Register with empty fields | POST /register |

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
| 8 | Register with empty fields | ✓ "Username and password are required" error |

## AI Vision Analysis

The frontend tests use AI Vision API (Qwen2.5-VL-72B-Instruct) to analyze screenshots for:

- **Error messages** - Detects red error text, error banners, and validation messages
- **Success states** - Identifies welcome messages, green success indicators
- **Page state** - Determines if on login, registration, or welcome screen

### Configuration

The tests use these default settings (built-in, no need to configure):

```python
API_URL = "https://llmapi.paratera.com"
API_MODEL = "Qwen2.5-VL-72B-Instruct"
```

You can override these with environment variables:

```bash
# Windows CMD
set AI_API_KEY=your_api_key
set AI_API_URL=https://your-api-url.com
set AI_MODEL=your-model-name

# Windows PowerShell
$env:AI_API_KEY="your_api_key"
$env:AI_API_URL="https://your-api-url.com"
$env:AI_MODEL="your-model-name"

# Linux/Mac
export AI_API_KEY=your_api_key
export AI_API_URL=https://your-api-url.com
export AI_MODEL=your-model-name
```

### How It Works

1. Playwright captures screenshots at each test step
2. Screenshots are encoded to base64
3. Sent to AI API with analysis prompt
4. AI analyzes image for specific UI elements
5. Test assertions verify expected error/success messages

### Alternative Vision Models

The following vision-capable models are available from the API:

- `Qwen2.5-VL-72B-Instruct` (default)
- `Qwen3-VL-30B-A3B-Instruct-2507`
- `Qwen3-VL-235B-A22B-Instruct`
- `Qwen2.5-VL-3B-Instruct`
- `Qwen2.5-VL-32B-Instruct`
- `Qwen3-VL-30B-A3B-Thinking`
- `Qwen3-VL-235B-A22B-Thinking-2507`
- `GLM-4.6V`
- `GLM-4V-Flash`
- `GLM-4V-Plus-0111`
- `DeepSeek-OCR`
- `PaddleOCR-VL-0.9`
- `PaddleOCR-VL-1.5`

To use a different model, set the `AI_MODEL` environment variable.

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
🤖 AI Analysis: {"has_error": true, "error_message": "User not found", ...}

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

### Python 3.13 Compatibility Issues

If you're using Python 3.13, you may encounter compilation errors for certain packages.

**Quick Fix:**
```bash
# Upgrade pip and setuptools first
pip install --upgrade pip setuptools wheel
```

**Alternative: Use Virtual Environment:**
```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate
```

For more detailed troubleshooting, see [TROUBLESHOOTING.md](TROUBLESHOOTING.md).

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

### AI API Errors

```
Error: 401 Unauthorized
Error: API request failed: 401
```

**Solution:** Check your API key configuration:
```bash
# Verify environment variable (if custom)
echo $AI_API_KEY
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
requests>=2.31.0       # HTTP client for backend tests
pytest>=8.0.0           # Test framework
pytest-asyncio>=0.23.0  # Async support for pytest
playwright>=1.42.0      # Browser automation
```

## Security Notes

- The `/reset_users` endpoint is only for testing and should be removed in production
- API keys should never be committed to version control
- Use environment variables for all sensitive data

## License

Same as the main project.
