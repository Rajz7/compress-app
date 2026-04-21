from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, FileResponse
from PIL import Image
import os
import fitz
import io
import aiofiles

app = FastAPI()

@app.get("/", response_class=HTMLResponse)

async def read_index():
    with open("templates/index.html", "r") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.post("/upload-image/")
async def upload_image(file: UploadFile = File(...)):
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Save the uploaded file
    file_location = f"uploads/{file.filename}"
    os.makedirs("uploads", exist_ok=True)
    
    async with aiofiles.open(file_location, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    return {"message": "Image uploaded successfully", "filename": file.filename, "path": file_location}

@app.post("/compress-image/{filename}")
async def compress_image(filename: str, quality: int = 50):
    try:
        file_path = f"uploads/{filename}"
        # Ensure file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {filename} not found in uploads directory")

        with Image.open(file_path) as img:
            os.makedirs("compressed", exist_ok=True)
            
            # Get file extension and create compressed filename
            name_without_ext = os.path.splitext(filename)[0]
            files = os.listdir("compressed")
            existing_compressed_files = [f for f in files if f.startswith(f"compressed_{name_without_ext}")]
            if existing_compressed_files:             
                compressed_filename = f"compressed/compressed_{name_without_ext}_{len(existing_compressed_files)+1}.jpg"
            else:
                compressed_filename = f"compressed/compressed_{name_without_ext}.jpg"
            
            # Convert to RGB if necessary (important for JPEG output)
            if img.mode in ("RGBA", "P", "LA"):
                img = img.convert("RGB")
            
            # Save as JPEG with specified quality (universal format)
            img.save(compressed_filename, format="JPEG", quality=quality, optimize=True)

        return {"message": f"Compressed image saved as {compressed_filename}", "compressed_path": compressed_filename}

    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error compressing image: {str(e)}") 
    
@app.post("/upload-pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    # Validate file type
    if not file.content_type == 'application/pdf':
        raise HTTPException(status_code=400, detail="File must be a PDF")
    
    # Save the uploaded file
    file_location = f"uploads/{file.filename}"
    os.makedirs("uploads", exist_ok=True)
    
    async with aiofiles.open(file_location, 'wb') as f:
        content = await file.read()
        await f.write(content)
    
    return {"message": "PDF uploaded successfully", "filename": file.filename, "path": file_location}

@app.post("/compress-pdf/{filename}")
async def compress_pdf(filename: str, mode: str, quality: int = 50):
    file_path = f"uploads/{filename}"
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="PDF not found")
        
    if mode == "images":
        doc = fitz.open(file_path)
        os.makedirs("compressed", exist_ok=True)
        files = os.listdir("compressed")
        existing_compressed_files = [f for f in files if f.startswith(f"compressed_{name_without_ext}")]
        if existing_compressed_files:             
            compressed_filename = f"compressed/compressed_{filename}_{len(existing_compressed_files)+1}.jpg"
        else:
            compressed_filename = f"compressed/compressed_{filename}.jpg"
        

        for page_index in range(len(doc)):
            page = doc[page_index]
            image_list = page.get_images(full=True)

            for img in image_list:
                xref = img[0]

                # Extract image bytes
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]

                try:
                    # Open with PIL
                    image = Image.open(io.BytesIO(image_bytes))

                    # Convert to RGB (important for JPEG)
                    if image.mode in ("RGBA", "P"):
                        image = image.convert("RGB")

                    # Recompress
                    img_io = io.BytesIO()
                    image.save(img_io, format="JPEG", quality=quality)
                    new_image_bytes = img_io.getvalue()

                    # Replace image in PDF
                    doc.update_stream(xref, new_image_bytes)

                except Exception:
                    # Skip unsupported images
                    continue

        # Save compressed PDF
        doc.save(compressed_filename, garbage=4, deflate=True)
        doc.close() 
        return {"message": f"Compressed PDF saved as {compressed_filename}", "compressed_path": compressed_filename}

    elif mode == "structure":
        # Remove metadata and compress streams using PyMuPDF
        try:
            doc = fitz.open(file_path)
            os.makedirs("compressed", exist_ok=True)
            files = os.listdir("compressed")
            existing_compressed_files = [f for f in files if f.startswith(f"compressed_{name_without_ext}")]
            if existing_compressed_files:             
                compressed_filename = f"compressed/compressed_{filename}_{len(existing_compressed_files)+1}.jpg"
            else:
                compressed_filename = f"compressed/compressed_{filename}.jpg"
            
            
            # Remove metadata
            doc.set_metadata({})
            
            # Save with aggressive compression settings
            doc.save(compressed_filename, 
                    garbage=4,          # Aggressive garbage collection 
                    deflate=True,       # Compress streams
                    clean=True,         # Clean up unused objects
                    ascii=False,        # Use binary encoding
                    expand=0,           # Don't expand streams
                    linear=False)       # Don't linearize
            doc.close()
            
            return {"message": f"Compressed PDF saved as {compressed_filename}", "compressed_path": compressed_filename}
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error compressing PDF structure: {str(e)}")

    elif mode == "full":
        # Full compression: images + structure using PyMuPDF
        try:
            doc = fitz.open(file_path)
            os.makedirs("compressed", exist_ok=True)
            files = os.listdir("compressed")
            existing_compressed_files = [f for f in files if f.startswith(f"compressed_{name_without_ext}")]
            if existing_compressed_files:             
                compressed_filename = f"compressed/compressed_{filename}_{len(existing_compressed_files)+1}.jpg"
            else:
                compressed_filename = f"compressed/compressed_{filename}.jpg"
            
            
            print(f"Starting full compression for {filename}")
            
            # First pass: Compress images
            image_count = 0
            for page_index in range(len(doc)):
                page = doc[page_index]
                image_list = page.get_images(full=True)
                
                for img in image_list:
                    xref = img[0]
                    
                    # Extract image bytes
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    
                    try:
                        # Open with PIL
                        image = Image.open(io.BytesIO(image_bytes))
                        
                        # Convert to RGB (important for JPEG)
                        if image.mode in ("RGBA", "P"):
                            image = image.convert("RGB")
                        
                        # Recompress with specified quality
                        img_io = io.BytesIO()
                        image.save(img_io, format="JPEG", quality=quality, optimize=True)
                        new_image_bytes = img_io.getvalue()
                        
                        # Replace image in PDF
                        doc.update_stream(xref, new_image_bytes)
                        image_count += 1
                        
                    except Exception:
                        # Skip unsupported images
                        continue
            
            print(f"Compressed {image_count} images")
            
            # Second pass: Remove metadata and compress structure
            doc.set_metadata({})
            
            # Save with all compression options
            doc.save(compressed_filename,
                    garbage=4,          # Maximum garbage collection
                    deflate=True,       # Compress all streams
                    clean=True,         # Clean unused objects
                    ascii=False,        # Binary encoding
                    expand=0,           # Don't expand streams  
                    linear=False)       # Don't linearize
            
            doc.close()
            
            # Get final file size for logging
            final_size = os.path.getsize(compressed_filename)
            print(f"Full compression completed, final file size: {final_size} bytes")
            
            return {"message": f"Fully compressed PDF saved as {compressed_filename}", "compressed_path": compressed_filename}
            
        except Exception as e:
            print(f"Full compression error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error with full PDF compression: {str(e)}")
    
    else:
        raise HTTPException(status_code=400, detail="Invalid compression mode. Use 'images', 'structure', or 'full'")
