import sqlite3

conn = sqlite3.connect('books.db')
c = conn.cursor()
c.execute('''
    CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL
    )
''')
conn.commit()
conn.close()
print("books.db 資料庫建立完成！")
