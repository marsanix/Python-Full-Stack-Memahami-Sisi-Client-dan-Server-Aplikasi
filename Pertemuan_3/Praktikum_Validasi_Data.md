# Praktikum Integrasi Data & Validasi dengan MySQL (30 menit)

Berikut adalah praktikum sederhana yang akan membantu Anda memahami konsep integrasi data dan validasi dengan MySQL dalam waktu 30 menit. Praktikum ini menerapkan prinsip Pareto, di mana dengan 20% usaha, Anda akan mendapatkan 80% pemahaman materi.

## Tujuan Praktikum
- Memahami validasi data di sisi server
- Mengimplementasikan constraints di database MySQL
- Menerapkan error handling dan feedback user

## Persiapan
1. MySQL server terinstal
2. Python dengan Flask dan mysql-connector-python
3. Editor kode (VS Code, PyCharm, dll)

## Langkah 1: Membuat Database dan Tabel dengan Constraints

```sql
-- Buat database
CREATE DATABASE IF NOT EXISTS praktikum_validasi;
USE praktikum_validasi;

-- Buat tabel siswa dengan constraints
CREATE TABLE siswa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(50) NOT NULL,
    umur INT NOT NULL CHECK (umur BETWEEN 10 AND 18),
    email VARCHAR(100) UNIQUE NOT NULL,
    kelas VARCHAR(10) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tambahkan beberapa data awal
INSERT INTO siswa (nama, umur, email, kelas) VALUES
('Budi Santoso', 12, 'budi@example.com', '7A'),
('Ani Wijaya', 13, 'ani@example.com', '8B'),
('Dedi Cahyono', 15, 'dedi@example.com', '9C');
```

## Langkah 2: Membuat Aplikasi Flask dengan Validasi

Buat file `app.py` dengan kode berikut:

```python
from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import re

app = Flask(__name__)
app.secret_key = 'praktikum_validasi_key'

# Konfigurasi database
DB_CONFIG = {
    'host': 'localhost',
    'database': 'praktikum_validasi',
    'user': 'root',
    'password': ''  # Sesuaikan dengan password MySQL Anda
}

# Fungsi validasi
def validasi_nama(nama):
    if not nama or len(nama.strip()) < 2:
        return False, "Nama minimal 2 karakter"
    if len(nama) > 50:
        return False, "Nama maksimal 50 karakter"
    return True, "Valid"

def validasi_umur(umur_str):
    try:
        umur = int(umur_str)
        if umur < 10 or umur > 18:
            return False, "Umur harus antara 10-18 tahun"
        return True, umur
    except ValueError:
        return False, "Umur harus berupa angka"

def validasi_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.match(pattern, email):
        return True, "Valid"
    return False, "Format email tidak valid"

# Fungsi database
def create_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
    return None

def execute_query(query, params=None, fetch=False):
    connection = create_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchall()
            return result
        else:
            connection.commit()
            return cursor.lastrowid
    except Error as e:
        print(f"Error executing query: {e}")
        if connection:
            connection.rollback()
        raise e
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Routes
@app.route('/')
def index():
    try:
        query = "SELECT * FROM siswa ORDER BY id DESC"
        siswa_list = execute_query(query, fetch=True)
        return render_template('index.html', siswa_list=siswa_list)
    except Exception as e:
        flash(f"Terjadi kesalahan: {str(e)}", "error")
        return render_template('index.html', siswa_list=[])

@app.route('/tambah', methods=['GET', 'POST'])
def tambah_siswa():
    if request.method == 'POST':
        try:
            # Ambil data dari form
            nama = request.form['nama'].strip()
            umur_str = request.form['umur']
            email = request.form['email'].strip()
            kelas = request.form['kelas'].strip()
            
            # Validasi data
            valid_nama, pesan_nama = validasi_nama(nama)
            if not valid_nama:
                flash(pesan_nama, "error")
                return render_template('tambah.html')
            
            valid_umur, hasil_umur = validasi_umur(umur_str)
            if not valid_umur:
                flash(hasil_umur, "error")
                return render_template('tambah.html')
            
            valid_email, pesan_email = validasi_email(email)
            if not valid_email:
                flash(pesan_email, "error")
                return render_template('tambah.html')
            
            if not kelas or len(kelas) < 2:
                flash("Kelas minimal 2 karakter", "error")
                return render_template('tambah.html')
            
            # Cek email duplikat
            check_query = "SELECT id FROM siswa WHERE email = %s"
            existing = execute_query(check_query, (email,), fetch=True)
            if existing:
                flash("Email sudah terdaftar!", "error")
                return render_template('tambah.html')
            
            # Simpan data
            insert_query = """
            INSERT INTO siswa (nama, umur, email, kelas) 
            VALUES (%s, %s, %s, %s)
            """
            execute_query(insert_query, (nama, hasil_umur, email, kelas))
            
            flash(f"Siswa {nama} berhasil ditambahkan!", "success")
            return redirect(url_for('index'))
            
        except mysql.connector.IntegrityError as e:
            if "Duplicate entry" in str(e):
                flash("Email sudah terdaftar!", "error")
            elif "CHECK constraint" in str(e):
                flash("Umur harus antara 10-18 tahun!", "error")
            else:
                flash(f"Terjadi kesalahan database: {str(e)}", "error")
            return render_template('tambah.html')
            
        except Exception as e:
            flash(f"Terjadi kesalahan: {str(e)}", "error")
            return render_template('tambah.html')
    
    return render_template('tambah.html')

if __name__ == '__main__':
    app.run(debug=True)
```

