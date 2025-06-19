import os
import shutil
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# The base path where your network volume is mounted inside the container
BASE_STORAGE_PATH = "/runpod-volume/datasets"

app = FastAPI()

# IMPORTANT: Configure CORS to allow requests from your website
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://mly.thiratpy.in.th", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload-image/")
async def upload_image(
    project_id: str = Form(...),
    class_name: str = Form(...),
    file: UploadFile = File(...)
):
    """
    Receives a single image and saves it to the RunPod Network Volume.
    """
    try:
        # Sanitize class_name to prevent directory traversal issues
        safe_class_name = os.path.basename(class_name)
        
        # Construct the full path where the file will be saved
        target_dir = os.path.join(BASE_STORAGE_PATH, project_id, safe_class_name)
        
        # Create the directories if they don't exist
        os.makedirs(target_dir, exist_ok=True)
        
        file_path = os.path.join(target_dir, file.filename)
        
        # Write the file chunk by chunk to the network storage
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        return {
            "status": "success",
            "message": f"File '{file.filename}' uploaded successfully.",
            "path": file_path
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload file: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)