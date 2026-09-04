# Flask Blogging Platform API

Sebuah *Headless CMS* berbasis REST API untuk platform blogging. Dibangun menggunakan **Python** dan **Flask**, repositori ini menyediakan infrastruktur *backend* yang tangguh, aman, dan siap dikonsumsi oleh aplikasi *frontend* modern (seperti Vue.js atau React).

## Fitur Utama

* **RESTful Architecture:** Respons sepenuhnya menggunakan format JSON.
* **Authentication:** Sistem registrasi dan login menggunakan `Flask-Login` dan enkripsi *password* `Werkzeug`.
* **Database Management:** Integrasi basis data MySQL menggunakan `Flask-SQLAlchemy` dan `Flask-Migrate` (Alembic).
* **Interactive Documentation:** Dokumentasi *endpoint* otomatis dan interaktif menggunakan `Flasgger` (Swagger UI).
* **Security & Anti-Spam:** Validasi input ketat dan proteksi *Brute-Force* menggunakan `Flask-Limiter`.
* **Data Optimization:** Pengambilan data dioptimalkan dengan fitur paginasi dan filter pencarian konten.
* **CORS Ready:** Siap dihubungkan lintas *port* dengan *frontend development server* (misal: Vite di port 5173).

## Teknologi yang Digunakan

* **Framework:** Flask 3.x
* **Database:** MySQL
* **ORM & Migration:** Flask-SQLAlchemy, PyMySQL, Flask-Migrate
* **API Docs:** Flasgger (OpenAPI/Swagger)
* **Security:** Flask-Login, Flask-Limiter, Flask-CORS

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
pip install Flask Flask-SQLAlchemy Flask-Migrate Flask-Login pymysql Flask-CORS Flask-Limiter flasgger

```


4. **Konfigurasi Database**
Buat *database* kosong bernama `flask_blog` di MySQL (melalui phpMyAdmin atau HeidiSQL). Pastikan URI koneksi di dalam `app/__init__.py` sudah sesuai dengan kredensial lokal Anda:
```python
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:@localhost/flask_blog"

```


5. **Migrasi Tabel Database**
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
👉 **[http://127.0.0.1:5000/apidocs](https://www.google.com/search?q=http://127.0.0.1:5000/apidocs)**

## Struktur Direktori

```text
flask-blog-platform/
│
├── app/
│   ├── __init__.py          # Application Factory & Konfigurasi Ekstensi
│   ├── extensions.py        # Deklarasi SQLAlchemy, Migrate, LoginManager, Limiter
│   ├── models.py            # Skema Database (User & Post)
│   └── blueprints/          # Modular Routing
│       ├── public.py        # /api/posts & /apidocs redirect
│       ├── user.py          # /api/user (Auth)
│       └── post.py          # /api/post (CRUD Artikel)
│
├── migrations/              # Berkas pelacakan versi database (Alembic)
├── run.py                   # Entry point aplikasi
└── README.md                # Dokumentasi Proyek
