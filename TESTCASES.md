# Test Cases for Login/Registration Application

## Scenario 1: Unregistered User Attempts Login
**Given**: User is not registered in the system
**When**: User submits login with username="nonexistent" and password="anypassword"
**Then**:
  - System returns HTTP 401 Unauthorized or HTTP 200 with `{"success": false, "message": "User not found"}`
  - No authentication session is created
  - Error message is displayed to user

## Scenario 2: Registered User Logs In with Correct Credentials
**Given**: User is registered with username="testuser" and password="testpass123"
**When**: User submits login with username="testuser" and password="testpass123"
**Then**:
  - System returns HTTP 200 OK with `{"success": true, "message": "Login successful", "username": "testuser"}`
  - Welcome message "Welcome, testuser!" is displayed
  - User is considered authenticated

## Scenario 3: Registered User Logs In with Incorrect Password
**Given**: User is registered with username="testuser" and password="testpass123"
**When**: User submits login with username="testuser" and password="wrongpass"
**Then**:
  - System returns HTTP 401 Unauthorized or HTTP 200 with `{"success": false, "message": "Incorrect password"}`
  - No authentication session is created
  - Error message "Incorrect password" is displayed to user

## Additional Test Cases

## Scenario 4: Register New User Successfully
**Given**: No user with username="newuser" exists
**When**: User submits registration with username="newuser" and password="password123"
**Then**:
  - System returns HTTP 200 OK with `{"success": true, "message": "Registration successful"}`
  - User is stored in the system
  - User can subsequently log in with those credentials

## Scenario 5: Register with Existing Username
**Given**: User with username="existinguser" already exists
**When**: User submits registration with username="existinguser" and password="anypass"
**Then**:
  - System returns HTTP 409 Conflict with `{"success": false, "message": "Username already exists"}`
  - No duplicate user is created

## Testing Notes

### Manual Testing Steps:
1. Start the backend server: `python backend/app.py`
2. Open `frontend/index.html` in a browser
3. Test each scenario through the UI

### Automated Testing (curl):
```bash
# Scenario 1: Unregistered user login
curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d '{"username":"nonexistent","password":"anypass"}'

# Scenario 4: Register new user
curl -X POST http://localhost:5000/register -H "Content-Type: application/json" -d '{"username":"testuser","password":"testpass123"}'

# Scenario 2: Login with correct credentials
curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d '{"username":"testuser","password":"testpass123"}'

# Scenario 3: Login with incorrect password
curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d '{"username":"testuser","password":"wrongpass"}'

# Scenario 5: Register existing username
curl -X POST http://localhost:5000/register -H "Content-Type: application/json" -d '{"username":"testuser","password":"anotherpass"}'
```
