from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

# In-memory user storage (in production, use a real database)
users = {}

@app.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    Expects JSON: {"username": string, "password": string}
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400

        username = data.get('username')
        password = data.get('password')

        # Validate required fields
        if not username or not password:
            return jsonify({"success": False, "message": "Username and password are required"}), 400

        # Check if user already exists
        if username in users:
            return jsonify({"success": False, "message": "Username already exists"}), 409

        # Store user (in production, hash the password!)
        users[username] = password

        return jsonify({"success": True, "message": "Registration successful"}), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@app.route('/login', methods=['POST'])
def login():
    """
    Authenticate a user.
    Expects JSON: {"username": string, "password": string}
    """
    try:
        data = request.get_json()

        if not data:
            return jsonify({"success": False, "message": "No data provided"}), 400

        username = data.get('username')
        password = data.get('password')

        # Validate required fields
        if not username or not password:
            return jsonify({"success": False, "message": "Username and password are required"}), 400

        # Check if user exists
        if username not in users:
            return jsonify({"success": False, "message": "User not found"}), 401

        # Check password
        if users[username] != password:
            return jsonify({"success": False, "message": "Incorrect password"}), 401

        # Successful login
        return jsonify({
            "success": True,
            "message": "Login successful",
            "username": username
        }), 200

    except Exception as e:
        return jsonify({"success": False, "message": f"Server error: {str(e)}"}), 500


@app.route('/reset_users', methods=['POST'])
def reset_users():
    """
    Reset the users dictionary (for testing purposes).
    This endpoint should only be used in testing environments.
    """
    global users
    users.clear()
    return jsonify({"success": True, "message": "Users reset"}), 200


if __name__ == '__main__':
    print("Starting Flask server on http://localhost:5000")
    print("Endpoints:")
    print("  POST /register  - Register a new user")
    print("  POST /login     - Authenticate a user")
    print("  POST /reset_users - Reset user database (testing only)")
    app.run(debug=True, host='0.0.0.0', port=5000)
