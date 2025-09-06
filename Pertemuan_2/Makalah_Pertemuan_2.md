# Pertemuan 2: Membangun Ulang dari Nol dengan MySQL

**Durasi**: 2 jam  
**Tujuan**: Membangun aplikasi CRUD dengan database MySQL dari awal dengan pemahaman yang lebih baik

---

## Tujuan Pembelajaran

Setelah mengikuti pertemuan ini, siswa diharapkan dapat:
1. Membuat aplikasi CRUD dengan database MySQL dari nol
2. Memahami hubungan antara Flask, MySQL, dan HTML templates
3. Menjelaskan alur data dari form HTML ke database MySQL
4. Menggunakan parameterized queries untuk keamanan SQL injection
5. Mengimplementasikan fitur CRUD dengan database yang persistent

## Filosofi Pertemuan Ini

### "Belajar dengan Membangun Database-Driven App"

Di pertemuan sebelumnya, kita sudah "membongkar" aplikasi CRUD dengan file JSON. Sekarang saatnya membangun dari nol dengan database MySQL yang lebih robust.

**Analogi**: Seperti upgrade dari buku catatan ke sistem perpustakaan digital
- Pertemuan 1: Kita "membongkar" sistem sederhana dengan file
- Pertemuan 2: Kita bangun sistem modern dengan database

### Prinsip "Database-First tapi User-Friendly"

Kita akan membuat aplikasi yang:
- ✅ Menggunakan database MySQL untuk penyimpanan persistent
- ✅ Aman dari SQL injection dengan parameterized queries
- ✅ Memiliki error handling yang robust untuk database operations
- ✅ Mudah dipahami struktur dan alur datanya
- ❌ Tidak menggunakan ORM yang kompleks (raw SQL dulu)

---

## Materi Pembelajaran

### A. Review Singkat Alur Pertemuan Sebelumnya (15 menit)

#### Konsep Kunci yang Sudah Dipelajari:
1. **Flask** = Framework web Python
2. **Route** = Alamat URL dalam aplikasi
3. **Template** = File HTML yang bisa diisi data
4. **GET vs POST** = Cara browser berkomunikasi dengan server
5. **CRUD** = Create, Read, Update, Delete

#### Pertanyaan Refleksi:
- "Apa yang paling mudah dipahami dari pertemuan lalu?"
- "Bagian mana yang masih membingungkan?"
- "Konsep apa yang ingin dipraktikkan lagi?"

### B. Persiapan Coding Session (15 menit)

#### 1. Setup Environment
```bash
# Buat folder baru untuk proyek
mkdir aplikasi_perpustakaan_mysql
cd aplikasi_perpustakaan_mysql

# Buat struktur folder
mkdir templates
mkdir static

# Install dependencies
pip install flask mysql-connector-python
```

#### 2. Rencana Aplikasi
**Tema**: Perpustakaan Mini  
**Fitur yang akan dibuat**:
- ✅ Lihat daftar buku (READ)
- ✅ Tambah buku baru (CREATE)
- ✅ Edit informasi buku (UPDATE)
- ✅ Hapus buku (DELETE)

**Data yang disimpan**:
- ID buku
- Judul buku
- Pengarang
- Tahun terbit
- Status (tersedia/dipinjam)

#### 3. Strategi Coding
**Langkah demi Langkah**:
1. Setup database MySQL dan buat tabel
2. Buat app.py dengan koneksi database
3. Implementasi fungsi helper untuk database operations
4. Implementasi READ (SELECT dari database)
5. Implementasi CREATE (INSERT ke database)
6. Implementasi UPDATE (UPDATE database)
7. Implementasi DELETE (DELETE dari database)

### C. Coding Session: Membangun Aplikasi Client-Server (90 menit)

#### Langkah 1: Membuat Kerangka Aplikasi Client-Server (15 menit)

