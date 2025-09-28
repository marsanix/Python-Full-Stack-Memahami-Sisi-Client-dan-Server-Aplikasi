-- =====================================================
-- DATABASE SETUP UNTUK PRAKTIK PERTEMUAN 1
-- =====================================================
-- File: database_setup.sql
-- Tujuan: Setup database dan tabel untuk aplikasi CRUD siswa
-- Target: Siswa SMP yang belajar Python Full-Stack

-- 1. MEMBUAT DATABASE
-- Hapus database jika sudah ada (hati-hati!)
DROP DATABASE IF EXISTS python_fullstack_smp;

-- Buat database baru
CREATE DATABASE python_fullstack_smp 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- Gunakan database yang baru dibuat
USE python_fullstack_smp;

-- 2. MEMBUAT TABEL SISWA
-- Tabel ini akan menyimpan data siswa
CREATE TABLE siswa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    kelas VARCHAR(20) NOT NULL,
    umur INT NOT NULL,
    alamat TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 3. MENAMBAHKAN DATA CONTOH (SAMPLE DATA)
-- Data ini untuk testing dan demonstrasi
INSERT INTO siswa (nama, kelas, umur, alamat) VALUES
('Ahmad Rizki', '7A', 13, 'Jl. Merdeka No. 123, Jakarta'),
('Siti Nurhaliza', '7B', 12, 'Jl. Sudirman No. 456, Bandung'),
('Budi Santoso', '8A', 14, 'Jl. Gatot Subroto No. 789, Surabaya'),
('Dewi Sartika', '8B', 13, 'Jl. Diponegoro No. 321, Yogyakarta'),
('Eko Prasetyo', '9A', 15, 'Jl. Ahmad Yani No. 654, Medan'),
('Fitri Handayani', '9B', 14, 'Jl. Pahlawan No. 987, Makassar'),
('Galih Pratama', '7A', 12, 'Jl. Veteran No. 147, Semarang'),
('Hani Rahmawati', '7B', 13, 'Jl. Kartini No. 258, Palembang'),
('Indra Gunawan', '8A', 14, 'Jl. Cut Nyak Dien No. 369, Denpasar'),
('Joko Widodo', '8B', 13, 'Jl. RA Kartini No. 741, Solo');

-- 4. MEMBUAT INDEX UNTUK PERFORMA YANG LEBIH BAIK
-- Index untuk pencarian berdasarkan nama
CREATE INDEX idx_nama ON siswa(nama);

-- Index untuk pencarian berdasarkan kelas
CREATE INDEX idx_kelas ON siswa(kelas);

-- 5. MENAMPILKAN STRUKTUR TABEL
-- Perintah untuk melihat struktur tabel yang telah dibuat
DESCRIBE siswa;

-- 6. MENAMPILKAN DATA YANG TELAH DIMASUKKAN
-- Perintah untuk melihat semua data siswa
SELECT * FROM siswa ORDER BY id;

-- =====================================================
-- PETUNJUK PENGGUNAAN:
-- =====================================================
-- 1. Buka MySQL Command Line atau phpMyAdmin
-- 2. Login dengan username dan password MySQL Anda
-- 3. Copy dan paste script ini, lalu jalankan
-- 4. Pastikan database dan tabel berhasil dibuat
-- 5. Sesuaikan konfigurasi di file Python (DB_CONFIG)
-- 
-- CATATAN PENTING:
-- - Pastikan MySQL server sudah berjalan
-- - Ganti username dan password di file Python sesuai dengan MySQL Anda
-- - Database ini akan menghapus data lama jika sudah ada
-- =====================================================

-- 7. QUERY TAMBAHAN UNTUK TESTING
-- Query untuk menghitung jumlah siswa
SELECT COUNT(*) as total_siswa FROM siswa;

-- Query untuk melihat siswa berdasarkan kelas
SELECT kelas, COUNT(*) as jumlah_siswa 
FROM siswa 
GROUP BY kelas 
ORDER BY kelas;

-- Query untuk mencari siswa berdasarkan nama (contoh pencarian)
SELECT * FROM siswa 
WHERE nama LIKE '%Ahmad%' 
ORDER BY nama;

-- Query untuk melihat umur termuda dan tertua
SELECT 
    MIN(umur) as umur_termuda,
    MAX(umur) as umur_tertua,
    AVG(umur) as rata_rata_umur
FROM siswa;