# HandwritingToTextApp

手書きノートの画像から文字を抽出するアプリです。

## 使い方
1. `uvicorn main:app --reload` でサーバーを起動
2. `index.html` を開いて画像をアップロード
3. 抽出されたテキストをコピー・保存

## スタック
- Python
- FastAPI
- OpenCV
- Tesseract OCR
- JavaScript

## 実行方法
1. venv\Scripts\activate
2. uvicorn main:app --reload
