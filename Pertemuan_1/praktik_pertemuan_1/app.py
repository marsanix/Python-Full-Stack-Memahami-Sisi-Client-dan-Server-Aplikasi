# Aplikasi Flask untuk Docker - Praktik Pertemuan 1
# Versi yang kompatibel dengan Docker environment

from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error
import os
import time
from datetime import datetime
from config import DB_CONFIG, config

# =====================================================
# FUNGSI DATABASE CONNECTION
# =====================================================

def create_connection():
    """Membuat koneksi ke database MySQL dengan retry mechanism untuk Docker"""
    max_retries = 30
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            connection = mysql.connector.connect(**DB_CONFIG)
            if connection.is_connected():
                print(f"✅ Berhasil terhubung ke MySQL database (attempt {attempt + 1})")
                return connection
        except Error as e:
            print(f"❌ Attempt {attempt + 1}/{max_retries} - Error connecting to MySQL: {e}")
            if attempt < max_retries - 1:
                print(f"⏳ Menunggu {retry_delay} detik sebelum mencoba lagi...")
                time.sleep(retry_delay)
            else:
                print("❌ Gagal terhubung ke database setelah semua percobaan")
                return None
    
    return None

def execute_query(query, params=None, fetch=False):
    """Eksekusi query dengan error handling"""
    connection = create_connection()
    if connection is None:
        return None
    
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params)
        
        if fetch:
            result = cursor.fetchall()
            return result
        else:
            connection.commit()
            return True
            
    except Error as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def test_connection():
    """Test koneksi database"""
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print("✅ Koneksi database berhasil!")
            return True
        except Error as e:
            print(f"Error testing connection: {e}")
            return False
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
    else:
        print("❌ Koneksi database gagal!")
        return False

# =====================================================
# FUNGSI CRUD OPERATIONS (MySQL)
# =====================================================

def get_all_siswa(filter_nama=None):
    """READ: Mengambil semua data siswa dengan filter opsional berdasarkan nama"""
    if filter_nama:
        query = "SELECT * FROM siswa WHERE nama LIKE %s ORDER BY id DESC"
        search_term = f"%{filter_nama}%"
        result = execute_query(query, (search_term,), fetch=True)
    else:
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

# =====================================================
# FLASK APPLICATION
# =====================================================

