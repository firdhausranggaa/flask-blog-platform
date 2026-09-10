# Flask Blogging Platform API

Sebuah *Headless CMS* berbasis REST API untuk platform blogging. Dibangun menggunakan **Python** dan **Flask**, repositori ini menyediakan infrastruktur *backend* yang tangguh, aman, dan siap dikonsumsi oleh aplikasi *frontend* modern (seperti Vue.js atau React).

## Fitur Utama

* **RESTful Architecture:** Respons sepenuhnya menggunakan format JSON, dilengkapi penangkap *Global Error Handling*.
* **Stateless Authentication:** Sistem registrasi dan otentikasi menggunakan JSON Web Tokens (JWT) via `Flask-JWT-Extended`.
* **Data Serialization:** Pemetaan dan validasi objek *database* ke JSON secara otomatis dan efisien menggunakan `Marshmallow`.
* **Database Management:** Integrasi basis data MySQL menggunakan `Flask-SQLAlchemy` dan `Flask-Migrate` (Alembic) beserta pelacakan *Audit Trail*.
* **Interactive Documentation:** Dokumentasi *endpoint* otomatis dan interaktif menggunakan `Flasgger` (Swagger UI) dengan dukungan otorisasi *Bearer Token*.
* **Security & Anti-Spam:** Validasi input ketat dan proteksi *Brute-Force* menggunakan `Flask-Limiter`.
* **Data Optimization:** Pengambilan data dioptimalkan dengan fitur paginasi dan filter pencarian konten.
* **CORS Ready:** Siap dihubungkan lintas *port* dengan *frontend development server* (misal: Vite di port 5173).

## Teknologi yang Digunakan

* **Framework:** Flask 3.x
* **Database:** MySQL
* **ORM & Migration:** Flask-SQLAlchemy, PyMySQL, Flask-Migrate
* **Serialization:** Flask-Marshmallow, marshmallow-sqlalchemy
* **Authentication:** Flask-JWT-Extended, Werkzeug
* **API Docs:** Flasgger (OpenAPI/Swagger)
* **Security:** Flask-Limiter, Flask-CORS

## Prasyarat

Sebelum menjalankan aplikasi, pastikan sistem Anda telah terinstal:
* Python 3.8+
* MySQL Server (XAMPP / native) aktif dan berjalan.
* Git

## Instalasi & Konfigurasi

1. **Kloning Repositori**
```bash
git clone [https://github.com/firdhausranggaa/flask-blog-platform.git](https://github.com/firdhausranggaa/flask-blog-platform.git)
cd flask-blog-platform

```

2. **Buat & Aktifkan Virtual Environment**

```bash
python -m venv venv

# Windows:
.\venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

```

3. **Instal Dependensi**

```bash
pip install Flask Flask-SQLAlchemy Flask-Migrate pymysql Flask-CORS Flask-Limiter flasgger flask-jwt-extended flask-marshmallow marshmallow-sqlalchemy python-dotenv

```

4. **Konfigurasi Environment (.env)**
Buat file bernama `.env` di direktori utama (sejajar dengan `run.py`) untuk mengamankan variabel kredensial. Pastikan file ini tidak di-push ke GitHub:

```env
JWT_SECRET_KEY=masukkan_kunci_rahasia_jwt_anda

```

5. **Konfigurasi Database**
Buat *database* kosong bernama `flask_blog` di MySQL (melalui phpMyAdmin atau HeidiSQL). Pastikan URI koneksi di dalam `app/__init__.py` sudah sesuai dengan kredensial lokal Anda:

```python
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/flask_blog"

```

6. **Migrasi Tabel Database**
Terapkan skema relasional ke dalam MySQL:

```bash
flask --app run db upgrade

```

## Menjalankan Aplikasi

Jalankan *server development* Flask:

```bash
python run.py

```

Aplikasi akan berjalan di `http://127.0.0.1:5000`.

## Dokumentasi API

Seluruh rute dan uji coba *endpoint* (*Try it out*) dapat diakses secara visual melalui antarmuka Swagger:
👉 **http://127.0.0.1:5000/apidocs**

## Struktur Direktori

```text
flask-blog-platform/
│
├── app/
│   ├── __init__.py          # Application Factory, Swagger UI, & Global Error Handler
│   ├── extensions.py        # Deklarasi Ekstensi (DB, Migrate, JWT, Limiter, Marshmallow)
│   ├── models.py            # Skema Database (User & Post)
│   ├── schemas.py           # Aturan Serialisasi Data (Marshmallow)
│   └── blueprints/          # Modular Routing
│       ├── public.py        # /api/posts & /apidocs redirect
│       ├── user.py          # /api/user (Auth JWT)
│       └── post.py          # /api/post (CRUD Artikel)
│
├── migrations/              # Berkas pelacakan versi database (Alembic)
├── .env                     # Variabel Environment rahasia (diabaikan oleh Git)
├── .gitignore               # Daftar pengecualian file Git
├── run.py                   # Entry point aplikasi
└── README.md                # Dokumentasi Proyek
