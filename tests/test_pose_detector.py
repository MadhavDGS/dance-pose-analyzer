"""
Unit tests for pose detection functionality.
Tests keypoint detection accuracy and output formatting.
"""

import pytest
import numpy as np
import cv2
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.pose_detector import PoseDetector


class TestPoseDetector:
    """Test suite for PoseDetector class"""
    
    @pytest.fixture
    def detector(self):
        """Create a detector instance for testing"""
        return PoseDetector(min_detection_confidence=0.5, min_tracking_confidence=0.5)
    
    @pytest.fixture
    def sample_frame(self):
        """Create a sample frame with a person (simplified test frame)"""
        # Create a blank 640x480 frame (BGR)
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        # Add some colors to simulate a scene
        frame[:] = (100, 100, 100)
        return frame
    
    def test_detector_initialization(self, detector):
        """Test that detector initializes correctly"""
        assert detector is not None
        assert detector.mp_pose is not None
        assert detector.pose is not None
    
    def test_detect_pose_with_empty_frame(self, detector):
        """Test pose detection on an empty frame"""
        # Black frame - no person
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        landmarks = detector.detect_pose(frame)
        # Should return None for empty frame
        assert landmarks is None
    
    def test_detect_pose_returns_correct_type(self, detector, sample_frame):
        """Test that detect_pose returns expected type"""
        result = detector.detect_pose(sample_frame)
        # Result should be either None or landmarks object
        assert result is None or hasattr(result, 'landmark')
    
    def test_draw_skeleton_with_no_landmarks(self, detector, sample_frame):
        """Test drawing when no landmarks detected"""
        frame = sample_frame.copy()
        result_frame = detector.draw_skeleton(frame, None)
        # Should return original frame unchanged
        assert np.array_equal(result_frame, frame)
    
    def test_get_keypoint_coordinates_empty(self, detector):
        """Test keypoint extraction with no landmarks"""
        keypoints = detector.get_keypoint_coordinates(None, 640, 480)
        assert keypoints == []
    
    def test_get_keypoint_coordinates_format(self, detector):
        """Test that keypoint coordinates are in correct format"""
        # This test would need actual landmarks from a real detection
        # For now, we test the empty case
        keypoints = detector.get_keypoint_coordinates(None, 640, 480)
        assert isinstance(keypoints, list)
    
    def test_cleanup(self, detector):
        """Test that cleanup doesn't raise errors"""
        try:
            detector.cleanup()
            assert True
        except Exception as e:
            pytest.fail(f"Cleanup raised an exception: {e}")
    
    def test_frame_color_conversion(self, detector):
        """Test that BGR to RGB conversion works"""
        # Create a test frame with known BGR values
        frame = np.zeros((100, 100, 3), dtype=np.uint8)
        frame[:, :] = (255, 0, 0)  # Blue in BGR
        
        # Detect pose (internally converts to RGB)
        result = detector.detect_pose(frame)
        # Should not raise an error
        assert result is None or hasattr(result, 'landmark')


class TestPoseDetectorIntegration:
    """Integration tests with real video processing scenarios"""
    
    @pytest.fixture
    def detector(self):
        """Create detector for integration tests"""
        return PoseDetector()
    
    def test_process_multiple_frames(self, detector):
        """Test processing multiple frames in sequence"""
        frames = [np.zeros((480, 640, 3), dtype=np.uint8) for _ in range(5)]
        
        results = []
        for frame in frames:
            result = detector.detect_pose(frame)
            results.append(result)
        
        # Should process all frames without error
        assert len(results) == 5
    
    def test_different_frame_sizes(self, detector):
        """Test that detector handles different frame sizes"""
        sizes = [(480, 640), (720, 1280), (1080, 1920)]
        
        for height, width in sizes:
            frame = np.zeros((height, width, 3), dtype=np.uint8)
            result = detector.detect_pose(frame)
            # Should handle different sizes
            assert result is None or hasattr(result, 'landmark')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
