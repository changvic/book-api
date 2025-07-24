from flask import Flask, jsonify, request
import json
import os

app = Flask(__name__)
DATA_FILE = 'books.json'

# 讀取資料
def load_books():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

# 寫入資料
def save_books(books):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(books, f, ensure_ascii=False, indent=2)

@app.route("/books", methods=["GET"])
def get_books():
    books = load_books()
    return jsonify(books)

@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    books = load_books()
    book = next((b for b in books if b["id"] == book_id), None)
    return jsonify(book) if book else ("", 404)

@app.route("/books", methods=["POST"])
def add_book():
    books = load_books()
    data = request.json
    new_book = {
        "id": books[-1]["id"]+1 if books else 1,
        "title": data["title"],
        "author": data["author"]
    }
    books.append(new_book)
    save_books(books)
    return jsonify(new_book), 201

@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    books = load_books()
    data = request.json
    for book in books:
        if book["id"] == book_id:
            book["title"] = data.get("title", book["title"])
            book["author"] = data.get("author", book["author"])
            save_books(books)
            return jsonify(book)
    return ("", 404)

@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    books = load_books()
    idx = next((i for i, b in enumerate(books) if b["id"] == book_id), None)
    if idx is not None:
        deleted = books.pop(idx)
        save_books(books)
        return jsonify(deleted)
    return ("", 404)

if __name__ == "__main__":
    app.run(debug=True)
