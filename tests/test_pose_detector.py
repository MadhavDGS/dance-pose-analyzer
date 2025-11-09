"""
Unit tests for pose detection.
"""

import pytest
import numpy as np
import cv2
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pose_detector import PoseDetector


class TestPoseDetector:
    
    @pytest.fixture
    def detector(self):
        return PoseDetector(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    
    @pytest.fixture
    def sample_frame(self):
        # 640x480 gray frame
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        frame[:] = (100, 100, 100)
        return frame
    
    def test_detector_initialization(self, detector):
        assert detector is not None
        assert detector.mp_pose is not None
        assert detector.pose is not None
    
    def test_detect_pose_with_empty_frame(self, detector):
        # Black frame with no person
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        landmarks = detector.detect_pose(frame)
        assert landmarks is None
    
    def test_detect_pose_returns_correct_type(self, detector, sample_frame):
        result = detector.detect_pose(sample_frame)
        assert result is None or hasattr(result, 'landmark')
    
    def test_draw_skeleton_with_no_landmarks(self, detector, sample_frame):
        frame = sample_frame.copy()
        result_frame = detector.draw_skeleton(frame, None)
        assert np.array_equal(result_frame, frame)
    
    def test_get_keypoint_coordinates_empty(self, detector):
        keypoints = detector.get_keypoint_coordinates(None, 640, 480)
        assert keypoints == []
    
    def test_get_keypoint_coordinates_format(self, detector):
        keypoints = detector.get_keypoint_coordinates(None, 640, 480)
        assert isinstance(keypoints, list)
    
    def test_cleanup(self, detector):
        try:
            detector.cleanup()
            assert True
        except Exception as e:
            pytest.fail(f"Cleanup raised an exception: {e}")
    
    def test_frame_color_conversion(self, detector):
        # Blue in BGR format
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        frame[:, :] = (255, 0, 0)
        
        result = detector.detect_pose(frame)
        assert result is None or hasattr(result, 'landmark')


class TestPoseDetectorIntegration:
    
    @pytest.fixture
    def detector(self):
        return PoseDetector()
    
    def test_process_multiple_frames(self, detector):
        frames = [np.zeros((480, 640, 3), dtype=np.uint8) for _ in range(5)]
        
        results = []
        for frame in frames:
            result = detector.detect_pose(frame)
            results.append(result)
        
        assert len(results) == 5
    
    def test_different_frame_sizes(self, detector):
        sizes = [(480, 640), (720, 1280), (1080, 1920)]
        
        for height, width in sizes:
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            result = detector.detect_pose(frame)
            assert result is None or hasattr(result, 'landmark')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
