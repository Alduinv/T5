import base64
import cv2
import numpy as np
from ultralytics import YOLO

def decode_base64_image(base64_string):
    # Decode base64 string to bytes
    img_data = base64.b64decode(base64_string)
    # Convert bytes to numpy array
    np_arr = np.frombuffer(img_data, np.uint8)
    # Decode the numpy array into an image
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    return img

def detect_labels_yolo8(base64_image, model_path='bestSeg.pt'):
    # Load YOLOv8 model
    model = YOLO(model_path)
    
    # Decode base64 image
    img = decode_base64_image(base64_image)
    
    # Perform detection
    results = model.predict(img)
    
    # Extract labels from results
    labels = [model.names[int(pred.cls)] for pred in results[0].boxes]    
    
    return labels
