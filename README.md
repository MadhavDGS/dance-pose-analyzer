# Dance Pose Analyzer

A cloud-based AI/ML server that analyzes body movements in dance videos using MediaPipe pose detection. The system processes uploaded videos and generates output videos with skeleton overlay showing detected body keypoints and movements in real-time.

## Overview

This project implements a complete video processing pipeline that:
- Accepts short-form dance videos through a REST API
- Detects human pose keypoints using MediaPipe
- Renders skeleton overlay on the video
- Returns the processed video with movement visualization

## Tech Stack

- **Python 3.10** - Core programming language
- **MediaPipe** - Google's ML solution for pose detection
- **OpenCV** - Video processing and rendering
- **FastAPI** - Modern, high-performance web framework
- **Docker** - Containerization for consistent deployment
- **NumPy** - Numerical computing for video frame manipulation

## Project Structure

```
dance-pose-analyzer/
├── src/
│   ├── __init__.py
│   ├── pose_detector.py      # MediaPipe pose detection logic
│   ├── video_processor.py    # Video I/O and frame processing
│   └── api.py                 # FastAPI REST endpoints
├── tests/
│   ├── test_pose_detector.py
│   └── test_video_processor.py
├── uploads/                   # Temporary storage for uploaded videos
├── outputs/                   # Processed videos with skeleton overlay
├── Dockerfile
├── requirements.txt
└── README.md
```

## Setup Instructions

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd dance-pose-analyzer
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server**
   Recommended: use the provided helper which ensures the project's virtual environment is used:
   ```bash
   ./start_server.sh
   ```
   Or run directly with the venv python:
   ```bash
   venv/bin/python -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
   ```

5. **Access the API**
   - API Documentation: `http://localhost:8000/docs`
   - Health Check: `http://localhost:8000/health`

### Docker Deployment

1. **Build the Docker image**
   ```bash
   docker build -t dance-pose-analyzer .
   ```

2. **Run the container**
   ```bash
   docker run -d -p 8000:8000 --name pose-analyzer dance-pose-analyzer
   ```

3. **Check logs**
   ```bash
   docker logs pose-analyzer
   ```

## API Usage

### Upload and Analyze Video

**Endpoint:** `POST /api/analyze`

**Request:**
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "video=@dance_video.mp4"
```

**Response:**
```json
{
  "video_id": "uuid-string",
  "status": "completed",
  "message": "Video processed successfully. Processed 150 frames. Pose detected in 145 frames (96.7%).",
  "download_url": "/api/download/uuid-string",
  "video_info": {
    "width": 1920,
    "height": 1080,
    "fps": 30,
    "frame_count": 150,
    "duration_seconds": 5.0
  }
}
```

### Download Processed Video

**Endpoint:** `GET /api/download/{video_id}`

```bash
curl -O "http://localhost:8000/api/download/uuid-string"
```

### Check Processing Status

**Endpoint:** `GET /api/status/{video_id}`

```bash
curl "http://localhost:8000/api/status/uuid-string"
```

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_pose_detector.py -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html
```

## Cloud Deployment

### Railway Deployment

1. Install Railway CLI:
   ```bash
   npm install -g @railway/cli
   ```

2. Login and deploy:
   ```bash
   railway login
   railway init
   railway up
   ```

### AWS EC2 Deployment

1. Launch EC2 instance (t2.medium or larger recommended)
2. SSH into instance
3. Install Docker:
   ```bash
   sudo yum update -y
   sudo yum install docker -y
   sudo service docker start
   ```
4. Clone repository and build:
   ```bash
   git clone <repo-url>
   cd dance-pose-analyzer
   sudo docker build -t pose-analyzer .
   sudo docker run -d -p 80:8000 pose-analyzer
   ```

### Google Cloud Run Deployment

1. Build and push to Container Registry:
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/pose-analyzer
   ```

2. Deploy to Cloud Run:
   ```bash
   gcloud run deploy pose-analyzer \
     --image gcr.io/PROJECT_ID/pose-analyzer \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

## Technical Implementation

### Pose Detection

The system uses MediaPipe Pose, which detects 33 body landmarks including:
- Face (eyes, nose, mouth)
- Upper body (shoulders, elbows, wrists)
- Torso (hips)
- Lower body (knees, ankles, feet)

Configuration parameters:
- `min_detection_confidence`: 0.5 (threshold for initial detection)
- `min_tracking_confidence`: 0.5 (threshold for tracking across frames)
- `model_complexity`: 1 (balance between speed and accuracy)

### Video Processing Pipeline

1. **Input Validation**: Check file format and size
2. **Frame Extraction**: Read video frame-by-frame using OpenCV
3. **Pose Detection**: Process each frame through MediaPipe
4. **Skeleton Rendering**: Draw connections between detected landmarks
5. **Video Reconstruction**: Write processed frames to output video
6. **Metadata Generation**: Track detection rates and processing stats

