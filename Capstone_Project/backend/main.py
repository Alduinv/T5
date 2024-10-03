from fastapi import FastAPI
from pydantic import BaseModel
import loc  # Module for location details
from model import detect_labels_yolo8  # Function to detect labels using YOLO model
from uplode import upload_to_mongodb  # Function to upload data to MongoDB

app = FastAPI()

# Model to define the expected input structure
class TextRequest(BaseModel):
    ing: str 
    lat: float 
    lon: float  
    speed: float  

# Model to define the response structure
class Response(BaseModel):
    states: str 

# Endpoint to handle POST requests for analyzing data and uploading results
@app.post("/upload/", response_model=Response)
def analyze_sentiment(request: TextRequest):
    # Get additional location details using the lat and lon
    location_details = loc.get_location_details(request.lat, request.lon)
    
    # Detect labels from the input string using YOLO model
    labels = detect_labels_yolo8(request.ing)
    
    # Prepare the data dictionary to be uploaded
    data = {
        "ing": request.ing,
        "lat": request.lat,
        "lon": request.lon,
        "speed": request.speed,
        "location_details": location_details,
        "label": labels[0]  # Use the first detected label
    }
    
    # Upload the data to MongoDB and print the result
    print(upload_to_mongodb(data=data))
    
    # Return a success response
    return {
        "states": "done",
    }
