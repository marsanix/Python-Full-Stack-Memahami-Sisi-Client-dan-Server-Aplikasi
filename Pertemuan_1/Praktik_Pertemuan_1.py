# =====================================================
# PRAKTIK PERTEMUAN 1: MEMBONGKAR ULANG APLIKASI CRUD
# =====================================================
# Durasi: 45 menit
# Fokus: Memahami konsep CRUD melalui hands-on practice dengan MySQL
# Target: Siswa SMP yang sudah paham Python dasar dan MySQL

from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime

# =====================================================
# KONFIGURASI DATABASE (MySQL)
# =====================================================

# Konfigurasi koneksi database
DB_CONFIG = {
    'host': 'localhost',
    'database': 'python_fullstack_smp',
    'user': 'root',  # Ganti dengan username MySQL Anda
    'password': 'toor',  # Ganti dengan password MySQL Anda
    'charset': 'utf8mb4'
}

def create_connection():
    """Membuat koneksi ke database MySQL"""
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def execute_query(query, params=None, fetch=False):
    """Menjalankan query ke database"""
    connection = create_connection()
    if not connection:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        
        if fetch:
            result = cursor.fetchall()
        else:
            connection.commit()
            result = cursor.rowcount
            
        return result
    except Error as e:
        print(f"Error executing query: {e}")
        connection.rollback()
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def test_connection():
    """Test koneksi database"""
    connection = create_connection()
    if connection:
        print("✅ Koneksi database berhasil!")
        connection.close()
        return True
    else:
        print("❌ Koneksi database gagal!")
        return False

# =====================================================
# FUNGSI CRUD OPERATIONS (MySQL)
# =====================================================

def get_all_siswa(filter_nama=None):
    """READ: Mengambil semua data siswa dengan filter opsional berdasarkan nama"""
    if filter_nama:
        # Jika ada filter nama, gunakan LIKE untuk pencarian partial
        query = "SELECT * FROM siswa WHERE nama LIKE %s ORDER BY id DESC"
        search_term = f"%{filter_nama}%"
        result = execute_query(query, (search_term,), fetch=True)
    else:
        # Jika tidak ada filter, ambil semua data
        query = "SELECT * FROM siswa ORDER BY id DESC"
        result = execute_query(query, fetch=True)
    
    return result or []

def get_siswa_by_id(siswa_id):
    """READ: Mengambil data siswa berdasarkan ID"""
    query = "SELECT * FROM siswa WHERE id = %s"
    result = execute_query(query, (siswa_id,), fetch=True)
    return result[0] if result else None

def add_siswa(nama, kelas, umur, alamat):
    """CREATE: Menambah siswa baru"""
    query = """
    INSERT INTO siswa (nama, kelas, umur, alamat) 
    VALUES (%s, %s, %s, %s)
    """
    result = execute_query(query, (nama, kelas, umur, alamat))
    
    if result:
        # Ambil data siswa yang baru ditambahkan
        query_select = "SELECT * FROM siswa WHERE nama = %s AND kelas = %s ORDER BY id DESC LIMIT 1"
        new_siswa = execute_query(query_select, (nama, kelas), fetch=True)
        return new_siswa[0] if new_siswa else None
    return None

def update_siswa(siswa_id, nama, kelas, umur, alamat):
    """UPDATE: Mengupdate data siswa"""
    query = """
    UPDATE siswa 
    SET nama = %s, kelas = %s, umur = %s, alamat = %s 
    WHERE id = %s
    """
    result = execute_query(query, (nama, kelas, umur, alamat, siswa_id))
    
    if result:
        return get_siswa_by_id(siswa_id)
    return None

def delete_siswa(siswa_id):
    """DELETE: Menghapus data siswa"""
    # Ambil data siswa sebelum dihapus
    siswa = get_siswa_by_id(siswa_id)
    
    if siswa:
        query = "DELETE FROM siswa WHERE id = %s"
        result = execute_query(query, (siswa_id,))
        return siswa if result else None
    return None

def search_siswa(keyword):
    """Mencari siswa berdasarkan nama atau kelas"""
    query = """
    SELECT * FROM siswa 
    WHERE nama LIKE %s OR kelas LIKE %s 
    ORDER BY nama
    """
    search_term = f"%{keyword}%"
    result = execute_query(query, (search_term, search_term), fetch=True)
    return result or []

# Membuat aplikasi Flask
app = Flask(__name__, template_folder='praktik_pertemuan_1/templates')
app.secret_key = 'kunci_rahasia_untuk_flash_message'  # Diperlukan untuk flash message

