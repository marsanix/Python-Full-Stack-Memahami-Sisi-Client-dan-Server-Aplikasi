# 🐳 Docker Setup untuk Praktik Pertemuan 1

Dokumentasi lengkap untuk menjalankan aplikasi CRUD Siswa menggunakan Docker dan Docker Compose.

## 📋 Prerequisites

Pastikan Anda sudah menginstall:
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) untuk Windows
- Docker Compose (sudah termasuk dalam Docker Desktop)

## 🏗️ Struktur Project

```
praktik_pertemuan_1/
├── app.py                  # Aplikasi Flask utama (Docker-ready)
├── config.py              # Konfigurasi database dan Flask
├── requirements.txt       # Dependencies Python
├── Dockerfile            # Docker image untuk Flask app
├── docker-compose.yml    # Orchestration untuk semua services
├── .dockerignore         # File yang diabaikan saat build
├── database_setup.sql    # Script inisialisasi database
├── templates/            # Template HTML
│   ├── index.html
│   ├── tambah.html
│   ├── edit.html
│   ├── cari.html
│   ├── hasil_cari.html
│   ├── konfirmasi_hapus.html
│   └── statistik.html
└── README-Docker.md      # Dokumentasi ini
```

## 🚀 Cara Menjalankan

### 1. Buka Terminal/PowerShell

Buka PowerShell sebagai Administrator dan navigasi ke direktori project:

```powershell
cd "C:\Users\infin\Documents\LMS.MARSANIX.COM\Python Full-Stack\Pertemuan_1\praktik_pertemuan_1"
```

### 2. Build dan Jalankan dengan Docker Compose

```powershell
# Build dan jalankan semua services
docker-compose up --build

# Atau jalankan di background
docker-compose up --build -d
```

### 3. Akses Aplikasi

Setelah semua container berjalan, Anda dapat mengakses:

- **Aplikasi Flask**: http://localhost:5000
- **phpMyAdmin**: http://localhost:8080
  - Server: `mysql`
  - Username: `root`
  - Password: `toor`

## 🔧 Services yang Berjalan

### 1. MySQL Database
- **Port**: 3306
- **Database**: `python_fullstack_smp`
- **Username**: `root`
- **Password**: `toor`
- **Volume**: Data persisten di `mysql_data`

### 2. Flask Application
- **Port**: 5000
- **Environment**: Production
- **Features**: 
  - Auto-restart saat code berubah
  - Health check endpoint
  - Retry mechanism untuk koneksi database

### 3. phpMyAdmin (Optional)
- **Port**: 8080
- **Purpose**: Manajemen database via web interface

## 📱 Fitur Aplikasi

1. **Halaman Utama** (`/`)
   - Daftar semua siswa
   - Filter berdasarkan nama
   - Statistik singkat

2. **Tambah Siswa** (`/tambah`)
   - Form untuk menambah siswa baru

3. **Edit Siswa** (`/edit/<id>`)
   - Form untuk mengubah data siswa

4. **Hapus Siswa** (`/hapus/<id>`)
   - Konfirmasi sebelum menghapus

5. **Cari Siswa** (`/cari`)
   - Pencarian berdasarkan nama atau kelas

6. **Statistik** (`/statistik`)
   - Statistik lengkap siswa

7. **Health Check** (`/health`)
   - Endpoint untuk monitoring

## 🛠️ Commands Berguna

### Melihat Status Container
```powershell
docker-compose ps
```

### Melihat Logs
```powershell
# Semua services
docker-compose logs

# Service tertentu
docker-compose logs flask_app
docker-compose logs mysql
```

### Menghentikan Services
```powershell
# Stop semua services
docker-compose down

# Stop dan hapus volumes (HATI-HATI: akan menghapus data database)
docker-compose down -v
```

### Restart Service Tertentu
```powershell
# Restart Flask app saja
docker-compose restart flask_app
```

### Masuk ke Container
```powershell
# Masuk ke container Flask
docker-compose exec flask_app bash

# Masuk ke container MySQL
docker-compose exec mysql mysql -u root -ptoor python_fullstack_smp
```

## 🔍 Troubleshooting

### 1. Port Sudah Digunakan
Jika port 5000 atau 3306 sudah digunakan:

```powershell
# Cek port yang digunakan
netstat -ano | findstr :5000
netstat -ano | findstr :3306

# Ubah port di docker-compose.yml jika perlu
```

### 2. Database Connection Error
```powershell
# Cek status MySQL container
docker-compose logs mysql

# Restart MySQL service
docker-compose restart mysql
```

### 3. Build Error
```powershell
# Clean build
docker-compose down
docker-compose build --no-cache
docker-compose up
```

### 4. Permission Error (Windows)
Pastikan Docker Desktop berjalan sebagai Administrator.

## 🔄 Development Mode

Untuk development dengan hot reload:

1. Ubah `FLASK_ENV=development` di `docker-compose.yml`
2. Restart container:
   ```powershell
   docker-compose restart flask_app
   ```

## 📊 Monitoring

### Health Checks
- Flask app: http://localhost:5000/health
- MySQL: Otomatis via Docker health check

### Debug Info
- Debug endpoint: http://localhost:5000/debug

## 🗃️ Data Persistence

- Database data disimpan di Docker volume `mysql_data`
- Data akan tetap ada meskipun container di-restart
- Untuk reset data: `docker-compose down -v`

## 🔒 Security Notes

- Password database hanya untuk development
- Untuk production, gunakan environment variables yang aman
- Jangan commit file `.env` dengan credentials asli

## 📝 Logs Location

Logs dapat dilihat dengan:
```powershell
docker-compose logs -f flask_app
```

## 🎯 Next Steps

1. Akses http://localhost:5000 untuk mulai menggunakan aplikasi
2. Tambah beberapa data siswa untuk testing
3. Coba fitur filter dan pencarian
4. Lihat statistik di http://localhost:5000/statistik

---

**Happy Coding! 🚀**

Jika ada masalah, cek logs dengan `docker-compose logs` atau buka issue di repository.