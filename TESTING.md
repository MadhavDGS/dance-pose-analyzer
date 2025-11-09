# Testing Guide

This guide helps you test the Dance Pose Analyzer locally before deploying.

## Quick Start

1. **Install dependencies** (already done if you followed README)
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Start the server**
   ```bash
   uvicorn src.api:app --reload --host 0.0.0.0 --port 8000
   ```

3. **Access API documentation**
   Open: http://localhost:8000/docs

## Testing with Sample Videos

### Download Test Videos

You can use free dance videos from:
- Pexels: https://www.pexels.com/search/videos/dance/
- Pixabay: https://pixabay.com/videos/search/dancing/

Or record a short 5-10 second dance video on your phone.

### Test Using CLI

```bash
python process_video.py input.mp4 output.mp4 --verbose
```

### Test Using API

1. **Start server**
   ```bash
   uvicorn src.api:app --host 0.0.0.0 --port 8000
   ```

2. **Upload video** (in another terminal)
   ```bash
   curl -X POST "http://localhost:8000/api/analyze" \
     -F "video=@your_dance_video.mp4" \
     | python -m json.tool > response.json
   ```

3. **Get video_id from response**
   ```bash
   cat response.json
   ```

4. **Download processed video**
   ```bash
   curl "http://localhost:8000/api/download/VIDEO_ID_HERE" \
     -o processed_dance.mp4
   ```

5. **Watch the result**
   ```bash
   open processed_dance.mp4  # macOS
   # or just open the file in your video player
   ```

## Running Unit Tests

```bash
# Run all tests
pytest tests/ -v

# Run with detailed output
pytest tests/ -v -s

# Run specific test file
pytest tests/test_pose_detector.py -v

# Run with coverage report
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html  # View coverage report
```

## Testing API with Swagger UI

1. Start server
2. Open http://localhost:8000/docs
3. Click on "POST /api/analyze"
4. Click "Try it out"
5. Upload a video file
6. Click "Execute"
7. Copy the video_id from response
8. Use GET /api/download/{video_id} to download result

## Verify Pose Detection Quality

Good indicators:
- Detection rate above 85% (shown in response message)
- Skeleton visible on person in video
- Smooth tracking across frames
- All major joints detected (shoulders, elbows, hips, knees)

## Expected Processing Times

- 5-second video (30fps): ~5-8 seconds
- 10-second video: ~10-15 seconds
- Longer videos may take proportionally longer

## Troubleshooting

### Issue: Import errors
**Solution**: Make sure virtual environment is activated
```bash
source venv/bin/activate
which python  # Should show venv/bin/python
```

### Issue: Slow processing
**Solution**: Normal on CPU. Processing time depends on:
- Video resolution (lower = faster)
- Video length
- Your CPU speed

### Issue: No pose detected
**Solution**: 
- Ensure person is visible in video
- Good lighting helps
- Person should be mostly in frame
- Try adjusting confidence threshold

### Issue: Port already in use
**Solution**: Use different port
```bash
uvicorn src.api:app --port 8001
```

## Demo Video Recording Tips

For your 2-minute demo video:

1. **Show the code structure** (10-15 seconds)
   - Open project in VS Code
   - Show main files: pose_detector.py, video_processor.py, api.py

2. **Explain key decisions** (30-40 seconds)
   - Why MediaPipe (fast, accurate, lightweight)
   - Why FastAPI (async, modern, auto-docs)
   - Docker for consistent deployment

3. **Live demonstration** (60-70 seconds)
   - Start the API server
   - Show Swagger UI at /docs
   - Upload a dance video
   - Show the response JSON
   - Download and play processed video
   - Show skeleton overlay working

4. **Show deployment** (15-20 seconds)
   - Show Dockerfile
   - Mention deployed URL
   - Quick curl test to live server

Recording tools:
- macOS: QuickTime Screen Recording or OBS
- Windows: OBS Studio
- Linux: OBS Studio or SimpleScreenRecorder

## Preparing for Submission

1. **Clean up test files**
   ```bash
   rm -rf uploads/* outputs/*
   ```

2. **Run all tests**
   ```bash
   pytest tests/ -v
   ```

3. **Test Docker build**
   ```bash
   docker build -t pose-analyzer-test .
   docker run -p 8000:8000 pose-analyzer-test
   ```

4. **Check README clarity**
   - All setup steps work
   - API examples accurate
   - Deployment instructions clear

5. **Record demo video**
   - 2 minutes maximum
   - Show working application
   - Explain code structure
   - Mention cloud deployment

6. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Complete dance pose analyzer implementation"
   git push origin main
   ```
