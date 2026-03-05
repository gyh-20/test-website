# Troubleshooting Guide

## Python 3.13 Compatibility Issues

If you're using Python 3.13, you may encounter compilation errors for certain packages.

### Quick Fix

```bash
# Upgrade pip and setuptools first
pip install --upgrade pip setuptools wheel

# Then run the test script
test\run_tests.bat
```

### Alternative: Use Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Run tests
test\run_tests.bat
```

### Known Issues & Solutions

#### 1. greenlet compilation error

**Error:**
```
fatal error C1083: 无法打开包括文件: "math.h"
```

**Solution:**
This is a Python 3.13 specific issue with greenlet. The updated requirements.txt uses compatible versions that should resolve this.

If it persists, try:
```bash
pip install --upgrade greenlet
```

#### 2. playwright installation fails

**Error:**
```
Failed to install Playwright browsers
```

**Solution:**
```bash
# Try installing browsers separately
playwright install chromium

# Or use system browsers
set PLAYWRIGHT_BROWSERS_PATH=0
```

#### 3. Port already in use

**Error:**
```
Address already in use
```

**Solution:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /F /PID <PID>

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

#### 4. AI API connection timeout

**Error:**
```
timeout: TimeoutError
```

**Solution:**
- Check internet connection
- Verify API URL is accessible: `curl https://llmapi.paratera.com`
- Check firewall settings
- Try increasing timeout in frontend_ui_test.py

#### 5. curl command not found

**Error:**
```
'curl' is not recognized
```

**Solution:**
- Install curl on Windows: https://curl.se/windows/
- Or use PowerShell's `Invoke-WebRequest`

## Manual Testing (Automated Tests Fail)

If automated tests don't work, you can test manually:

### 1. Start Backend

```bash
cd backend
python app.py
```

### 2. Start Frontend (new terminal)

```bash
cd frontend
python -m http.server 8000
```

### 3. Test API with curl

```bash
# Test backend
curl http://localhost:5000

# Test login
curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d "{\"username\":\"test\",\"password\":\"test\"}"
```

### 4. Test in Browser

Open `http://localhost:8000` in your browser and test:
1. Login with non-existent user
2. Register a new user
3. Login with correct credentials
4. Login with wrong password

## Getting Help

If you continue to have issues:

1. Check logs:
   - `test/backend.log` - Backend server logs
   - `test/frontend.log` - Frontend server logs

2. Run with verbose output:
   - Remove `-q` flags from run_tests.bat/run_tests.sh

3. Check Python version:
   ```bash
   python --version
   ```
   Recommended: Python 3.10, 3.11, or 3.12

4. Verify dependencies:
   ```bash
   pip list
   ```

## Environment Variables

You can configure the test suite with environment variables:

```bash
# Windows CMD
set AI_API_KEY=your_key
set AI_API_URL=your_url
set AI_MODEL=your_model

# Windows PowerShell
$env:AI_API_KEY="your_key"
$env:AI_API_URL="your_url"
$env:AI_MODEL="your_model"

# Linux/Mac
export AI_API_KEY=your_key
export AI_API_URL=your_url
export AI_MODEL=your_model
```

## Alternative Browsers

If Playwright Chromium doesn't work, you can use other browsers:

1. Install browser: `playwright install firefox`
2. Modify `frontend_ui_test.py`:
   ```python
   browser = await p.firefox.launch(headless=False)
   ```
