from flask import Flask, jsonify, request, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Mock user database
# In a real application, this would be in MongoDB
MOCK_USERS = {
    "admin": {
        "hash": generate_password_hash("admin_pass"),
        "role": "Administrator"
    },
    "analyst": {
        "hash": generate_password_hash("analyst_pass"),
        "role": "Analyst"
    }
}

def create_app():
    app = Flask(__name__, static_folder='../../frontend', static_url_path='')
    app.secret_key = os.urandom(24)

    @app.route('/')
    def index():
        return app.send_static_file('index.html')

    @app.route('/api/auth/login', methods=['POST'])
    def login():
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = MOCK_USERS.get(username)
        if user and check_password_hash(user['hash'], password):
            session['username'] = username
            session['role'] = user['role']
            return jsonify({"success": True, "message": "Login successful", "role": user['role']})
        
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

    @app.route('/api/auth/logout', methods=['POST'])
    def logout():
        session.clear()
        return jsonify({"success": True, "message": "Logout successful"})

    @app.route('/api/auth/status')
    def status():
        if 'username' in session:
            return jsonify({"isLoggedIn": True, "username": session['username'], "role": session['role']})
        return jsonify({"isLoggedIn": False})

    # Mock encryption function for sensitive data
    def encrypt_data(data):
        # This is a mock function. In a real-world scenario, use a robust
        # encryption library like cryptography.
        return f"encrypted_{data}"

    # Mock decryption function
    def decrypt_data(encrypted_data):
        return encrypted_data.replace("encrypted_", "")

    @app.route('/api/climate-data')
    def get_climate_data():
        if 'username' not in session:
            return jsonify({"error": "Unauthorized"}), 401
        
        # In a real app, this data would come from HDFS/processed jobs
        mock_data = {
            "average_temp_region": {
                "North": encrypt_data("15.5°C"),
                "South": encrypt_data("22.3°C"),
                "East": encrypt_data("18.1°C"),
                "West": encrypt_data("20.8°C")
            },
            "humidity_trends": {
                "North": "Stable",
                "South": "Increasing",
            }
        }
        return jsonify(mock_data)

    @app.route('/api/alerts')
    def get_alerts():
        if 'username' not in session:
            return jsonify({"error": "Unauthorized"}), 401
        
        # Mock alerts from the ML model
        mock_alerts = [
            {"id": 1, "severity": "High", "message": "Anomaly Detected: Unusually high temperature spike in South region."},
            {"id": 2, "severity": "Medium", "message": "Prediction: Increased probability of drought in West region next quarter."}
        ]
        return jsonify(mock_alerts)

    @app.route('/api/feedback', methods=['POST'])
    def submit_feedback():
        if 'username' not in session:
            return jsonify({"error": "Unauthorized"}), 401
        
        data = request.get_json()
        # In a real app, store this feedback in a database
        print(f"Feedback received from {session['username']}: {data.get('feedback')}")
        return jsonify({"success": True, "message": "Thank you for your feedback!"})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
