# Praktik Pertemuan 4: Proyek Mandiri & Kreativitas dengan MySQL
# Durasi: 90 menit
# Target: Siswa SMP - Membuat aplikasi web dengan MySQL database

"""
🎯 TUJUAN PRAKTIK:
1. Merancang dan membangun aplikasi web dengan MySQL database
2. Mengintegrasikan semua konsep MySQL yang telah dipelajari
3. Menambahkan fitur kreatif dengan database operations
4. Melakukan testing dan debugging MySQL secara mandiri
5. Mempresentasikan hasil karya database dengan percaya diri

📋 STRUKTUR PRAKTIK:
- Database Design & Setup (15 menit)
- Core Development dengan MySQL (45 menit)
- Creative Features dengan Analytics (20 menit)
- Testing & Polish Database (10 menit)

💡 TIPS SUKSES:
- Mulai dengan schema database yang sederhana
- Focus pada CRUD operations dulu, baru fitur advanced
- Jangan takut bereksperimen dengan MySQL queries
- Ask for help jika stuck > 10 menit dengan database
"""

# ============================================================================
# TEMPLATE STARTER CODE
# ============================================================================

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import mysql.connector
from mysql.connector import Error
import os
from datetime import datetime
import random
import logging

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Ganti dengan secret key unikmu

# Konfigurasi MySQL Database
DB_CONFIG = {
    'host': 'localhost',
    'database': 'siswa_db',  # Gunakan database yang sudah dibuat
    'user': 'root',
    'password': '',  # Sesuaikan dengan password MySQL Anda
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}

UPLOAD_FOLDER = 'static/uploads'

