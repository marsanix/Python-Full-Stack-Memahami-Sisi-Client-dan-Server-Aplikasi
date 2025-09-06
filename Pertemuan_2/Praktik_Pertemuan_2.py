# Praktik Pertemuan 2: Membangun Ulang dari Nol
# Tema: Aplikasi Perpustakaan Mini dengan MySQL
# Durasi: 90 menit dari total 2 jam pertemuan

"""
INSTRUKSI PRAKTIK:
1. Ikuti langkah-langkah secara berurutan
2. Jangan copy-paste, ketik ulang untuk memahami
3. Test setiap langkah sebelum lanjut ke langkah berikutnya
4. Tanyakan jika ada yang tidak dipahami
5. Eksperimen dengan mengubah kode setelah selesai

TUJUAN:
- Membangun aplikasi CRUD dari nol dengan MySQL
- Memahami alur data dari form ke Python ke Database
- Mengatasi error secara mandiri
- Memahami konsep database relational
"""

from flask import Flask, render_template, request, redirect, flash
import mysql.connector
from mysql.connector import Error

# LANGKAH 1: SETUP APLIKASI DASAR DAN DATABASE
app = Flask(__name__)
app.secret_key = 'rahasia_perpustakaan_mini'  # Diperlukan untuk flash message

# Konfigurasi Database MySQL
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # Sesuaikan dengan password MySQL Anda
    'database': 'perpustakaan_db',
    'charset': 'utf8mb4'
}

