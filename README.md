# EduBooks 📘✨

**EduBooks** adalah platform berbasis web untuk penjualan buku edukasi, menyediakan akses login terpisah untuk pembeli dan mitra. Proyek ini menggunakan **Flask** untuk backend, **Firebase** sebagai database, dan dideploy di **Railway** untuk akses yang lancar dan skalabilitas tinggi.

---

## 🚀 Fitur

### 🔐 **Akses Login**

- **Pembeli**:
  - Melihat katalog buku.
  - Menambahkan buku ke keranjang.
  - Melakukan pembelian.
- **Mitra**:
  - Menambahkan buku baru untuk dijual.
  - Mengedit dan menghapus detail buku.

### 📚 **Manajemen Buku**

- Tambah, edit, dan hapus detail buku.
- Tampilkan katalog buku dengan filter berdasarkan kategori.

### 💳 **Transaksi Pembelian**

- Fitur keranjang untuk pembeli.
- Proses checkout untuk menyelesaikan pembelian.

### 🌐 **Deployment**

- Deploy menggunakan **Railway** untuk performa tinggi dan skalabilitas.

---

## 🛠 **Teknologi yang Digunakan**

| **Komponen**     | **Teknologi**                        |
| ---------------- | ------------------------------------ |
| Backend          | Flask (Python) 🐍                    |
| Database         | Firebase Firestore 🔥                |
| Deployment       | Railway 🚂                           |
| Frontend         | HTML, CSS, Javascript 🎨             |
| Dependency Utama | Flask-Cors, Firebase-admin, Requests |

---

## 🏗 **Struktur Proyek**

```plaintext
bookmsibv1/
├── app.py                # File utama Flask
├── requirements.txt      # Daftar dependencies Python
├── serviceAccountKey.json# Kredensial Firebase
├── templates/            # File HTML
├── static/               # File CSS dan JavaScript
├── .env                  # Konfigurasi variabel lingkungan
└── README.md             # Dokumentasi proyek
```

---

## 🚀 **Instalasi Lokal**

Ikuti langkah-langkah berikut untuk menjalankan proyek di lokal:

### 1. Clone Repository

```bash
git clone https://github.com/wahyupratamaaa/bookmsibv1.git
cd bookmsibv1
```

### 2. Buat Virtual Environment

```bash
python -m venv venv
source venv/bin/activate # Untuk Linux/Mac
venv\Scripts\activate   # Untuk Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Konfigurasi Firebase

1. Buka [Firebase Console](https://console.firebase.google.com/).
2. Buat proyek baru atau gunakan proyek yang sudah ada.
3. Unduh file `serviceAccountKey.json` dari pengaturan proyek Firebase.
4. Tempatkan file tersebut di root direktori proyek Anda.

### 5. Konfigurasi Environment Variables

Buat file `.env` di direktori utama dengan konten berikut:

```plaintext
FIREBASE_ADMIN_CREDENTIALS=serviceAccountKey.json
FIREBASE_DATABASE_URL=https://<project-id>.firebaseio.com
SECRET_KEY=your_secret_key
```

### 6. Jalankan Server

```bash
flask run
```

Akses proyek di: **http://127.0.0.1:5000**

---

## 🌐 **Deployment di Railway**

### 1. Login ke Railway

- Buka [Railway](https://railway.app/) dan login.

### 2. Buat Proyek Baru

- Klik **New Project** > **Deploy from GitHub Repo**.
- Sambungkan repository Anda ke Railway.

### 4. Deploy

- Klik tombol **Deploy**.
- Railway akan otomatis membangun dan menjalankan aplikasi Anda.

Aplikasi akan tersedia di:  
**[EduBooks App](https://bookmsibv1.up.railway.app/)** 🚀

---

## 🤝 **Kontribusi**

Jika Anda ingin berkontribusi dalam proyek ini:

1. Fork repository ini.
2. Buat branch baru: `git checkout -b fitur-anda`.
3. Commit perubahan Anda: `git commit -m 'Menambahkan fitur baru'`.
4. Push ke branch Anda: `git push origin fitur-anda`.
5. Buat pull request.

---

## 👥 **Anggota Kelompok**

- **Wahyu Pratama** - Developer
- **Tanujaya Chandra Setyawan** - Developer
- **Firda Nur Laily** - UI/UX Designer

---

## 📞 **Kontak**

Jika ada pertanyaan atau saran, hubungi kami:

- **Nama Tim**: Be Quiet! 📚
- **Email**: [wahyupratamaa.id@gmail.com](mailto:wahyupratamaa.id@gmail.com) ✉️
- **GitHub**: [Wahyu Pratama](https://github.com/wahyupratamaaa) 🐙
- **Aplikasi**: [EduBooks](https://bookmsibv1.up.railway.app/) 🌐

---

## 🌟 **Demo Langsung**

Klik di sini untuk mengeksplorasi aplikasi:  
👉 [EduBooks App](https://bookmsibv1.up.railway.app/)
