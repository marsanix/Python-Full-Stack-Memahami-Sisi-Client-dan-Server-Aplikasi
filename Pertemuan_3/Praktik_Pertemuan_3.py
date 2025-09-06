# Praktik Pertemuan 3: Integrasi Data & Validasi
# Program: Python Full-Stack untuk SMP
# Durasi: 90 menit
# Fokus: Implementasi validasi lengkap dan database MySQL

"""
🎯 TUJUAN PRAKTIK:
1. Implementasi validasi data yang komprehensif
2. Integrasi dengan database JSON
3. Error handling dan user feedback
4. Testing berbagai skenario input

📚 YANG AKAN DIPELAJARI:
- Server-side validation dengan Python
- Database operations dengan JSON
- Flash messages dan error handling
- Regex untuk validasi format
- Backup dan recovery data
"""

# ============================================================================
# IMPORT LIBRARIES
# ============================================================================

from flask import Flask, render_template, request, redirect, flash, jsonify
import mysql.connector
from mysql.connector import Error
import os
import re
import shutil
from datetime import datetime
import logging

# ============================================================================
# KONFIGURASI APLIKASI
# ============================================================================

app = Flask(__name__)
app.secret_key = 'rahasia_validasi_smp_2024'

# Konfigurasi validasi
CONFIG = {
    'MIN_NAME_LENGTH': 2,
    'MAX_NAME_LENGTH': 50,
    'MIN_AGE': 10,
    'MAX_AGE': 18,
    'BACKUP_FOLDER': 'backups/'
}

# Konfigurasi database MySQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'siswa_db'
}

# Setup logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ============================================================================
# DATABASE JSON CLASS
# ============================================================================