# Setup logging untuk debugging
logging.basicConfig(
    filename='project.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ============================================================================
# DATABASE HELPER FUNCTIONS WITH MYSQL
# ============================================================================

class DatabaseHelper:
    """Helper class untuk operasi database MySQL"""
    
    def __init__(self, config=DB_CONFIG):
        self.config = config
        self.connection = None
    
    def connect(self):
        """Buat koneksi ke MySQL database"""
        try:
            self.connection = mysql.connector.connect(**self.config)
            if self.connection.is_connected():
                logging.info("Database connection established")
                return True
        except Error as e:
            logging.error(f"Error connecting to MySQL: {e}")
            print(f"❌ Database connection failed: {e}")
            return False
    
    def disconnect(self):
        """Tutup koneksi database"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logging.info("Database connection closed")
    
    def execute_query(self, query, params=None, fetch=False, fetch_one=False):
        """Eksekusi query dengan error handling"""
        try:
            if not self.connection or not self.connection.is_connected():
                if not self.connect():
                    return None
            
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params or ())
            
            if fetch_one:
                result = cursor.fetchone()
            elif fetch:
                result = cursor.fetchall()
            else:
                self.connection.commit()
                result = cursor.lastrowid or cursor.rowcount
            
            cursor.close()
            return result
            
        except mysql.connector.IntegrityError as e:
            logging.error(f"Integrity error: {e}")
            self.connection.rollback()
            raise e
        except mysql.connector.DataError as e:
            logging.error(f"Data error: {e}")
            self.connection.rollback()
            raise e
        except Error as e:
            logging.error(f"MySQL error: {e}")
            if self.connection:
                self.connection.rollback()
            raise e
    
    def create_project_table(self, table_name, schema):
        """Buat tabel untuk proyek (dinamis)"""
        try:
            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({schema})"
            self.execute_query(query)
            logging.info(f"Table {table_name} created successfully")
            return True
        except Exception as e:
            logging.error(f"Error creating table {table_name}: {e}")
            return False
    
    def add_item(self, table_name, item_data):
        """Tambah item baru ke tabel"""
        try:
            columns = ', '.join(item_data.keys())
            placeholders = ', '.join(['%s'] * len(item_data))
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
            
            new_id = self.execute_query(query, list(item_data.values()))
            logging.info(f"Item added to {table_name} with ID: {new_id}")
            return new_id
        except Exception as e:
            logging.error(f"Error adding item to {table_name}: {e}")
            raise e
    
    def get_all_items(self, table_name, order_by='id'):
        """Ambil semua items dari tabel"""
        try:
            query = f"SELECT * FROM {table_name} ORDER BY {order_by}"
            return self.execute_query(query, fetch=True) or []
        except Exception as e:
            logging.error(f"Error fetching items from {table_name}: {e}")
            return []
    
    def get_item_by_id(self, table_name, item_id):
        """Ambil item berdasarkan ID"""
        try:
            query = f"SELECT * FROM {table_name} WHERE id = %s"
            return self.execute_query(query, (item_id,), fetch_one=True)
        except Exception as e:
            logging.error(f"Error fetching item {item_id} from {table_name}: {e}")
            return None
    
    def update_item(self, table_name, item_id, update_data):
        """Update item berdasarkan ID"""
        try:
            set_clause = ', '.join([f"{key} = %s" for key in update_data.keys()])
            query = f"UPDATE {table_name} SET {set_clause} WHERE id = %s"
            params = list(update_data.values()) + [item_id]
            
            rows_affected = self.execute_query(query, params)
            logging.info(f"Updated item {item_id} in {table_name}")
            return rows_affected > 0
        except Exception as e:
            logging.error(f"Error updating item {item_id} in {table_name}: {e}")
            raise e
    
    def delete_item(self, table_name, item_id):
        """Hapus item berdasarkan ID"""
        try:
            query = f"DELETE FROM {table_name} WHERE id = %s"
            rows_affected = self.execute_query(query, (item_id,))
            logging.info(f"Deleted item {item_id} from {table_name}")
            return rows_affected > 0
        except Exception as e:
            logging.error(f"Error deleting item {item_id} from {table_name}: {e}")
            raise e
    
    def search_items(self, table_name, search_field, query_text):
        """Cari items berdasarkan field tertentu"""
        try:
            query = f"SELECT * FROM {table_name} WHERE {search_field} LIKE %s ORDER BY id"
            search_pattern = f"%{query_text}%"
            return self.execute_query(query, (search_pattern,), fetch=True) or []
        except Exception as e:
            logging.error(f"Error searching in {table_name}: {e}")
            return []
    
    def get_statistics(self, table_name):
        """Ambil statistik dari tabel"""
        try:
            # Total records
            count_query = f"SELECT COUNT(*) as total FROM {table_name}"
            total_result = self.execute_query(count_query, fetch_one=True)
            total_items = total_result['total'] if total_result else 0
            
            # Latest update (jika ada kolom updated_at)
            latest_query = f"""
            SELECT updated_at FROM {table_name} 
            WHERE updated_at IS NOT NULL 
            ORDER BY updated_at DESC LIMIT 1
            """
            latest_result = self.execute_query(latest_query, fetch_one=True)
            last_updated = latest_result['updated_at'] if latest_result else 'N/A'
            
            # Database size info
            size_query = """
            SELECT 
                ROUND(((data_length + index_length) / 1024 / 1024), 2) AS 'size_mb'
            FROM information_schema.tables 
            WHERE table_schema = %s AND table_name = %s
            """
            size_result = self.execute_query(size_query, (self.config['database'], table_name), fetch_one=True)
            table_size = f"{size_result['size_mb']} MB" if size_result and size_result['size_mb'] else "< 0.01 MB"
            
            return {
                'total_items': total_items,
                'last_updated': str(last_updated),
                'table_size': table_size,
                'database_name': self.config['database']
            }
        except Exception as e:
            logging.error(f"Error getting statistics for {table_name}: {e}")
            return {
                'total_items': 0,
                'last_updated': 'Error',
                'table_size': 'Unknown',
                'database_name': self.config['database']
            }

# Inisialisasi database helper
db = DatabaseHelper()

# ============================================================================
# VALIDATION FUNCTIONS
# ============================================================================

def validate_required(value, field_name):
    """
    Validasi field yang wajib diisi
    Args: value (str), field_name (str)
    Returns: tuple (bool, str) - (is_valid, error_message)
    """
    if not value or not value.strip():
        return False, f"{field_name} tidak boleh kosong"
    return True, value.strip()

def validate_length(value, min_len=1, max_len=255, field_name="Field"):
    """
    Validasi panjang string
    Args: value (str), min_len (int), max_len (int), field_name (str)
    Returns: tuple (bool, str) - (is_valid, error_message)
    """
    if len(value) < min_len:
        return False, f"{field_name} minimal {min_len} karakter"
    if len(value) > max_len:
        return False, f"{field_name} maksimal {max_len} karakter"
    return True, value

def validate_email(email, table_name='siswa', exclude_id=None):
    """
    Validasi format email dengan MySQL UNIQUE constraint check
    Args: email (str), table_name (str), exclude_id (int)
    Returns: tuple (bool, str) - (is_valid, error_message_or_clean_email)
    """
    import re
    
    if not email or not email.strip():
        return False, "Email tidak boleh kosong (NOT NULL constraint)"
    
    email = email.strip().lower()
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False, "Format email tidak valid"
    
    # Cek UNIQUE constraint di database
    try:
        if exclude_id:
            query = f"SELECT COUNT(*) as count FROM {table_name} WHERE email = %s AND id != %s"
            params = (email, exclude_id)
        else:
            query = f"SELECT COUNT(*) as count FROM {table_name} WHERE email = %s"
            params = (email,)
        
        result = db.execute_query(query, params, fetch_one=True)
        if result and result['count'] > 0:
            return False, "Email sudah terdaftar (UNIQUE constraint)"
    except Exception as e:
        logging.error(f"Error checking email uniqueness: {e}")
        return False, "Error validasi email di database"
    
    return True, email

# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def get_random_color():
    """
    Generate random color untuk theme
    Returns: str - Hex color code
    """
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7', 
              '#DDA0DD', '#98D8C8', '#F7DC6F', '#BB8FCE', '#85C1E9']
    return random.choice(colors)

def format_date(date_string):
    """
    Format tanggal untuk display
    Args: date_string (str) - Format YYYY-MM-DD
    Returns: str - Format yang lebih readable
    """
    try:
        date_obj = datetime.strptime(date_string, '%Y-%m-%d')
        return date_obj.strftime('%d %B %Y')
    except:
        return date_string

def search_items(items, query, search_fields):
    """
    Search items berdasarkan query
    Args: items (list), query (str), search_fields (list)
    Returns: list - Filtered items
    """
    if not query:
        return items
    
    query = query.lower()
    results = []
    
    for item in items:
        for field in search_fields:
            if field in item and query in str(item[field]).lower():
                results.append(item)
                break
    
    return results

# ============================================================================
# MAIN ROUTES - CUSTOMIZE SESUAI PROYEKMU!
# ============================================================================

@app.route('/')
def home():
    """
    Halaman utama - Dashboard dengan MySQL
    TODO: Sesuaikan dengan tema aplikasimu
    """
    try:
        # Gunakan tabel yang sesuai dengan proyek Anda
        table_name = 'siswa'  # Ganti sesuai proyek: 'products', 'books', dll
        
        # Ambil query search jika ada
        search_query = request.args.get('search', '')
        
        if search_query:
            # Search berdasarkan nama (sesuaikan field dengan tabel Anda)
            items = db.search_items(table_name, 'nama', search_query)
        else:
            items = db.get_all_items(table_name)
        
        stats = db.get_statistics(table_name)
        
        return render_template('index.html', 
                             items=items, 
                             search_query=search_query,
                             stats=stats)
    except Exception as e:
        logging.error(f"Error loading home page: {e}")
        flash(f'❌ Error loading data: {str(e)}', 'error')
        return render_template('index.html', items=[], search_query='', stats={})

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    """
    Tambah item baru dengan MySQL
    TODO: Sesuaikan form fields dengan kebutuhan aplikasimu
    """
    if request.method == 'POST':
        # TODO: Ambil data dari form sesuai dengan tabel MySQL Anda
        # Contoh untuk tabel siswa:
        nama = request.form.get('nama', '').strip()
        umur = request.form.get('umur', '')
        email = request.form.get('email', '').strip()
        kelas = request.form.get('kelas', '').strip()
        
        # Validasi data
        errors = []
        
        # Validasi nama
        is_valid, result = validate_required(nama, 'Nama')
        if not is_valid:
            errors.append(result)
        else:
            nama = result
            is_valid, result = validate_length(nama, 2, 100, 'Nama')
            if not is_valid:
                errors.append(result)
        
        # Validasi umur
        is_valid, result = validate_required(umur, 'Umur')
        if not is_valid:
            errors.append(result)
        else:
            try:
                umur = int(umur)
                if umur < 10 or umur > 18:
                    errors.append('Umur harus antara 10-18 tahun')
            except ValueError:
                errors.append('Umur harus berupa angka')
        
        # Validasi email dengan database check
        is_valid, result = validate_email(email, 'siswa')
        if not is_valid:
            errors.append(result)
        else:
            email = result
        
        # Validasi kelas
        is_valid, result = validate_required(kelas, 'Kelas')
        if not is_valid:
            errors.append(result)
        
        # Jika ada error, kembali ke form
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('add.html')
        
        # Buat item baru untuk MySQL
        new_item = {
            'nama': nama,
            'umur': umur,
            'email': email,
            'kelas': kelas,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        
        # TODO: Tambahkan field lain sesuai tabel MySQL Anda
        # Contoh:
        # new_item['alamat'] = request.form.get('alamat', '')
        # new_item['no_hp'] = request.form.get('no_hp', '')
        
        # Simpan ke database MySQL
        try:
            table_name = 'siswa'  # Ganti sesuai tabel proyek Anda
            new_id = db.add_item(table_name, new_item)
            
            if new_id:
                flash(f'✅ {nama} berhasil ditambahkan dengan ID {new_id}!', 'success')
                return redirect(url_for('home'))
            else:
                flash('❌ Gagal menyimpan data', 'error')
                
        except mysql.connector.IntegrityError as e:
            if e.errno == 1062:  # Duplicate entry
                flash('❌ Email sudah terdaftar! (UNIQUE constraint)', 'error')
            else:
                flash(f'❌ Data melanggar aturan database: {e.msg}', 'error')
        except mysql.connector.DataError as e:
            flash(f'❌ Format data tidak sesuai: {e.msg}', 'error')
        except Exception as e:
            logging.error(f"Error adding item: {e}")
            flash(f'❌ Error sistem: {str(e)}', 'error')
    
    return render_template('add.html')

@app.route('/edit/<int:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    """
    Edit item berdasarkan ID
    TODO: Sesuaikan dengan field aplikasimu
    """
    data = load_data()
    
    # Cari item berdasarkan ID
    item = None
    for i, current_item in enumerate(data['items']):
        if current_item['id'] == item_id:
            item = current_item
            item_index = i
            break
    
    if not item:
        flash('❌ Item tidak ditemukan', 'error')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        # TODO: Update field sesuai dengan aplikasimu
        nama = request.form.get('nama', '')
        deskripsi = request.form.get('deskripsi', '')
        kategori = request.form.get('kategori', '')
        
        # Validasi (sama seperti add_item)
        errors = []
        
        is_valid, result = validate_required(nama, 'Nama')
        if not is_valid:
            errors.append(result)
        else:
            nama = result
        
        if errors:
            for error in errors:
                flash(error, 'error')
            return render_template('edit.html', item=item)
        
        # Update item
        data['items'][item_index].update({
            'nama': nama,
            'deskripsi': deskripsi,
            'kategori': kategori,
            'tanggal_diupdate': datetime.now().strftime('%Y-%m-%d')
        })
        
        if save_data(data):
            flash(f'✅ {nama} berhasil diupdate!', 'success')
            return redirect(url_for('home'))
        else:
            flash('❌ Gagal mengupdate data', 'error')
    
    return render_template('edit.html', item=item)

@app.route('/delete/<int:item_id>')
def delete_item(item_id):
    """
    Hapus item berdasarkan ID
    """
    data = load_data()
    
    # Cari dan hapus item
    for i, item in enumerate(data['items']):
        if item['id'] == item_id:
            deleted_item = data['items'].pop(i)
            
            if save_data(data):
                flash(f'✅ {deleted_item.get("nama", "Item")} berhasil dihapus!', 'success')
            else:
                flash('❌ Gagal menghapus data', 'error')
            break
    else:
        flash('❌ Item tidak ditemukan', 'error')
    
    return redirect(url_for('home'))

# ============================================================================
# CREATIVE ROUTES - TAMBAHKAN FITUR UNIKMU DI SINI!
# ============================================================================

@app.route('/stats')
def show_stats():
    """
    Halaman statistik MySQL - Contoh fitur kreatif
    TODO: Sesuaikan dengan data MySQL aplikasimu
    """
    try:
        table_name = 'siswa'  # Ganti sesuai tabel proyek Anda
        
        # Hitung statistik dengan MySQL queries
        stats = {
            'total_items': 0,
            'created_today': 0,
            'categories': [],
            'recent_items': [],
            'age_distribution': []
        }
        
        # Total items
        total_query = f"SELECT COUNT(*) as total FROM {table_name}"
        total_result = db.execute_query(total_query, fetch_one=True)
        stats['total_items'] = total_result['total'] if total_result else 0
        
        # Items created today
        today = datetime.now().strftime('%Y-%m-%d')
        today_query = f"SELECT COUNT(*) as today FROM {table_name} WHERE DATE(created_at) = %s"
        today_result = db.execute_query(today_query, (today,), fetch_one=True)
        stats['created_today'] = today_result['today'] if today_result else 0
        
        # Group by categories (contoh: kelas)
        category_query = f"""
        SELECT kelas, COUNT(*) as count 
        FROM {table_name} 
        GROUP BY kelas 
        ORDER BY count DESC
        """
        stats['categories'] = db.execute_query(category_query, fetch=True) or []
        
        # Recent items (5 terbaru)
        recent_query = f"""
        SELECT nama, kelas, created_at 
        FROM {table_name} 
        ORDER BY created_at DESC 
        LIMIT 5
        """
        stats['recent_items'] = db.execute_query(recent_query, fetch=True) or []
        
        # Age distribution (contoh analytics)
        age_query = f"""
        SELECT 
            CASE 
                WHEN umur BETWEEN 10 AND 12 THEN '10-12 tahun'
                WHEN umur BETWEEN 13 AND 15 THEN '13-15 tahun'
                WHEN umur BETWEEN 16 AND 18 THEN '16-18 tahun'
                ELSE 'Lainnya'
            END as age_group,
            COUNT(*) as count
        FROM {table_name}
        GROUP BY age_group
        ORDER BY count DESC
        """
        stats['age_distribution'] = db.execute_query(age_query, fetch=True) or []
        
        return render_template('stats.html', stats=stats)
        
    except Exception as e:
        logging.error(f"Error loading stats: {e}")
        flash(f'❌ Error loading statistics: {str(e)}', 'error')
        return render_template('stats.html', stats={})

@app.route('/random')
def random_item():
    """
    Tampilkan item random - Contoh fitur fun
    """
    data = load_data()
    items = data['items']
    
    if not items:
        flash('📭 Belum ada item untuk ditampilkan', 'info')
        return redirect(url_for('home'))
    
    random_item = random.choice(items)
    return render_template('random.html', item=random_item)

@app.route('/export')
def export_data():
    """
    Export data MySQL ke JSON - Contoh fitur utilitas
    """
    try:
        table_name = 'siswa'  # Ganti sesuai tabel proyek Anda
        items = db.get_all_items(table_name)
        
        # Convert datetime objects to string for JSON serialization
        import json
        from datetime import datetime, date
        
        def json_serial(obj):
            if isinstance(obj, (datetime, date)):
                return obj.isoformat()
            raise TypeError(f"Type {type(obj)} not serializable")
        
        # Create export data
        export_data = {
            'table_name': table_name,
            'export_date': datetime.now().isoformat(),
            'total_records': len(items),
            'database_info': {
                'host': db.config['host'],
                'database': db.config['database']
            },
            'data': items
        }
        
        # Simpan ke file JSON
        export_filename = f"export_{table_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(export_filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False, default=json_serial)
        
        flash(f'✅ Data MySQL berhasil diekspor ke {export_filename}', 'success')
        logging.info(f"Data exported to {export_filename}")
        
    except Exception as e:
        logging.error(f"Error exporting data: {e}")
        flash(f'❌ Gagal mengekspor data: {e}', 'error')
    
    return redirect(url_for('home'))

@app.route('/theme')
def change_theme():
    """
    Ganti tema warna - Contoh fitur personalisasi
    """
    color = get_random_color()
    flash(f'🎨 Tema berubah! Warna baru: {color}', 'info')
    
    # TODO: Implementasi penyimpanan preferensi tema
    # Bisa disimpan di session atau database
    
    return redirect(url_for('home'))

# ============================================================================
# TEMPLATE EXAMPLES - CONTOH STRUKTUR HTML
# ============================================================================

"""
Buat folder 'templates' dan file-file HTML berikut:

1. templates/base.html - Template dasar
2. templates/index.html - Halaman utama
3. templates/add.html - Form tambah item
4. templates/edit.html - Form edit item
5. templates/stats.html - Halaman statistik
6. templates/random.html - Halaman item random

Contoh base.html:

<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}My Amazing App{% endblock %}</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .navbar {
            background: #2c3e50;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
        }
        .navbar a {
            color: white;
            text-decoration: none;
            margin-right: 20px;
            padding: 8px 15px;
            border-radius: 5px;
            transition: background 0.3s;
        }
        .navbar a:hover {
            background: #34495e;
        }
        .btn {
            background: #4CAF50;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            margin: 5px;
            transition: background 0.3s;
        }
        .btn:hover { background: #45a049; }
        .btn-danger { background: #f44336; }
        .btn-danger:hover { background: #da190b; }
        .btn-info { background: #2196F3; }
        .btn-info:hover { background: #1976D2; }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
        }
        input, textarea, select {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            box-sizing: border-box;
            font-size: 14px;
        }
        .alert {
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
            border-left: 5px solid;
        }
        .alert-success { 
            background: #d4edda; 
            color: #155724; 
            border-color: #28a745;
        }
        .alert-error { 
            background: #f8d7da; 
            color: #721c24; 
            border-color: #dc3545;
        }
        .alert-info { 
            background: #d1ecf1; 
            color: #0c5460; 
            border-color: #17a2b8;
        }
        .card {
            border: 1px solid #ddd;
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 15px;
            background: #f9f9f9;
        }
        .card h3 {
            margin-top: 0;
            color: #2c3e50;
        }
        .search-box {
            margin-bottom: 20px;
        }
        .search-box input {
            display: inline-block;
            width: 70%;
            margin-right: 10px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        .stat-card {
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 20px;
            border-radius: 10px;
            text-align: center;
        }
        .stat-number {
            font-size: 2em;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="navbar">
            <a href="{{ url_for('home') }}">🏠 Home</a>
            <a href="{{ url_for('add_item') }}">➕ Tambah</a>
            <a href="{{ url_for('show_stats') }}">📊 Statistik</a>
            <a href="{{ url_for('random_item') }}">🎲 Random</a>
            <a href="{{ url_for('export_data') }}">📤 Export</a>
            <a href="{{ url_for('change_theme') }}">🎨 Tema</a>
        </div>
        
        <h1>{% block header %}My Amazing App{% endblock %}</h1>
        
        <!-- Flash Messages -->
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="alert alert-{{ category }}">
                        {{ message }}
                    </div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        
        {% block content %}{% endblock %}
        
        <footer style="margin-top: 40px; text-align: center; color: #666; border-top: 1px solid #eee; padding-top: 20px;">
            <p>Made with ❤️ by [Your Name] | Python Full-Stack Project</p>
        </footer>
    </div>
</body>
</html>
"""

# ============================================================================
# EXERCISE CHALLENGES - TANTANGAN UNTUK SISWA
# ============================================================================

"""
🎯 TANTANGAN WAJIB (Pilih minimal 3):

1. 🔍 SEARCH FUNCTIONALITY
   - Tambahkan search box di halaman utama
   - Implementasikan pencarian berdasarkan nama/deskripsi
   - Bonus: Highlight hasil pencarian

2. 📊 STATISTICS DASHBOARD
   - Buat halaman statistik dengan data menarik
   - Tampilkan total items, items per kategori, dll
   - Bonus: Buat chart sederhana dengan ASCII art

3. 🎲 RANDOM FEATURE
   - Buat fitur "Random Item" yang menampilkan item acak
   - Tambahkan tombol "Get Another Random"
   - Bonus: Tambahkan animasi atau efek menarik

4. 📤 EXPORT/IMPORT
   - Implementasikan export data ke file text
   - Bonus: Import data dari file text
   - Extra bonus: Export ke format CSV

5. 🎨 THEME CUSTOMIZATION
   - Buat sistem ganti tema warna
   - Simpan preferensi tema user
   - Bonus: Buat beberapa preset tema

6. 🏷️ TAGGING SYSTEM
   - Tambahkan field "tags" untuk setiap item
   - Implementasikan filter berdasarkan tags
   - Bonus: Auto-suggest tags yang sudah ada

7. ⭐ RATING SYSTEM
   - Tambahkan rating (1-5 bintang) untuk setiap item
   - Tampilkan rata-rata rating
   - Bonus: Sort berdasarkan rating tertinggi

8. 📅 DATE FILTERING
   - Filter items berdasarkan tanggal dibuat
   - Tampilkan items "hari ini", "minggu ini", dll
   - Bonus: Calendar picker untuk pilih tanggal

🚀 TANTANGAN KREATIF (Pilih 1-2):

1. 🎮 GAMIFICATION
   - Tambahkan poin/achievement system
   - Buat level user berdasarkan aktivitas
   - Badge untuk pencapaian tertentu

2. 🔔 NOTIFICATION SYSTEM
   - Reminder untuk items dengan deadline
   - Notifikasi achievement
   - Daily summary

3. 🌙 DARK MODE
   - Implementasikan toggle dark/light mode
   - Simpan preferensi di browser
   - Smooth transition animation

4. 📱 MOBILE RESPONSIVE
   - Buat design yang mobile-friendly
   - Touch-friendly buttons
   - Responsive grid layout

5. 🎵 SOUND EFFECTS
   - Tambahkan sound effect untuk aksi tertentu
   - Background music (optional)
   - Volume control

💡 TANTANGAN ADVANCED (Untuk yang sudah selesai semua):

1. 🔐 USER AUTHENTICATION
   - Simple login system
   - Session management
   - User-specific data

2. 🌐 API ENDPOINTS
   - Buat API untuk CRUD operations
   - JSON response format
   - API documentation

3. 📊 DATA VISUALIZATION
   - Integrate dengan library chart
   - Interactive graphs
   - Data insights

4. 🔄 REAL-TIME UPDATES
   - Auto-refresh data
   - Live notifications
   - WebSocket integration
"""

# ============================================================================
# TESTING SCENARIOS - SKENARIO UNTUK TESTING
# ============================================================================

"""
🧪 TESTING CHECKLIST:

✅ BASIC FUNCTIONALITY:
[ ] Aplikasi bisa dijalankan tanpa error
[ ] Halaman utama tampil dengan benar
[ ] Form tambah item berfungsi
[ ] Data tersimpan ke JSON file
[ ] Data bisa ditampilkan kembali
[ ] Edit item berfungsi
[ ] Delete item berfungsi

✅ VALIDATION TESTING:
[ ] Input kosong ditolak dengan pesan error yang jelas
[ ] Input terlalu panjang ditolak
[ ] Format email (jika ada) divalidasi
[ ] Flash message muncul dengan kategori yang tepat

✅ USER EXPERIENCE:
[ ] Navigasi mudah dipahami
[ ] Design konsisten di semua halaman
[ ] Button dan link berfungsi dengan baik
[ ] Form mudah digunakan
[ ] Error message informatif dan helpful

✅ CREATIVE FEATURES:
[ ] Fitur unik berfungsi dengan baik
[ ] Tidak mengganggu fungsionalitas utama
[ ] Menambah value untuk user
[ ] Implementasi sesuai dengan ide awal

✅ EDGE CASES:
[ ] Bagaimana jika file JSON tidak ada?
[ ] Bagaimana jika file JSON corrupted?
[ ] Bagaimana jika tidak ada data?
[ ] Bagaimana jika ID tidak ditemukan?

🐛 COMMON BUGS TO CHECK:
[ ] Template not found error
[ ] JSON decode error
[ ] KeyError in form data
[ ] File permission error
[ ] Encoding issues dengan karakter Indonesia
"""

# ============================================================================
# PROJECT IDEAS - INSPIRASI PROYEK
# ============================================================================

"""
💡 INSPIRASI PROYEK BERDASARKAN MINAT:

🎮 GAMING & ENTERTAINMENT:
1. **Quiz App**: Bank soal dengan kategori, skor, leaderboard
2. **Story Generator**: Generate cerita random berdasarkan input
3. **Game Collection**: Katalog game favorit dengan rating
4. **Meme Generator**: Template meme dengan text custom
5. **Trivia Night**: Soal trivia dengan timer dan skor

📚 EDUCATION & LEARNING:
1. **Study Planner**: Jadwal belajar dengan reminder
2. **Vocabulary Builder**: Kamus personal dengan quiz
3. **Grade Tracker**: Pencatat nilai dengan analisis
4. **Note Taking**: Catatan dengan kategori dan search
5. **Flashcard App**: Kartu belajar digital

🏠 LIFESTYLE & PERSONAL:
1. **Habit Tracker**: Track kebiasaan harian dengan streak
2. **Mood Journal**: Diary dengan mood tracking
3. **Recipe Book**: Koleksi resep dengan rating
4. **Wishlist Manager**: Daftar barang yang diinginkan
5. **Budget Tracker**: Pencatat pengeluaran sederhana

🎨 CREATIVE & ARTISTIC:
1. **Art Gallery**: Portfolio karya seni digital
2. **Music Playlist**: Organizer lagu berdasarkan mood
3. **Photo Album**: Galeri foto dengan caption
4. **Creative Writing**: Platform untuk menulis cerita
5. **Design Inspiration**: Koleksi inspirasi design

🏫 SCHOOL & SOCIAL:
1. **Class Schedule**: Jadwal pelajaran dengan reminder
2. **Club Manager**: Manajemen kegiatan ekstrakurikuler
3. **Event Planner**: Organizer acara sekolah
4. **Book Library**: Katalog buku dengan review
5. **Friend Directory**: Kontak teman dengan info

🌟 UNIQUE & INNOVATIVE:
1. **Dream Journal**: Catat dan analisis mimpi
2. **Random Decision Maker**: Bantuan pengambilan keputusan
3. **Gratitude Log**: Catat hal-hal yang disyukuri
4. **Time Capsule**: Pesan untuk diri sendiri di masa depan
5. **Achievement Tracker**: Pencatat pencapaian personal
"""

# ============================================================================
# REFLECTION QUESTIONS - PERTANYAAN REFLEKSI
# ============================================================================

"""
🤔 PERTANYAAN REFLEKSI SETELAH SELESAI:

📋 TENTANG PROSES:
1. Bagian mana dari pengembangan yang paling menyenangkan?
2. Tantangan terbesar apa yang dihadapi?
3. Bagaimana cara mengatasi masalah yang muncul?
4. Apa yang akan dilakukan berbeda jika mengulang?
5. Seberapa sesuai hasil akhir dengan rencana awal?

💻 TENTANG TEKNIS:
1. Konsep mana yang akhirnya "klik" dan dipahami?
2. Fitur apa yang paling bangga berhasil dibuat?
3. Bug apa yang paling sulit dipecahkan?
4. Skill apa yang merasa paling berkembang?
5. Apa yang ingin dipelajari selanjutnya?

🎨 TENTANG KREATIVITAS:
1. Dari mana ide aplikasi ini berasal?
2. Fitur unik apa yang berhasil diimplementasikan?
3. Bagaimana proses brainstorming ide kreatif?
4. Apa yang membuat aplikasi ini berbeda?
5. Ide apa yang tidak sempat diimplementasikan?

🚀 TENTANG MASA DEPAN:
1. Bagaimana rencana pengembangan aplikasi ini?
2. Fitur apa yang ingin ditambahkan selanjutnya?
3. Apakah tertarik melanjutkan belajar programming?
4. Bidang tech mana yang ingin dieksplorasi?
5. Bagaimana pengalaman ini mengubah pandangan tentang coding?

💡 TIPS UNTUK PRESENTASI:
1. Mulai dengan cerita di balik ide aplikasi
2. Demo fitur utama dengan antusias
3. Jelaskan tantangan dan cara mengatasinya
4. Highlight fitur unik yang membedakan
5. Bagikan rencana pengembangan ke depan
6. Jangan takut menunjukkan passion dan excitement!
"""

# ============================================================================
# MAIN APPLICATION RUNNER
# ============================================================================

if __name__ == '__main__':
    # Buat folder templates jika belum ada
    if not os.path.exists('templates'):
        os.makedirs('templates')
        print("📁 Folder 'templates' dibuat. Jangan lupa buat file HTML!")
    
    # Buat folder static jika belum ada
    if not os.path.exists('static'):
        os.makedirs('static')
        print("📁 Folder 'static' dibuat untuk CSS/JS/images")
    
    # Test koneksi database
    print("🔌 Testing MySQL connection...")
    if db.connect():
        print("✅ MySQL connection successful!")
        
        # Contoh: Buat tabel jika belum ada (sesuaikan dengan proyek Anda)
        sample_schema = """
        id INT AUTO_INCREMENT PRIMARY KEY,
        nama VARCHAR(100) NOT NULL,
        umur INT NOT NULL CHECK (umur BETWEEN 10 AND 18),
        email VARCHAR(100) UNIQUE NOT NULL,
        kelas VARCHAR(10) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        """
        
        if db.create_project_table('siswa', sample_schema):
            print("✅ Sample table 'siswa' ready!")
        
        db.disconnect()
    else:
        print("❌ MySQL connection failed! Check your configuration.")
        print("💡 Make sure MySQL is running and database 'siswa_db' exists.")
    
    print("\n🚀 Starting your amazing MySQL app...")
    print("📝 Jangan lupa buat file HTML di folder 'templates'!")
    print("🎨 Customize routes dan MySQL queries sesuai ide proyekmu!")
    print("💡 Lihat comments di atas untuk inspirasi dan tantangan MySQL!")
    print("🗄️ Database: MySQL dengan full CRUD operations")
    print("\n" + "="*50)
    print("🌟 SELAMAT BERKREASI DENGAN MYSQL! 🌟")
    print("="*50 + "\n")
    
    # Jalankan aplikasi
    app.run(debug=True, port=5000)

"""
🎉 SELAMAT! Kamu sudah siap memulai proyek mandiri!

📋 LANGKAH SELANJUTNYA:
1. Tentukan ide aplikasi yang ingin dibuat
2. Customize kode di atas sesuai kebutuhan
3. Buat file HTML di folder 'templates'
4. Implementasikan fitur-fitur kreatif
5. Test aplikasi secara menyeluruh
6. Siapkan presentasi yang menarik

💪 REMEMBER:
- Mulai dengan sederhana, tambahkan kompleksitas bertahap
- Jangan takut bereksperimen dan membuat kesalahan
- Focus pada fungsionalitas dulu, baru design
- Ask for help jika stuck lebih dari 10 menit
- Yang terpenting: HAVE FUN dan ENJOY THE PROCESS!

🚀 Happy Coding! Wujudkan ide kreatifmu! 🚀
"""