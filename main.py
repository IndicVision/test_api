import requests
from flask import Flask, request, jsonify
from PIL import Image, UnidentifiedImageError
from io import BytesIO

app = Flask(__name__)

@app.route("/test", methods=["GET"])
def default_method():
    return "Eikon test API"

@app.route("/upload-image/", methods=["POST"])
def upload_image():
    data = request.get_json()

    # Check if "url" field exists in the JSON payload
    if "url" not in data:
        return jsonify({"detail": "No URL provided"}), 400

    image_url = data["url"]

    try:
        # Download the image from the provided URL
        response = requests.get(image_url)
        response.raise_for_status()  # Check for HTTP errors

        # Open the image using PIL
        image = Image.open(BytesIO(response.content))
        
        # Get image details
        image_name = image_url.split("/")[-1]  # Extract file name from URL
        image_size = image.size  # (width, height)

        return jsonify({"name": image_name, "size": image_size})
    
    except UnidentifiedImageError:
        # Handle cases where the file cannot be identified as an image
        return jsonify({"detail": "Unsupported or corrupted image file"}), 400
    
    except requests.exceptions.RequestException as e:
        # Handle network-related errors
        return jsonify({"detail": f"Failed to fetch image: {str(e)}"}), 500
    
    except Exception as e:
        # Handle other unexpected errors
        return jsonify({"detail": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
