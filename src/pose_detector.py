"""
Pose detection using MediaPipe for dance movement analysis.
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import Optional, Tuple, List


class PoseDetector:
    """Detects human pose keypoints and draws skeleton overlay."""
    
    def __init__(self, 
                 min_detection_confidence: float = 0.5,
                 min_tracking_confidence: float = 0.5):
        
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        # static_image_mode=False optimizes for video (tracks across frames)
        # model_complexity=1 balances speed vs accuracy
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=1,
            smooth_landmarks=True,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence
        )
        
    def detect_pose(self, frame: np.ndarray) -> Optional[any]:
        """Detect pose landmarks in a frame. Returns None if no pose found."""
        
        # Convert BGR to RGB (MediaPipe requirement)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_frame)
        
        return results.pose_landmarks if results else None
    
    def draw_skeleton(self, frame: np.ndarray, landmarks: any) -> np.ndarray:
        """Draw skeleton overlay on frame. Returns unmodified frame if no landmarks."""
        
        if landmarks is None:
            return frame
        
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
        """Extract pixel coordinates for all 33 keypoints. Returns empty list if no pose."""
        
        if landmarks is None:
            return []
        
        keypoints = []
        for landmark in landmarks.landmark:
            # MediaPipe gives normalized coords (0-1), convert to pixels
            x = int(landmark.x * frame_width)
            y = int(landmark.y * frame_height)
            keypoints.append((x, y))
        
        return keypoints
    
    def cleanup(self):
        self.pose.close()
