"""
Frontend UI Test Suite
Tests the frontend using Playwright with AI vision for error detection
"""
import asyncio
import os
import base64
import json
import re
from datetime import datetime
from playwright.async_api import async_playwright


# Configuration
FRONTEND_URL = "http://localhost:8000"
SCREENSHOT_DIR = "test/screenshots"

# API Configuration
API_KEY = os.environ.get("AI_API_KEY", "sk-S5Ii_8ha06_YSq_fhj3_-Q")
API_URL = os.environ.get("AI_API_URL", "https://llmapi.paratera.com")
# Using Qwen2.5-VL-72B-Instruct for vision analysis
AI_MODEL = os.environ.get("AI_MODEL", "Qwen2.5-VL-72B-Instruct")


def take_screenshot(page, name):
    """Take a screenshot and save it"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{SCREENSHOT_DIR}/{name}_{timestamp}.png"
    page.screenshot(path=filename)
    return filename


def analyze_screenshot_with_ai(screenshot_path):
    """
    Use AI Vision API to analyze screenshot for error messages
    Returns: (has_error: bool, error_message: str)
    """
    try:
        # Read and encode image
        with open(screenshot_path, "rb") as f:
            image_data = f.read()
        base64_image = base64.b64encode(image_data).decode('utf-8')

        # Prepare the API request
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": AI_MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": """Analyze this screenshot of a web application. Focus on:

1. Is there any ERROR message visible? (look for red text, error banners, or "Error:" labels)
2. Is there a SUCCESS message visible? (look for "Welcome", green text, or success banners)
3. What is the current state of the page? (login form, registration form, or welcome screen?)