# LANGKAH 2: FUNGSI HELPER DATABASE
def get_db_connection():
    """
    Fungsi untuk membuat koneksi ke database MySQL
    
    KONSEP PENTING:
    - Database connection
    - Error handling
    - Connection management
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None

def execute_query(query, params=None, fetch=False):
    """
    Fungsi untuk mengeksekusi query MySQL
    
    KONSEP PENTING:
    - SQL query execution
    - Parameterized queries (mencegah SQL injection)
    - Transaction handling
    """
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
        print(f"Error executing query: {e}")
        connection.rollback()
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# LANGKAH 3: IMPLEMENTASI READ (Menampilkan Data)
@app.route('/')
def halaman_utama():
    """
    Fungsi untuk menampilkan halaman utama dengan daftar buku dari database
    
    PERTANYAAN UNTUK DIPAHAMI:
    1. Bagaimana data dari database sampai ke template HTML?
    2. Apa fungsi parameter daftar_buku?
    3. Kenapa perlu execute_query dengan fetch=True?
    4. Bagaimana menangani jika database error?
    """
    query = "SELECT * FROM buku ORDER BY id DESC"
    buku_list = execute_query(query, fetch=True)
    
    if buku_list is None:
        buku_list = []
        flash('Error mengambil data dari database!', 'error')
    
    return render_template('index.html', daftar_buku=buku_list)

# LANGKAH 4: IMPLEMENTASI CREATE (Tambah Data)
@app.route('/tambah', methods=['GET', 'POST'])
def tambah_buku():
    """
    Fungsi untuk menambah buku baru
    
    ALUR KERJA:
    1. Jika GET: Tampilkan form tambah
    2. Jika POST: Proses data dari form
    
    PERTANYAAN UNTUK DIPAHAMI:
    1. Kenapa perlu cek request.method?
    2. Dari mana request.form['judul'] datangnya?
    3. Kenapa perlu validasi?
    4. Apa fungsi flash() dan redirect()?
    """
    
    if request.method == 'POST':
        # Ambil data dari form
        judul = request.form['judul']
        pengarang = request.form['pengarang']
        tahun = int(request.form['tahun'])
        status = request.form['status']
        
        # VALIDASI SEDERHANA
        if not judul.strip():
            flash('Judul buku tidak boleh kosong!', 'error')
            return render_template('tambah.html')
        
        if not pengarang.strip():
            flash('Nama pengarang tidak boleh kosong!', 'error')
            return render_template('tambah.html')
        
        if tahun < 1000 or tahun > 2024:
            flash('Tahun tidak valid!', 'error')
            return render_template('tambah.html')
        
        # Simpan ke database menggunakan INSERT query
        query = """
        INSERT INTO buku (judul, pengarang, tahun, status) 
        VALUES (%s, %s, %s, %s)
        """
        result = execute_query(query, (judul, pengarang, tahun, status))
        
        if not result:
            flash('Error menyimpan data ke database!', 'error')
            return render_template('tambah.html')
        
        # Berikan feedback sukses
        flash(f'Buku "{judul}" berhasil ditambahkan!', 'success')
        
        # Redirect ke halaman utama
        return redirect('/')
    
    # Jika method GET, tampilkan form
    return render_template('tambah.html')

# LANGKAH 5: IMPLEMENTASI UPDATE (Edit Data)
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_buku(id):
    """
    Fungsi untuk mengedit buku berdasarkan ID
    
    PERTANYAAN UNTUK DIPAHAMI:
    1. Apa arti <int:id> dalam route?
    2. Bagaimana cara mencari buku berdasarkan ID?
    3. Kenapa perlu cek if buku_ditemukan?
    4. Bagaimana cara mengupdate data dalam list?
    """
    
    # Cari buku berdasarkan ID dari database
    query = "SELECT * FROM buku WHERE id = %s"
    result = execute_query(query, (id,), fetch=True)
    buku_ditemukan = result[0] if result else None
    
    # Jika buku tidak ditemukan
    if not buku_ditemukan:
        flash('Buku tidak ditemukan!', 'error')
        return redirect('/')
    
    if request.method == 'POST':
        # Update data buku di database
        judul = request.form['judul']
        pengarang = request.form['pengarang']
        tahun = int(request.form['tahun'])
        status = request.form['status']
        
        query = """
        UPDATE buku 
        SET judul = %s, pengarang = %s, tahun = %s, status = %s 
        WHERE id = %s
        """
        result = execute_query(query, (judul, pengarang, tahun, status, id))
        
        if result:
            flash(f'Buku "{judul}" berhasil diupdate!', 'success')
        else:
            flash('Error mengupdate data!', 'error')
        
        return redirect('/')
    
    # Jika method GET, tampilkan form edit dengan data buku
    return render_template('edit.html', buku=buku_ditemukan)

# LANGKAH 6: IMPLEMENTASI DELETE (Hapus Data)
@app.route('/hapus/<int:id>')
def hapus_buku(id):
    """
    Fungsi untuk menghapus buku berdasarkan ID
    
    PERTANYAAN UNTUK DIPAHAMI:
    1. Bagaimana cara menghapus item dari list?
    2. Kenapa perlu simpan judul sebelum dihapus?
    3. Apa yang terjadi jika ID tidak ditemukan?
    """
    
    # Ambil data buku sebelum dihapus untuk pesan
    query_select = "SELECT judul FROM buku WHERE id = %s"
    result = execute_query(query_select, (id,), fetch=True)
    
    if result:
        judul = result[0]['judul']
        
        # Hapus buku dari database
        query_delete = "DELETE FROM buku WHERE id = %s"
        delete_result = execute_query(query_delete, (id,))
        
        if delete_result:
            flash(f'Buku "{judul}" berhasil dihapus!', 'success')
        else:
            flash('Error menghapus data!', 'error')
    else:
        flash('Buku tidak ditemukan!', 'error')
    
    return redirect('/')

# FITUR TAMBAHAN: STATISTIK PERPUSTAKAAN
@app.route('/statistik')
def statistik():
    """
    Fungsi untuk menampilkan statistik perpustakaan
    
    TANTANGAN: Lengkapi fungsi ini!
    Hitung:
    1. Total buku
    2. Buku tersedia
    3. Buku dipinjam
    4. Tahun terbit tertua dan terbaru
    """
    
    # Hitung statistik menggunakan SQL aggregate functions
    query_stats = """
    SELECT 
        COUNT(*) as total_buku,
        SUM(CASE WHEN status = 'tersedia' THEN 1 ELSE 0 END) as buku_tersedia,
        SUM(CASE WHEN status = 'dipinjam' THEN 1 ELSE 0 END) as buku_dipinjam,
        MIN(tahun) as tahun_tertua,
        MAX(tahun) as tahun_terbaru
    FROM buku
    """
    
    result = execute_query(query_stats, fetch=True)
    
    if result and result[0]['total_buku'] > 0:
        data = result[0]
        total_buku = data['total_buku']
        buku_tersedia = data['buku_tersedia'] or 0
        buku_dipinjam = data['buku_dipinjam'] or 0
        tahun_tertua = data['tahun_tertua']
        tahun_terbaru = data['tahun_terbaru']
        
        stats = {
            'total': total_buku,
            'tersedia': buku_tersedia,
            'dipinjam': buku_dipinjam,
            'tahun_tertua': tahun_tertua,
            'tahun_terbaru': tahun_terbaru
        }
    else:
        stats = {
            'total': 0,
            'tersedia': 0,
            'dipinjam': 0,
            'tahun_tertua': 'Tidak ada data',
            'tahun_terbaru': 'Tidak ada data'
        }
    
    return render_template('statistik.html', stats=stats)

# FITUR TAMBAHAN: PENCARIAN BUKU
@app.route('/cari', methods=['GET', 'POST'])
def cari_buku():
    """
    Fungsi untuk mencari buku berdasarkan judul atau pengarang
    
    TANTANGAN: Lengkapi fungsi ini!
    """
    
    if request.method == 'POST':
        kata_kunci = request.form['kata_kunci']
        
        # Implementasi pencarian menggunakan SQL LIKE
        query = """
        SELECT * FROM buku 
        WHERE judul LIKE %s OR pengarang LIKE %s 
        ORDER BY judul
        """
        search_term = f"%{kata_kunci}%"
        hasil_cari = execute_query(query, (search_term, search_term), fetch=True)
        
        if hasil_cari is None:
            hasil_cari = []
            flash('Error melakukan pencarian!', 'error')
        
        return render_template('hasil_cari.html', 
                             hasil=hasil_cari, 
                             kata_kunci=kata_kunci)
    
    return render_template('cari.html')

# ROUTE UNTUK DEBUGGING
@app.route('/debug')
def debug_info():
    """
    Route khusus untuk melihat isi data buku_list
    Berguna untuk debugging
    """
    debug_html = "<h1>🐛 Debug Info</h1>"
    # Ambil data dari database untuk debugging
    query = "SELECT * FROM buku ORDER BY id"
    buku_list = execute_query(query, fetch=True)
    
    if buku_list is None:
        buku_list = []
    
    debug_html += f"<p><strong>Total buku:</strong> {len(buku_list)}</p>"
    debug_html += "<h2>Data Buku dari Database:</h2>"
    debug_html += "<pre>"
    
    for i, buku in enumerate(buku_list):
        debug_html += f"{i+1}. {buku}\n"
    
    debug_html += "</pre>"
    debug_html += '<p><a href="/">🔙 Kembali ke halaman utama</a></p>'
    
    return debug_html

# TANTANGAN UNTUK SISWA

# TANTANGAN 1: Buat route untuk detail buku
@app.route('/detail/<int:id>')
def detail_buku(id):
    """
    TODO: Lengkapi fungsi ini!
    
    Fungsi ini harus:
    1. Mencari buku berdasarkan ID
    2. Menampilkan detail lengkap buku
    3. Jika tidak ditemukan, redirect ke halaman utama dengan pesan error
    """
    # Cari buku berdasarkan ID dari database
    query = "SELECT * FROM buku WHERE id = %s"
    result = execute_query(query, (id,), fetch=True)
    buku_ditemukan = result[0] if result else None
    
    if not buku_ditemukan:
        flash('Buku tidak ditemukan!', 'error')
        return redirect('/')
    
    return render_template('detail.html', buku=buku_ditemukan)

# TANTANGAN 2: Buat route untuk mengubah status buku
@app.route('/ubah_status/<int:id>')
def ubah_status(id):
    """
    TODO: Lengkapi fungsi ini!
    
    Fungsi ini harus:
    1. Mencari buku berdasarkan ID
    2. Mengubah status dari 'tersedia' ke 'dipinjam' atau sebaliknya
    3. Memberikan pesan feedback
    4. Redirect ke halaman utama
    """
    # Ambil data buku saat ini
    query_select = "SELECT * FROM buku WHERE id = %s"
    result = execute_query(query_select, (id,), fetch=True)
    
    if result:
        buku = result[0]
        status_baru = 'dipinjam' if buku['status'] == 'tersedia' else 'tersedia'
        
        # Update status di database
        query_update = "UPDATE buku SET status = %s WHERE id = %s"
        update_result = execute_query(query_update, (status_baru, id))
        
        if update_result:
            if status_baru == 'dipinjam':
                flash(f'Buku "{buku["judul"]}" berhasil dipinjam!', 'success')
            else:
                flash(f'Buku "{buku["judul"]}" berhasil dikembalikan!', 'success')
        else:
            flash('Error mengubah status buku!', 'error')
    else:
        flash('Buku tidak ditemukan!', 'error')
    
    return redirect('/')

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 PRAKTIK PERTEMUAN 2: MEMBANGUN APLIKASI CLIENT-SERVER")
    print("📚 Aplikasi: Perpustakaan Mini dengan MySQL Database")
    print("="*60)
    print("\n📍 Server berjalan di: http://localhost:5000")
    print("\n🔗 Route yang tersedia:")
    print("   /           - Halaman utama (daftar buku)")
    print("   /tambah     - Tambah buku baru")
    print("   /edit/<id>  - Edit buku")
    print("   /hapus/<id> - Hapus buku")
    print("   /detail/<id>- Detail buku (TANTANGAN)")
    print("   /ubah_status/<id> - Ubah status buku (TANTANGAN)")
    print("   /cari       - Cari buku (TANTANGAN)")
    print("   /statistik  - Statistik perpustakaan (TANTANGAN)")
    print("   /debug      - Debug info")
    print("\n⚠️  PENTING:")
    print("   1. Setup database MySQL dan buat database 'perpustakaan_db'")
    print("   2. Buat tabel 'buku' dengan kolom: id, judul, pengarang, tahun, status")
    print("   3. Install mysql-connector-python: pip install mysql-connector-python")
    print("   4. Sesuaikan konfigurasi DB_CONFIG dengan setting MySQL Anda")
    print("   5. Buat folder 'templates' di direktori yang sama")
    print("   6. Buat file HTML yang diperlukan di folder templates")
    print("   7. Test setiap fitur setelah implementasi")
    print("   8. Gunakan /debug untuk melihat data")
    print("\n⌨️  Tekan Ctrl+C untuk menghentikan server")
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000)

"""
📝 CHECKLIST UNTUK SISWA:

