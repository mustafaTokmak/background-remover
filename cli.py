#!/usr/bin/env python3
"""
CLI interface for the background remover tool
"""

import argparse
import sys
from pathlib import Path

from remover import BackgroundRemover


def main():
    parser = argparse.ArgumentParser(
        description="Remove backgrounds from images using AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Remove background from a single image
  python cli.py input.jpg
  
  # Specify output path
  python cli.py input.jpg -o output.png
  
  # Process entire directory
  python cli.py ./images --directory
  
  # Use different model
  python cli.py input.jpg --model u2net_human_seg
  
  # Enable alpha matting for better edges
  python cli.py input.jpg --alpha-matting
  
  # Output only the mask
  python cli.py input.jpg --only-mask
        """
    )
    
    parser.add_argument(
        "input",
        help="Input image file or directory path"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output file or directory path"
    )
    
    parser.add_argument(
        "-d", "--directory",
        action="store_true",
        help="Process all images in a directory"
    )
    
    parser.add_argument(
        "-m", "--model",
        default="u2net",
        choices=["u2net", "u2netp", "u2net_human_seg", "u2net_cloth_seg"],
        help="Model to use for background removal (default: u2net)"
    )
    
    parser.add_argument(
        "-a", "--alpha-matting",
        action="store_true",
        help="Enable alpha matting for better edge quality"
    )
    
    parser.add_argument(
        "--only-mask",
        action="store_true",
        help="Output only the mask instead of transparent image"
    )
    
    parser.add_argument(
        "-e", "--extensions",
        nargs="+",
        default=[".jpg", ".jpeg", ".png", ".bmp", ".webp"],
        help="Image extensions to process when using directory mode"
    )
    
    args = parser.parse_args()
    
    # Validate input
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: Input path does not exist: {args.input}", file=sys.stderr)
        sys.exit(1)
    
    # Initialize remover
    try:
        print(f"Initializing background remover with model: {args.model}")
        remover = BackgroundRemover(model=args.model)
    except Exception as e:
        print(f"Error initializing remover: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Process based on mode
    try:
        if args.directory or input_path.is_dir():
            # Directory mode
            if not input_path.is_dir():
                print(f"Error: {args.input} is not a directory", file=sys.stderr)
                sys.exit(1)
            
            extensions = tuple(ext if ext.startswith('.') else f'.{ext}' for ext in args.extensions)
            processed = remover.process_directory(
                str(input_path),
                args.output,
                extensions=extensions,
                alpha_matting=args.alpha_matting
            )
            
            if processed:
                print(f"\nSuccessfully processed {len(processed)} images")
                if args.output:
                    print(f"Output saved to: {args.output}")
                else:
                    print(f"Output saved to: {input_path}/no_bg/")
            else:
                print("No images were processed")
                
        else:
            # Single file mode
            if args.only_mask and args.alpha_matting:
                print("Warning: --only-mask and --alpha-matting cannot be used together")
                args.alpha_matting = False
            
            output = remover.remove_background(
                str(input_path),
                args.output,
                alpha_matting=args.alpha_matting,
                only_mask=args.only_mask
            )
            print(f"Background removed successfully!")
            print(f"Output saved to: {output}")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()