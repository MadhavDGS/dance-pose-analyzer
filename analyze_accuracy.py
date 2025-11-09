"""
Analyze pose detection accuracy and provide recommendations.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.pose_detector import PoseDetector
from src.video_processor import VideoProcessor
import cv2
import numpy as np


def analyze_detection_quality(video_path: str):
    """Analyze detailed detection metrics for a video."""
    
    detector = PoseDetector(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"❌ Cannot open video: {video_path}")
        return
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"\n{'='*60}")
    print(f"ANALYZING: {Path(video_path).name}")
    print(f"{'='*60}")
    print(f"Resolution: {width}x{height}")
    print(f"FPS: {fps}")
    print(f"Total Frames: {total_frames}")
    print(f"Duration: {total_frames/fps:.2f} seconds\n")
    
    frames_detected = 0
    confidence_scores = []
    keypoint_counts = []
    
    frame_num = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        landmarks = detector.detect_pose(frame)
        
        if landmarks:
            frames_detected += 1
            
            # Calculate average confidence across all landmarks
            confidences = [lm.visibility for lm in landmarks.landmark]
            avg_confidence = np.mean(confidences)
            confidence_scores.append(avg_confidence)
            
            # Count visible keypoints (visibility > 0.5)
            visible_keypoints = sum(1 for c in confidences if c > 0.5)
            keypoint_counts.append(visible_keypoints)
        
        frame_num += 1
    
    cap.release()
    detector.cleanup()
    
    # Calculate metrics
    detection_rate = (frames_detected / total_frames * 100) if total_frames > 0 else 0
    avg_confidence = np.mean(confidence_scores) if confidence_scores else 0
    avg_keypoints = np.mean(keypoint_counts) if keypoint_counts else 0
    
    print(f"📊 DETECTION METRICS:")
    print(f"├─ Detection Rate: {detection_rate:.1f}% ({frames_detected}/{total_frames} frames)")
    print(f"├─ Average Confidence: {avg_confidence:.3f}")
    print(f"├─ Average Visible Keypoints: {avg_keypoints:.1f}/33")
    print(f"└─ Min Keypoints: {min(keypoint_counts) if keypoint_counts else 0}")
    
    # Accuracy assessment
    print(f"\n🎯 ACCURACY ASSESSMENT:")
    
    if detection_rate >= 95:
        print(f"✅ EXCELLENT - Detection rate is outstanding!")
        print(f"   Your video has ideal conditions for pose detection.")
    elif detection_rate >= 85:
        print(f"✅ GOOD - Detection rate is solid.")
        print(f"   Minor improvements possible with better lighting.")
    elif detection_rate >= 70:
        print(f"⚠️  ACCEPTABLE - Detection rate is usable.")
        print(f"   Consider improving: lighting, camera angle, or occlusion.")
    else:
        print(f"❌ POOR - Detection rate needs improvement.")
        print(f"   Issues: poor lighting, heavy occlusion, or extreme angles.")
    
    if avg_confidence >= 0.8:
        print(f"✅ High confidence scores - landmarks are well-detected")
    elif avg_confidence >= 0.6:
        print(f"⚠️  Medium confidence - acceptable but could be better")
    else:
        print(f"❌ Low confidence - poor detection quality")
    
    if avg_keypoints >= 30:
        print(f"✅ Most keypoints visible - full body tracking working well")
    elif avg_keypoints >= 25:
        print(f"⚠️  Some keypoints missing - partial body tracking")
    else:
        print(f"❌ Many keypoints missing - body heavily occluded")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS:")
    
    if detection_rate < 95:
        print(f"├─ Increase min_detection_confidence to 0.6 or 0.7 for stricter detection")
        print(f"├─ Ensure good lighting (avoid shadows and backlighting)")
        print(f"└─ Keep full body in frame with minimal occlusion")
    
    if avg_confidence < 0.7:
        print(f"├─ Use model_complexity=2 for better accuracy (slower processing)")
        print(f"└─ Improve video quality (resolution, bitrate)")
    
    print(f"\n{'='*60}\n")


def compare_model_settings():
    """Show how different settings affect accuracy."""
    
    print(f"\n{'='*60}")
    print(f"MODEL CONFIGURATION ANALYSIS")
    print(f"{'='*60}\n")
    
    print("📌 CURRENT SETTINGS:")
    print("├─ model_complexity: 1 (BALANCED)")
    print("├─ min_detection_confidence: 0.5 (MODERATE)")
    print("├─ min_tracking_confidence: 0.5 (MODERATE)")
    print("└─ smooth_landmarks: True (ENABLED)\n")
    
    print("⚙️  ALTERNATIVE CONFIGURATIONS:\n")
    
    print("🚀 FASTER (Lower Accuracy):")
    print("   model_complexity=0, confidence=0.4")
    print("   → 50-80 FPS, ~90% detection rate")
    print("   → Good for: real-time apps, high frame rate needs\n")
    
    print("⚖️  BALANCED (Current):")
    print("   model_complexity=1, confidence=0.5")
    print("   → 20-30 FPS, ~95% detection rate")
    print("   → Good for: general purpose, dance videos\n")
    
    print("🎯 ACCURATE (Slower):")
    print("   model_complexity=2, confidence=0.7")
    print("   → 10-15 FPS, ~97% detection rate")
    print("   → Good for: high-quality analysis, professional use\n")
    
    print("✅ RECOMMENDATION FOR CALLUS:")
    print("   Current settings (complexity=1) are OPTIMAL for:")
    print("   ├─ Dance video processing")
    print("   ├─ Cloud deployment (CPU-based)")
    print("   └─ Good accuracy/speed trade-off")
    print(f"\n{'='*60}\n")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        video_path = sys.argv[1]
        analyze_detection_quality(video_path)
    else:
        # Analyze the most recent processed video
        output_dir = Path(__file__).parent / "uploads"
        videos = list(output_dir.glob("*.mp4"))
        
        if videos:
            latest_video = max(videos, key=lambda p: p.stat().st_mtime)
            print(f"📹 Analyzing most recent video...")
            analyze_detection_quality(str(latest_video))
        else:
            print("❌ No videos found in uploads/ directory")
            print("\nUsage: python analyze_accuracy.py <video_path>")
            print("   or: Upload a video via the API first\n")
        
        compare_model_settings()
