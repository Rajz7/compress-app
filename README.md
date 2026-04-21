<<<<<<< HEAD
# compress-app
Created this simple app which compresses images and pdfs locally. 
=======
# 🗜️ Compress App

*A simple, privacy-focused file compression tool that runs locally on your machine.*

## Why I Built This 📝

You know that feeling when you're filling out important government forms online and you hit that dreaded "file too large" error? Yeah, that was me last week. I had all my documents ready to go, but they were just a bit too chunky for the upload limits.

Sure, I could've used one of those online compression tools, but honestly? I wasn't thrilled about uploading my personal documents to some random website. Who knows what they're doing with that data, right? Call me paranoid, but when it comes to sensitive documents, I'd rather keep things local.

So I thought, "How hard could it be to build a simple compression tool?" Turns out, not that hard! And now I've got my own little app that compresses files without sending them anywhere. Privacy? Check. ✅

## What It Does 🛠️

- **Image Compression**: Drop in your images and compress them with adjustable quality settings
- **PDF Compression**: Three powerful compression modes powered by PyMuPDF:
  - **Images Only**: Compress embedded images in PDFs  
  - **Structure**: Remove metadata and optimize PDF streams
  - **Full Compression**: Combined image compression + structure optimization
- **Privacy First**: Everything runs locally - your files never leave your computer
- **Simple Interface**: Clean web UI that's actually pleasant to use
- **No Size Limits**: Compress files as big as your storage can handle

## Supported Formats 📁

**Images**: JPEG files (the most common format for photos and documents)
**PDFs**: Any PDF file - with three different compression strategies to choose from

*Note: All images get optimized and saved as JPEG files for maximum compatibility.*

## Installation & Setup 🚀

### Prerequisites
- Python 3.8 or higher
- A few minutes and maybe a cup of coffee ☕

### Step 1: Clone or Download
```bash
git clone <your-repo-url>
# or just download and extract the files
cd compress-app
```

### Step 2: Set Up Virtual Environment
```bash
python -m venv .venv

# On Linux/Mac:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### Step 3: Install Python Dependencies
```bash
pip install fastapi uvicorn pillow PyMuPDF aiofiles python-multipart
```

### Step 4: Run the App
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Step 6: Open Your Browser
Head over to `http://localhost:8000` and you're good to go! 🎉

## How to Use 📖

### For Images:
1. Click "Select Image File" and choose your image
2. Adjust the quality slider (lower = smaller file, higher = better quality)
3. Hit "Upload Image" 
4. Once uploaded, click "Compress Image"
5. Your compressed image will be saved in the `compressed/` folder

### For PDFs:
1. Select your PDF file
2. Choose compression mode:
   - **Images Only**: Compress embedded images (good for image-heavy PDFs)
   - **Structure**: Remove metadata + optimize streams (good for text PDFs)
   - **Full**: Combined compression for maximum size reduction
3. Set your quality preference
4. Upload and compress!

## File Structure 📂

```
compress-app/
├── app.py              # The main FastAPI application
├── templates/
│   └── index.html      # Web interface
├── uploads/            # Where uploaded files go
├── compressed/         # Where the magic happens ✨
└── README.md           # You are here!
```

## Tips & Tricks 💡

- **For government forms**: Usually 50-70% quality works great and keeps file sizes reasonable
- **For photos you want to keep**: Go with 80-90% quality
- **Need tiny files?**: Try 20-40% quality - you'll be surprised how good it still looks!
- **Batch processing**: You can compress multiple files one after another without restarting

## Privacy Notes 🔒

- **Everything stays local** - no internet required after setup
- **No tracking, no analytics** - just you and your files
- **No file limits** - compress whatever you need
- **Open source** - you can see exactly what the code does

## Troubleshooting 🔧

**Port already in use?** Try a different port:
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8001
```

**Images not compressing?** Make sure they're JPEG files - other formats aren't supported yet.

**Need help?** Feel free to open an issue or reach out!

## Future Ideas 💭

- Support for more image formats (PNG, WebP, GIF, etc.)
- Batch processing multiple files at once
- Drag & drop interface
- Download links for compressed files
- File size comparison stats
- Maybe a desktop app version?

## Contributing 🤝

Found a bug? Have an idea? Pull requests and issues are welcome! This started as a personal tool, but I'm happy to make it better for everyone.

---

*Built with ❤️ and a healthy dose of privacy paranoia*
>>>>>>> 21f9b25 (pilot)