**File: app.py**
```python
# Import yang diperlukan
from flask import Flask, render_template, request, redirect, flash
import mysql.connector
from mysql.connector import Error

# Buat aplikasi Flask
app = Flask(__name__)
app.secret_key = 'rahasia_perpustakaan'  # Untuk flash message

# Konfigurasi database
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Sesuaikan dengan password MySQL Anda
    'database': 'perpustakaan_db'
}

# Fungsi untuk koneksi database
def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Database error: {e}")
        return None

# Route pertama - halaman utama
@app.route('/')
def halaman_utama():
    return "<h1>Perpustakaan Mini - MySQL Version</h1><p>Aplikasi sedang dalam pengembangan...</p>"

# Jalankan aplikasi
if __name__ == '__main__':
    app.run(debug=True)
```

**Test**: Jalankan dan pastikan bisa diakses di `http://localhost:5000`

#### Langkah 2: Setup Database dan Tabel (15 menit)

**Buat database dan tabel di MySQL:**
```sql
-- Buat database
CREATE DATABASE perpustakaan_db;
USE perpustakaan_db;

-- Buat tabel buku
CREATE TABLE buku (
    id INT AUTO_INCREMENT PRIMARY KEY,
    judul VARCHAR(255) NOT NULL,
    pengarang VARCHAR(255) NOT NULL,
    tahun INT NOT NULL,
    status ENUM('tersedia', 'dipinjam') DEFAULT 'tersedia',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert data dummy
INSERT INTO buku (judul, pengarang, tahun, status) VALUES
('Laskar Pelangi', 'Andrea Hirata', 2005, 'tersedia'),
('Dilan 1990', 'Pidi Baiq', 2014, 'dipinjam');
```

**Diskusi**: 
- Kenapa pakai AUTO_INCREMENT untuk ID?
- Apa kegunaan ENUM untuk status?
- Kenapa perlu TIMESTAMP untuk created_at?

#### Langkah 3: Implementasi READ - Menampilkan Data (20 menit)

**Update app.py dengan fungsi database helper:**
```python
# Fungsi helper untuk eksekusi query
def execute_query(query, params=None, fetch=False):
    connection = get_db_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchall()
        else:
            connection.commit()
            result = True
            
        return result
    except Error as e:
        print(f"Query error: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()

@app.route('/')
def halaman_utama():
    query = "SELECT * FROM buku ORDER BY id DESC"
    daftar_buku = execute_query(query, fetch=True)
    
    if daftar_buku is None:
        daftar_buku = []
        flash('Error mengambil data dari database!', 'error')
    
    return render_template('index.html', daftar_buku=daftar_buku)
```

