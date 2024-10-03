import cv2
from ultralytics import YOLO
import base64
import numpy as np
import gpsd
gpsd.connect()

from uplode import upload_base64_image

# Load the YOLOv8 model
model = YOLO('best.pt')  # Replace with your actual model path

# Initialize the webcam (0 is the default camera, change if necessary)
cap = cv2.VideoCapture(0)

# Check if the camera is opened successfully
if not cap.isOpened():
    print("Error: Could not open camera")
    exit()

def encode_frame_to_base64(frame):
    """Encodes a frame (image) as a base64 string."""
    # Convert the frame to JPEG format
    _, buffer = cv2.imencode('.jpg', frame)
    
    # Convert the buffer to a byte array and then to a base64 string
    img_base64 = base64.b64encode(buffer).decode('utf-8')
    
    return img_base64

# Loop to continuously capture frames and perform object detection
while True:
    ret, frame = cap.read()  # Capture frame-by-frame
    if not ret:
        print("Error: Failed to capture image")
        break

    # Run YOLOv8 inference on the captured frame
    results = model(frame)

    # Check if any objects are detected
    if len(results[0].boxes) > 0:
        # Get the highest confidence of detected objects
        if results[0].boxes.conf.max() > 0.5:
            print("Object detected!")

            # Encode the frame as base64
            frame_base64 = encode_frame_to_base64(frame)
            packet = gpsd.get_current()
            print(f"Latitude: {packet.lat}")
            upload_base64_image(frame_base64,packet)
            
    # Exit loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
