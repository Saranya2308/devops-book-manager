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
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        )
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        return None

@app.route("/")
def home():
    return "🚀 DevOps Book Manager is live!", 200

@app.route("/books", methods=["GET"])
def get_books():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM books;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        # Convert rows to list of dicts (optional)
        books = [
            {"id": r[0], "title": r[1], "author": r[2], "published_date": str(r[3]) if r[3] else None}
            for r in rows
        ]
        return jsonify(books), 200
    except Exception as e:
        print(f"Error fetching books: {e}")
        return jsonify({"error": "Failed to fetch books"}), 500

@app.route("/books", methods=["POST"])
def add_book():
    new_book = request.json
    if not new_book or not all(k in new_book for k in ("title", "author", "published_date")):
        return jsonify({"error": "Missing book data"}), 400
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO books (title, author, published_date) VALUES (%s, %s, %s)",
            (new_book["title"], new_book["author"], new_book["published_date"])
        )
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Book added"}), 201
    except Exception as e:
        print(f"Error adding book: {e}")
        return jsonify({"error": "Failed to add book"}), 500

if __name__ == "__main__":
    # Listen on all interfaces on port 5000
    app.run(host="0.0.0.0", port=5000)