# Fungsi koneksi database MySQL
def get_db_connection():
    """Membuat koneksi ke database MySQL"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        logging.error(f"Database connection error: {e}")
        print(f"❌ Error koneksi database: {e}")
        return None

def execute_query(query, params=None, fetch=False):
    """Fungsi universal untuk eksekusi SQL query dengan error handling"""
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
            result = cursor.lastrowid if cursor.lastrowid else True
            
        return result
    except Error as e:
        logging.error(f"Query execution error: {e}")
        print(f"❌ Error eksekusi query: {e}")
        connection.rollback()
        return None
    finally:
        cursor.close()
        connection.close()

class DatabaseMySQL:
    """Class untuk mengelola database MySQL sederhana"""
    
    def __init__(self):
        self.init_database()
    
    def init_database(self):
        """Inisialisasi database dan tabel"""
        try:
            # Buat database jika belum ada
            connection = mysql.connector.connect(
                host=DB_CONFIG['host'],
                user=DB_CONFIG['user'],
                password=DB_CONFIG['password']
            )
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']}")
            cursor.close()
            connection.close()
            
            # Buat tabel siswa jika belum ada
            create_table_query = """
            CREATE TABLE IF NOT EXISTS siswa (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nama VARCHAR(100) NOT NULL,
                umur INT NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                kelas VARCHAR(10) NOT NULL,
                tanggal_daftar DATE DEFAULT (CURRENT_DATE),
                status ENUM('aktif', 'nonaktif') DEFAULT 'aktif',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            )
            """
            
            execute_query(create_table_query)
            print("✅ Database dan tabel berhasil diinisialisasi")
            
        except Exception as e:
            print(f"❌ Error inisialisasi database: {e}")
    
    def get_all_siswa(self):
        """Mengambil semua data siswa"""
        query = "SELECT * FROM siswa ORDER BY id DESC"
        result = execute_query(query, fetch=True)
        return result if result else []
    
    def get_siswa_by_id(self, siswa_id):
        """Mencari siswa berdasarkan ID"""
        query = "SELECT * FROM siswa WHERE id = %s"
        result = execute_query(query, (siswa_id,), fetch=True)
        return result[0] if result else None
    
    def add_siswa(self, siswa_data):
        """Menambah siswa baru"""
        try:
            query = """
            INSERT INTO siswa (nama, umur, email, kelas, status) 
            VALUES (%s, %s, %s, %s, %s)
            """
            params = (
                siswa_data['nama'],
                siswa_data['umur'],
                siswa_data['email'],
                siswa_data['kelas'],
                'aktif'
            )
            
            result = execute_query(query, params)
            if result:
                # Ambil data siswa yang baru ditambahkan
                new_siswa = self.get_siswa_by_id(result)
                print(f"✅ Siswa {siswa_data['nama']} berhasil ditambahkan dengan ID {result}")
                return new_siswa
            return None
            
        except Exception as e:
            print(f"❌ Error menambah siswa: {e}")
            return None
    
    def update_siswa(self, siswa_id, siswa_data):
        """Update data siswa"""
        try:
            query = """
            UPDATE siswa 
            SET nama = %s, umur = %s, email = %s, kelas = %s 
            WHERE id = %s
            """
            params = (
                siswa_data['nama'],
                siswa_data['umur'],
                siswa_data['email'],
                siswa_data['kelas'],
                siswa_id
            )
            
            result = execute_query(query, params)
            if result:
                updated_siswa = self.get_siswa_by_id(siswa_id)
                print(f"✅ Data siswa ID {siswa_id} berhasil diupdate")
                return updated_siswa
            return None
            
        except Exception as e:
            print(f"❌ Error update siswa: {e}")
            return None
    
    def delete_siswa(self, siswa_id):
        """Hapus siswa berdasarkan ID"""
        try:
            # Ambil data siswa sebelum dihapus
            siswa = self.get_siswa_by_id(siswa_id)
            if not siswa:
                print(f"❌ Siswa dengan ID {siswa_id} tidak ditemukan")
                return None
            
            query = "DELETE FROM siswa WHERE id = %s"
            result = execute_query(query, (siswa_id,))
            
            if result:
                print(f"✅ Siswa {siswa['nama']} berhasil dihapus")
                return siswa
            return None
            
        except Exception as e:
            print(f"❌ Error hapus siswa: {e}")
            return None
    
    def search_siswa(self, keyword):
        """Mencari siswa berdasarkan nama, email, atau kelas"""
        keyword = keyword.lower().strip()
        
        query = """
        SELECT * FROM siswa 
        WHERE LOWER(nama) LIKE %s 
           OR LOWER(email) LIKE %s 
           OR LOWER(kelas) LIKE %s
        ORDER BY nama
        """
        
        search_term = f"%{keyword}%"
        result = execute_query(query, (search_term, search_term, search_term), fetch=True)
        
        hasil = result if result else []
        print(f"🔍 Ditemukan {len(hasil)} siswa dengan keyword '{keyword}'")
        return hasil
    
    def get_statistics(self):
        """Mendapatkan statistik data siswa"""
        try:
            # Query untuk statistik dasar
            query = """
            SELECT 
                COUNT(*) as total_siswa,
                COUNT(CASE WHEN status = 'aktif' THEN 1 END) as siswa_aktif,
                AVG(umur) as rata_rata_umur
            FROM siswa
            """
            
            result = execute_query(query, fetch=True)
            
            if result and result[0]['total_siswa'] > 0:
                stats = result[0]
                
                # Query untuk distribusi kelas
                query_kelas = """
                SELECT kelas, COUNT(*) as jumlah 
                FROM siswa 
                GROUP BY kelas 
                ORDER BY jumlah DESC
                """
                
                kelas_result = execute_query(query_kelas, fetch=True)
                kelas_count = {row['kelas']: row['jumlah'] for row in kelas_result} if kelas_result else {}
                
                return {
                    'total_siswa': int(stats['total_siswa']),
                    'siswa_aktif': int(stats['siswa_aktif']),
                    'rata_rata_umur': round(float(stats['rata_rata_umur'] or 0), 1),
                    'distribusi_kelas': kelas_count,
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            else:
                return {
                    'total_siswa': 0,
                    'siswa_aktif': 0,
                    'rata_rata_umur': 0,
                    'distribusi_kelas': {},
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
                
        except Exception as e:
            print(f"❌ Error mendapatkan statistik: {e}")
            return {
                'total_siswa': 0,
                'siswa_aktif': 0,
                'rata_rata_umur': 0,
                'distribusi_kelas': {},
                'last_updated': 'Error'
            }

# ============================================================================
# FUNGSI VALIDASI
# ============================================================================

def validasi_nama(nama):
    """Validasi nama siswa dengan berbagai aturan"""
    if not nama or not nama.strip():
        return False, "Nama tidak boleh kosong"
    
    nama = nama.strip()
    
    if len(nama) < CONFIG['MIN_NAME_LENGTH']:
        return False, f"Nama minimal {CONFIG['MIN_NAME_LENGTH']} karakter"
    
    if len(nama) > CONFIG['MAX_NAME_LENGTH']:
        return False, f"Nama maksimal {CONFIG['MAX_NAME_LENGTH']} karakter"
    
    # Cek karakter yang diizinkan (huruf, spasi, titik, koma)
    if not re.match(r'^[a-zA-Z\s.,]+$', nama):
        return False, "Nama hanya boleh mengandung huruf, spasi, titik, dan koma"
    
    # Cek tidak boleh hanya spasi
    if nama.replace(' ', '').replace('.', '').replace(',', '') == '':
        return False, "Nama tidak boleh hanya berisi spasi dan tanda baca"
    
    return True, nama.title()  # Return nama dengan format Title Case

def validasi_umur(umur_str):
    """Validasi umur siswa"""
    if not umur_str or not umur_str.strip():
        return False, "Umur tidak boleh kosong"
    
    try:
        umur = int(umur_str.strip())
        
        if umur < CONFIG['MIN_AGE']:
            return False, f"Umur minimal {CONFIG['MIN_AGE']} tahun"
        
        if umur > CONFIG['MAX_AGE']:
            return False, f"Umur maksimal {CONFIG['MAX_AGE']} tahun"
        
        return True, umur
        
    except ValueError:
        return False, "Umur harus berupa angka"

def validasi_email(email):
    """Validasi format email dengan regex"""
    if not email or not email.strip():
        return False, "Email tidak boleh kosong"
    
    email = email.strip().lower()
    
    # Pattern regex untuk email
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False, "Format email tidak valid (contoh: nama@domain.com)"
    
    # Cek panjang email
    if len(email) > 100:
        return False, "Email terlalu panjang (maksimal 100 karakter)"
    
    return True, email

def validasi_kelas(kelas):
    """Validasi kelas siswa"""
    if not kelas or not kelas.strip():
        return False, "Kelas tidak boleh kosong"
    
    kelas = kelas.strip().upper()
    
    # Pattern untuk kelas (contoh: 7A, 8B, 9C)
    if not re.match(r'^[7-9][A-Z]$', kelas):
        return False, "Format kelas tidak valid (contoh: 7A, 8B, 9C)"
    
    return True, kelas

def validasi_email_unik(email, db, exclude_id=None):
    """Cek apakah email sudah terdaftar"""
    email = email.lower().strip()
    
    for siswa in db.get_all_siswa():
        if siswa['email'].lower() == email and siswa['id'] != exclude_id:
            return False, "Email sudah terdaftar oleh siswa lain"
    
    return True, "Email tersedia"

# ============================================================================
# INISIALISASI DATABASE
# ============================================================================

# Buat instance database
db = DatabaseMySQL()

# Buat folder backup jika belum ada
if not os.path.exists(CONFIG['BACKUP_FOLDER']):
    os.makedirs(CONFIG['BACKUP_FOLDER'])
    print(f"📁 Folder backup dibuat: {CONFIG['BACKUP_FOLDER']}")

# ============================================================================
# FLASK ROUTES
# ============================================================================

@app.route('/')
def index():
    """Halaman utama dengan daftar siswa"""
    try:
        siswa_list = db.get_all_siswa()
        stats = db.get_statistics()
        
        print(f"📊 Menampilkan {len(siswa_list)} siswa")
        
        # Simulasi template (dalam praktik nyata gunakan HTML template)
        return f"""
        <h1>📚 Data Siswa SMP</h1>
        <p>Total Siswa: {stats['total_siswa']} | Aktif: {stats['siswa_aktif']} | Rata-rata Umur: {stats['rata_rata_umur']} tahun</p>
        <p><a href='/tambah'>➕ Tambah Siswa</a> | <a href='/cari'>🔍 Cari Siswa</a> | <a href='/statistik'>📊 Statistik</a> | <a href='/backup'>💾 Backup</a></p>
        <hr>
        {''.join([f"<p>{s['id']}. {s['nama']} ({s['umur']} tahun) - {s['email']} - Kelas {s.get('kelas', 'N/A')} | <a href='/edit/{s['id']}'>✏️ Edit</a> | <a href='/hapus/{s['id']}'>🗑️ Hapus</a></p>" for s in siswa_list])}
        """
        
    except Exception as e:
        print(f"❌ Error di halaman index: {e}")
        return f"<h1>❌ Error: {e}</h1><p><a href='/'>🔄 Refresh</a></p>"

@app.route('/tambah', methods=['GET', 'POST'])
def tambah_siswa():
    """Tambah siswa baru dengan validasi lengkap"""
    if request.method == 'POST':
        try:
            # Ambil data dari form
            nama = request.form.get('nama', '').strip()
            umur_str = request.form.get('umur', '').strip()
            email = request.form.get('email', '').strip()
            kelas = request.form.get('kelas', '').strip()
            
            print(f"📝 Mencoba menambah siswa: {nama}")
            
            # Validasi nama
            valid_nama, hasil_nama = validasi_nama(nama)
            if not valid_nama:
                flash(f"❌ {hasil_nama}", 'error')
                return redirect('/tambah')
            
            # Validasi umur
            valid_umur, hasil_umur = validasi_umur(umur_str)
            if not valid_umur:
                flash(f"❌ {hasil_umur}", 'error')
                return redirect('/tambah')
            
            # Validasi email
            valid_email, hasil_email = validasi_email(email)
            if not valid_email:
                flash(f"❌ {hasil_email}", 'error')
                return redirect('/tambah')
            
            # Cek email unik
            valid_unik, pesan_unik = validasi_email_unik(hasil_email, db)
            if not valid_unik:
                flash(f"❌ {pesan_unik}", 'error')
                return redirect('/tambah')
            
            # Validasi kelas
            valid_kelas, hasil_kelas = validasi_kelas(kelas)
            if not valid_kelas:
                flash(f"❌ {hasil_kelas}", 'error')
                return redirect('/tambah')
            
            # Semua validasi passed, simpan data
            siswa_data = {
                'nama': hasil_nama,
                'umur': hasil_umur,
                'email': hasil_email,
                'kelas': hasil_kelas
            }
            
            siswa_baru = db.add_siswa(siswa_data)
            if siswa_baru:
                flash(f"✅ Siswa {hasil_nama} berhasil ditambahkan!", 'success')
                return redirect('/')
            else:
                flash("❌ Gagal menyimpan data siswa!", 'error')
                return redirect('/tambah')
                
        except Exception as e:
            print(f"❌ Error saat menambah siswa: {e}")
            flash(f"❌ Error sistem: {e}", 'error')
            return redirect('/tambah')
    
    # GET request - tampilkan form
    return f"""
    <h1>➕ Tambah Siswa Baru</h1>
    <form method='POST'>
        <p>Nama: <input type='text' name='nama' required minlength='2' maxlength='50' placeholder='Masukkan nama lengkap'></p>
        <p>Umur: <input type='number' name='umur' min='10' max='18' required placeholder='10-18 tahun'></p>
        <p>Email: <input type='email' name='email' required placeholder='nama@domain.com'></p>
        <p>Kelas: <input type='text' name='kelas' required pattern='[7-9][A-Z]' placeholder='7A, 8B, 9C'></p>
        <p><button type='submit'>💾 Simpan</button> <a href='/'>🔙 Kembali</a></p>
    </form>
    """

@app.route('/edit/<int:siswa_id>', methods=['GET', 'POST'])
def edit_siswa(siswa_id):
    """Edit data siswa dengan validasi"""
    siswa = db.get_siswa_by_id(siswa_id)
    if not siswa:
        flash('❌ Siswa tidak ditemukan!', 'error')
        return redirect('/')
    
    if request.method == 'POST':
        try:
            # Ambil data dari form
            nama = request.form.get('nama', '').strip()
            umur_str = request.form.get('umur', '').strip()
            email = request.form.get('email', '').strip()
            kelas = request.form.get('kelas', '').strip()
            
            print(f"✏️ Mengedit siswa ID {siswa_id}: {nama}")
            
            # Validasi nama
            valid_nama, hasil_nama = validasi_nama(nama)
            if not valid_nama:
                flash(f"❌ {hasil_nama}", 'error')
                return redirect(f'/edit/{siswa_id}')
            
            # Validasi umur
            valid_umur, hasil_umur = validasi_umur(umur_str)
            if not valid_umur:
                flash(f"❌ {hasil_umur}", 'error')
                return redirect(f'/edit/{siswa_id}')
            
            # Validasi email
            valid_email, hasil_email = validasi_email(email)
            if not valid_email:
                flash(f"❌ {hasil_email}", 'error')
                return redirect(f'/edit/{siswa_id}')
            
            # Cek email unik (exclude current siswa)
            valid_unik, pesan_unik = validasi_email_unik(hasil_email, db, exclude_id=siswa_id)
            if not valid_unik:
                flash(f"❌ {pesan_unik}", 'error')
                return redirect(f'/edit/{siswa_id}')
            
            # Validasi kelas
            valid_kelas, hasil_kelas = validasi_kelas(kelas)
            if not valid_kelas:
                flash(f"❌ {hasil_kelas}", 'error')
                return redirect(f'/edit/{siswa_id}')
            
            # Update data
            siswa_data = {
                'nama': hasil_nama,
                'umur': hasil_umur,
                'email': hasil_email,
                'kelas': hasil_kelas
            }
            
            siswa_updated = db.update_siswa(siswa_id, siswa_data)
            if siswa_updated:
                flash(f"✅ Data siswa {hasil_nama} berhasil diupdate!", 'success')
                return redirect('/')
            else:
                flash("❌ Gagal mengupdate data siswa!", 'error')
                return redirect(f'/edit/{siswa_id}')
                
        except Exception as e:
            print(f"❌ Error saat edit siswa: {e}")
            flash(f"❌ Error sistem: {e}", 'error')
            return redirect(f'/edit/{siswa_id}')
    
    # GET request - tampilkan form edit
    return f"""
    <h1>✏️ Edit Siswa: {siswa['nama']}</h1>
    <form method='POST'>
        <p>Nama: <input type='text' name='nama' value='{siswa['nama']}' required minlength='2' maxlength='50'></p>
        <p>Umur: <input type='number' name='umur' value='{siswa['umur']}' min='10' max='18' required></p>
        <p>Email: <input type='email' name='email' value='{siswa['email']}' required></p>
        <p>Kelas: <input type='text' name='kelas' value='{siswa.get('kelas', '')}' required pattern='[7-9][A-Z]'></p>
        <p><button type='submit'>💾 Update</button> <a href='/'>🔙 Kembali</a></p>
    </form>
    <p><small>📅 Terdaftar: {siswa['tanggal_daftar']} | Status: {siswa.get('status', 'aktif')}</small></p>
    """

@app.route('/hapus/<int:siswa_id>')
def hapus_siswa(siswa_id):
    """Hapus siswa dengan konfirmasi"""
    try:
        siswa = db.get_siswa_by_id(siswa_id)
        if not siswa:
            flash('❌ Siswa tidak ditemukan!', 'error')
            return redirect('/')
        
        # Hapus siswa
        deleted_siswa = db.delete_siswa(siswa_id)
        if deleted_siswa:
            flash(f"✅ Siswa {deleted_siswa['nama']} berhasil dihapus!", 'success')
        else:
            flash("❌ Gagal menghapus siswa!", 'error')
        
        return redirect('/')
        
    except Exception as e:
        print(f"❌ Error saat hapus siswa: {e}")
        flash(f"❌ Error sistem: {e}", 'error')
        return redirect('/')

@app.route('/cari', methods=['GET', 'POST'])
def cari_siswa():
    """Pencarian siswa dengan keyword"""
    if request.method == 'POST':
        try:
            keyword = request.form.get('keyword', '').strip()
            
            if not keyword:
                flash('❌ Masukkan kata kunci pencarian!', 'error')
                return redirect('/cari')
            
            if len(keyword) < 2:
                flash('❌ Kata kunci minimal 2 karakter!', 'error')
                return redirect('/cari')
            
            hasil = db.search_siswa(keyword)
            
            if hasil:
                hasil_html = ''.join([f"<p>{s['id']}. {s['nama']} ({s['umur']} tahun) - {s['email']} - Kelas {s.get('kelas', 'N/A')} | <a href='/edit/{s['id']}'>✏️ Edit</a></p>" for s in hasil])
                return f"""
                <h1>🔍 Hasil Pencarian: "{keyword}"</h1>
                <p>Ditemukan {len(hasil)} siswa</p>
                <hr>
                {hasil_html}
                <p><a href='/cari'>🔍 Cari Lagi</a> | <a href='/'>🔙 Kembali</a></p>
                """
            else:
                return f"""
                <h1>🔍 Hasil Pencarian: "{keyword}"</h1>
                <p>❌ Tidak ada siswa yang ditemukan</p>
                <p><a href='/cari'>🔍 Cari Lagi</a> | <a href='/'>🔙 Kembali</a></p>
                """
                
        except Exception as e:
            print(f"❌ Error saat pencarian: {e}")
            flash(f"❌ Error sistem: {e}", 'error')
            return redirect('/cari')
    
    # GET request - tampilkan form pencarian
    return f"""
    <h1>🔍 Cari Siswa</h1>
    <form method='POST'>
        <p>Kata Kunci: <input type='text' name='keyword' required minlength='2' placeholder='Nama, email, atau kelas'></p>
        <p><button type='submit'>🔍 Cari</button> <a href='/'>🔙 Kembali</a></p>
    </form>
    <p><small>💡 Tips: Masukkan nama, email, atau kelas yang ingin dicari</small></p>
    """

@app.route('/statistik')
def statistik():
    """Halaman statistik data siswa"""
    try:
        stats = db.get_statistics()
        
        # Format distribusi kelas
        kelas_html = ''.join([f"<li>{kelas}: {jumlah} siswa</li>" for kelas, jumlah in stats['distribusi_kelas'].items()])
        
        return f"""
        <h1>📊 Statistik Data Siswa</h1>
        <h3>📈 Ringkasan:</h3>
        <ul>
            <li>Total Siswa: {stats['total_siswa']}</li>
            <li>Siswa Aktif: {stats['siswa_aktif']}</li>
            <li>Rata-rata Umur: {stats['rata_rata_umur']} tahun</li>
            <li>Terakhir Update: {stats['last_updated']}</li>
        </ul>
        
        <h3>🏫 Distribusi Kelas:</h3>
        <ul>{kelas_html}</ul>
        
        <p><a href='/'>🔙 Kembali</a> | <a href='/backup'>💾 Backup Data</a></p>
        """
        
    except Exception as e:
        print(f"❌ Error saat menampilkan statistik: {e}")
        return f"<h1>❌ Error: {e}</h1><p><a href='/'>🔙 Kembali</a></p>"

@app.route('/backup')
def backup_data():
    """Backup data siswa ke file JSON"""
    try:
        # Ambil semua data siswa
        siswa_list = db.get_all_siswa()
        stats = db.get_statistics()
        
        # Buat struktur data backup
        backup_data = {
            'siswa': siswa_list,
            'metadata': {
                'backup_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'total_siswa': stats['total_siswa'],
                'version': '1.0'
            }
        }
        
        # Buat nama file backup dengan timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_filename = f'backup_siswa_{timestamp}.json'
        backup_path = os.path.join(CONFIG['BACKUP_FOLDER'], backup_filename)
        
        # Simpan ke file JSON
        with open(backup_path, 'w', encoding='utf-8') as file:
            import json
            json.dump(backup_data, file, indent=2, ensure_ascii=False, default=str)
        
        # Verifikasi backup
        if os.path.exists(backup_path):
            file_size = os.path.getsize(backup_path)
            flash(f"✅ Backup berhasil: {backup_filename} ({file_size} bytes)", 'success')
            print(f"💾 Backup dibuat: {backup_path}")
        else:
            flash("❌ Gagal membuat backup!", 'error')
        
        return redirect('/')
        
    except Exception as e:
        print(f"❌ Error saat backup: {e}")
        flash(f"❌ Error backup: {e}", 'error')
        return redirect('/')

# ============================================================================
# LATIHAN DAN CHALLENGE
# ============================================================================

"""
🎯 LATIHAN 1: VALIDASI TAMBAHAN (15 menit)
Tambahkan validasi untuk field baru:
1. Nomor HP (format: 08xxxxxxxxxx)
2. Alamat (minimal 10 karakter)
3. Nama Orang Tua (minimal 3 karakter)

