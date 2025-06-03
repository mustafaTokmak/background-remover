#!/usr/bin/env python3
"""
Background Remover - Remove backgrounds from images using rembg
"""

import os
import sys
from pathlib import Path
from typing import Optional

from PIL import Image
from rembg import remove, new_session


class BackgroundRemover:
    """Main class for removing backgrounds from images"""
    
    def __init__(self, model: str = "u2net"):
        """
        Initialize the background remover with a specific model
        
        Args:
            model: Model to use for background removal. Options:
                   'u2net' (default) - General purpose
                   'u2netp' - Lightweight version
                   'u2net_human_seg' - Human segmentation
                   'u2net_cloth_seg' - Clothing segmentation
        """
        self.session = new_session(model)
    
    def remove_background(
        self, 
        input_path: str, 
        output_path: Optional[str] = None,
        alpha_matting: bool = False,
        only_mask: bool = False
    ) -> str:
        """
        Remove background from a single image
        
        Args:
            input_path: Path to input image
            output_path: Path to save output image (optional)
            alpha_matting: Enable alpha matting for better edges
            only_mask: Output only the mask instead of transparent image
            
        Returns:
            Path to the output image
        """
        # Validate input
        input_file = Path(input_path)
        if not input_file.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        # Generate output path if not provided
        if output_path is None:
            output_path = input_file.parent / f"{input_file.stem}_no_bg.png"
        else:
            output_path = Path(output_path)
        
        # Create output directory if needed
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Load and process image
        with open(input_file, 'rb') as input_file:
            input_data = input_file.read()
            
        output_data = remove(
            input_data, 
            session=self.session,
            alpha_matting=alpha_matting,
            only_mask=only_mask
        )
        
        # Save output
        with open(output_path, 'wb') as output_file:
            output_file.write(output_data)
            
        return str(output_path)
    
    def process_directory(
        self, 
        input_dir: str, 
        output_dir: Optional[str] = None,
        extensions: tuple = ('.jpg', '.jpeg', '.png', '.bmp', '.webp'),
        alpha_matting: bool = False
    ) -> list[str]:
        """
        Process all images in a directory
        
        Args:
            input_dir: Directory containing images
            output_dir: Directory to save processed images
            extensions: Tuple of valid image extensions
            alpha_matting: Enable alpha matting for better edges
            
        Returns:
            List of output file paths
        """
        input_path = Path(input_dir)
        if not input_path.is_dir():
            raise NotADirectoryError(f"Input is not a directory: {input_dir}")
        
        # Set output directory
        if output_dir is None:
            output_path = input_path / "no_bg"
        else:
            output_path = Path(output_dir)
        
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Process images
        processed_files = []
        image_files = [
            f for f in input_path.iterdir() 
            if f.is_file() and f.suffix.lower() in extensions
        ]
        
        if not image_files:
            print(f"No image files found in {input_dir}")
            return processed_files
        
        print(f"Processing {len(image_files)} images...")
        
        for idx, image_file in enumerate(image_files, 1):
            try:
                output_file = output_path / f"{image_file.stem}_no_bg.png"
                self.remove_background(
                    str(image_file), 
                    str(output_file),
                    alpha_matting=alpha_matting
                )
                processed_files.append(str(output_file))
                print(f"[{idx}/{len(image_files)}] Processed: {image_file.name}")
            except Exception as e:
                print(f"Error processing {image_file.name}: {e}")
        
        return processed_files


def main():
    """Example usage"""
    remover = BackgroundRemover()
    
    # Example: Remove background from a single image
    # output = remover.remove_background("input.jpg", "output.png")
    # print(f"Saved to: {output}")
    
    # Example: Process entire directory
    # outputs = remover.process_directory("./images", "./output")
    # print(f"Processed {len(outputs)} images")
    
    print("Background remover initialized. Import and use the BackgroundRemover class.")


if __name__ == "__main__":
    main()