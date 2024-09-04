import streamlit as st
import torch
import tempfile
import os
from ultralytics import YOLO

# Load the YOLO model
model = YOLO('best.pt')

def process_video(video_file):
    # Save the uploaded video to a temporary file
    temp_input = tempfile.NamedTemporaryFile(delete=False, suffix='.mp4')
    temp_input.write(video_file.read())
    temp_input.close()

    # Predict using YOLO and save the output video
    results = model.predict(source=temp_input.name, save=True)

    # Determine the directory where the YOLO model saved the output
    output_dir = results[0].save_dir

    # Find the saved output video
    output_file = None
    for f in os.listdir(output_dir):
        if f.endswith('.avi'):
            output_file = f
            break

    if output_file is None:
        raise FileNotFoundError("Processed video file not found.")

    out_video_path = os.path.join(output_dir, output_file)

    return out_video_path

# Streamlit UI
st.title('Pothole Detection on Video')
st.write('Upload a video containing potholes to perform object detection using YOLO.')

uploaded_file = st.file_uploader("Choose a video file", type=["mp4", "avi", "mov", "mkv"])

if uploaded_file is not None:
    st.video(uploaded_file)

    st.write("Processing the video... This may take some time.")
    processed_video_path = process_video(uploaded_file)
    
    st.write("Object detection complete. Download the file to view")
    st.download_button("Download Processed Video", data=open(processed_video_path, 'rb').read(), file_name="processed_video.mp4")

    # Clean up temporary files
    os.remove(processed_video_path)