Contoh implementasi:

def validasi_hp(hp):
    # TODO: Implementasikan validasi nomor HP
    pass

def validasi_alamat(alamat):
    # TODO: Implementasikan validasi alamat
    pass
"""

"""
🎯 LATIHAN 2: FITUR IMPORT/EXPORT (20 menit)
Buat fungsi untuk:
1. Export data ke CSV
2. Import data dari CSV
3. Validasi data saat import

Contoh route:

@app.route('/export')
def export_csv():
    # TODO: Export data siswa ke file CSV
    pass

@app.route('/import', methods=['GET', 'POST'])
def import_csv():
    # TODO: Import data dari file CSV
    pass
"""

"""
🎯 LATIHAN 3: SISTEM LOGGING (15 menit)
Buat sistem logging untuk:
1. Log semua operasi CRUD
2. Log error yang terjadi
3. Log aktivitas user

Contoh implementasi:

import logging

# Setup logging
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def log_activity(action, details):
    # TODO: Implementasikan logging
    pass
"""

"""
🎯 CHALLENGE 1: VALIDASI ADVANCED (25 menit)
Implementasikan validasi yang lebih kompleks:
1. Cek nama tidak boleh sama persis (case-insensitive)
2. Validasi email dengan blacklist domain
3. Validasi umur berdasarkan tanggal lahir
4. Sistem scoring untuk kekuatan password (jika ada field password)