def create_app(config_name='default'):
    """Factory function untuk membuat Flask app"""
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(config[config_name])
    
    # Routes
    @app.route('/')
    def halaman_utama():
        """Halaman utama dengan filter nama"""
        filter_nama = request.args.get('filter_nama', '').strip()
        
        if not filter_nama:
            filter_nama = None
        
        data_siswa = get_all_siswa(filter_nama=filter_nama)
        
        return render_template('index.html', 
                             siswa_list=data_siswa, 
                             current_filter=filter_nama)

    @app.route('/tambah', methods=['GET', 'POST'])
    def tambah_siswa():
        """Tambah siswa baru"""
        if request.method == 'POST':
            nama = request.form['nama']
            kelas = request.form['kelas']
            umur = int(request.form['umur'])
            alamat = request.form['alamat']
            
            new_siswa = add_siswa(nama, kelas, umur, alamat)
            
            if new_siswa:
                flash(f'✅ Siswa {nama} berhasil ditambahkan!', 'success')
                return redirect(url_for('halaman_utama'))
            else:
                flash('❌ Gagal menambahkan siswa. Silakan coba lagi.', 'error')
        
        return render_template('tambah.html')

    @app.route('/edit/<int:id>', methods=['GET', 'POST'])
    def edit_siswa(id):
        """Edit data siswa"""
        siswa = get_siswa_by_id(id)
        if not siswa:
            flash('❌ Data siswa tidak ditemukan!', 'error')
            return redirect(url_for('halaman_utama'))
        
        if request.method == 'POST':
            nama = request.form['nama']
            kelas = request.form['kelas']
            umur = int(request.form['umur'])
            alamat = request.form['alamat']
            
            updated_siswa = update_siswa(id, nama, kelas, umur, alamat)
            
            if updated_siswa:
                flash(f'✅ Data siswa {nama} berhasil diupdate!', 'success')
                return redirect(url_for('halaman_utama'))
            else:
                flash('❌ Gagal mengupdate data siswa.', 'error')
        
        return render_template('edit.html', siswa=siswa)

    @app.route('/hapus/<int:id>')
    @app.route('/hapus/<int:id>/<konfirmasi>')
    def hapus_siswa(id, konfirmasi=None):
        """Hapus data siswa"""
        siswa = get_siswa_by_id(id)
        if not siswa:
            flash('❌ Data siswa tidak ditemukan!', 'error')
            return redirect(url_for('halaman_utama'))
        
        if konfirmasi == 'ya':
            deleted_siswa = delete_siswa(id)
            if deleted_siswa:
                flash(f'✅ Data siswa {deleted_siswa["nama"]} berhasil dihapus!', 'success')
            else:
                flash('❌ Gagal menghapus data siswa.', 'error')
            return redirect(url_for('halaman_utama'))
        
        return render_template('konfirmasi_hapus.html', siswa=siswa)

    @app.route('/cari', methods=['GET', 'POST'])
    def cari_siswa():
        """Halaman pencarian siswa"""
        if request.method == 'POST':
            keyword = request.form['keyword']
            hasil_cari = search_siswa(keyword)
            return render_template('hasil_cari.html', 
                                 siswa_list=hasil_cari, 
                                 keyword=keyword)
        
        return render_template('cari.html')

    @app.route('/statistik')
    def statistik_siswa():
        """Halaman statistik siswa"""
        data_siswa = get_all_siswa()
        
        if data_siswa:
            total_siswa = len(data_siswa)
            kelas_list = list(set([siswa['kelas'] for siswa in data_siswa]))
            rata_rata_umur = sum([siswa['umur'] for siswa in data_siswa]) / total_siswa
            
            statistik = {
                'total_siswa': total_siswa,
                'jumlah_kelas': len(kelas_list),
                'rata_rata_umur': round(rata_rata_umur, 1),
                'kelas_list': kelas_list,
                'data_siswa': data_siswa
            }
        else:
            statistik = {
                'total_siswa': 0,
                'jumlah_kelas': 0,
                'rata_rata_umur': 0,
                'kelas_list': [],
                'data_siswa': []
            }
        
        return render_template('statistik.html', statistik=statistik)

    @app.route('/debug')
    def debug_info():
        """Debug information"""
        return {
            'database_config': {k: v for k, v in DB_CONFIG.items() if k != 'password'},
            'environment': os.environ.get('FLASK_ENV', 'development'),
            'debug_mode': app.debug
        }

    @app.route('/health')
    def health_check():
        """Health check endpoint untuk Docker"""
        try:
            if test_connection():
                return {'status': 'healthy', 'database': 'connected'}, 200
            else:
                return {'status': 'unhealthy', 'database': 'disconnected'}, 503
        except Exception as e:
            return {'status': 'error', 'message': str(e)}, 500

    return app

# =====================================================
# MAIN APPLICATION
# =====================================================

if __name__ == '__main__':
    print("\n" + "="*50)
    print("PRAKTIK PERTEMUAN 1: APLIKASI CRUD DENGAN DOCKER")
    print("="*50)
    
    # Tentukan environment
    env = os.getenv('FLASK_ENV', 'development')
    print(f"🌍 Environment: {env}")
    print(f"🗄️  Database Host: {DB_CONFIG['host']}")
    print(f"🗄️  Database Name: {DB_CONFIG['database']}")
    
    # Test koneksi database
    if test_connection():
        print("✅ Database connection successful!")
        
        # Buat aplikasi Flask
        app = create_app(env)
        
        print("🚀 Server akan berjalan di: http://localhost:5000")
        print("\n📋 Route yang tersedia:")
        print("- / : Halaman utama (daftar siswa)")
        print("- /tambah : Tambah siswa baru")
        print("- /edit/<id> : Edit siswa")
        print("- /hapus/<id> : Hapus siswa")
        print("- /cari : Cari siswa")
        print("- /statistik : Statistik siswa")
        print("- /debug : Debug info")
        print("- /health : Health check")
        print("\n🐳 Untuk Docker: http://localhost:5000")
        print("🗄️  phpMyAdmin: http://localhost:8080")
        print("\nTekan Ctrl+C untuk menghentikan server")
        print("="*50 + "\n")
        
        # Jalankan aplikasi
        app.run(host='0.0.0.0', port=5000, debug=app.config['DEBUG'])
    else:
        print("\n❌ Tidak dapat menjalankan aplikasi karena koneksi database gagal!")
        print("🐳 Jika menggunakan Docker, pastikan service MySQL sudah running.")
        print("💻 Jika local development, pastikan MySQL server berjalan.")
        print("="*50 + "\n")
        exit(1)