## Langkah 3: Membuat Template HTML

Buat folder `templates` dan tambahkan file berikut:

### templates/base.html
```html
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Praktikum Validasi Data</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .container {
            background-color: #f9f9f9;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
        h1 {
            color: #333;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        table, th, td {
            border: 1px solid #ddd;
        }
        th, td {
            padding: 10px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        .btn {
            display: inline-block;
            padding: 8px 16px;
            background-color: #4CAF50;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            border: none;
            cursor: pointer;
        }
        .btn-primary {
            background-color: #2196F3;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
        }
        input, select {
            width: 100%;
            padding: 8px;
            border: 1px solid #ddd;
            border-radius: 4px;
            box-sizing: border-box;
        }
        .flash-messages {
            margin-bottom: 20px;
        }
        .alert {
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 10px;
        }
        .alert-success {
            background-color: #dff0d8;
            color: #3c763d;
            border: 1px solid #d6e9c6;
        }
        .alert-error {
            background-color: #f2dede;
            color: #a94442;
            border: 1px solid #ebccd1;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Praktikum Validasi Data</h1>
        
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                <div class="flash-messages">
                    {% for category, message in messages %}
                        <div class="alert alert-{{ category }}">
                            {{ message }}
                        </div>
                    {% endfor %}
                </div>
            {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
    </div>
</body>
</html>
```

### templates/index.html
```html
{% extends 'base.html' %}

{% block content %}
    <h2>Daftar Siswa</h2>
    
    <a href="{{ url_for('tambah_siswa') }}" class="btn btn-primary">Tambah Siswa</a>
    
    {% if siswa_list %}
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Nama</th>
                    <th>Umur</th>
                    <th>Email</th>
                    <th>Kelas</th>
                </tr>
            </thead>
            <tbody>
                {% for siswa in siswa_list %}
                    <tr>
                        <td>{{ siswa.id }}</td>
                        <td>{{ siswa.nama }}</td>
                        <td>{{ siswa.umur }}</td>
                        <td>{{ siswa.email }}</td>
                        <td>{{ siswa.kelas }}</td>
                    </tr>
                {% endfor %}
            </tbody>
        </table>
    {% else %}
        <p>Belum ada data siswa.</p>
    {% endif %}
{% endblock %}
```

### templates/tambah.html
```html
{% extends 'base.html' %}

{% block content %}
    <h2>Tambah Siswa Baru</h2>
    
    <form method="POST">
        <div class="form-group">
            <label for="nama">Nama:</label>
            <input type="text" id="nama" name="nama" required minlength="2" maxlength="50">
        </div>
        
        <div class="form-group">
            <label for="umur">Umur:</label>
            <input type="number" id="umur" name="umur" required min="10" max="18">
        </div>
        
        <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>
        </div>
        
        <div class="form-group">
            <label for="kelas">Kelas:</label>
            <input type="text" id="kelas" name="kelas" required minlength="2" maxlength="10">
        </div>
        
        <button type="submit" class="btn">Simpan</button>
        <a href="{{ url_for('index') }}" class="btn">Batal</a>
    </form>
{% endblock %}
```

## Langkah 4: Menjalankan Aplikasi

1. Jalankan skrip SQL untuk membuat database dan tabel
2. Jalankan aplikasi Flask dengan perintah:
   ```
   python app.py
   ```
3. Buka browser dan akses `http://localhost:5000`

## Penjelasan Praktikum

### 1. Validasi Data
Praktikum ini menerapkan validasi data di tiga level:
- **Client-side**: Menggunakan atribut HTML5 (`required`, `minlength`, `type="email"`, dll)
- **Server-side**: Fungsi validasi Python untuk nama, umur, dan email
- **Database**: Constraints MySQL (`NOT NULL`, `UNIQUE`, `CHECK`)

### 2. Error Handling
Aplikasi menangani berbagai jenis error:
- Error validasi input
- Error duplikasi (email sudah terdaftar)
- Error constraint database (umur di luar range)
- Error koneksi database

### 3. User Feedback
Aplikasi memberikan feedback yang jelas kepada pengguna:
- Pesan sukses (hijau)
- Pesan error (merah)
- Pesan spesifik untuk setiap jenis error

## Tantangan Tambahan (Jika Waktu Masih Tersisa)
1. Tambahkan fitur edit data siswa
2. Implementasikan fitur hapus data
3. Tambahkan validasi untuk format kelas (misal: harus dalam format [Angka][Huruf], seperti 7A, 8B)

## Kesimpulan
Praktikum ini telah mendemonstrasikan konsep penting dalam integrasi data dan validasi:
1. Pentingnya validasi multi-level
2. Penggunaan constraints database untuk integritas data
3. Error handling yang komprehensif
4. User feedback yang informatif

Dengan menyelesaikan praktikum ini, Anda telah memahami 80% dari materi Pertemuan 3 dan mengaplikasikan konsep-konsep dari Pertemuan 1 dan 2.