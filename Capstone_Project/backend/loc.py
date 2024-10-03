import requests

def get_location_details(lat, lon):
    api_key = "pk.4970a7f3c6c68895b6fbce460a4aa0ee"
    url = f"https://us1.locationiq.com/v1/reverse.php?key={api_key}&lat={lat}&lon={lon}&format=json"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an error for HTTP errors
        data = response.json()

        # Return the address details directly
        return data.get("address", {})

    except requests.exceptions.HTTPError as e:
        if response.status_code == 401:
            print("Error 401: Unauthorized. Please check your API key.")
        else:
            print(f"HTTP error occurred: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching location data: {e}")
    
    return None