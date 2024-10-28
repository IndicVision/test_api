from fastapi import FastAPI, File, UploadFile, HTTPException
from PIL import Image, UnidentifiedImageError
from io import BytesIO

app = FastAPI()

@app.get("/test")
async def default_method():
    return "Eikon test API"
    
@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    # Check if the uploaded file is an image
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File is not an image.")

    try:
        # Read image content
        contents = await file.read()
        image = Image.open(BytesIO(contents))
        
        # Get image details
        image_name = file.filename
        image_size = image.size  # (width, height)

        return {"name": image_name, "size": image_size}
    
    except UnidentifiedImageError:
        # Handle cases where the file cannot be identified as an image
        raise HTTPException(status_code=400, detail="Unsupported or corrupted image file.")
    
    except Exception as e:
        # Handle other unexpected errors
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
