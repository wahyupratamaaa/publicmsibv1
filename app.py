from flask import Flask, render_template
from server_admin import admin_blueprint
from server_user import user_blueprint
from connection import get_collection

books = get_collection("books")
toko = get_collection("mitra")

app = Flask(__name__)

app.register_blueprint(admin_blueprint, url_prefix='/admin')
app.register_blueprint(user_blueprint, url_prefix='/user')

print('-' * 50, 'app.py', '-' * 50)

@app.route("/")
def index():
    return render_template("index.html")

@app.route('/footer')
def footer():
    return render_template("dev/footer.html")

@app.route("/ruangdeveloper")
def tentang():
    return render_template("dev/ruangdeveloper.html")

if __name__ == "__main__":
    app.run('0.0.0.0', port=3000, debug=True)