### Performance Considerations

- Frame processing: ~30-50ms per frame on CPU
- GPU acceleration available through MediaPipe
- Async processing for multiple concurrent requests
- File cleanup to manage storage

## Thought Process & Technical Decisions

### Architecture Philosophy
The project follows a **modular pipeline architecture** with clear separation of concerns:
- `PoseDetector`: Encapsulates MediaPipe logic and rendering
- `VideoProcessor`: Handles video I/O and frame-by-frame processing
- `API Layer`: Exposes functionality via REST endpoints

This design enables:
- Easy testing of individual components
- Swapping detection algorithms without changing the API
- Reusing the video processor for batch jobs or CLI tools

### Why MediaPipe over OpenPose?
**OpenPose** was the initial consideration as the gold standard for pose estimation, but **MediaPipe** was chosen for several reasons:

1. **Performance**: MediaPipe runs at 30-50ms/frame on CPU vs OpenPose's 200-300ms
2. **Deployment**: MediaPipe has Python pip package vs OpenPose's complex CMake build
3. **Model Size**: MediaPipe models are ~20MB vs OpenPose's ~200MB
4. **Cloud Economics**: Faster processing = lower compute costs for cloud deployment
5. **Maintenance**: Google actively maintains MediaPipe with regular updates
6. **Production Ready**: Used in Google products (YouTube, Lens) proving reliability

**Trade-off**: MediaPipe detects 33 landmarks vs OpenPose's 25, but has slightly lower accuracy on complex poses. For dance videos with clear body visibility, MediaPipe's accuracy is sufficient.

### Why FastAPI over Flask/Django?
1. **Async Native**: Critical for handling multiple video uploads without blocking
2. **Auto Documentation**: Swagger UI at `/docs` provides interactive testing
3. **Type Safety**: Pydantic models catch errors before they reach production
4. **Performance**: 2-3x faster than Flask due to async architecture
5. **Modern Python**: Embraces Python 3.10+ features (type hints, async/await)

### Why Frame-by-Frame Processing?
Alternative approaches considered:
- **Batch Processing**: Load all frames into memory → Rejected due to memory constraints (4K video = 2GB+ RAM)
- **GPU Batching**: Process multiple frames simultaneously → Saved for future optimization
- **Frame-by-Frame**: Chosen for memory efficiency and simplicity

Current approach allows processing videos of any length with constant memory usage (~100MB).

### Docker Multi-Stage Build Strategy
The Dockerfile uses a single-stage build but could be optimized:
```
Current: Python 3.10 slim (500MB final image)
Future: Multi-stage with builder pattern (300MB possible)
```
Trade-off: Simplicity vs image size. For cloud deployment with container registries, 500MB is acceptable.

## Security Considerations

### Current Implementation
1. **File Type Validation**: Only `.mp4`, `.avi`, `.mov` allowed
2. **CORS Enabled**: `allow_origins=["*"]` for development
3. **No Authentication**: Public API for demo purposes
4. **No Rate Limiting**: Unlimited requests per IP
5. **File Storage**: Uploaded videos stored indefinitely in `uploads/`

### Production Hardening Required

#### 1. Authentication & Authorization
```python
# Add JWT token validation
from fastapi.security import HTTPBearer
security = HTTPBearer()

@app.post("/api/analyze")
async def analyze_video(
    video: UploadFile = File(...),
    token: str = Depends(security)
):
    verify_jwt_token(token)  # Validate user identity
```

#### 2. Rate Limiting
```python
# Add per-IP rate limits
from slowapi import Limiter
limiter = Limiter(key_func=get_remote_address)

@limiter.limit("5/minute")
@app.post("/api/analyze")
async def analyze_video(...):
```

#### 3. File Size Limits
```python
# Current: No limit (DoS vulnerability)
# Production: Enforce maximum size
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

@app.post("/api/analyze")
async def analyze_video(video: UploadFile = File(...)):
    if video.size > MAX_FILE_SIZE:
        raise HTTPException(413, "File too large")
```

#### 4. Content Validation
```python
# Add video codec validation
import magic
mime = magic.Magic(mime=True)
file_mime = mime.from_file(input_path)
if file_mime not in ['video/mp4', 'video/avi', 'video/quicktime']:
    raise HTTPException(400, "Invalid video format")
```

#### 5. Secure File Storage
- **Current Risk**: Files stored with predictable UUIDs
- **Solution**: Use signed URLs with expiration (AWS S3, GCS)
- **Cleanup**: Auto-delete files after 24 hours

#### 6. CORS Restrictions
```python
# Production: Whitelist specific domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://callus.com", "https://app.callus.com"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)
```

