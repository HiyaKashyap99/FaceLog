# import cv2
# import face_recognition
# import os

# # Paths
# KNOWN_FACES_DIR = "known_faces"
# if not os.path.exists(KNOWN_FACES_DIR):
#     os.makedirs(KNOWN_FACES_DIR)

# # Load known faces
# known_encodings = []
# known_names = []

# # Load existing known faces
# for filename in os.listdir(KNOWN_FACES_DIR):
#     image_path = os.path.join(KNOWN_FACES_DIR, filename)
#     image = face_recognition.load_image_file(image_path)
#     encoding = face_recognition.face_encodings(image)
#     if encoding:
#         known_encodings.append(encoding[0])
#         known_names.append(os.path.splitext(filename)[0])  # Remove file extension

# # Start webcam
# video_capture = cv2.VideoCapture(0)

# try:
#     while True:
#         ret, frame = video_capture.read()
#         if not ret:
#             print("Failed to access the webcam!")
#             break

#         rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

#         # Detect faces
#         face_locations = face_recognition.face_locations(rgb_frame)
#         face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

#         for face_encoding, face_location in zip(face_encodings, face_locations):
#             matches = face_recognition.compare_faces(known_encodings, face_encoding)
#             name = "Unknown"

#             if True in matches:
#                 matched_index = matches.index(True)
#                 name = known_names[matched_index]
#             else:
#                 # New Face Detected
#                 print("\n🔹 New face detected! Please enter your name:")
#                 user_name = input("Enter your name: ").strip()

#                 if user_name:
#                     # Save the new face
#                     file_path = os.path.join(KNOWN_FACES_DIR, f"{user_name}.jpg")
#                     top, right, bottom, left = face_location
#                     face_image = frame[top:bottom, left:right]
#                     cv2.imwrite(file_path, face_image)

#                     print(f"✅ Face saved as {file_path}")

#                     # Reload the new face
#                     new_image = face_recognition.load_image_file(file_path)
#                     new_encoding = face_recognition.face_encodings(new_image)

#                     if new_encoding:
#                         known_encodings.append(new_encoding[0])
#                         known_names.append(user_name)
#                         name = user_name
#                     else:
#                         print("⚠️ Error encoding the new face!")

#             # Draw rectangle & name
#             top, right, bottom, left = face_location
#             cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
#             cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

#         # Display the video frame
#         cv2.imshow("Face Recognition Attendance", frame)

#         # Check if 'q' is pressed or if the window is closed
#         if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty("Face Recognition Attendance", cv2.WND_PROP_VISIBLE) < 1:
#             break

# finally:
#     # Release camera and close all windows
#     video_capture.release()
#     cv2.destroyAllWindows()
#     print("\n🎯 Webcam closed successfully!")

import cv2
import face_recognition
import os
import csv
from datetime import datetime

# Paths
KNOWN_FACES_DIR = "known_faces"
ATTENDANCE_FILE = "attendance.csv"

# Ensure directories and files exist
if not os.path.exists(KNOWN_FACES_DIR):
    os.makedirs(KNOWN_FACES_DIR)

if not os.path.exists(ATTENDANCE_FILE):
    with open(ATTENDANCE_FILE, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Date", "Time"])  # Write header if file is new

# Load known faces
known_encodings = []
known_names = []

# Load existing known faces
for filename in os.listdir(KNOWN_FACES_DIR):
    image_path = os.path.join(KNOWN_FACES_DIR, filename)
    image = face_recognition.load_image_file(image_path)
    encoding = face_recognition.face_encodings(image)
    if encoding:
        known_encodings.append(encoding[0])
        known_names.append(os.path.splitext(filename)[0])  # Remove file extension

# Start webcam
video_capture = cv2.VideoCapture(0)

try:
    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("⚠️ Failed to access the webcam!")
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect faces
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_encodings, face_encoding)
            name = "Unknown"

            if True in matches:
                matched_index = matches.index(True)
                name = known_names[matched_index]

                # Mark attendance
                now = datetime.now()
                date = now.strftime("%Y-%m-%d")
                time = now.strftime("%H:%M:%S")

                with open(ATTENDANCE_FILE, "r") as file:
                    reader = csv.reader(file)
                    recorded_entries = [row for row in reader]

                if [name, date] not in [[row[0], row[1]] for row in recorded_entries]:
                    with open(ATTENDANCE_FILE, "a", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow([name, date, time])
                        print(f"✅ Attendance marked for {name} at {time}")

            else:
                # New Face Detected
                print("\n🔹 New face detected! Please enter your name:")
                user_name = input("Enter your name: ").strip()

                if user_name:
                    # Save the new face
                    file_path = os.path.join(KNOWN_FACES_DIR, f"{user_name}.jpg")
                    top, right, bottom, left = face_location
                    face_image = frame[top:bottom, left:right]
                    cv2.imwrite(file_path, face_image)

                    print(f"✅ Face saved as {file_path}")

                    # Reload the new face
                    new_image = face_recognition.load_image_file(file_path)
                    new_encoding = face_recognition.face_encodings(new_image)

                    if new_encoding:
                        known_encodings.append(new_encoding[0])
                        known_names.append(user_name)
                        name = user_name
                    else:
                        print("⚠️ Error encoding the new face!")

            # Draw rectangle & name
            top, right, bottom, left = face_location
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        # Display the video frame
        cv2.imshow("Face Recognition Attendance", frame)

        # Check if 'q' is pressed or if the window is closed
        if cv2.waitKey(1) & 0xFF == ord('q') or cv2.getWindowProperty("Face Recognition Attendance", cv2.WND_PROP_VISIBLE) < 1:
            break

finally:
    # Release camera and close all windows
    video_capture.release()
    cv2.destroyAllWindows()
    print("\n🎯 Webcam closed successfully!")