**Buat templates/index.html**:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Perpustakaan Mini</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { border-collapse: collapse; width: 100%; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #f2f2f2; }
        .btn { padding: 5px 10px; margin: 2px; text-decoration: none; }
        .btn-primary { background-color: #007bff; color: white; }
        .btn-warning { background-color: #ffc107; color: black; }
        .btn-danger { background-color: #dc3545; color: white; }
    </style>
</head>
<body>
    <h1>📚 Perpustakaan Mini</h1>
    
    <a href="/tambah" class="btn btn-primary">➕ Tambah Buku</a>
    
    <h2>Daftar Buku</h2>
    
    {% if daftar_buku %}
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Judul</th>
                <th>Pengarang</th>
                <th>Tahun</th>
                <th>Status</th>
                <th>Aksi</th>
            </tr>
        </thead>
        <tbody>
            {% for buku in daftar_buku %}
            <tr>
                <td>{{ buku.id }}</td>
                <td>{{ buku.judul }}</td>
                <td>{{ buku.pengarang }}</td>
                <td>{{ buku.tahun }}</td>
                <td>
                    {% if buku.status == 'tersedia' %}
                        <span style="color: green;">✅ Tersedia</span>
                    {% else %}
                        <span style="color: red;">❌ Dipinjam</span>
                    {% endif %}
                </td>
                <td>
                    <a href="/edit/{{ buku.id }}" class="btn btn-warning">✏️ Edit</a>
                    <a href="/hapus/{{ buku.id }}" class="btn btn-danger">🗑️ Hapus</a>
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
    {% else %}
    <p>Belum ada buku di perpustakaan. <a href="/tambah">Tambah buku pertama</a>!</p>
    {% endif %}
</body>
</html>
```

**Diskusi**:
- Bagaimana data dari MySQL sampai ke HTML?
- Apa fungsi `execute_query()` dan kenapa perlu error handling?
- Kenapa pakai `cursor(dictionary=True)` untuk hasil query?
- Apa bedanya `fetch=True` dan `fetch=False`?

#### Langkah 4: Implementasi CREATE - Tambah Data (25 menit)

**Tambah route di app.py**:
```python
@app.route('/tambah', methods=['GET', 'POST'])
def tambah_buku():
    if request.method == 'POST':
        # Ambil data dari form
        judul = request.form.get('judul', '').strip()
        pengarang = request.form.get('pengarang', '').strip()
        tahun = request.form.get('tahun', '').strip()
        status = request.form.get('status', 'tersedia')
        
        # Validasi input
        if not all([judul, pengarang, tahun]):
            flash('Semua field harus diisi!', 'error')
            return render_template('tambah.html')
        
        try:
            tahun = int(tahun)
        except ValueError:
            flash('Tahun harus berupa angka!', 'error')
            return render_template('tambah.html')
        
        # Insert ke database dengan parameterized query
        query = """
        INSERT INTO buku (judul, pengarang, tahun, status) 
        VALUES (%s, %s, %s, %s)
        """
        result = execute_query(query, (judul, pengarang, tahun, status))
        
        if result:
            flash(f'Buku "{judul}" berhasil ditambahkan!', 'success')
            return redirect('/')
        else:
            flash('Error menyimpan data ke database!', 'error')
    
    # Jika GET, tampilkan form
    return render_template('tambah.html')
```

**Buat templates/tambah.html**:
```html
<!DOCTYPE html>
<html>
<head>
    <title>Tambah Buku - Perpustakaan Mini</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; font-weight: bold; }
        input, select { width: 300px; padding: 8px; border: 1px solid #ddd; }
        button { padding: 10px 20px; background-color: #007bff; color: white; border: none; cursor: pointer; }
        .btn-secondary { background-color: #6c757d; }
        .alert { padding: 10px; margin: 10px 0; border-radius: 4px; }
        .alert-error { background-color: #f8d7da; color: #721c24; }
    </style>
</head>
<body>
    <h1>📚 Tambah Buku Baru</h1>
    
    <!-- Flash Messages -->
    {% with messages = get_flashed_messages(with_categories=true) %}
        {% if messages %}
            {% for category, message in messages %}
                <div class="alert alert-{{ category }}">{{ message }}</div>
            {% endfor %}
        {% endif %}
    {% endwith %}
    
    <form method="POST">
        <div class="form-group">
            <label for="judul">Judul Buku:</label>
            <input type="text" id="judul" name="judul" required>
        </div>
        
        <div class="form-group">
            <label for="pengarang">Pengarang:</label>
            <input type="text" id="pengarang" name="pengarang" required>
        </div>
        
        <div class="form-group">
            <label for="tahun">Tahun Terbit:</label>
            <input type="number" id="tahun" name="tahun" min="1000" max="2024" required>
        </div>
        
        <div class="form-group">
            <label for="status">Status:</label>
            <select id="status" name="status" required>
                <option value="tersedia">Tersedia</option>
                <option value="dipinjam">Dipinjam</option>
            </select>
        </div>
        
        <button type="submit">💾 Simpan Buku</button>
        <a href="/" class="btn-secondary" style="padding: 10px 20px; text-decoration: none; color: white;">🔙 Kembali</a>
    </form>
</body>
</html>
```

**Diskusi**:
- Kenapa perlu validasi input sebelum insert ke database?
- Bagaimana cara kerja parameterized query `(%s, %s, %s, %s)`?
- Apa bahayanya jika tidak pakai parameterized query?
- Apa fungsi `execute_query()` dalam mencegah SQL injection?

#### Langkah 5: Implementasi UPDATE - Edit Data (20 menit)

**Tambah route di app.py**:
```python
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_buku(id):
    # Ambil data buku saat ini dari database
    query_select = "SELECT * FROM buku WHERE id = %s"
    result = execute_query(query_select, (id,), fetch=True)
    
    if not result:
        flash('Buku tidak ditemukan!', 'error')
        return redirect('/')
    
    buku = result[0]
    
    if request.method == 'POST':
        # Validasi input
        judul = request.form.get('judul', '').strip()
        pengarang = request.form.get('pengarang', '').strip()
        tahun = request.form.get('tahun', '').strip()
        status = request.form.get('status', 'tersedia')
        
        if not all([judul, pengarang, tahun]):
            flash('Semua field harus diisi!', 'error')
            return render_template('edit.html', buku=buku)
        
        try:
            tahun = int(tahun)
        except ValueError:
            flash('Tahun harus berupa angka!', 'error')
            return render_template('edit.html', buku=buku)
        
        # Update data dengan SQL UPDATE
        query_update = """
        UPDATE buku 
        SET judul = %s, pengarang = %s, tahun = %s, status = %s 
        WHERE id = %s
        """
        params = (judul, pengarang, tahun, status, id)
        
        if execute_query(query_update, params):
            flash(f'Buku "{judul}" berhasil diupdate!', 'success')
        else:
            flash('Error mengupdate data!', 'error')
        
        return redirect('/')
    
    # Jika GET, tampilkan form edit dengan data buku
    return render_template('edit.html', buku=buku)
```

**Buat templates/edit.html** (mirip tambah.html tapi dengan value yang sudah terisi)

#### Langkah 6: Implementasi DELETE - Hapus Data (10 menit)

**Tambah route di app.py**:
```python
@app.route('/hapus/<int:id>')
def hapus_buku(id):
    # Ambil judul buku untuk pesan konfirmasi
    query_select = "SELECT judul FROM buku WHERE id = %s"
    result = execute_query(query_select, (id,), fetch=True)
    
    if result:
        judul = result[0]['judul']
        
        # Hapus dari database
        query_delete = "DELETE FROM buku WHERE id = %s"
        if execute_query(query_delete, (id,)):
            flash(f'Buku "{judul}" berhasil dihapus!', 'success')
        else:
            flash('Error menghapus data!', 'error')
    else:
        flash('Buku tidak ditemukan!', 'error')
    
    return redirect('/')
```

### D. Pentingnya Template HTML (15 menit)

#### Hubungan Python dan HTML

**Analogi**: Python dan HTML seperti "Chef dan Pelayan"
- **Python (Chef)**: Menyiapkan data, memproses pesanan
- **HTML (Pelayan)**: Menyajikan data ke customer dengan cantik

#### Alur Data dari Python ke HTML

```python
# Di Python (app.py)
data = {'nama': 'Budi', 'umur': 15}
return render_template('profil.html', siswa=data)
```

```html
<!-- Di HTML (profil.html) -->
<h1>Profil Siswa</h1>
<p>Nama: {{ siswa.nama }}</p>
<p>Umur: {{ siswa.umur }}</p>
```

**Hasil di Browser**:
```
Profil Siswa
Nama: Budi
Umur: 15
```

#### Template Engine Jinja2

**Fitur Utama**:
1. **Variabel**: `{{ nama_variabel }}`
2. **Loop**: `{% for item in list %} ... {% endfor %}`
3. **Kondisi**: `{% if kondisi %} ... {% endif %}`
4. **Filter**: `{{ nama|upper }}` (mengubah ke huruf besar)

**Contoh Praktis**:
```html
<!-- Loop dengan kondisi -->
{% for buku in daftar_buku %}
    {% if buku.status == 'tersedia' %}
        <p style="color: green;">{{ buku.judul }} - Tersedia</p>
    {% else %}
        <p style="color: red;">{{ buku.judul }} - Dipinjam</p>
    {% endif %}
{% endfor %}
```

---

## Troubleshooting dan Debugging

### Error Umum dan Solusinya

#### 1. "TemplateNotFound"
**Penyebab**: File HTML tidak ditemukan  
**Solusi**: 
- Pastikan file ada di folder `templates/`
- Cek nama file (case-sensitive)
- Pastikan ekstensi `.html`

#### 2. "KeyError: 'nama_field'"
**Penyebab**: Field form tidak ditemukan  
**Solusi**:
- Cek nama field di HTML: `<input name="nama_field">`
- Pastikan form menggunakan method POST
- Cek spelling nama field

#### 3. "Method Not Allowed"
**Penyebab**: Route tidak menerima method yang dikirim  
**Solusi**:
- Tambahkan `methods=['GET', 'POST']` di route
- Pastikan form menggunakan `method="POST"`

#### 4. Data Tidak Muncul di HTML
**Penyebab**: Data tidak dikirim ke template  
**Solusi**:
- Pastikan ada parameter di `render_template()`
- Cek nama variabel di HTML
- Gunakan `{{ variabel }}` bukan `{ variabel }`

### Tips Debugging

1. **Gunakan `print()` untuk debug**:
```python
print(f"Data yang diterima: {request.form}")
print(f"Jumlah buku: {len(buku_list)}")
```

2. **Cek terminal untuk error message**
3. **Gunakan browser developer tools (F12)**
4. **Test satu fitur dalam satu waktu**
5. **Simpan kode yang working sebelum menambah fitur baru**

---

## Rangkuman dan Refleksi

### Apa yang Sudah Dicapai

✅ **Membuat aplikasi client-server lengkap dengan MySQL**  
✅ **Memahami alur data dari client ke server ke database**  
✅ **Mengimplementasikan komunikasi HTTP request-response**  
✅ **Mengatasi error dalam arsitektur client-server**  
✅ **Memahami hubungan frontend-backend-database**  

### Konsep Penting yang Dipelajari

1. **Struktur Aplikasi Flask**:
   - `app.py` = Logic utama
   - `templates/` = File HTML
   - `static/` = CSS, JS, gambar

2. **Pattern CRUD**:
   - **CREATE**: Form → POST → Simpan → Redirect
   - **READ**: GET → Ambil data → Tampilkan
   - **UPDATE**: Form dengan data lama → POST → Update → Redirect
   - **DELETE**: Link → GET → Hapus → Redirect

3. **Template Engine**:
   - `{{ variabel }}` = Tampilkan data
   - `{% for %}` = Loop data
   - `{% if %}` = Kondisi

### Perbedaan dengan Pertemuan 1

| Pertemuan 1 | Pertemuan 2 |
|-------------|-------------|
| Memahami arsitektur client-server | Membangun aplikasi client-server |
| Fokus konsep komunikasi HTTP | Fokus implementasi dengan MySQL |
| Menganalisis alur request-response | Mempraktikkan integrasi database |
| Teori arsitektur | Praktik pengembangan |

### Pertanyaan Refleksi

1. **Bagian mana yang paling mudah?**
2. **Konsep apa yang masih membingungkan?**
3. **Error apa yang paling sering muncul?**
4. **Fitur apa yang ingin ditambahkan?**
5. **Apa perbedaan pemahaman sebelum dan sesudah coding session?**

---

## Persiapan Pertemuan Selanjutnya

### Preview Pertemuan 3: Integrasi Data & Validasi

Di pertemuan berikutnya, kita akan:
1. **Memperbaiki cara penyimpanan data** (dari list ke file/database)
2. **Menambahkan validasi yang lebih robust**
3. **Memahami alur data yang lebih kompleks**
4. **Menangani error dengan lebih baik**

### Tugas Rumah

1. **Eksperimen dengan aplikasi yang sudah dibuat**:
   - Tambahkan field baru (misal: kategori buku)
   - Ubah tampilan dengan CSS
   - Coba buat fitur pencarian sederhana

2. **Refleksi dan dokumentasi**:
   - Tulis catatan tentang error yang ditemui
   - Buat list pertanyaan untuk pertemuan berikutnya
   - Screenshot aplikasi yang sudah jadi

3. **Persiapan mental**:
   - Siap untuk belajar konsep yang lebih advanced
   - Bawa laptop dengan aplikasi yang sudah dibuat
   - Siapkan pertanyaan tentang hal yang masih bingung

### Bahan yang Perlu Disiapkan

- Laptop dengan Python dan Flask
- Aplikasi yang sudah dibuat di pertemuan ini
- Text editor favorit
- Browser untuk testing
- Catatan dari pertemuan 1 dan 2

---

**"Selamat! Kalian sudah berhasil membuat aplikasi web dari nol. Ini adalah pencapaian yang luar biasa untuk siswa SMP!"** 🎉