#### 7. HTTPS Only
- Deploy behind reverse proxy (nginx/Caddy) with TLS certificates
- Redirect HTTP → HTTPS
- Use HSTS headers

#### 8. Error Message Sanitization
```python
# Current: Exposes internal paths
raise HTTPException(500, f"Processing failed: {str(e)}")

# Production: Generic messages
logger.error(f"Processing failed: {str(e)}")
raise HTTPException(500, "Video processing failed. Please try again.")
```

### Infrastructure Security
- **Container Scanning**: Run `docker scan` to detect vulnerabilities
- **Secrets Management**: Use environment variables, not hardcoded values
- **Network Isolation**: Run containers in private networks
- **Monitoring**: Log all API requests with IP addresses and file metadata

## How This Fits Callus's Vision

Callus aims to **connect global talents through engaging, short-form content**. This pose analysis system directly supports that mission:

### 1. **Democratizing Talent Assessment**
Traditional dance evaluation requires:
- Physical presence of judges
- Subjective human scoring
- Limited reach (local competitions only)

**This system enables**:
- Global competitions without travel
- Objective movement metrics (symmetry, speed, range of motion)
- Instant feedback for creators uploading dance videos

**Real-world application**: When a user uploads a dance to Callus's platform, this API could automatically:
- Score technical execution (did they hit the choreography?)
- Highlight best moments (frames with highest pose confidence)
- Suggest improvements ("left arm extension could be wider")

### 2. **Content Discovery Through Movement**
Callus's short-form video platform needs smart content recommendations. Pose analysis unlocks:
- **Movement-based search**: "Find me dancers with high kicks like this video"
- **Style classification**: Automatically tag videos as hip-hop, ballet, contemporary
- **Challenge verification**: Detect if users actually completed the #CallousChallenge dance moves

**Technical foundation**: The skeleton keypoints extracted here (33 landmarks × XYZ coordinates) are perfect inputs for ML models that classify dance styles or compare movements between videos.

### 3. **Scalable Infrastructure for Global Growth**
Callus targets **global creators** uploading thousands of videos daily. This project's architecture scales:

| Component | Scalability Feature |
|-----------|---------------------|
| **FastAPI** | Async handles 1000+ concurrent uploads |
| **Docker** | Horizontal scaling: spin up 100 containers in seconds |
| **Stateless API** | No session storage = load balance across regions |
| **Cloud-agnostic** | Deploy to AWS/GCP/Azure based on regional user demand |

**Cost efficiency**: MediaPipe runs on CPU (no expensive GPUs needed), making it economical to process millions of videos. At $0.05/compute-hour (AWS t3.medium), processing 10,000 videos/day costs ~$60/month.

### 4. **Real-Time Feedback for Creators**
Callus creators need **instant validation** that their content will perform well. Processing speed matters:
- **Current**: 30-50ms per frame = 5-second video processed in 7 seconds
- **User experience**: Upload → see skeleton overlay in < 10 seconds
- **Engagement**: Creators iterate faster, upload more content

**Future integration**: Embed this API in Callus's mobile app: "Record dance → See real-time skeleton overlay → Auto-share to feed"

### 5. **Data-Driven Talent Scouting**
For Callus to become the **"LinkedIn for creative talent"**, it needs quantifiable skills data:
- Traditional: "I'm a good dancer" (unverifiable)
- **With pose analysis**: "I maintain 95%+ pose detection across 50 videos, with 180° leg extensions"

**Recruiter value**: Brands searching for talent on Callus could filter by:
- Movement precision score
- Video consistency (pose detection rate)
- Body control metrics (how stable are keypoints frame-to-frame?)

### Vision Alignment Summary
| Callus Goal | This Project's Contribution |
|-------------|----------------------------|
| Connect global talents | Cloud API accessible worldwide, no geographic barriers |
| Short-form engagement | Fast processing keeps users in-app, not waiting |
| Discover hidden talent | Objective movement metrics surface skilled creators |
| Scalable platform | Docker + stateless design handles viral growth |
| Creator tools | Skeleton overlay adds production value to videos |

**The bigger picture**: This pose analysis system isn't just a video processor—it's the foundation for **AI-powered talent discovery** at scale. As Callus grows, this API could evolve into a full "Movement Intelligence Platform" that understands, scores, and recommends dance content globally.

## Future Enhancements

- [ ] GPU acceleration for faster processing
- [ ] Batch video processing
- [ ] Movement analysis metrics (speed, range of motion, symmetry)
- [ ] Comparison between multiple dancers
- [ ] Real-time streaming support
- [ ] Machine learning for dance style classification
- [ ] Integration with mobile apps

## License

MIT License - See LICENSE file for details

## Author

Sree Madhav - AI/ML Engineer
