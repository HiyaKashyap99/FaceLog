from flask import Flask, request, jsonify, render_template
import pandas as pd
import os
from flask_cors import CORS

app = Flask(__name__, template_folder="templates")
CORS(app)  # Allow frontend requests

# CSV file paths
STUDENT_CSV = "students.csv"
# Use the global attendance.csv file
ATTENDANCE_CSV = "/Users/hiyakashyap/facelog/attendance.csv"

# Ensure the correct CSV exists
def ensure_csv(file_path, columns):
    if not os.path.exists(file_path) or os.stat(file_path).st_size == 0:
        pd.DataFrame(columns=columns).to_csv(file_path, index=False)

ensure_csv(ATTENDANCE_CSV, ["Date", "Name", "Roll No", "Class", "Status"])
# ✅ Home Route (Serve index.html)
@app.route('/')
def home():
    return render_template('index.html')

# ✅ Route: Render Login Page
@app.route('/login')
def login_page():
    return render_template('login.html')

# ✅ Route: Render Student Records Page
@app.route('/records')
def records_page():
    return render_template('records.html')

# ✅ Route: Register Student
@app.route('/register', methods=['POST'])  # Only allows POST requests
def register():
    data = request.json
    df = pd.read_csv(STUDENT_CSV)

    # Check if student already exists
    if str(data["Roll No"]) in df["Roll No"].astype(str).values:
        return jsonify({"message": "Student already registered!"}), 400

    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
    df.to_csv(STUDENT_CSV, index=False)
    return jsonify({"message": "Student registered successfully!"})


# ✅ Route: Get Student List
@app.route('/students', methods=['GET'])
def get_students():
    df = pd.read_csv(STUDENT_CSV)
    return jsonify(df.to_dict(orient="records"))

# ✅ Route: Get Attendance Records
@app.route('/attendance', methods=['GET'])
def get_attendance():
    ensure_csv(ATTENDANCE_CSV, ["Date", "Name", "Roll No", "Class", "Status"])
    df = pd.read_csv(ATTENDANCE_CSV)

    if df.empty:
        return jsonify({"message": "No attendance records found!"}), 200

    return jsonify(df.to_dict(orient="records"))

# ✅ Run Server on Port 5001
if __name__ == '__main__':
    app.run(debug=True, port=5001)