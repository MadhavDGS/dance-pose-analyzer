"""
FastAPI server for dance pose analysis.
Provides endpoints for video upload and processing.
"""

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import uuid
import shutil
from pathlib import Path
from typing import Optional

from .video_processor import VideoProcessor
from .pose_detector import PoseDetector


# Initialize FastAPI app
app = FastAPI(
    title="Dance Pose Analyzer API",
    description="API for analyzing body movements in dance videos using MediaPipe",
    version="1.0.0"
)

# Add CORS middleware to allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup directories
BASE_DIR = Path(__file__).parent.parent
UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"

UPLOAD_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)

# Initialize processor (reused across requests)
pose_detector = PoseDetector(min_detection_confidence=0.5, min_tracking_confidence=0.5)
video_processor = VideoProcessor(pose_detector)

# Store to keep track of processed videos
processed_videos = {}


@app.get("/")
async def root():
    """Root endpoint - redirects to API documentation"""
    return {
        "service": "Dance Pose Analyzer API",
        "version": "1.0.0",
        "status": "running",
        "description": "Analyzes body movements in dance videos using MediaPipe pose detection",
        "documentation": "/docs",
        "usage": {
            "step_1": "POST /api/analyze with video file",
            "step_2": "Copy video_id from response",
            "step_3": "GET /api/download/{video_id} to download processed video"
        },
        "endpoints": {
            "upload": "POST /api/analyze",
            "download": "GET /api/download/{video_id}",
            "status": "GET /api/status/{video_id}",
            "health": "GET /health"
        }
    }





@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "dance-pose-analyzer"}


@app.post("/api/analyze")
async def analyze_video(video: UploadFile = File(...)):
    """
    Upload and analyze a dance video.
    
    Args:
        video: Video file (mp4, avi, mov supported)
        
    Returns:
        JSON with video_id and download URL
    """
    # Validate file type
    allowed_extensions = {'.mp4', '.avi', '.mov'}
    file_ext = Path(video.filename).suffix.lower()
    
    if file_ext not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Invalid file format",
                "your_file": video.filename,
                "allowed_formats": ["mp4", "avi", "mov"],
                "message": "Please upload a video file in one of the supported formats"
            }
        )
    
    # Generate unique ID for this video
    video_id = str(uuid.uuid4())
    
    # Save uploaded file
    input_path = UPLOAD_DIR / f"{video_id}{file_ext}"
    output_path = OUTPUT_DIR / f"{video_id}_processed.mp4"
    
    try:
        # Write uploaded file to disk
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(video.file, buffer)
        
        # Get video info before processing
        video_info = video_processor.get_video_info(str(input_path))
        
        if video_info is None:
            raise HTTPException(status_code=400, detail="Invalid video file")
        
        # Process the video
        success, message = video_processor.process_video(
            str(input_path),
            str(output_path),
            show_progress=True
        )
        
        if not success:
            raise HTTPException(status_code=500, detail=message)
        
        # Store metadata
        processed_videos[video_id] = {
            "original_filename": video.filename,
            "input_path": str(input_path),
            "output_path": str(output_path),
            "status": "completed",
            "message": message,
            "video_info": video_info
        }
        
        return {
            "success": True,
            "video_id": video_id,
            "status": "completed",
            "processing_info": message,
            "download": {
                "url": f"/api/download/{video_id}",
                "direct_link": f"http://localhost:8000/api/download/{video_id}",
                "note": "Click the direct_link to download your processed video"
            },
            "original_video": video_info
        }
    
    except HTTPException:
        raise
    except Exception as e:
        # Clean up on error
        if input_path.exists():
            input_path.unlink()
        if output_path.exists():
            output_path.unlink()
        
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@app.get("/api/download/{video_id}")
async def download_video(video_id: str):
    """
    Download processed video.
    
    Args:
        video_id: Unique video identifier
        
    Returns:
        Processed video file
    """
    if video_id not in processed_videos:
        raise HTTPException(status_code=404, detail="Video not found")
    
    video_data = processed_videos[video_id]
    output_path = video_data["output_path"]
    
    if not os.path.exists(output_path):
        raise HTTPException(status_code=404, detail="Processed video file not found")
    
    return FileResponse(
        output_path,
        media_type="video/mp4",
        filename=f"processed_{video_data['original_filename']}"
    )


@app.get("/api/status/{video_id}")
async def get_status(video_id: str):
    """
    Get processing status for a video.
    
    Args:
        video_id: Unique video identifier
        
    Returns:
        Status information
    """
    if video_id not in processed_videos:
        raise HTTPException(status_code=404, detail="Video not found")
    
    return processed_videos[video_id]


@app.delete("/api/cleanup/{video_id}")
async def cleanup_video(video_id: str):
    """
    Delete processed video files to free up space.
    
    Args:
        video_id: Unique video identifier
    """
    if video_id not in processed_videos:
        raise HTTPException(status_code=404, detail="Video not found")
    
    video_data = processed_videos[video_id]
    
    # Remove files
    for path_key in ["input_path", "output_path"]:
        path = Path(video_data[path_key])
        if path.exists():
            path.unlink()
    
    # Remove from tracking
    del processed_videos[video_id]
    
    return {"message": "Video files cleaned up successfully"}


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup resources on shutdown"""
    video_processor.cleanup()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
