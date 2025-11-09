# How to Use the Dance Pose Analyzer

## Quick Start - 3 Ways to Test

The server is running at: **http://localhost:8000**

---

### Method 1: Web Interface (EASIEST - Click and Upload)

1. **Open your browser**
   ```
   http://localhost:8000
   ```

2. **You'll see a nice upload interface**
   - Click "Choose File"
   - Select your dance video
   - Click "Analyze Video"
   - Wait for processing (shows spinner)
   - Click "Download Processed Video" when done

**This is the best way for your demo video!**

---

### Method 2: Swagger API Docs (Interactive API Testing)

1. **Open Swagger UI**
   ```
   http://localhost:8000/docs
   ```

2. **Test the API:**
   - Expand `POST /api/analyze`
   - Click "Try it out"
   - Click "Choose File" and select video
   - Click "Execute"
   - **IMPORTANT:** Copy the `video_id` from the response
   
3. **Download your result:**
   - Scroll to `GET /api/download/{video_id}`
   - Click "Try it out"
   - Paste your `video_id`
   - Click "Execute"
   - Click "Download" button

---

### Method 3: Command Line (For Developers)

**Upload video:**
```bash
curl -X POST "http://localhost:8000/api/analyze" \
  -F "video=@your_dance_video.mp4" \
  -o response.json

# View response
cat response.json
```

**Extract video_id and download:**
```bash
# Get the video_id
video_id=$(cat response.json | python3 -c "import sys, json; print(json.load(sys.stdin)['video_id'])")

# Download processed video
curl "http://localhost:8000/api/download/$video_id" -o result.mp4

# Watch it
open result.mp4
```

---

## What You Already Did (And What Was Missing)

### What You Did Correctly ✅
- Uploaded video through Swagger UI
- Got successful response with video_id: `8854d90e-5960-4672-bacf-b46591d45025`
- Video was processed (217 frames, 100% detection rate)

### What Was Missing ❌
- **You didn't download the processed video!**
- The output video with skeleton overlay is sitting in `outputs/` folder
- You need to use the download endpoint to get it

### Your Processed Video Location
```bash
# Your video is here:
/Users/sreemadhav/SreeMadhav/Mhv CODES/Callus/dance-pose-analyzer/outputs/8854d90e-5960-4672-bacf-b46591d45025_processed.mp4

# Open it directly:
open /Users/sreemadhav/SreeMadhav/Mhv\ CODES/Callus/dance-pose-analyzer/outputs/8854d90e-5960-4672-bacf-b46591d45025_processed.mp4
```

Or download via browser:
```
http://localhost:8000/api/download/8854d90e-5960-4672-bacf-b46591d45025
```

---

## What the Output Video Shows

The processed video will have:
- **Original video content** (your dancer)
- **Green skeleton overlay** with:
  - Circles on body joints (shoulders, elbows, wrists, hips, knees, ankles)
  - Lines connecting the joints
  - Skeleton follows the dancer's movements
  - 33 body landmarks tracked in real-time

---

## Improvements Made

### Before (Your Concerns):
- Response looked "AI generated"
- Unclear where to download output
- No visual interface

### After (Fixed):
1. **Added Web UI** at http://localhost:8000
   - Simple upload interface
   - Shows progress
   - Direct download button
   - Clear instructions

2. **Improved API Response:**
   ```json
   {
     "success": true,
     "video_id": "...",
     "download": {
       "url": "/api/download/...",
       "direct_link": "http://localhost:8000/api/download/...",
       "note": "Click the direct_link to download"
     }
   }
   ```

3. **Better Error Messages:**
   - Clear validation errors
   - Helpful suggestions
   - Human-readable responses

---

## Test Right Now

**Option 1: Try the new Web UI**
```bash
# Open in browser
open http://localhost:8000
```

**Option 2: Download your existing result**
```bash
# Open the video you already processed
open http://localhost:8000/api/download/8854d90e-5960-4672-bacf-b46591d45025
```

**Option 3: Process a new video**
```bash
# Upload another video through the web interface
open http://localhost:8000
# Click "Choose File" → Select video → Click "Analyze Video"
```

---

## For Your Demo Video

**Show this workflow (looks professional):**

1. **Start with code** (10 sec)
   ```
   "Here's the project structure - pose detector, video processor, and FastAPI server"
   ```

2. **Open Web UI** (15 sec)
   ```
   "I built a web interface for easy testing"
   http://localhost:8000
   ```

3. **Upload video** (30 sec)
   - Click upload
   - Show processing
   - Explain: "MediaPipe detects 33 body landmarks per frame"

4. **Download and play result** (30 sec)
   - Click download
   - Play video showing skeleton overlay
   - Explain: "Green skeleton tracks all body movements"

5. **Show API docs** (15 sec)
   ```
   "Also has REST API with auto-generated docs"
   http://localhost:8000/docs
   ```

6. **Mention deployment** (10 sec)
   ```
   "Dockerized and ready for cloud deployment"
   ```

---

## Need Help?

**Server not running?**
```bash
./start_server.sh
```

**Want to see all processed videos?**
```bash
ls -lh outputs/
```

**Clear old videos?**
```bash
rm outputs/*.mp4
rm uploads/*.mp4
```

---

## Summary

You already successfully processed a video! The system worked perfectly. You just needed to:
1. Download the result using the video_id
2. Watch the processed video with skeleton overlay

Now with the web UI, it's even easier - just click upload and download!
