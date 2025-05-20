from flask import Flask, request, jsonify
from flask_cors import CORS
import db_helper

app = Flask(__name__)
CORS(app)

# Dummy credentials (for demo)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"
AUTH_TOKEN = "secret-token"

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    if data.get("username") == ADMIN_USERNAME and data.get("password") == ADMIN_PASSWORD:
        return jsonify({"token": AUTH_TOKEN})
    return jsonify({"message": "Invalid credentials"}), 401

@app.route("/api/upload", methods=["POST"])
def upload():
    auth = request.headers.get("Authorization")
    if auth != f"Bearer {AUTH_TOKEN}":
        return jsonify({"message": "Unauthorized"}), 403
    data = request.json
    roll = data.get("roll")
    name = data.get("name")
    marks = data.get("marks")
    if roll and name and marks:
        db_helper.insert_result(roll, name, marks)
        return jsonify({"message": "Result uploaded successfully!"})
    return jsonify({"message": "Missing data"}), 400

@app.route("/api/result/<roll_no>", methods=["GET"])
def get_result(roll_no):
    result = db_helper.get_result(roll_no)
    if result:
        return jsonify({"name": result[0], "marks": result[1]})
    return jsonify({"message": "Result not found"}), 404

db_helper.create_table()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