Tips:
- Gunakan regex yang lebih kompleks
- Buat fungsi helper untuk setiap jenis validasi
- Implementasikan sistem whitelist/blacklist
"""

"""
🎯 CHALLENGE 2: DATABASE ADVANCED (30 menit)
Tingkatkan sistem database:
1. Implementasi soft delete (status: aktif/nonaktif)
2. Sistem versioning data (history perubahan)
3. Auto backup berkala
4. Compression untuk file backup

Tips:
- Tambahkan field 'deleted_at' untuk soft delete
- Buat table history untuk tracking perubahan
- Gunakan threading untuk auto backup
- Implementasikan gzip untuk compression
"""

# ============================================================================
# TESTING SCENARIOS
# ============================================================================

def test_validasi():
    """Test semua fungsi validasi"""
    print("\n🧪 TESTING VALIDASI:")
    
    # Test validasi nama
    test_cases_nama = [
        ("", False),  # Kosong
        ("A", False),  # Terlalu pendek
        ("Ahmad Fauzi", True),  # Valid
        ("123", False),  # Angka
        ("Ahmad@Fauzi", False),  # Karakter tidak valid
    ]
    
    for nama, expected in test_cases_nama:
        valid, result = validasi_nama(nama)
        status = "✅" if valid == expected else "❌"
        print(f"  {status} Nama '{nama}': {result}")
    
    # Test validasi umur
    test_cases_umur = [
        ("15", True),  # Valid
        ("9", False),  # Terlalu muda
        ("19", False),  # Terlalu tua
        ("abc", False),  # Bukan angka
        ("", False),  # Kosong
    ]
    
    for umur, expected in test_cases_umur:
        valid, result = validasi_umur(umur)
        status = "✅" if valid == expected else "❌"
        print(f"  {status} Umur '{umur}': {result}")
    
    # Test validasi email
    test_cases_email = [
        ("ahmad@email.com", True),  # Valid
        ("invalid-email", False),  # Tidak ada @
        ("test@", False),  # Tidak ada domain
        ("@domain.com", False),  # Tidak ada username
        ("", False),  # Kosong
    ]
    
    for email, expected in test_cases_email:
        valid, result = validasi_email(email)
        status = "✅" if valid == expected else "❌"
        print(f"  {status} Email '{email}': {result}")

def test_database():
    """Test operasi database"""
    print("\n🧪 TESTING DATABASE:")
    
    # Test tambah siswa
    test_siswa = {
        'nama': 'Test Siswa',
        'umur': 15,
        'email': 'test@email.com',
        'kelas': '9A'
    }
    
    result = db.add_siswa(test_siswa.copy())
    if result:
        print(f"  ✅ Tambah siswa: {result['nama']} (ID: {result['id']})")
        
        # Test update
        test_siswa['nama'] = 'Test Siswa Updated'
        updated = db.update_siswa(result['id'], test_siswa)
        if updated:
            print(f"  ✅ Update siswa: {updated['nama']}")
        
        # Test hapus
        deleted = db.delete_siswa(result['id'])
        if deleted:
            print(f"  ✅ Hapus siswa: {deleted['nama']}")
    else:
        print("  ❌ Gagal tambah siswa test")

# ============================================================================
# MAIN PROGRAM
# ============================================================================

if __name__ == '__main__':
    print("🚀 PRAKTIK PERTEMUAN 3: INTEGRASI DATA & VALIDASI")
    print("=" * 60)
    
    # Jalankan test jika diperlukan
    # test_validasi()
    # test_database()
    
    print("\n📚 PETUNJUK PRAKTIK:")
    print("1. Jalankan aplikasi dengan: python praktik_pertemuan_3.py")
    print("2. Buka browser ke: http://localhost:5000")
    print("3. Coba tambah siswa dengan data valid dan invalid")
    print("4. Test semua fitur validasi")
    print("5. Coba fitur pencarian dan statistik")
    print("6. Lakukan backup data")
    print("7. Kerjakan latihan dan challenge")
    
    print("\n🎯 FOKUS PEMBELAJARAN:")
    print("- Implementasi validasi yang komprehensif")
    print("- Integrasi dengan database JSON")
    print("- Error handling dan user feedback")
    print("- Testing berbagai skenario input")
    
    print("\n⚠️  CATATAN PENTING:")
    print("- Selalu backup data sebelum testing")
    print("- Perhatikan pesan error dan perbaiki")
    print("- Test dengan berbagai jenis input")
    print("- Jangan lupa save file sebelum run")
    
    # Jalankan aplikasi Flask
    app.run(debug=True, host='0.0.0.0', port=5000)

"""
📝 CHECKLIST PRAKTIK:

□ Setup dan konfigurasi aplikasi
□ Implementasi class DatabaseJSON
□ Fungsi validasi nama, umur, email, kelas
□ Route tambah siswa dengan validasi
□ Route edit siswa dengan validasi
□ Route hapus siswa
□ Fitur pencarian siswa
□ Halaman statistik
□ Sistem backup data
□ Error handling di semua route
□ Testing validasi dengan berbagai input
□ Testing operasi database
□ Implementasi latihan tambahan
□ Challenge advanced features

🎯 TUJUAN AKHIR:
Siswa dapat membuat aplikasi web dengan validasi data yang komprehensif,
terintegrasi dengan database JSON, dan memiliki error handling yang baik.

💡 TIPS SUKSES:
1. Baca error message dengan teliti
2. Test setiap fitur secara bertahap
3. Backup data sebelum testing
4. Gunakan print() untuk debugging
5. Jangan takut eksperimen!
"""