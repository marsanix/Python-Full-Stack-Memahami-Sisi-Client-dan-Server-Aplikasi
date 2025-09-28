# 📚 Praktik Pertemuan 1 - Python Full-Stack untuk SMP

## 🎯 Deskripsi Proyek

Aplikasi web sederhana untuk manajemen data siswa yang dibuat menggunakan Flask (Python) sebagai backend dan HTML/CSS/JavaScript sebagai frontend. Proyek ini dirancang khusus untuk siswa SMP sebagai pengenalan konsep **client-server architecture** dan pengembangan web full-stack.

## 🌟 Fitur Utama

### ✨ CRUD Operations (Create, Read, Update, Delete)
- **Create**: Menambah data siswa baru
- **Read**: Menampilkan daftar siswa
- **Update**: Mengedit data siswa yang sudah ada
- **Delete**: Menghapus data siswa

### 🔍 Fitur Pencarian
- Pencarian berdasarkan nama siswa
- Filter berdasarkan kelas
- Pencarian berdasarkan rentang umur
- Pencarian berdasarkan alamat
- Pencarian lanjutan dengan multiple criteria

### 📊 Statistik dan Analisis
- Dashboard statistik siswa
- Grafik distribusi per kelas
- Grafik distribusi umur
- Analisis tren pendaftaran
- Export data dalam format CSV, Excel, dan PDF

### 🎨 User Interface
- Desain responsif (mobile-friendly)
- Interface yang user-friendly
- Animasi dan transisi yang smooth
- Dark mode support (opsional)

## 📁 Struktur Proyek

```
praktik_pertemuan_1/
├── Praktik_Pertemuan_1.py          # File utama aplikasi Flask
├── database_setup.sql              # Script setup database MySQL
├── README.md                       # Dokumentasi proyek (file ini)
└── templates/                      # Folder template HTML
    ├── index.html                  # Halaman utama (daftar siswa)
    ├── tambah.html                 # Form tambah siswa
    ├── edit.html                   # Form edit siswa
    ├── konfirmasi_hapus.html       # Konfirmasi penghapusan
    ├── cari.html                   # Form pencarian
    ├── hasil_cari.html             # Hasil pencarian
    └── statistik.html              # Dashboard statistik
```

## 🛠️ Teknologi yang Digunakan

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **MySQL** - Database
- **PyMySQL** - MySQL connector untuk Python

### Frontend
- **HTML5** - Struktur halaman
- **CSS3** - Styling dan layout
- **JavaScript** - Interaktivitas
- **Chart.js** - Grafik dan visualisasi data

### Tools & Libraries
- **Bootstrap** (opsional) - CSS framework
- **Font Awesome** - Icons
- **Google Fonts** - Typography

## 📋 Prerequisites

Sebelum menjalankan aplikasi, pastikan Anda telah menginstall:

1. **Python 3.8 atau lebih baru**
   ```bash
   python --version
   ```

