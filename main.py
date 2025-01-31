from fastapi import FastAPI, File, UploadFile
import cv2
import numpy as np
import pytesseract
from PIL import Image
import io

# Tesseract のパスを指定（Windows の場合）
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

app = FastAPI()

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    # 画像を読み込む
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    # OpenCVで前処理（グレースケール化）
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)

    # OCR でテキストを抽出
    text = pytesseract.image_to_string(image, lang="eng")

    return {"extracted_text": text}

# サーバー起動
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