# LATIHAN 1: PAHAMI ROUTING DASAR
@app.route('/')
def halaman_utama():
    """
    Fungsi ini akan dijalankan ketika user mengakses alamat utama (/)
    
    PERTANYAAN UNTUK DIPAHAMI:
    1. Kenapa pakai @app.route('/')?
    2. Apa yang dikembalikan oleh fungsi ini?
    3. Bagaimana data_siswa sampai ke template HTML?
    4. Bagaimana filter nama bekerja melalui query parameter?
    """
    # Ambil parameter filter nama dari query string (contoh: /?filter_nama=john)
    filter_nama = request.args.get('filter_nama', '').strip()
    
    # Jika filter_nama kosong, set ke None agar mengambil semua data
    if not filter_nama:
        filter_nama = None
    
    data_siswa = get_all_siswa(filter_nama=filter_nama)
    
    # Kirim juga informasi filter ke template untuk ditampilkan
    return render_template('index.html', 
                         siswa_list=data_siswa, 
                         current_filter=filter_nama)

# LATIHAN 2: PAHAMI METHOD GET DAN POST
@app.route('/tambah', methods=['GET', 'POST'])
def tambah_siswa():
    """
    Fungsi ini menangani dua jenis request:
    - GET: Menampilkan form tambah siswa
    - POST: Memproses data yang dikirim dari form
    
    PERTANYAAN UNTUK DIPAHAMI:
    1. Kenapa perlu ada methods=['GET', 'POST']?
    2. Apa bedanya GET dan POST?
    3. Dari mana request.form['nama'] datangnya?
    4. Kenapa pakai redirect('/') di akhir?
    """
    
    if request.method == 'POST':
        # Ambil data dari form
        nama = request.form['nama']
        kelas = request.form['kelas']
        umur = int(request.form['umur'])
        alamat = request.form['alamat']
        
        # LATIHAN: Tambahkan validasi di sini
        # Pastikan nama tidak kosong
        if not nama.strip():
            flash('Nama siswa tidak boleh kosong!', 'error')
            return render_template('tambah.html')
        
        # Tambahkan siswa ke database
        siswa_baru = add_siswa(nama, kelas, umur, alamat)
        
        if not siswa_baru:
            flash('Gagal menambahkan siswa ke database!', 'error')
            return render_template('tambah.html')
        
        # Berikan pesan sukses
        flash(f'Siswa "{nama}" berhasil ditambahkan!', 'success')
        
        # Redirect ke halaman utama
        return redirect('/')
    
    # Jika method GET, tampilkan form
    return render_template('tambah.html')

# LATIHAN 3: PAHAMI PARAMETER URL
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_siswa(id):
    """
    Fungsi ini menangani edit siswa berdasarkan ID
    
    PERTANYAAN UNTUK DIPAHAMI:
    1. Apa arti <int:id> dalam route?
    2. Bagaimana cara mencari siswa berdasarkan ID?
    3. Kenapa perlu cek if siswa_ditemukan?
    """
    
    # Cari siswa berdasarkan ID dari database
    siswa_ditemukan = get_siswa_by_id(id)
    
    # Jika siswa tidak ditemukan
    if not siswa_ditemukan:
        flash('Siswa tidak ditemukan!', 'error')
        return redirect('/')
    
    if request.method == 'POST':
        # Update data siswa di database
        nama = request.form['nama']
        kelas = request.form['kelas']
        umur = int(request.form['umur'])
        alamat = request.form['alamat']
        
        updated_siswa = update_siswa(id, nama, kelas, umur, alamat)
        
        if updated_siswa:
            flash(f'Data siswa "{nama}" berhasil diupdate!', 'success')
        else:
            flash('Gagal mengupdate data siswa!', 'error')
        
        return redirect('/')
    
    # Jika method GET, tampilkan form edit dengan data siswa
    return render_template('edit.html', siswa=siswa_ditemukan)

# LATIHAN 4: PAHAMI KONFIRMASI HAPUS
@app.route('/hapus/<int:id>')
@app.route('/hapus/<int:id>/<konfirmasi>')
def hapus_siswa(id, konfirmasi=None):
    """
    Fungsi ini menangani penghapusan siswa dengan konfirmasi
    
    PERTANYAAN UNTUK DIPAHAMI:
    1. Kenapa ada dua @app.route?
    2. Apa fungsi parameter konfirmasi=None?
    3. Bagaimana cara menghapus item dari database?
    """
    
    # Cari siswa berdasarkan ID dari database
    siswa_ditemukan = get_siswa_by_id(id)
    
    if not siswa_ditemukan:
        flash('Siswa tidak ditemukan!', 'error')
        return redirect('/')
    
    # Jika belum konfirmasi, tampilkan halaman konfirmasi
    if konfirmasi != 'ya':
        return render_template('konfirmasi_hapus.html', siswa=siswa_ditemukan)
    
    # Jika sudah konfirmasi, hapus siswa dari database
    deleted_siswa = delete_siswa(id)
    
    if deleted_siswa:
        flash(f'Data siswa "{deleted_siswa["nama"]}" berhasil dihapus!', 'success')
    else:
        flash('Gagal menghapus data siswa!', 'error')
    
    return redirect('/')

# LATIHAN 5: ROUTE UNTUK DEBUGGING
@app.route('/debug')
def debug_info():
    """
    Route khusus untuk melihat isi data_siswa dari database
    Berguna untuk debugging
    """
    data_siswa = get_all_siswa()
    return f"<h1>Debug Info</h1><pre>{data_siswa}</pre>"