2. **MySQL Server**
   - Download dari [MySQL Official Website](https://dev.mysql.com/downloads/)
   - Atau gunakan XAMPP/WAMP yang sudah include MySQL

3. **pip** (Python package manager)
   ```bash
   pip --version
   ```

## 🚀 Instalasi dan Setup

### 1. Clone atau Download Proyek
```bash
# Jika menggunakan Git
git clone <repository-url>

# Atau download dan extract file ZIP
```

### 2. Install Dependencies
```bash
# Masuk ke folder proyek
cd praktik_pertemuan_1

# Install Flask dan PyMySQL
pip install flask pymysql

# Atau install semua dependencies sekaligus
pip install -r requirements.txt
```

### 3. Setup Database

#### A. Buat Database
1. Buka MySQL Command Line atau phpMyAdmin
2. Jalankan perintah berikut:
```sql
CREATE DATABASE python_fullstack_smp;
USE python_fullstack_smp;
```

#### B. Import Database Schema
```bash
# Melalui MySQL Command Line
mysql -u root -p python_fullstack_smp < database_setup.sql

# Atau copy-paste isi file database_setup.sql ke phpMyAdmin
```

### 4. Konfigurasi Database Connection

Edit file `Praktik_Pertemuan_1.py` pada bagian konfigurasi database:

```python
# Konfigurasi Database
DB_CONFIG = {
    'host': 'localhost',        # Sesuaikan dengan host MySQL Anda
    'user': 'root',            # Username MySQL
    'password': '',            # Password MySQL (kosong jika default)
    'database': 'python_fullstack_smp',
    'charset': 'utf8mb4'
}
```

## ▶️ Cara Menjalankan Aplikasi

### 1. Jalankan Server Flask
```bash
# Masuk ke folder proyek
cd praktik_pertemuan_1

# Jalankan aplikasi
python Praktik_Pertemuan_1.py
```

### 2. Akses Aplikasi
Buka browser dan kunjungi:
```
http://localhost:5000
```

### 3. Testing Aplikasi
- Aplikasi akan otomatis membuat beberapa data contoh siswa
- Anda dapat langsung mencoba semua fitur yang tersedia

## 📖 Panduan Penggunaan

### 🏠 Halaman Utama (Dashboard)
- Menampilkan daftar semua siswa
- Statistik ringkas (total siswa, jumlah kelas, rata-rata umur)
- Tombol aksi untuk tambah, edit, dan hapus siswa
- Link ke halaman pencarian dan statistik

### ➕ Menambah Siswa Baru
1. Klik tombol "Tambah Siswa Baru"
2. Isi form dengan data siswa:
   - Nama lengkap
   - Kelas (pilih dari dropdown)
   - Umur (12-18 tahun)
   - Alamat lengkap
3. Klik "Simpan Data"

### ✏️ Mengedit Data Siswa
1. Klik tombol "Edit" pada siswa yang ingin diubah
2. Ubah data yang diperlukan
3. Klik "Simpan Perubahan"

### 🗑️ Menghapus Data Siswa
1. Klik tombol "Hapus" pada siswa yang ingin dihapus
2. Konfirmasi penghapusan
3. Data akan terhapus permanen

### 🔍 Mencari Siswa
1. Klik menu "Cari Siswa"
2. Pilih jenis pencarian:
   - **Pencarian Dasar**: Berdasarkan nama atau kata kunci
   - **Pencarian Lanjutan**: Multiple criteria
   - **Filter & Sorting**: Dengan pengurutan hasil
3. Masukkan kriteria pencarian
4. Klik "Cari"

### 📊 Melihat Statistik
1. Klik menu "Statistik"
2. Lihat berbagai grafik dan analisis:
   - Distribusi siswa per kelas
   - Distribusi umur
   - Tren pendaftaran bulanan
   - Insight dan rekomendasi

## 🔧 Troubleshooting

### ❌ Error: "No module named 'flask'"
**Solusi:**
```bash
pip install flask
```

### ❌ Error: "Can't connect to MySQL server"
**Solusi:**
1. Pastikan MySQL server berjalan
2. Periksa konfigurasi database di `Praktik_Pertemuan_1.py`
3. Pastikan username dan password benar

### ❌ Error: "Table 'siswa' doesn't exist"
**Solusi:**
1. Pastikan database sudah dibuat
2. Import file `database_setup.sql`
3. Restart aplikasi Flask

### ❌ Error: "Port 5000 already in use"
**Solusi:**
```python
# Ubah port di file Praktik_Pertemuan_1.py
if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Ganti ke port lain
```

### ❌ Template tidak ditemukan
**Solusi:**
1. Pastikan folder `templates` ada di direktori yang sama dengan `Praktik_Pertemuan_1.py`
2. Pastikan semua file HTML ada di folder `templates`

## 🎓 Konsep Pembelajaran

### 1. Client-Server Architecture
- **Client**: Browser web (frontend)
- **Server**: Aplikasi Flask (backend)
- **Database**: MySQL (penyimpanan data)

### 2. HTTP Methods
- **GET**: Mengambil data (menampilkan halaman)
- **POST**: Mengirim data (submit form)

### 3. MVC Pattern (Model-View-Controller)
- **Model**: Fungsi database (CRUD operations)
- **View**: Template HTML
- **Controller**: Route handlers di Flask

### 4. Frontend Technologies
- **HTML**: Struktur halaman web
- **CSS**: Styling dan layout
- **JavaScript**: Interaktivitas dan validasi

### 5. Backend Technologies
- **Python**: Bahasa pemrograman
- **Flask**: Web framework
- **MySQL**: Database relational

## 📝 Tugas dan Latihan

### 🔰 Level Pemula
1. Tambahkan 5 data siswa baru
2. Coba edit data siswa yang sudah ada
3. Lakukan pencarian berdasarkan nama
4. Lihat statistik siswa

### 🔥 Level Menengah
1. Tambahkan field baru (misal: nomor telepon, email)
2. Buat validasi form yang lebih ketat
3. Tambahkan fitur export data
4. Implementasikan pagination

### 🚀 Level Lanjutan
1. Tambahkan sistem login/authentication
2. Implementasikan role-based access
3. Tambahkan fitur upload foto siswa
4. Buat API REST untuk mobile app

## 🤝 Kontribusi

Jika Anda ingin berkontribusi pada proyek ini:

1. Fork repository
2. Buat branch baru (`git checkout -b feature/AmazingFeature`)
3. Commit perubahan (`git commit -m 'Add some AmazingFeature'`)
4. Push ke branch (`git push origin feature/AmazingFeature`)
5. Buat Pull Request

## 📞 Support

Jika Anda mengalami kesulitan atau memiliki pertanyaan:

1. **Email**: support@marsanix.com
2. **Discord**: [Join our Discord](https://discord.gg/marsanix)
3. **Forum**: [LMS Marsanix Forum](https://lms.marsanix.com/forum)

## 📄 Lisensi

Proyek ini dibuat untuk tujuan edukasi dan dapat digunakan secara bebas untuk pembelajaran.

## 🙏 Acknowledgments

- **Flask Documentation**: https://flask.palletsprojects.com/
- **MySQL Documentation**: https://dev.mysql.com/doc/
- **Chart.js**: https://www.chartjs.org/
- **Bootstrap**: https://getbootstrap.com/

## 📚 Referensi Tambahan

### Dokumentasi Resmi
- [Python Official Documentation](https://docs.python.org/3/)
- [Flask Quickstart](https://flask.palletsprojects.com/en/2.0.x/quickstart/)
- [MySQL Tutorial](https://dev.mysql.com/doc/mysql-tutorial-excerpt/8.0/en/)

### Tutorial Video
- [Python Flask Tutorial - YouTube](https://www.youtube.com/results?search_query=python+flask+tutorial)
- [MySQL Basics - YouTube](https://www.youtube.com/results?search_query=mysql+basics+tutorial)

### Buku Referensi
- "Flask Web Development" by Miguel Grinberg
- "Learning MySQL" by Seyed M.M. Tahaghoghi

---

**Happy Coding! 🚀**

*Dibuat dengan ❤️ untuk siswa SMP yang ingin belajar web development*