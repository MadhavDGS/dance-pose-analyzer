"""
Pose detection module using MediaPipe for dance movement analysis.
Handles keypoint detection and skeleton overlay rendering.
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Optional, Tuple, List


class PoseDetector:
    """
    Detects human pose keypoints in video frames using MediaPipe.
    Draws skeleton connections between detected landmarks.
    """
    
    def __init__(self, 
                 min_detection_confidence: float = 0.5,
                 min_tracking_confidence: float = 0.5):
        """
        Initialize the pose detector with MediaPipe.
        
        Args:
            min_detection_confidence: Minimum confidence for pose detection
            min_tracking_confidence: Minimum confidence for pose tracking
        """
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # Initialize pose detector - using static_image_mode=False for video
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,  # balance between speed and accuracy
            smooth_landmarks=True,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        
    def detect_pose(self, frame: np.ndarray) -> Optional[any]:
        """
        Detect pose landmarks in a single frame.
        
        Args:
            frame: Input image frame in BGR format (OpenCV standard)
            
        Returns:
            Pose landmarks if detected, None otherwise
        """
        # MediaPipe expects RGB, OpenCV uses BGR
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.pose.process(rgb_frame)
        
        return results.pose_landmarks if results else None
    
    def draw_skeleton(self, 
                     frame: np.ndarray, 
                     landmarks: any) -> np.ndarray:
        """
        Draw pose skeleton overlay on the frame.
        
        Args:
            frame: Input frame to draw on
            landmarks: Detected pose landmarks
            
        Returns:
            Frame with skeleton overlay
        """
        if landmarks is None:
            return frame
        
        # Draw the pose landmarks and connections
        self.mp_drawing.draw_landmarks(
            frame,
            landmarks,
            self.mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=self.mp_drawing_styles.get_default_pose_landmarks_style()
        )
        
        return frame
    
    def get_keypoint_coordinates(self, 
                                 landmarks: any, 
                                 frame_width: int, 
                                 frame_height: int) -> List[Tuple[int, int]]:
        """
        Extract normalized keypoint coordinates.
        Useful for testing and analysis.
        
        Args:
            landmarks: Detected pose landmarks
            frame_width: Width of the frame
            frame_height: Height of the frame
            
        Returns:
            List of (x, y) coordinates for each keypoint
        """
        if landmarks is None:
            return []
        
        keypoints = []
        for landmark in landmarks.landmark:
            # Convert normalized coordinates to pixel coordinates
            x = int(landmark.x * frame_width)
            y = int(landmark.y * frame_height)
            keypoints.append((x, y))
        
        return keypoints
    
    def cleanup(self):
        """Release resources"""
        self.pose.close()