# TANTANGAN PRAKTIK:

# TANTANGAN 1: Buat route untuk mencari buku
@app.route('/cari', methods=['GET', 'POST'])
def cari_siswa():
    """
    TODO: Lengkapi fungsi ini!
    
    Fungsi ini harus:
    1. Menampilkan form pencarian (GET)
    2. Memproses pencarian berdasarkan nama atau kelas (POST)
    3. Menampilkan hasil pencarian
    
    PETUNJUK:
    - Gunakan method .lower() untuk pencarian case-insensitive
    - Gunakan operator LIKE untuk pencarian substring di MySQL
    """
    if request.method == 'POST':
        kata_kunci = request.form['kata_kunci']
        hasil_cari = search_siswa(kata_kunci)
        
        return render_template('hasil_cari.html', hasil=hasil_cari, kata_kunci=kata_kunci)
    
    return render_template('cari.html')

# TANTANGAN 2: Buat route untuk statistik
@app.route('/statistik')
def statistik_siswa():
    """
    TODO: Lengkapi fungsi ini!
    
    Fungsi ini harus menampilkan:
    1. Total jumlah siswa
    2. Umur termuda dan tertua
    3. Kelas yang paling banyak siswanya
    
    PETUNJUK:
    - Gunakan len() untuk menghitung jumlah
    - Gunakan min() dan max() untuk umur
    - Gunakan dictionary untuk menghitung kelas
    """
    data_siswa = get_all_siswa()
    total_siswa = len(data_siswa)
    
    if data_siswa:
        umur_termuda = min([siswa['umur'] for siswa in data_siswa])
        umur_tertua = max([siswa['umur'] for siswa in data_siswa])
        
        # Hitung kelas terbanyak
        kelas_count = {}
        for siswa in data_siswa:
            kelas = siswa['kelas']
            kelas_count[kelas] = kelas_count.get(kelas, 0) + 1
        
        kelas_terbanyak = max(kelas_count, key=kelas_count.get) if kelas_count else 'Tidak ada data'
        
        statistik = {
            'total': total_siswa,
            'umur_termuda': umur_termuda,
            'umur_tertua': umur_tertua,
            'kelas_terbanyak': kelas_terbanyak
        }
    else:
        statistik = {
            'total': 0,
            'umur_termuda': 'Tidak ada data',
            'umur_tertua': 'Tidak ada data',
            'kelas_terbanyak': 'Tidak ada data'
        }
    
    return render_template('statistik.html', stats=statistik)

if __name__ == '__main__':
    print("\n" + "="*50)
    print("PRAKTIK PERTEMUAN 1: MEMAHAMI ARSITEKTUR CLIENT-SERVER")
    print("="*50)
    
    # Test koneksi database
    if test_connection():
        print("Server akan berjalan di: http://localhost:5000")
        print("\nRoute yang tersedia:")
        print("- / : Halaman utama (daftar buku)")
        print("- /tambah : Tambah buku baru")
        print("- /edit/<id> : Edit buku")
        print("- /hapus/<id> : Hapus buku")
        print("- /cari : Cari buku (TANTANGAN)")
        print("- /statistik : Statistik buku (TANTANGAN)")
        print("- /debug : Debug info")
        print("\nTekan Ctrl+C untuk menghentikan server")
        print("="*50 + "\n")
        
        app.run(debug=True, port=5000)
    else:
        print("\n❌ Tidak dapat menjalankan aplikasi karena koneksi database gagal!")
        print("Pastikan MySQL server berjalan dan konfigurasi database benar.")
        print("="*50 + "\n")

"""
CATATAN PENTING UNTUK SISWA:

1. PAHAMI SEBELUM MENJALANKAN:
   - Baca setiap komentar dengan teliti
   - Pahami alur kerja setiap fungsi
   - Tanyakan jika ada yang tidak jelas

2. CARA MENJALANKAN:
   - Pastikan Flask dan MySQL Connector sudah terinstall: 
     pip install flask mysql-connector-python
   - Pastikan MySQL server berjalan
   - Buat database 'python_fullstack_smp' dan tabel 'buku'
   - Sesuaikan konfigurasi database di DB_CONFIG
   - Jalankan file ini: python praktik_pertemuan_1.py
   - Buka browser ke http://localhost:5000

3. YANG HARUS DILAKUKAN:
   - Coba setiap fitur yang ada
   - Perhatikan pesan error jika ada
   - Lengkapi tantangan yang diberikan
   - Eksperimen dengan mengubah kode

4. DEBUGGING TIPS:
   - Gunakan route /debug untuk melihat data
   - Perhatikan terminal untuk pesan error
   - Gunakan print() untuk debug
   - Reload halaman setelah mengubah kode

5. PERTANYAAN REFLEKSI:
   - Bagaimana data mengalir dari form ke server?
   - Kenapa perlu redirect setelah POST?
   - Apa yang terjadi jika tidak ada validasi?
   - Bagaimana cara menambah fitur baru?
"""