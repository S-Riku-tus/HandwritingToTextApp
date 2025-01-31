import requests

url = "http://127.0.0.1:8000/upload/"
files = {"file": open("sample.png", "rb")}  # 任意の画像を用意
response = requests.post(url, files=files)

print(response.json())  # OCRで抽出したテキストが表示される
