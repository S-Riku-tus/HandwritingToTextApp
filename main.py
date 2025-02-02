from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse, FileResponse
from fastapi.responses import HTMLResponse
import cv2
import numpy as np
import pytesseract
from PIL import Image
import io
import markdown
from fpdf import FPDF
import os

# Tesseract のパスを指定（Windows の場合）
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()
    

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...), output_format: str = Form("text")):
    # 画像を読み込む
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    # OpenCVで前処理（グレースケール化）
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)

    # OCR でテキストを抽出
    text = pytesseract.image_to_string(image, lang="jpn")

    # 出力形式に応じて処理
    if output_format == "markdown":
        md_text = markdown.markdown(text)
        return JSONResponse(content={"extracted_text": md_text})
    elif output_format == "pdf":
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.multi_cell(0, 10, text)
        pdf_output = "output.pdf"
        pdf.output(pdf_output)
        return FileResponse(pdf_output, media_type='application/pdf', filename="output.pdf")
    else:
        return JSONResponse(content={"extracted_text": text})

# サーバー起動
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
