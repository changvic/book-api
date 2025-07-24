# Day 3 - 迷你 RESTful Book API

用 Python Flask 快速打造 RESTful API，支援 CRUD 操作。

## 安裝

pip install flask
python app.py

## API 使用

- GET `/books`：取得所有書
- GET `/books/<id>`：查單本
- POST `/books`：新增書（需傳 title, author）
- PUT `/books/<id>`：修改書
- DELETE `/books/<id>`：刪除書

## 範例

curl http://127.0.0.1:5000/books
curl -X POST -H "Content-Type: application/json" -d '{"title":"新書", "author":"小明"}' http://127.0.0.1:5000/books

更新 V1.1

- 新增 books.jon，用 JSON 檔存書籍資料

更新 V1.2

- Flask + SQLite 迷你書籍 API

更新 V1.3

- 增加驗證欄位
