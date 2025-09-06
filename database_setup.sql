-- =====================================================
-- SETUP DATABASE MYSQL UNTUK PYTHON FULL-STACK SMP
-- =====================================================
-- File ini berisi schema database yang akan digunakan
-- di semua pertemuan (1-4) untuk latihan CRUD dengan MySQL

-- Buat database baru
CREATE DATABASE IF NOT EXISTS python_fullstack_smp;
USE python_fullstack_smp;

-- =====================================================
-- PERTEMUAN 1: MEMBONGKAR ULANG APLIKASI CRUD
-- =====================================================

-- Tabel siswa untuk latihan CRUD dasar
CREATE TABLE IF NOT EXISTS siswa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama VARCHAR(100) NOT NULL,
    kelas VARCHAR(10) NOT NULL,
    umur INT NOT NULL,
    alamat TEXT,
    tanggal_daftar TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('aktif', 'tidak_aktif') DEFAULT 'aktif'
);

-- Insert data sample untuk Pertemuan 1
INSERT INTO siswa (nama, kelas, umur, alamat) VALUES
('Ahmad Rizki', '8A', 14, 'Jl. Merdeka No. 123'),
('Siti Nurhaliza', '8B', 13, 'Jl. Sudirman No. 456'),
('Budi Santoso', '8A', 14, 'Jl. Gatot Subroto No. 789'),
('Dewi Sartika', '8C', 13, 'Jl. Diponegoro No. 321'),
('Eko Prasetyo', '8B', 14, 'Jl. Ahmad Yani No. 654');

-- =====================================================
-- PERTEMUAN 2: MEMBANGUN ULANG DARI NOL
-- =====================================================

