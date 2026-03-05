# Login/Registration Web Application

A simple full-stack web application with a Python Flask backend and TypeScript frontend.

## Project Structure

```
test/
├── backend/
│   ├── app.py               # Flask application
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── index.html           # Main HTML page
│   ├── style.css            # Styling
│   ├── script.ts            # TypeScript source
│   ├── script.js            # Compiled JavaScript
│   └── tsconfig.json        # TypeScript config
├── TESTCASES.md             # Test cases documentation
└── README.md                # This file
```

## Prerequisites

- Python 3.8+
- Node.js 16+ (for TypeScript compilation)
- A web browser

## Setup Instructions

### 1. Install Backend Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Install TypeScript (if not already installed)

```bash
npm install -g typescript
```

### 3. Compile TypeScript

```bash
cd frontend
tsc
```

This compiles `script.ts` to `script.js`.

## Running the Application

### Start the Backend Server

```bash
cd backend
python app.py
```

The backend will start on `http://localhost:5000`. You should see:
```
Starting Flask server on http://localhost:5000
Endpoints:
  POST /register  - Register a new user
  POST /login     - Authenticate a user
```

### Open the Frontend

Simply open `frontend/index.html` in your web browser:
- Double-click the file in your file explorer, or
- Use `file:///` URL in your browser, or
- Serve it with a simple HTTP server: `python -m http.server 8000` in the frontend directory

## API Endpoints

### POST /register

Registers a new user.

**Request:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Registration successful"
}
```

**Error Response (409 Conflict):**
```json
{
  "success": false,
  "message": "Username already exists"
}
```

### POST /login

Authenticates a user.

**Request:**
```json
{
  "username": "string",
  "password": "string"
}
```

**Success Response (200 OK):**
```json
{
  "success": true,
  "message": "Login successful",
  "username": "string"
}
```

**Error Responses (401 Unauthorized):**
```json
{
  "success": false,
  "message": "User not found"
}
```
or
```json
{
  "success": false,
  "message": "Incorrect password"
}
```

## Testing

### Manual Testing

1. Ensure the backend is running (`python backend/app.py`)
2. Open `frontend/index.html` in your browser
3. Test the three main scenarios:
   - Try logging in with unregistered credentials
   - Register a new user
   - Log in with correct credentials
   - Log in with incorrect password

### Automated Testing (curl)

Make sure the backend is running, then execute:

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

## Important Notes

⚠️ **Security Warning**: This is a demo application with the following simplifications:
- Passwords are stored in plain text (no hashing)
- User data is stored in-memory (lost on server restart)
- No session management or JWT tokens
- No input sanitization beyond basic validation

In a production application, you would need:
- Password hashing (bcrypt, argon2)
- Persistent database (PostgreSQL, MongoDB)
- Session management or JWT authentication
- Input validation and sanitization
- Rate limiting and CSRF protection

## Test Verification

All test cases from `TESTCASES.md` have been verified:

| Scenario | Status |
|----------|--------|
| Unregistered user login | ✅ Pass - Returns "User not found" |
| Login with correct credentials | ✅ Pass - Shows welcome message |
| Login with incorrect password | ✅ Pass - Returns "Incorrect password" |
| Register new user | ✅ Pass - Creates user successfully |
| Register existing username | ✅ Pass - Returns "Username already exists" |

## Troubleshooting

**Backend won't start:**
- Ensure Python 3.8+ is installed
- Check that Flask is installed: `pip show flask`
- Check that port 5000 is not in use by another application

**Frontend shows connection errors:**
- Verify the backend is running on `http://localhost:5000`
- Check browser console for CORS errors
- Ensure flask-cors is installed

**TypeScript compilation issues:**
- Ensure TypeScript is installed: `tsc --version`
- Check that `tsconfig.json` exists in the frontend directory
