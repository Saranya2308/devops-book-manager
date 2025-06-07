from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Environment variables for database connection
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "books")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

@app.route("/books", methods=["GET"])
def get_books():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM books;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(rows)

@app.route("/books", methods=["POST"])
def add_book():
    new_book = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO books (title, author, published_date) VALUES (%s, %s, %s)",
        (new_book["title"], new_book["author"], new_book["published_date"])
    )
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"message": "Book added"}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
