"""
Command-line interface for testing pose detection locally.
Useful for development and debugging.
"""

import argparse
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.video_processor import VideoProcessor


def main():
    parser = argparse.ArgumentParser(
        description='Process dance videos with pose detection'
    )
    parser.add_argument(
        'input',
        type=str,
        help='Path to input video file'
    )
    parser.add_argument(
        'output',
        type=str,
        help='Path for output video file'
    )
    parser.add_argument(
        '--confidence',
        type=float,
        default=0.5,
        help='Minimum detection confidence (0.0-1.0, default: 0.5)'
    )
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Show processing progress'
    )
    
    args = parser.parse_args()
    
    # Validate input file
    if not Path(args.input).exists():
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)
    
    # Create output directory if needed
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Initialize processor
    print(f"Initializing pose detector (confidence: {args.confidence})...")
    processor = VideoProcessor()
    
    # Process video
    print(f"Processing video: {args.input}")
    success, message = processor.process_video(
        args.input,
        args.output,
        show_progress=args.verbose
    )
    
    # Show results
    if success:
        print(f"\n✓ {message}")
        print(f"Output saved to: {args.output}")
    else:
        print(f"\n✗ Processing failed: {message}")
        sys.exit(1)
    
    # Cleanup
    processor.cleanup()


if __name__ == "__main__":
    main()
