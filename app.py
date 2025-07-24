from flask import Flask, jsonify, request

app = Flask(__name__)

# 範例書籍資料（記憶體，重啟會消失）
books = [
    {"id": 1, "title": "Python 入門", "author": "Vic"},
    {"id": 2, "title": "Flask 實戰", "author": "Anna"}
]

@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(books)

@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = next((b for b in books if b["id"] == book_id), None)
    return jsonify(book) if book else ("", 404)

@app.route("/books", methods=["POST"])
def add_book():
    data = request.json
    new_book = {
        "id": books[-1]["id"]+1 if books else 1,
        "title": data["title"],
        "author": data["author"]
    }
    books.append(new_book)
    return jsonify(new_book), 201

@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    data = request.json
    for book in books:
        if book["id"] == book_id:
            book["title"] = data.get("title", book["title"])
            book["author"] = data.get("author", book["author"])
            return jsonify(book)
    return ("", 404)

@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    idx = next((i for i, b in enumerate(books) if b["id"] == book_id), None)
    if idx is not None:
        deleted = books.pop(idx)
        return jsonify(deleted)
    return ("", 404)

if __name__ == "__main__":
    app.run(debug=True)
