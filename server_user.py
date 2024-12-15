from flask import Flask, Blueprint, render_template, request, jsonify, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from connection import db, get_collection

books = get_collection("books")

user_blueprint = Blueprint('user', __name__, template_folder='templates')

@user_blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        print('Data Toko', data)
        username = data.get("username")
        password = data.get("password")

        user_ref = db.collection('Pengguna').where("username", "==", username).limit(1).stream()
        user = next(user_ref, None)

        if user and check_password_hash(user.to_dict()["password"], password):
            return jsonify({"message": f"Hi Selamat Datang "}), 200
        else:
            return jsonify({"error": "Username atau password salah"}), 401
    return render_template("clients/login.html")


@user_blueprint.route("/registrasi", methods=["GET", "POST"])
def registrasi():
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        confirm_password = data.get("confirm_password")

        if not username or not password or not confirm_password:
            return jsonify({"error": "Semua field harus diisi"}), 400
        if password != confirm_password:
            return jsonify({"error": "Password dan konfirmasi password tidak cocok"}), 400

        hashed_password = generate_password_hash(password)

        user_data = {
            "username": username,
            "password": hashed_password,
            "created_at": datetime.now()
        }

        db.collection('Pengguna').add(user_data)
        return jsonify({"message": "Registrasi berhasil!"}), 201

    return render_template("clients/registrasi.html")

@user_blueprint.route("/logout")
def logout():
    return render_template('index.html')


@user_blueprint.route("/dashboard")
def dashboard():
    return render_template("clients/dashboard.html")

@user_blueprint.route("/produk")
def produk():
    return render_template("clients/produk.html")

@user_blueprint.route("/produk_json_user", methods=["GET"])
def produk_json():
    books_ref = books.stream()
    books_list = []
    for book in books_ref:
        book_data = book.to_dict()
        book_data['id'] = book.id
        book_data['image'] = url_for('static', filename=f'uploads/{book_data["image"]}')
        books_list.append(book_data)
    return jsonify({'books': books_list})


@user_blueprint.route("/checkout/<book_id>")
def checkout(book_id):
    try:
        book_ref = books.document(book_id).get()
        if book_ref.exists:
            book = book_ref.to_dict()
            book['id'] = book_id
            book['image'] = url_for('static', filename=f'uploads/{book["image"]}')
        else:
            return jsonify({"error": "Book not found"}), 404
    except Exception as e:
        return jsonify({"error": "Invalid book ID"}), 400

    return render_template("clients/checkout.html", book=book)

@user_blueprint.route("/complete_checkout", methods=["POST"])
def complete_checkout():
    data = request.get_json()
    book_id = data.get("book_id")
    user_id = data.get("user_id")

    if not book_id:
        return jsonify({"error": "Book ID is required"}), 400

    try:
        book_ref = books.document(book_id).get()
        if not book_ref.exists:
            return jsonify({"error": "Book not found"}), 404

        book = book_ref.to_dict()

        order = {
            "user_id": user_id,
            "book_id": book_id,
            "book_title": book["judul"],
            "book_price": book["harga"],
            "order_date": datetime.utcnow()
        }

        orders = get_collection("orders")
        orders.add(order)

        return jsonify({"message": "Purchase completed successfully!"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@user_blueprint.route("/dashboardProduk")
def dashboardProduk():
    return render_template("clients/dashboardProduk.html")

@user_blueprint.route("/kontak")
def kontak():
    return render_template("clients/kontak.html")


@user_blueprint.route("/dashboardPenjual")
def dashboardPenjual():
    return render_template("clients/dashboardPenjual.html")



@user_blueprint.route("/user_books", methods=["GET"])
def user_books():
    # Replace with actual logic to get user books
    books_ref = books.stream()
    books_list = []
    for book in books_ref:
        book_data = book.to_dict()
        book_data['id'] = book.id
        book_data['image'] = url_for('static', filename=f'uploads/{book_data["image"]}')
        books_list.append(book_data)
    return jsonify({"books": books_list})


def create_app():
    app = Flask(__name__)
    app.register_blueprint(user_blueprint, url_prefix='/user')
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)