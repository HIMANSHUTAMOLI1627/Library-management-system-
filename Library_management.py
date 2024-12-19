from flask import Flask, request, jsonify
import uuid
import hashlib

app = Flask(__name__)

# In-memory storage
books = []
members = []
tokens = {}

# Utility functions
def generate_token(username):
    token = hashlib.sha256(username.encode()).hexdigest()
    tokens[token] = username
    return token

def authenticate(token):
    return tokens.get(token)

# Routes
@app.route('/books', methods=['GET', 'POST'])
def manage_books():
    token = request.headers.get('Authorization')
    if not authenticate(token):
        return jsonify({"error": "Unauthorized"}), 401

    if request.method == 'POST':
        data = request.json
        book = {
            "id": str(uuid.uuid4()),
            "title": data["title"],
            "author": data["author"],
            "year": data["year"]
        }
        books.append(book)
        return jsonify(book), 201

    # GET request
    query = request.args.get('query')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 5))
    filtered_books = books

    if query:
        filtered_books = [book for book in books if query.lower() in book['title'].lower() or query.lower() in book['author'].lower()]

    start = (page - 1) * per_page
    end = start + per_page
    return jsonify(filtered_books[start:end])

@app.route('/books/<book_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_single_book(book_id):
    token = request.headers.get('Authorization')
    if not authenticate(token):
        return jsonify({"error": "Unauthorized"}), 401

    book = next((book for book in books if book["id"] == book_id), None)
    if not book:
        return jsonify({"error": "Book not found"}), 404

    if request.method == 'GET':
        return jsonify(book)

    if request.method == 'PUT':
        data = request.json
        book.update(data)
        return jsonify(book)

    if request.method == 'DELETE':
        books.remove(book)
        return '', 204

@app.route('/members', methods=['GET', 'POST'])
def manage_members():
    token = request.headers.get('Authorization')
    if not authenticate(token):
        return jsonify({"error": "Unauthorized"}), 401

    if request.method == 'POST':
        data = request.json
        member = {
            "id": str(uuid.uuid4()),
            "name": data["name"],
            "email": data["email"]
        }
        members.append(member)
        return jsonify(member), 201

    return jsonify(members)

@app.route('/members/<member_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_single_member(member_id):
    token = request.headers.get('Authorization')
    if not authenticate(token):
        return jsonify({"error": "Unauthorized"}), 401

    member = next((member for member in members if member["id"] == member_id), None)
    if not member:
        return jsonify({"error": "Member not found"}), 404

    if request.method == 'GET':
        return jsonify(member)

    if request.method == 'PUT':
        data = request.json
        member.update(data)
        return jsonify(member)

    if request.method == 'DELETE':
        members.remove(member)
        return '', 204

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    # Dummy authentication
    if username == "admin" and password == "password":
        token = generate_token(username)
        return jsonify({"token": token})

    return jsonify({"error": "Invalid credentials"}), 401

# Run the app
if __name__ == '__main__':
    app.run(debug=True)