□ LANGKAH 1: Setup aplikasi dasar
  □ Import Flask dan library yang diperlukan
  □ Buat instance Flask app
  □ Set secret_key untuk flash message

□ LANGKAH 2: Setup database dan fungsi helper
  □ Buat database MySQL 'perpustakaan_db'
  □ Buat tabel 'buku' dengan kolom yang sesuai
  □ Implementasi fungsi get_db_connection()
  □ Implementasi fungsi execute_query()

□ LANGKAH 3: Implementasi READ
  □ Buat route '/' untuk halaman utama
  □ Kirim data buku_list ke template
  □ Buat file templates/index.html

□ LANGKAH 4: Implementasi CREATE
  □ Buat route '/tambah' dengan method GET dan POST
  □ Handle form submission
  □ Tambahkan validasi
  □ Buat file templates/tambah.html

□ LANGKAH 5: Implementasi UPDATE
  □ Buat route '/edit/<int:id>'
  □ Cari buku berdasarkan ID
  □ Update data buku
  □ Buat file templates/edit.html

□ LANGKAH 6: Implementasi DELETE
  □ Buat route '/hapus/<int:id>'
  □ Hapus buku dari list
  □ Berikan feedback

□ TESTING:
  □ Test semua fitur CRUD
  □ Test validasi form
  □ Test error handling
  □ Test flash messages

□ TANTANGAN (OPSIONAL):
  □ Implementasi pencarian
  □ Implementasi statistik
  □ Implementasi detail buku
  □ Implementasi ubah status

🎯 TUJUAN AKHIR:
   Aplikasi perpustakaan mini yang berfungsi penuh dengan fitur CRUD
   dan pemahaman yang mendalam tentang alur kerja Flask.

💡 TIPS SUKSES:
   1. Ketik ulang kode, jangan copy-paste
   2. Test setiap langkah sebelum lanjut
   3. Baca dan pahami setiap komentar
   4. Tanyakan jika ada yang tidak jelas
   5. Eksperimen setelah selesai
"""

# TEMPLATE HTML YANG DIPERLUKAN:
# 1. templates/index.html - Halaman utama
# 2. templates/tambah.html - Form tambah buku
# 3. templates/edit.html - Form edit buku
# 4. templates/detail.html - Detail buku (tantangan)
# 5. templates/cari.html - Form pencarian (tantangan)
# 6. templates/hasil_cari.html - Hasil pencarian (tantangan)
# 7. templates/statistik.html - Statistik (tantangan)