#!/usr/bin/env python3
"""
FastAPI server for background removal service
"""

import io
import os
import tempfile
from pathlib import Path
from typing import List, Optional

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.responses import StreamingResponse
from PIL import Image

from remover import BackgroundRemover

app = FastAPI(
    title="Background Remover API",
    description="API for removing backgrounds from images",
    version="1.0.0"
)

# Initialize background remover with default model
remover = BackgroundRemover(model="u2net")


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Background Remover API",
        "endpoints": {
            "/docs": "API documentation",
            "/remove": "Remove background from single image",
            "/remove-batch": "Remove background from multiple images",
            "/models": "List available models"
        }
    }


@app.get("/models")
async def get_models():
    """Get list of available models"""
    return {
        "models": [
            {
                "name": "u2net",
                "description": "General purpose background removal (default)"
            },
            {
                "name": "u2netp",
                "description": "Lightweight version, faster but less accurate"
            },
            {
                "name": "u2net_human_seg",
                "description": "Optimized for human segmentation"
            },
            {
                "name": "u2net_cloth_seg",
                "description": "Optimized for clothing segmentation"
            }
        ]
    }


@app.post("/remove")
async def remove_background(
    file: UploadFile = File(...),
    model: Optional[str] = Form("u2net"),
    alpha_matting: bool = Form(False),
    only_mask: bool = Form(False),
    output_format: str = Form("png")
):
    """
    Remove background from a single image
    
    Args:
        file: Image file to process
        model: Model to use (u2net, u2netp, u2net_human_seg, u2net_cloth_seg)
        alpha_matting: Enable alpha matting for better edges
        only_mask: Return only the mask instead of transparent image
        output_format: Output format (png or webp)
    
    Returns:
        Processed image with transparent background
    """
    # Validate file type
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Validate output format
    if output_format not in ["png", "webp"]:
        raise HTTPException(status_code=400, detail="Output format must be png or webp")
    
    # Create temporary file for processing
    with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_input:
        content = await file.read()
        tmp_input.write(content)
        tmp_input_path = tmp_input.name
    
    try:
        # Initialize remover with specified model if different
        if model != "u2net":
            temp_remover = BackgroundRemover(model=model)
        else:
            temp_remover = remover
        
        # Process image
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{output_format}") as tmp_output:
            tmp_output_path = tmp_output.name
        
        temp_remover.remove_background(
            tmp_input_path,
            tmp_output_path,
            alpha_matting=alpha_matting,
            only_mask=only_mask
        )
        
        # Read processed image
        with open(tmp_output_path, "rb") as f:
            output_data = f.read()
        
        # Clean up temp files
        os.unlink(tmp_input_path)
        os.unlink(tmp_output_path)
        
        # Return processed image
        return StreamingResponse(
            io.BytesIO(output_data),
            media_type=f"image/{output_format}",
            headers={
                "Content-Disposition": f"attachment; filename={Path(file.filename).stem}_no_bg.{output_format}"
            }
        )
        
    except Exception as e:
        # Clean up temp files on error
        if os.path.exists(tmp_input_path):
            os.unlink(tmp_input_path)
        if 'tmp_output_path' in locals() and os.path.exists(tmp_output_path):
            os.unlink(tmp_output_path)
        
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


@app.post("/remove-batch")
async def remove_background_batch(
    files: List[UploadFile] = File(...),
    model: Optional[str] = Form("u2net"),
    alpha_matting: bool = Form(False),
    only_mask: bool = Form(False)
):
    """
    Remove background from multiple images
    
    Args:
        files: List of image files to process
        model: Model to use (u2net, u2netp, u2net_human_seg, u2net_cloth_seg)
        alpha_matting: Enable alpha matting for better edges
        only_mask: Return only the mask instead of transparent image
    
    Returns:
        JSON response with processing results
    """
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 images per batch")
    
    # Initialize remover with specified model
    if model != "u2net":
        temp_remover = BackgroundRemover(model=model)
    else:
        temp_remover = remover
    
    results = []
    
    for file in files:
        # Validate file type
        if not file.content_type.startswith("image/"):
            results.append({
                "filename": file.filename,
                "success": False,
                "error": "File must be an image"
            })
            continue
        
        # Create temporary file for processing
        with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as tmp_input:
            content = await file.read()
            tmp_input.write(content)
            tmp_input_path = tmp_input.name
        
        try:
            # Process image
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_output:
                tmp_output_path = tmp_output.name
            
            temp_remover.remove_background(
                tmp_input_path,
                tmp_output_path,
                alpha_matting=alpha_matting,
                only_mask=only_mask
            )
            
            # Get file size
            output_size = os.path.getsize(tmp_output_path)
            
            # Clean up temp files
            os.unlink(tmp_input_path)
            os.unlink(tmp_output_path)
            
            results.append({
                "filename": file.filename,
                "success": True,
                "output_size": output_size
            })
            
        except Exception as e:
            # Clean up temp files on error
            if os.path.exists(tmp_input_path):
                os.unlink(tmp_input_path)
            if 'tmp_output_path' in locals() and os.path.exists(tmp_output_path):
                os.unlink(tmp_output_path)
            
            results.append({
                "filename": file.filename,
                "success": False,
                "error": str(e)
            })
    
    return {
        "processed": len(files),
        "successful": sum(1 for r in results if r["success"]),
        "failed": sum(1 for r in results if not r["success"]),
        "results": results
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)