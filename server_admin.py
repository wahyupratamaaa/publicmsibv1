from flask import Flask, Blueprint, render_template, request, jsonify, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from dotenv import load_dotenv
from connection import get_collection

books = get_collection("books")
toko = get_collection("mitra")

UPLOAD_FOLDER = 'static/uploads'

def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'avif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

admin_blueprint = Blueprint('admin', __name__, template_folder='templates')

@admin_blueprint.route("/login_server", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        
        user_ref = toko.where("username", "==", username).limit(1).stream()
        user = next(user_ref, None)

        if user and check_password_hash(user.to_dict()["password"], password):
            return jsonify({"message": f"Hi , Selamat Datang "}), 200
        else:
            return jsonify({"error": "Username atau password salah"}), 401
    return render_template("server/login_server.html")


# server_admin.py

@admin_blueprint.route("/registrasi_server", methods=["GET", "POST"])
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

        toko.add(user_data)
        return jsonify({"message": "Registrasi EduBooks MarketPlace berhasil!"}), 201

    return render_template("server/registrasi_server.html")

# server_admin.py

@admin_blueprint.route("/dashboard_toko", methods=['GET', 'POST'])
def dashboardPenjual():
    try:
        if request.method == 'POST':
            penulis_receive = request.form.get('penulis_give')
            judul_receive = request.form.get('judul_give')
            harga_receive = request.form.get('harga_give')

            if 'file_give' not in request.files:
                return jsonify({'error': 'Tidak ada file yang diunggah'}), 400

            file = request.files['file_give']
            harga_receive = int(harga_receive)

            if file and allowed_file(file.filename):
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                filename = secure_filename(f"{file.filename.rsplit('.', 1)[0]}-{timestamp}.{file.filename.rsplit('.', 1)[-1]}")
                filepath = os.path.join(UPLOAD_FOLDER, filename)

                file.save(filepath)
            else:
                return jsonify({'error': 'Format file tidak didukung'}), 400
            
            doc = {
                'penulis': penulis_receive,
                'judul': judul_receive,
                'harga': harga_receive,
                'image': filename,
            }
            
            books.add(doc)
            print(f"Data berhasil disimpan: {doc}")
            return jsonify({'msg': 'Data buku berhasil disimpan!'}), 200

        return render_template("server/dashboard_toko.html")

    except Exception as e:
        print(f"Error saat menyimpan data: {e}")
        return jsonify({'error': 'Terjadi kesahalan dalam menyimpan data'}), 500
    
@admin_blueprint.route("/update/<judul>", methods=['GET', 'POST'])
def edit_data(judul):
    print(judul)
    try:
        if request.method == 'POST':
            penulis_receive = request.form.get('penulis')
            judul_receive = request.form.get('judul')
            harga_receive = request.form.get('harga')

            if not penulis_receive or not judul_receive or not harga_receive:
                return jsonify({'error': 'Semua field harus diisi'}), 400

            harga_receive = int(harga_receive)

            file = request.files.get('file_give')
            if file and allowed_file(file.filename):
                timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                filename = secure_filename(f"{file.filename.rsplit('.', 1)[0]}-{timestamp}.{file.filename.rsplit('.', 1)[-1]}")
                filepath = os.path.join(UPLOAD_FOLDER, filename)

                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                file.save(filepath)

                update_data = {
                    'penulis': penulis_receive,
                    'judul': judul_receive,
                    'harga': harga_receive,
                    'image': filename,
                }
            else:
                update_data = {
                    'penulis': penulis_receive,
                    'judul': judul_receive,
                    'harga': harga_receive,
                }

            book_ref = books.where('judul', '==', judul).limit(1).stream()
            book = next(book_ref, None)
            if not book:
                return jsonify({'error': 'Data tidak ditemukan atau tidak ada perubahan'}), 404

            book.reference.update(update_data)

            return jsonify({'msg': 'Data berhasil diperbarui!'}), 200

        book_ref = books.where('judul', '==', judul).limit(1).stream()
        book = next(book_ref, None)
        if not book:
            return jsonify({'error': 'Data tidak ditemukan'}), 404

        data = book.to_dict()
        return render_template("dev/dashboard_edit.html", data=data)
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return jsonify({'error': 'Terjadi kesalahan pada server'}), 500

@admin_blueprint.route("/delete/<judul>", methods=['POST'])
def delete_data(judul):
    try:
        book_ref = books.where('judul', '==', judul).limit(1).stream()
        book = next(book_ref, None)
        if not book:
            return jsonify({'error': 'Data tidak ditemukan'}), 404

        book.reference.delete()
        return jsonify({'msg': 'Data berhasil dihapus!'}), 200
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")
        return jsonify({'error': 'Terjadi kesalahan pada server'}), 500

@admin_blueprint.route("/logout")
def logout():
    return render_template("./templates/index.html")

@admin_blueprint.route("/dashboard_server")
def dashboard():
        return render_template("server/dashboard_server.html")

@admin_blueprint.route("/produk_server")
def produk_server():
    return render_template("server/produk_server.html")

@admin_blueprint.route("/produk_json", methods=["GET"])
def produk_json():
    books_ref = books.stream()
    books_list = []
    for book in books_ref:
        book_data = book.to_dict()
        book_data['id'] = book.id
        book_data['image'] = url_for('static', filename=f'uploads/{book_data["image"]}')
        books_list.append(book_data)
    return jsonify({'books': books_list})

@admin_blueprint.route("/checkout")
def checkout():
    return render_template("clients/checkout.html")

@admin_blueprint.route("/dashboardProduk")
def dashboardProduk():
    return render_template("clients/dashboardProduk.html")

@admin_blueprint.route("/kontak")
def kontak():
    return render_template("clients/kontak.html")


def create_app():
    app = Flask(__name__)
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    return app

# Menjalankan aplikasi Flask
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)