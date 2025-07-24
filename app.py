from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

DB_FILE = 'books.db'

# 共用：查詢所有書
def get_all_books():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM books")
    books = [dict(row) for row in c.fetchall()]
    conn.close()
    return books

# 共用：查詢單本
def get_book_by_id(book_id):
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    row = c.fetchone()
    conn.close()
    return dict(row) if row else None

@app.route("/books", methods=["GET"])
def get_books():
    return jsonify(get_all_books())

@app.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    book = get_book_by_id(book_id)
    return jsonify(book) if book else ("", 404)

@app.route("/books", methods=["POST"])
def add_book():
    data = request.json
    title = data.get("title")
    author = data.get("author")
    if not title or not author:
        # 欄位缺失時回傳 400
        return jsonify({"error": "title 與 author 為必填"}), 400

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("INSERT INTO books (title, author) VALUES (?, ?)", (title, author))
    conn.commit()
    new_id = c.lastrowid
    conn.close()
    return jsonify({"id": new_id, "title": title, "author": author}), 201


@app.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    data = request.json
    title = data.get("title")
    author = data.get("author")
    if not title or not author:
        return jsonify({"error": "title 與 author 為必填"}), 400

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE books SET title = ?, author = ? WHERE id = ?", (title, author, book_id))
    conn.commit()
    updated = c.rowcount
    conn.close()
    if updated:
        return jsonify(get_book_by_id(book_id))
    else:
        return ("", 404)


@app.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    deleted = c.rowcount
    conn.close()
    if deleted:
        return jsonify({"id": book_id, "deleted": True})
    else:
        return ("", 404)

if __name__ == "__main__":
    app.run(debug=True)
