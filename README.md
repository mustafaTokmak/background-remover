# Background Remover

A Python tool for removing backgrounds from images using the [rembg](https://github.com/danielgatis/rembg) library.

## Features

- Remove backgrounds from single images or entire directories
- Multiple AI models for different use cases
- Alpha matting for improved edge quality
- Mask-only output option
- Support for various image formats (JPG, PNG, BMP, WebP)
- Simple CLI interface

## Installation

1. Make sure you have Python 3.8+ installed
2. Clone this repository
3. Install dependencies using uv:

```bash
uv sync
```

Or with pip:

```bash
pip install rembg pillow
```

## Usage

### Command Line Interface

Remove background from a single image:
```bash
python cli.py input.jpg
```

Specify output path:
```bash
python cli.py input.jpg -o output.png
```

Process entire directory:
```bash
python cli.py ./images --directory
```

Use different model for human segmentation:
```bash
python cli.py portrait.jpg --model u2net_human_seg
```

Enable alpha matting for better edges:
```bash
python cli.py input.jpg --alpha-matting
```

Output only the mask:
```bash
python cli.py input.jpg --only-mask
```

### Python API

```python
from remover import BackgroundRemover

# Initialize remover
remover = BackgroundRemover(model="u2net")

# Remove background from single image
output_path = remover.remove_background("input.jpg", "output.png")

# Process entire directory
processed_files = remover.process_directory("./images", "./output")

# With alpha matting
output = remover.remove_background(
    "input.jpg", 
    alpha_matting=True
)
```

## Available Models

- `u2net` (default) - General purpose background removal
- `u2netp` - Lightweight version, faster but less accurate
- `u2net_human_seg` - Optimized for human/portrait segmentation
- `u2net_cloth_seg` - Optimized for clothing segmentation

## Output

- By default, images are saved as PNG with transparent background
- When processing directories, output is saved to a `no_bg` subdirectory
- Use `--only-mask` to get a black and white mask instead

## Requirements

- Python 3.8+
- rembg
- Pillow
- numpy
- Other dependencies handled by rembg

## Tips

- For best results with portraits, use `--model u2net_human_seg`
- Enable `--alpha-matting` for images with fine details like hair
- The first run will download the AI model (~170MB)
- Processing time depends on image size and model used

## License

This tool uses the [rembg](https://github.com/danielgatis/rembg) library which is MIT licensed.