-- Tabel buku untuk mini library app
CREATE TABLE IF NOT EXISTS buku (
    id INT AUTO_INCREMENT PRIMARY KEY,
    judul VARCHAR(200) NOT NULL,
    penulis VARCHAR(100) NOT NULL,
    kategori ENUM('fiksi', 'non-fiksi', 'sains', 'sejarah', 'biografi') NOT NULL,
    tahun_terbit YEAR NOT NULL,
    isbn VARCHAR(20) UNIQUE,
    jumlah_halaman INT,
    status ENUM('tersedia', 'dipinjam', 'rusak') DEFAULT 'tersedia',
    tanggal_tambah TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert data sample untuk Pertemuan 2
INSERT INTO buku (judul, penulis, kategori, tahun_terbit, isbn, jumlah_halaman) VALUES
('Laskar Pelangi', 'Andrea Hirata', 'fiksi', 2005, '978-979-22-2592-5', 529),
('Bumi Manusia', 'Pramoedya Ananta Toer', 'fiksi', 1980, '978-979-22-0000-1', 535),
('Sejarah Indonesia', 'Prof. Dr. Sartono', 'sejarah', 2010, '978-979-22-1111-2', 450),
('Fisika Dasar', 'Dr. Bambang', 'sains', 2018, '978-979-22-2222-3', 320),
('Steve Jobs', 'Walter Isaacson', 'biografi', 2011, '978-979-22-3333-4', 656);

-- =====================================================
-- PERTEMUAN 3: INTEGRASI DATA & VALIDASI
-- =====================================================

-- Tabel mahasiswa dengan validasi lebih kompleks
CREATE TABLE IF NOT EXISTS mahasiswa (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nim VARCHAR(20) UNIQUE NOT NULL,
    nama VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    jurusan VARCHAR(50) NOT NULL,
    semester INT CHECK (semester BETWEEN 1 AND 8),
    ipk DECIMAL(3,2) CHECK (ipk BETWEEN 0.00 AND 4.00),
    tanggal_lahir DATE NOT NULL,
    jenis_kelamin ENUM('L', 'P') NOT NULL,
    no_telepon VARCHAR(15),
    alamat TEXT,
    status ENUM('aktif', 'cuti', 'lulus', 'drop_out') DEFAULT 'aktif',
    tanggal_daftar TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tanggal_update TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Insert data sample untuk Pertemuan 3
INSERT INTO mahasiswa (nim, nama, email, jurusan, semester, ipk, tanggal_lahir, jenis_kelamin, no_telepon, alamat) VALUES
('2023001001', 'Andi Pratama', 'andi.pratama@email.com', 'Teknik Informatika', 2, 3.75, '2005-03-15', 'L', '081234567890', 'Jl. Teknologi No. 1'),
('2023001002', 'Bella Sari', 'bella.sari@email.com', 'Sistem Informasi', 2, 3.85, '2005-07-22', 'P', '081234567891', 'Jl. Informasi No. 2'),
('2023001003', 'Candra Wijaya', 'candra.wijaya@email.com', 'Teknik Komputer', 2, 3.60, '2005-01-10', 'L', '081234567892', 'Jl. Komputer No. 3');

-- =====================================================
-- PERTEMUAN 4: PROYEK MANDIRI & IMPROVISASI
-- =====================================================

-- Tabel untuk berbagai jenis proyek mandiri
-- Siswa bisa memilih salah satu atau membuat yang baru

-- 1. Tabel untuk Habit Tracker
CREATE TABLE IF NOT EXISTS habits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_habit VARCHAR(100) NOT NULL,
    deskripsi TEXT,
    target_harian INT DEFAULT 1,
    kategori ENUM('kesehatan', 'belajar', 'olahraga', 'produktivitas', 'lainnya') NOT NULL,
    tanggal_mulai DATE NOT NULL,
    status ENUM('aktif', 'selesai', 'berhenti') DEFAULT 'aktif',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS habit_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    habit_id INT,
    tanggal DATE NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    catatan TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE
);

-- 2. Tabel untuk Recipe Collection
CREATE TABLE IF NOT EXISTS resep (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_resep VARCHAR(150) NOT NULL,
    kategori ENUM('makanan_utama', 'cemilan', 'minuman', 'dessert') NOT NULL,
    tingkat_kesulitan ENUM('mudah', 'sedang', 'sulit') NOT NULL,
    waktu_memasak INT NOT NULL, -- dalam menit
    porsi INT NOT NULL,
    bahan TEXT NOT NULL,
    cara_membuat TEXT NOT NULL,
    tips TEXT,
    rating DECIMAL(2,1) CHECK (rating BETWEEN 1.0 AND 5.0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Tabel untuk Study Planner
CREATE TABLE IF NOT EXISTS mata_pelajaran (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nama_mapel VARCHAR(50) NOT NULL,
    guru VARCHAR(100),
    hari ENUM('senin', 'selasa', 'rabu', 'kamis', 'jumat', 'sabtu') NOT NULL,
    jam_mulai TIME NOT NULL,
    jam_selesai TIME NOT NULL,
    ruang VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS tugas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    mapel_id INT,
    judul_tugas VARCHAR(150) NOT NULL,
    deskripsi TEXT,
    tanggal_deadline DATE NOT NULL,
    prioritas ENUM('rendah', 'sedang', 'tinggi') DEFAULT 'sedang',
    status ENUM('belum_mulai', 'sedang_dikerjakan', 'selesai', 'terlambat') DEFAULT 'belum_mulai',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (mapel_id) REFERENCES mata_pelajaran(id) ON DELETE CASCADE
);

-- 4. Tabel untuk Personal Diary
CREATE TABLE IF NOT EXISTS diary_entries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tanggal DATE NOT NULL,
    judul VARCHAR(150),
    isi_diary TEXT NOT NULL,
    mood ENUM('sangat_senang', 'senang', 'biasa', 'sedih', 'sangat_sedih') NOT NULL,
    cuaca ENUM('cerah', 'berawan', 'hujan', 'mendung') DEFAULT 'cerah',
    aktivitas_utama VARCHAR(200),
    is_private BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- =====================================================
-- INSERT SAMPLE DATA UNTUK PERTEMUAN 4
-- =====================================================

-- Sample data untuk Habit Tracker
INSERT INTO habits (nama_habit, deskripsi, target_harian, kategori, tanggal_mulai) VALUES
('Baca Buku', 'Membaca buku minimal 30 menit setiap hari', 1, 'belajar', '2024-01-01'),
('Olahraga Pagi', 'Jogging atau senam pagi', 1, 'olahraga', '2024-01-01'),
('Minum Air', 'Minum air putih 8 gelas per hari', 8, 'kesehatan', '2024-01-01');

-- Sample data untuk Recipe Collection
INSERT INTO resep (nama_resep, kategori, tingkat_kesulitan, waktu_memasak, porsi, bahan, cara_membuat, rating) VALUES
('Nasi Goreng Sederhana', 'makanan_utama', 'mudah', 20, 2, 
 'Nasi putih 2 piring, Telur 2 butir, Bawang merah 3 siung, Bawang putih 2 siung, Kecap manis 2 sdm, Garam secukupnya, Minyak goreng', 
 '1. Tumis bawang merah dan putih\n2. Masukkan telur, orak-arik\n3. Masukkan nasi, aduk rata\n4. Tambahkan kecap dan garam\n5. Aduk hingga matang', 
 4.5),
('Es Teh Manis', 'minuman', 'mudah', 5, 1,
 'Teh celup 1 sachet, Air panas 200ml, Gula 2 sdm, Es batu secukupnya',
 '1. Seduh teh dengan air panas\n2. Tambahkan gula, aduk\n3. Biarkan dingin\n4. Tambahkan es batu',
 4.0);

-- Sample data untuk Study Planner
INSERT INTO mata_pelajaran (nama_mapel, guru, hari, jam_mulai, jam_selesai, ruang) VALUES
('Matematika', 'Bu Sari', 'senin', '07:00:00', '08:30:00', '8A'),
('Bahasa Indonesia', 'Pak Budi', 'senin', '08:30:00', '10:00:00', '8A'),
('IPA', 'Bu Dewi', 'selasa', '07:00:00', '08:30:00', 'Lab IPA');

INSERT INTO tugas (mapel_id, judul_tugas, deskripsi, tanggal_deadline, prioritas) VALUES
(1, 'PR Aljabar', 'Mengerjakan soal halaman 45-50', '2024-01-15', 'tinggi'),
(2, 'Esai Lingkungan', 'Menulis esai tentang pelestarian lingkungan 500 kata', '2024-01-20', 'sedang'),
(3, 'Laporan Praktikum', 'Laporan hasil praktikum fotosintesis', '2024-01-18', 'tinggi');

-- Sample data untuk Personal Diary
INSERT INTO diary_entries (tanggal, judul, isi_diary, mood, cuaca, aktivitas_utama) VALUES
('2024-01-01', 'Tahun Baru', 'Hari ini adalah awal tahun baru. Aku berharap tahun ini bisa lebih baik dari tahun lalu. Resolusiku adalah belajar programming dengan lebih serius!', 'senang', 'cerah', 'Merayakan tahun baru dengan keluarga'),
('2024-01-02', 'Hari Pertama Sekolah', 'Kembali ke sekolah setelah libur panjang. Bertemu teman-teman lagi rasanya menyenangkan. Dapat tugas baru dari Bu Sari.', 'biasa', 'berawan', 'Sekolah dan mengerjakan PR');

-- =====================================================
-- VIEWS UNTUK MEMUDAHKAN QUERY
-- =====================================================

-- View untuk statistik siswa per kelas (Pertemuan 1)
CREATE VIEW IF NOT EXISTS statistik_siswa_per_kelas AS
SELECT 
    kelas,
    COUNT(*) as jumlah_siswa,
    AVG(umur) as rata_rata_umur,
    COUNT(CASE WHEN status = 'aktif' THEN 1 END) as siswa_aktif
FROM siswa
GROUP BY kelas;

-- View untuk statistik buku per kategori (Pertemuan 2)
CREATE VIEW IF NOT EXISTS statistik_buku_per_kategori AS
SELECT 
    kategori,
    COUNT(*) as jumlah_buku,
    COUNT(CASE WHEN status = 'tersedia' THEN 1 END) as buku_tersedia,
    COUNT(CASE WHEN status = 'dipinjam' THEN 1 END) as buku_dipinjam
FROM buku
GROUP BY kategori;

-- View untuk statistik mahasiswa per jurusan (Pertemuan 3)
CREATE VIEW IF NOT EXISTS statistik_mahasiswa_per_jurusan AS
SELECT 
    jurusan,
    COUNT(*) as jumlah_mahasiswa,
    AVG(ipk) as rata_rata_ipk,
    COUNT(CASE WHEN status = 'aktif' THEN 1 END) as mahasiswa_aktif
FROM mahasiswa
GROUP BY jurusan;

-- =====================================================
-- STORED PROCEDURES UNTUK OPERASI UMUM
-- =====================================================

-- Procedure untuk menambah siswa baru (Pertemuan 1)
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS TambahSiswa(
    IN p_nama VARCHAR(100),
    IN p_kelas VARCHAR(10),
    IN p_umur INT,
    IN p_alamat TEXT
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    INSERT INTO siswa (nama, kelas, umur, alamat) 
    VALUES (p_nama, p_kelas, p_umur, p_alamat);
    
    COMMIT;
END //
DELIMITER ;

-- Procedure untuk update status buku (Pertemuan 2)
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS UpdateStatusBuku(
    IN p_id INT,
    IN p_status ENUM('tersedia', 'dipinjam', 'rusak')
)
BEGIN
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        RESIGNAL;
    END;
    
    START TRANSACTION;
    
    UPDATE buku 
    SET status = p_status 
    WHERE id = p_id;
    
    IF ROW_COUNT() = 0 THEN
        SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Buku tidak ditemukan';
    END IF;
    
    COMMIT;
END //
DELIMITER ;

-- =====================================================
-- INDEXES UNTUK PERFORMA
-- =====================================================

-- Index untuk pencarian yang sering dilakukan
CREATE INDEX idx_siswa_kelas ON siswa(kelas);
CREATE INDEX idx_siswa_status ON siswa(status);
CREATE INDEX idx_buku_kategori ON buku(kategori);
CREATE INDEX idx_buku_status ON buku(status);
CREATE INDEX idx_mahasiswa_jurusan ON mahasiswa(jurusan);
CREATE INDEX idx_mahasiswa_status ON mahasiswa(status);
CREATE INDEX idx_habits_kategori ON habits(kategori);
CREATE INDEX idx_diary_tanggal ON diary_entries(tanggal);

-- =====================================================
-- KONFIGURASI DAN CATATAN
-- =====================================================

/*
CATATAN PENTING UNTUK GURU:

1. SETUP AWAL:
   - Pastikan MySQL server sudah terinstall
   - Jalankan script ini untuk membuat database dan tabel
   - Berikan akses yang sesuai untuk user yang akan digunakan

2. KONEKSI DARI PYTHON:
   - Install library: pip install mysql-connector-python
   - Atau gunakan: pip install PyMySQL
   - Konfigurasi koneksi di setiap file praktik

3. KEAMANAN:
   - Jangan hardcode password di kode
   - Gunakan environment variables atau config file
   - Validasi input untuk mencegah SQL injection

4. BACKUP:
   - Lakukan backup database secara berkala
   - Simpan script ini sebagai referensi

5. TROUBLESHOOTING:
   - Cek koneksi database sebelum menjalankan aplikasi
   - Pastikan semua tabel sudah dibuat dengan benar
   - Monitor log error untuk debugging

CONTOH KONEKSI PYTHON:

import mysql.connector
from mysql.connector import Error

def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='python_fullstack_smp',
            user='your_username',
            password='your_password'
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None
*/

-- Tampilkan informasi database yang telah dibuat
SELECT 'Database python_fullstack_smp berhasil dibuat!' as status;
SHOW TABLES;