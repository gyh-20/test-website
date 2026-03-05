@echo off
REM One-click test runner for the Login/Registration application (Windows)
REM Tests both backend API and frontend UI

setlocal enabledelayedexpansion

set PROJECT_ROOT=%~dp0..
set TEST_ROOT=%~dp0

echo ========================================
echo    Login/Registration App Test Suite
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed
    exit /b 1
)

REM Step 1: Install test dependencies
echo [1/5] Installing test dependencies...
cd /d "%TEST_ROOT%"
pip install -r requirements.txt -q
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install test dependencies
    exit /b 1
)
echo [OK] Dependencies installed

REM Install Playwright browsers
echo [1/5] Installing Playwright browsers...
playwright install chromium -q
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install Playwright browsers
    exit /b 1
)
echo [OK] Playwright browsers installed

REM Step 2: Install backend dependencies
echo [2/5] Installing backend dependencies...
cd /d "%PROJECT_ROOT%\backend"
pip install -r requirements.txt -q
if %errorlevel% neq 0 (
    echo [ERROR] Failed to install backend dependencies
    exit /b 1
)
echo [OK] Backend dependencies installed

REM Step 3: Start backend server
echo [3/5] Starting backend server...
start /B python "%PROJECT_ROOT%\backend\app.py" > "%TEST_ROOT%\backend.log" 2>&1
set BACKEND_PID=%errorlevel%

REM Wait for backend to be ready
echo Waiting for backend to start...
timeout /t 3 /nobreak >nul

curl -s http://localhost:5000 >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Backend failed to start
    echo Check logs at: %TEST_ROOT%\backend.log
    exit /b 1
)
echo [OK] Backend server is running

REM Step 4: Start frontend server
echo [4/5] Starting frontend server...
cd /d "%PROJECT_ROOT%\frontend"
start /B python -m http.server 8000 > "%TEST_ROOT%\frontend.log" 2>&1
set FRONTEND_PID=%errorlevel%

REM Wait for frontend to be ready
echo Waiting for frontend to start...
timeout /t 3 /nobreak >nul

curl -s http://localhost:8000 >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Frontend failed to start
    echo Check logs at: %TEST_ROOT%\frontend.log
    REM Kill backend
    taskkill /F /IM python.exe >nul 2>&1
    exit /b 1
)
echo [OK] Frontend server is running

REM Step 5: Run tests
echo [5/5] Running tests...
echo.

REM Backend tests
echo ========================================
echo    Backend API Tests
echo ========================================
cd /d "%TEST_ROOT%"
python backend_api_test.py
set BACKEND_RESULT=%errorlevel%

REM Frontend tests
echo.
echo ========================================
echo    Frontend UI Tests
echo ========================================

if not defined ANTHROPIC_API_KEY (
    echo [WARNING] ANTHROPIC_API_KEY not set
    echo AI vision analysis will be skipped
    echo Set it with: set ANTHROPIC_API_KEY=your_key
    echo.
)

python frontend_ui_test.py
set FRONTEND_RESULT=%errorlevel%

REM Cleanup
echo.
echo Cleaning up...
taskkill /F /IM python.exe >nul 2>&1

REM Final summary
echo.
echo ========================================
echo    Test Summary
echo ========================================

if %BACKEND_RESULT% equ 0 (
    echo [OK] Backend tests: PASSED
) else (
    echo [FAIL] Backend tests: FAILED
)

if %FRONTEND_RESULT% equ 0 (
    echo [OK] Frontend tests: PASSED
) else (
    echo [FAIL] Frontend tests: FAILED
)

echo.
echo Screenshots saved to: %TEST_ROOT%\screenshots\
echo Backend logs: %TEST_ROOT%\backend.log
echo Frontend logs: %TEST_ROOT%\frontend.log

if %BACKEND_RESULT% equ 0 if %FRONTEND_RESULT% equ 0 (
    echo.
    echo ========================================
    echo    ALL TESTS PASSED!
    echo ========================================
    exit /b 0
) else (
    echo.
    echo ========================================
    echo    SOME TESTS FAILED
    echo ========================================
    exit /b 1
)
