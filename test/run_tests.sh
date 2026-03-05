#!/bin/bash

# One-click test runner for the Login/Registration application
# Tests both backend API and frontend UI

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Project root directory
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   Login/Registration App Test Suite   ${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# Check if Python is available
if ! command -v python &> /dev/null; then
    echo -e "${RED}Error: Python is not installed${NC}"
    exit 1
fi

# Function to kill background processes
cleanup() {
    echo -e "\n${YELLOW}Cleaning up...${NC}"
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi
    echo -e "${GREEN}Cleanup complete${NC}"
}

# Set trap to cleanup on exit
trap cleanup EXIT

# Step 1: Install test dependencies
echo -e "${BLUE}[1/5] Installing test dependencies...${NC}"
cd "$PROJECT_ROOT/test"
pip install -r requirements.txt -q
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Install Playwright browsers
echo -e "${BLUE}[1/5] Installing Playwright browsers...${NC}"
playwright install chromium -q
echo -e "${GREEN}✓ Playwright browsers installed${NC}"

# Step 2: Install backend dependencies
echo -e "${BLUE}[2/5] Installing backend dependencies...${NC}"
cd "$PROJECT_ROOT/backend"
pip install -r requirements.txt -q
echo -e "${GREEN}✓ Backend dependencies installed${NC}"

# Step 3: Start backend server
echo -e "${BLUE}[3/5] Starting backend server...${NC}"
python app.py > "$PROJECT_ROOT/test/backend.log" 2>&1 &
BACKEND_PID=$!

# Wait for backend to be ready
echo "Waiting for backend to start..."
for i in {1..30}; do
    if curl -s http://localhost:5000 > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Backend server is running (PID: $BACKEND_PID)${NC}"
        break
    fi
    sleep 1
done

if ! curl -s http://localhost:5000 > /dev/null 2>&1; then
    echo -e "${RED}Error: Backend failed to start${NC}"
    echo "Check logs at: $PROJECT_ROOT/test/backend.log"
    exit 1
fi

# Step 4: Start frontend server
echo -e "${BLUE}[4/5] Starting frontend server...${NC}"
cd "$PROJECT_ROOT/frontend"
python -m http.server 8000 > "$PROJECT_ROOT/test/frontend.log" 2>&1 &
FRONTEND_PID=$!

# Wait for frontend to be ready
echo "Waiting for frontend to start..."
for i in {1..30}; do
    if curl -s http://localhost:8000 > /dev/null 2>&1; then
        echo -e "${GREEN}✓ Frontend server is running (PID: $FRONTEND_PID)${NC}"
        break
    fi
    sleep 1
done

if ! curl -s http://localhost:8000 > /dev/null 2>&1; then
    echo -e "${RED}Error: Frontend failed to start${NC}"
    echo "Check logs at: $PROJECT_ROOT/test/frontend.log"
    exit 1
fi

# Step 5: Run tests
echo -e "${BLUE}[5/5] Running tests...${NC}"
echo ""

# Backend tests
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   Backend API Tests                  ${NC}"
echo -e "${BLUE}========================================${NC}"
cd "$PROJECT_ROOT/test"
python backend_api_test.py

BACKEND_TEST_RESULT=$?

# Frontend tests
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   Frontend UI Tests                   ${NC}"
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}AI API: Qwen2.5-VL-72B-Instruct${NC}"
echo -e "${BLUE}API URL: https://llmapi.paratera.com${NC}"
echo ""

python frontend_ui_test.py

FRONTEND_TEST_RESULT=$?

# Final summary
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}   Test Summary                        ${NC}"
echo -e "${BLUE}========================================${NC}"

if [ $BACKEND_TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}✓ Backend tests: PASSED${NC}"
else
    echo -e "${RED}✗ Backend tests: FAILED${NC}"
fi

if [ $FRONTEND_TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}✓ Frontend tests: PASSED${NC}"
else
    echo -e "${RED}✗ Frontend tests: FAILED${NC}"
fi

echo ""
echo "Screenshots saved to: $PROJECT_ROOT/test/screenshots/"
echo "Backend logs: $PROJECT_ROOT/test/backend.log"
echo "Frontend logs: $PROJECT_ROOT/test/frontend.log"

if [ $BACKEND_TEST_RESULT -eq 0 ] && [ $FRONTEND_TEST_RESULT -eq 0 ]; then
    echo -e "${GREEN}"
    echo "╔════════════════════════════════════════╗"
    echo "║   ALL TESTS PASSED! ✓                  ║"
    echo "╚════════════════════════════════════════╝"
    echo -e "${NC}"
    exit 0
else
    echo -e "${RED}"
    echo "╔════════════════════════════════════════╗"
    echo "║   SOME TESTS FAILED ✗                  ║"
    echo "╚════════════════════════════════════════╝"
    echo -e "${NC}"
    exit 1
fi