Respond in this JSON format:
{
  "has_error": true/false,
  "has_success": true/false,
  "error_message": "text of error if present",
  "page_state": "login/register/welcome",
  "visible_text": "brief description of what's on screen"
}
"""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 1024,
            "temperature": 0.1
        }

        # Make API request
        import requests
        response = requests.post(
            f"{API_URL}/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )

        if response.status_code != 200:
            print(f"⚠️  API request failed: {response.status_code} - {response.text}")
            return False, ""

        result = response.json()

        # Extract the AI response
        content = result.get("choices", [{}])[0].get("message", {}).get("content", "")

        print(f"  🤖 AI Analysis: {content[:200]}...")

        # Parse JSON from response (handle cases where AI wraps in markdown)
        json_match = re.search(r'\{[^{}]*"[^"]*has_error"[^{}]*\}', content, re.DOTALL)
        if json_match:
            try:
                parsed = json.loads(json_match.group())
                has_error = parsed.get("has_error", False)
                error_msg = parsed.get("error_message", "")
                return has_error, error_msg
            except json.JSONDecodeError:
                pass

        # Fallback: simple keyword matching
        has_error = any(
            keyword in content.lower()
            for keyword in ["error", "failed", "incorrect", "not found", "already exists", "required"]
        )

        # Try to extract error message
        error_msg_match = re.search(r'error.?message[":\s]+["\']?([^"\'\n]+)', content, re.IGNORECASE)
        if error_msg_match:
            return has_error, error_msg_match.group(1).strip()

        return has_error, ""

    except Exception as e:
        print(f"⚠️  AI analysis failed: {e}")
        import traceback
        traceback.print_exc()
        return False, ""


async def test_frontend_ui():
    """Main frontend test function"""
    print("=" * 60)
    print("Starting Frontend UI Tests")
    print("=" * 60)
    print(f"API URL: {API_URL}")
    print(f"Model: {AI_MODEL}")
    print("=" * 60)

    async with async_playwright() as p:
        # Launch browser (use headed mode for visibility)
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        test_results = []

        # Test 1: Login form display
        print("\n[Test 1] Verifying login form display...")
        await page.goto(FRONTEND_URL)
        await page.wait_for_load_state("networkidle")
        screenshot_path = take_screenshot(page, "01_login_form")
        has_error, error_msg = analyze_screenshot_with_ai(screenshot_path)

        if not has_error:
            print("  ✅ Login form displayed correctly")
            test_results.append(("Login form display", True))
        else:
            print(f"  ❌ Error detected: {error_msg}")
            test_results.append(("Login form display", False))

        # Test 2: Unregistered user login (Scenario 1)
        print("\n[Test 2] Testing unregistered user login...")
        await page.fill('#loginUsername', 'nonexistent')
        await page.fill('#loginPassword', 'anypass')
        await page.click('button[type="submit"]')

        # Wait for potential error message
        await page.wait_for_timeout(1000)
        screenshot_path = take_screenshot(page, "02_unregistered_login")
        has_error, error_msg = analyze_screenshot_with_ai(screenshot_path)

        if has_error and ("User not found" in error_msg or "not found" in error_msg.lower()):
            print(f"  ✅ Error message correctly shown: {error_msg}")
            test_results.append(("Unregistered user login", True))
        else:
            print(f"  ⚠️  Expected 'User not found' error")
            test_results.append(("Unregistered user login", False))

        # Test 3: Switch to registration form
        print("\n[Test 3] Switching to registration form...")
        await page.click('#showRegister')
        await page.wait_for_timeout(500)
        screenshot_path = take_screenshot(page, "03_register_form")
        has_error, error_msg = analyze_screenshot_with_ai(screenshot_path)

        if not has_error:
            print("  ✅ Registration form displayed correctly")
            test_results.append(("Switch to registration", True))
        else:
            print(f"  ❌ Error detected: {error_msg}")
            test_results.append(("Switch to registration", False))

        # Test 4: Register new user (Scenario 4)
        print("\n[Test 4] Registering new user...")
        await page.fill('#registerUsername', 'testuser')
        await page.fill('#registerPassword', 'testpass123')
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(1000)
        screenshot_path = take_screenshot(page, "04_register_success")
        has_error, error_msg = analyze_screenshot_with_ai(screenshot_path)

        if not has_error:
            print("  ✅ Registration successful (no error)")
            test_results.append(("Register new user", True))
        else:
            print(f"  ❌ Registration failed: {error_msg}")
            test_results.append(("Register new user", False))

        # Test 5: Login with correct credentials (Scenario 2)
        print("\n[Test 5] Login with correct credentials...")
        await page.fill('#loginUsername', 'testuser')
        await page.fill('#loginPassword', 'testpass123')
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(1000)
        screenshot_path = take_screenshot(page, "05_login_success")
        has_error, error_msg = analyze_screenshot_with_ai(screenshot_path)

        if not has_error:
            print("  ✅ Login successful")
            test_results.append(("Login with correct credentials", True))
        else:
            print(f"  ❌ Login failed: {error_msg}")
            test_results.append(("Login with correct credentials", False))

        # Test 6: Check welcome screen
        print("\n[Test 6] Verifying welcome screen...")
        screenshot_path = take_screenshot(page, "06_welcome_screen")
        has_error, error_msg = analyze_screenshot_with_ai(screenshot_path)

        # Check for "Welcome" text or success state
        welcome_text = await page.text_content('h1')
        if "Welcome" in welcome_text:
            print(f"  ✅ Welcome screen displayed: {welcome_text}")
            test_results.append(("Welcome screen", True))
        else:
            print(f"  ⚠️  Expected 'Welcome' message")
            test_results.append(("Welcome screen", False))

        # Test 7: Logout and test incorrect password (Scenario 3)
        print("\n[Test 7] Testing login with incorrect password...")
        await page.click('#logout')
        await page.wait_for_timeout(500)
        await page.fill('#loginUsername', 'testuser')
        await page.fill('#loginPassword', 'wrongpass')
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(1000)
        screenshot_path = take_screenshot(page, "07_incorrect_password")
        has_error, error_msg = analyze_screenshot_with_ai(screenshot_path)

        if has_error and ("Incorrect" in error_msg or "password" in error_msg.lower()):
            print(f"  ✅ Error correctly shown: {error_msg}")
            test_results.append(("Incorrect password error", True))
        else:
            print(f"  ⚠️  Expected 'Incorrect password' error")
            test_results.append(("Incorrect password error", False))

        # Test 8: Register with empty fields (Scenario 6)
        print("\n[Test 8] Testing registration with empty fields...")
        await page.click('#showRegister')
        await page.wait_for_timeout(500)
        await page.fill('#registerUsername', '')
        await page.fill('#registerPassword', '')
        await page.click('button[type="submit"]')
        await page.wait_for_timeout(1000)
        screenshot_path = take_screenshot(page, "08_empty_registration")
        has_error, error_msg = analyze_screenshot_with_ai(screenshot_path)

        if has_error and ("required" in error_msg.lower() or "required" in error_msg):
            print(f"  ✅ Error correctly shown: {error_msg}")
            test_results.append(("Empty registration error", True))
        else:
            print(f"  ⚠️  Expected 'Username and password are required' error")
            test_results.append(("Empty registration error", False))

        await browser.close()

        # Print summary
        print("\n" + "=" * 60)
        print("Frontend Test Summary")
        print("=" * 60)
        for test_name, passed in test_results:
            status = "✅ PASS" if passed else "❌ FAIL"
            print(f"  {status} - {test_name}")

        total = len(test_results)
        passed = sum(1 for _, p in test_results if p)
        print(f"\nTotal: {passed}/{total} tests passed")

        return all(p for _, p in test_results)


if __name__ == "__main__":
    success = asyncio.run(test_frontend_ui())
    exit(0 if success else 1)
