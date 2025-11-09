"""
Video processing module that applies pose detection to video files.
Handles video I/O and frame-by-frame processing.
"""

import cv2
import os
from typing import Tuple, Optional
from .pose_detector import PoseDetector


class VideoProcessor:
    """
    Processes dance videos to add pose detection skeleton overlay.
    """
    
    def __init__(self, pose_detector: Optional[PoseDetector] = None):
        """
        Initialize video processor.
        
        Args:
            pose_detector: PoseDetector instance, creates new one if not provided
        """
        self.pose_detector = pose_detector or PoseDetector()
        
    def process_video(self, 
                     input_path: str, 
                     output_path: str,
                     show_progress: bool = False) -> Tuple[bool, str]:
        """
        Process a video file and add pose skeleton overlay.
        
        Args:
            input_path: Path to input video file
            output_path: Path where output video will be saved
            show_progress: Whether to print progress information
            
        Returns:
            Tuple of (success: bool, message: str)
        """
        # Validate input file exists
        if not os.path.exists(input_path):
            return False, f"Input video not found: {input_path}"
        
        # Open input video
        cap = cv2.VideoCapture(input_path)
        if not cap.isOpened():
            return False, "Failed to open input video"
        
        # Get video properties
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        # Setup video writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
        
        if not out.isOpened():
            cap.release()
            return False, "Failed to create output video"
        
        frame_count = 0
        frames_with_pose = 0
        
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Detect pose in current frame
                landmarks = self.pose_detector.detect_pose(frame)
                
                # Draw skeleton if pose detected
                if landmarks:
                    frame = self.pose_detector.draw_skeleton(frame, landmarks)
                    frames_with_pose += 1
                
                # Write processed frame
                out.write(frame)
                
                frame_count += 1
                
                # Print progress every 30 frames (roughly every second for 30fps video)
                if show_progress and frame_count % 30 == 0:
                    progress = (frame_count / total_frames) * 100
                    print(f"Processing: {progress:.1f}% ({frame_count}/{total_frames} frames)")
        
        except Exception as e:
            cap.release()
            out.release()
            return False, f"Error during processing: {str(e)}"
        
        finally:
            cap.release()
            out.release()
        
        # Calculate detection rate
        detection_rate = (frames_with_pose / frame_count * 100) if frame_count > 0 else 0
        
        success_msg = (f"Video processed successfully. "
                      f"Processed {frame_count} frames. "
                      f"Pose detected in {frames_with_pose} frames ({detection_rate:.1f}%).")
        
        return True, success_msg
    
    def get_video_info(self, video_path: str) -> Optional[dict]:
        """
        Extract basic information about a video file.
        
        Args:
            video_path: Path to video file
            
        Returns:
            Dictionary with video info or None if failed
        """
        if not os.path.exists(video_path):
            return None
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return None
        
        info = {
            'width': int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
            'height': int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
            'fps': int(cap.get(cv2.CAP_PROP_FPS)),
            'frame_count': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
            'duration_seconds': int(cap.get(cv2.CAP_PROP_FRAME_COUNT)) / int(cap.get(cv2.CAP_PROP_FPS))
        }
        
        cap.release()
        return info
    
    def cleanup(self):
        """Release resources"""
        if self.pose_detector:
            self.pose_detector.cleanup()
