import cv2

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("❌ Camera failed to open!")
else:
    print("✅ Camera opened successfully!")
cap.release()
