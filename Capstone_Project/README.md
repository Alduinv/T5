Spothole: Pothole Detection and Severity Classification System

Overview:

Spothole is a pothole detection system integrated with a Raspberry Pi 4 and computer vision technology using YOLOv8 for real-time object detection. The project aims to detect potholes from dash cam footage connected to the Raspberry Pi and then sends the image and GPS location to an API. The API processes the GPS coordinates and stores them in a database, while the image is forwarded to another YOLOv8 model to classify the pothole's severity. Finally, the results are visualized on a Power BI dashboard, showing the locations and relevant statistics for road maintenance and traffic management.

Features:

Real-time Pothole Detection: Detect potholes from dash cam footage using YOLOv8 running on a Raspberry Pi 4.
GPS Integration: Capture and send GPS coordinates along with pothole images for accurate location tracking.
Severity Classification: Classify detected potholes based on severity using a secondary YOLOv8 model.
API Integration: Send pothole data (images and GPS) to an API for processing and database storage.
Dashboard Visualization: Display pothole locations and statistics on a Power BI dashboard for easy monitoring and decision-making.


System Architecture:

Pothole Detection:

Dash cam captures road footage.
Raspberry Pi 4 processes the video feed using YOLOv8 to detect potholes in real-time.
Data Transmission:

When a pothole is detected, the system sends the captured image and GPS coordinates to the API.
API Processing:

The API stores the GPS coordinates in a database.
The API passes the image to another YOLOv8 model to classify the severity of the pothole.
Data Storage & Visualization:

The API saves the results (severity and GPS location) in a database.
Power BI pulls the data from the database to visualize pothole locations and statistics, aiding road maintenance efforts.



Demo 
