"""
Unit tests for video processing functionality.
Tests video I/O and processing pipeline.
"""

import pytest
import numpy as np
import cv2
from pathlib import Path
import sys
import tempfile
import os

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.video_processor import VideoProcessor
from src.pose_detector import PoseDetector


class TestVideoProcessor:
    """Test suite for VideoProcessor class"""
    
    @pytest.fixture
    def processor(self):
        """Create processor instance"""
        return VideoProcessor()
    
    @pytest.fixture
    def create_test_video(self):
        """Create a minimal test video file"""
        def _create_video(output_path, num_frames=10, fps=30):
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (640, 480))
            
            for i in range(num_frames):
                # Create simple frames
                frame = np.zeros((480, 640, 3), dtype=np.uint8)
                frame[:] = (i * 25, i * 25, i * 25)  # Gradient effect
                out.write(frame)
            
            out.release()
            return output_path
        
        return _create_video
    
    def test_processor_initialization(self, processor):
        """Test processor initializes correctly"""
        assert processor is not None
        assert processor.pose_detector is not None
    
    def test_processor_with_custom_detector(self):
        """Test processor accepts custom detector"""
        custom_detector = PoseDetector(min_detection_confidence=0.7)
        processor = VideoProcessor(custom_detector)
        assert processor.pose_detector is custom_detector
    
    def test_process_nonexistent_video(self, processor):
        """Test processing a video that doesn't exist"""
        success, message = processor.process_video(
            "/nonexistent/path.mp4",
            "/tmp/output.mp4"
        )
        assert success is False
        assert "not found" in message.lower()
    
    def test_get_video_info_nonexistent(self, processor):
        """Test getting info for nonexistent video"""
        info = processor.get_video_info("/nonexistent/path.mp4")
        assert info is None
    
    def test_process_video_with_real_file(self, processor, create_test_video):
        """Test processing an actual video file"""
        with tempfile.TemporaryDirectory() as tmpdir:
            input_path = os.path.join(tmpdir, "test_input.mp4")
            output_path = os.path.join(tmpdir, "test_output.mp4")
            
            # Create test video
            create_test_video(input_path, num_frames=5)
            
            # Process it
            success, message = processor.process_video(input_path, output_path)
            
            # Check results
            assert success is True
            assert os.path.exists(output_path)
            assert "processed successfully" in message.lower()
    
    def test_get_video_info_with_real_file(self, processor, create_test_video):
        """Test extracting video information"""
        with tempfile.TemporaryDirectory() as tmpdir:
            video_path = os.path.join(tmpdir, "test.mp4")
            create_test_video(video_path, num_frames=30, fps=30)
            
            info = processor.get_video_info(video_path)
            
            assert info is not None
            assert info['width'] == 640
            assert info['height'] == 480
            assert info['fps'] == 30
            assert info['frame_count'] == 30
            assert 'duration_seconds' in info
    
    def test_cleanup(self, processor):
        """Test cleanup doesn't raise errors"""
        try:
            processor.cleanup()
            assert True
        except Exception as e:
            pytest.fail(f"Cleanup raised exception: {e}")


class TestVideoProcessorIntegration:
    """Integration tests for video processing pipeline"""
    
    def test_full_pipeline(self, create_test_video=None):
        """Test complete processing pipeline"""
        # This would need a real test video file
        # For now, we ensure the basic structure works
        processor = VideoProcessor()
        assert processor is not None
        
        # Test that methods exist
        assert hasattr(processor, 'process_video')
        assert hasattr(processor, 'get_video_info')
        assert hasattr(processor, 'cleanup')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
