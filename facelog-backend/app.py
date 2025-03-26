
from flask import Flask, request, jsonify, render_template, redirect, url_for
import os
import pandas as pd
import face_recognition
import cv2

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "known_faces"

# Ensure known_faces directory exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# CSV File for Attendance
CSV_FILE = "attendance.csv"

# Ensure CSV exists
if not os.path.exists(CSV_FILE):
    df = pd.DataFrame(columns=["Name", "Roll No", "Class", "Time"])
    df.to_csv(CSV_FILE, index=False)

# Load known faces from storage
def load_known_faces():
    global known_encodings, known_names
    known_encodings = []
    known_names = []
    for filename in os.listdir(app.config["UPLOAD_FOLDER"]):
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        image = face_recognition.load_image_file(filepath)
        encoding = face_recognition.face_encodings(image)
        if encoding:
            known_encodings.append(encoding[0])
            known_names.append(os.path.splitext(filename)[0])

load_known_faces()

# 🔹 Homepage Route
@app.route("/")
def home():
    return render_template("index.html")

# 🔹 Register Route
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        roll_no = request.form.get("roll_no")
        student_class = request.form.get("class")

        if not name or not roll_no or not student_class:
            return "All fields are required!", 400

        # Save to CSV
        df = pd.read_csv(CSV_FILE)
        df = df.append({"Name": name, "Roll No": roll_no, "Class": student_class, "Time": ""}, ignore_index=True)
        df.to_csv(CSV_FILE, index=False)

        return redirect(url_for("home"))

    return render_template("register.html")

# 🔹 Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        roll_no = request.form.get("roll_no")

        # Check if roll_no exists in CSV
        df = pd.read_csv(CSV_FILE)
        student = df[df["Roll No"] == roll_no]

        if student.empty:
            return "Student not found!", 404

        return f"Welcome, {student.iloc[0]['Name']}!"

    return render_template("login.html")

# 🔹 Get Attendance
@app.route("/attendance", methods=["GET"])
def get_attendance():
    df = pd.read_csv(CSV_FILE)
    return render_template("student_records.html", records=df.to_dict(orient="records"))

# ✅ Run the app
if __name__ == "__main__":
    app.run(port=5001, debug=True)