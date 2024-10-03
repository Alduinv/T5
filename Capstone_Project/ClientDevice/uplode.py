import requests


# Function to upload data to the backend
def upload_base64_image(base64_image,packet):
    url = 'http://192.168.100.7/upload'

    data = {
        "ing": base64_image,
        "lat": packet.lat,
        "lon": packet.lon,
        "speed": packet.hspeed
    }
    
    try:
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print("Success:", response.json())
        else:
            print(f"Failed with status code {response.status_code}: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")