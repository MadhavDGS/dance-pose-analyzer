# Quick Start Guide

Get the Dance Pose Analyzer running in 5 minutes.

## Prerequisites

- Python 3.10 or higher
- 2GB free disk space
- A dance video to test (or download from Pexels)

## Installation

```bash
# 1. Navigate to project
cd dance-pose-analyzer

# 2. Run start script (installs everything automatically)
./start_server.sh
```

That's it! The server will install dependencies and start automatically.

## Test It Out

### Option 1: Use Swagger UI (Easiest)

1. Open http://localhost:8000/docs in your browser
2. Click on "POST /api/analyze"
3. Click "Try it out"
4. Click "Choose File" and select a dance video
5. Click "Execute"
6. Copy the `video_id` from the response
7. Go to "GET /api/download/{video_id}"
8. Paste your video_id and click "Execute"
9. Click "Download file" to get your processed video

### Option 2: Use CLI Tool

```bash
# Process a video directly
python process_video.py input_dance.mp4 output_processed.mp4 --verbose

# Watch the output
open output_processed.mp4
```

### Option 3: Use curl

```bash
# Upload video
curl -X POST "http://localhost:8000/api/analyze" \
  -F "video=@dance.mp4" > response.json

# Extract video_id
video_id=$(cat response.json | grep -o '"video_id":"[^"]*' | grep -o '[^"]*$')

# Download result
curl "http://localhost:8000/api/download/$video_id" -o result.mp4
```

## Get Sample Videos

Free dance videos:
- https://www.pexels.com/search/videos/dance/
- https://pixabay.com/videos/search/dancing/

Look for:
- Short videos (5-15 seconds work best)
- Person clearly visible
- Good lighting
- Not too fast movement

## Expected Result

The output video will show:
- Original video content
- Skeleton overlay on the dancer
- Green lines connecting body joints
- Circles marking key body points

## Troubleshooting

**Server won't start:**
```bash
# Make sure port 8000 is free
lsof -ti:8000 | xargs kill -9

# Try again
./start_server.sh
```

**Video processing fails:**
- Try a shorter video
- Check video format (MP4, AVI, MOV supported)
- Ensure person is visible in frame

**Want to use a different port:**
```bash
uvicorn src.api:app --port 8001
```

## Running Tests

```bash
# Quick test
./run_tests.sh

# Detailed tests
pytest tests/ -v
```

## Next Steps

- Read README.md for full documentation
- Check TESTING.md for testing strategies
- See DEPLOYMENT.md for cloud deployment
- Review PROJECT_SUMMARY.md for technical details

## Stopping the Server

Press `Ctrl+C` in the terminal where the server is running.

## Clean Up Test Files

```bash
# Remove uploaded and processed videos
rm -rf uploads/* outputs/*
```

## Docker Quick Start

If you prefer Docker:

```bash
# Build image
docker build -t pose-analyzer .

# Run container
docker run -p 8000:8000 pose-analyzer

# Access at http://localhost:8000
```

That's all you need to get started!
