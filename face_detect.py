import cv2  
import os  

# Load Haar Cascade  
face_cascade = cv2.CascadeClassifier('/Users/hiyakashyap/facelog/haarcascade_frontalface_default.xml')

# Create the folder if it doesn't exist  
if not os.path.exists("captured_faces"):  
    os.makedirs("captured_faces")  

# Start Webcam  
cap = cv2.VideoCapture(0)  
img_counter = 0  

while True:  
    ret, frame = cap.read()  
    if not ret:  
        print("Failed to capture image")  
        break  

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))  

    for (x, y, w, h) in faces:  
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)  

    cv2.imshow('Face Detection', frame)  

    key = cv2.waitKey(1)  
    if key == ord("s"):  # Press 's' to Save Image  
        img_name = f"captured_faces/captured_face_{img_counter}.jpg"  
        cv2.imwrite(img_name, frame)  
        print(f"✅ Image saved as {img_name}")  
        img_counter += 1  

    elif key == ord("q"):  # Press 'q' to Quit  
        break  

cap.release()  
cv2.destroyAllWindows()  