from flask import Flask, request, jsonify
from PIL import Image, UnidentifiedImageError
from io import BytesIO

app = Flask(__name__)

@app.route("/test", methods=["GET"])
def default_method():
    return "Eikon test API"

@app.route("/upload-image/", methods=["POST"])
def upload_image():
    # Check if a file was uploaded
    if 'file' not in request.files:
        return jsonify({"detail": "No file uploaded"}), 400

    file = request.files['file']

    # Check if the uploaded file is an image
    if not file.content_type.startswith("image/"):
        return jsonify({"detail": "File is not an image"}), 400

    try:
        # Read image content
        contents = file.read()
        image = Image.open(BytesIO(contents))
        
        # Get image details
        image_name = file.filename
        image_size = image.size  # (width, height)

        return jsonify({"name": image_name, "size": image_size})
    
    except UnidentifiedImageError:
        # Handle cases where the file cannot be identified as an image
        return jsonify({"detail": "Unsupported or corrupted image file"}), 400
    
    except Exception as e:
        # Handle other unexpected errors
        return jsonify({"detail": f"An error occurred: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
