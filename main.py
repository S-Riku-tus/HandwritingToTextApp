from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import pytesseract
from PIL import Image
import pdfkit
import io
import markdown
from fpdf import FPDF
import os

# Tesseract のパスを指定（Windows の場合）
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = FastAPI()

# CORS設定（フロントエンドとの通信を許可）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()
    

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...), output_format: str = "text"):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    # OpenCVで前処理（グレースケール化）
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)

    # OCR でテキストを抽出（日本語対応）
    text = pytesseract.image_to_string(image, lang="jpn")

    if output_format == "markdown":
        markdown_text = f"# OCR抽出結果\n\n{text}"
        with open("output.md", "w", encoding="utf-8") as md_file:
            md_file.write(markdown_text)
        return {"message": "Markdownに保存しました", "file": "output.md"}

    elif output_format == "pdf":
        pdf_path = "output.pdf"
        pdfkit.from_string(text, pdf_path)
        return {"message": "PDFに保存しました", "file": pdf_path}

    return {"extracted_text": text}

# サーバー起動
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)


# サーバー起動
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
