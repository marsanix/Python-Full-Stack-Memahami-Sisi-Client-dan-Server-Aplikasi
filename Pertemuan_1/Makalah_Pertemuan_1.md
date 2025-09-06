# Pertemuan 1: Memahami Arsitektur Client-Server dalam Aplikasi Web

**Durasi**: 2 jam  
**Tujuan**: Memahami bagaimana client (browser) dan server (Flask) berinteraksi dalam aplikasi web CRUD dengan MySQL

---

## Tujuan Pembelajaran

Setelah mengikuti pertemuan ini, siswa diharapkan dapat:
1. Menjelaskan konsep client-server architecture dalam aplikasi web
2. Memahami bagaimana browser (client) berkomunikasi dengan Flask (server)
3. Membuat diagram alur komunikasi HTTP request-response
4. Memahami peran database MySQL dalam arsitektur client-server
5. Mengidentifikasi perbedaan antara method GET dan POST dalam konteks client-server

## Materi Pembelajaran

### A. Review Konsep Dasar (15 menit)

#### 1. Apa itu Flask?

**Analogi Sederhana**: Flask seperti "kerangka rumah"
- Rumah butuh fondasi, dinding, atap → Aplikasi web butuh routing, template, database
- Flask menyediakan "kerangka" untuk membangun aplikasi web dengan Python
- Seperti LEGO, Flask memberikan blok-blok yang bisa disusun menjadi aplikasi

**Kode Dasar Flask**:
```python
from flask import Flask

app = Flask(__name__)  # Membuat "rumah" aplikasi

@app.route('/')        # "Alamat pintu masuk"
def home():
    return "Selamat datang di rumah saya!"

if __name__ == '__main__':
    app.run(debug=True)  # "Menyalakan lampu rumah"
```

#### 2. Apa itu Routing?

**Analogi**: Routing seperti "papan nama di rumah"
- `/` = Pintu depan (halaman utama)
- `/kamar` = Kamar tidur
- `/dapur` = Dapur

**Contoh Routing**:
```python
@app.route('/')           # Halaman utama
@app.route('/tentang')    # Halaman tentang
@app.route('/kontak')     # Halaman kontak
```

#### 3. Apa itu Template HTML?

**Analogi**: Template seperti "cetakan kue"
- Cetakan yang sama, bisa diisi adonan berbeda
- Template HTML yang sama, bisa diisi data berbeda

### B. Memahami Arsitektur Client-Server dalam Aplikasi CRUD (30 menit)

Mari kita analisis bagaimana client dan server berinteraksi dalam aplikasi CRUD:

#### 1. Struktur Aplikasi CRUD
```
app.py              # Otak aplikasi (server)
templates/
  ├── index.html    # Halaman utama (daftar data)
  ├── tambah.html   # Halaman tambah data
  └── edit.html     # Halaman edit data
```

#### 2. Analisis app.py

**Bagian Import**:
```python
from flask import Flask, render_template, request, redirect
```
**Pertanyaan untuk dipahami**:
- `Flask`: Untuk apa?
- `render_template`: Untuk apa?
- `request`: Untuk apa?
- `redirect`: Untuk apa?

**Bagian Data**:
```python
data_siswa = [
    {'id': 1, 'nama': 'Budi', 'kelas': '7A'},
    {'id': 2, 'nama': 'Sari', 'kelas': '7B'}
]
```
**Pertanyaan untuk dipahami**:
- Kenapa pakai list of dictionary?
- Apa kelemahan menyimpan data seperti ini?

**Bagian READ (Menampilkan Data)**:
```python
@app.route('/')
def index():
    return render_template('index.html', siswa=data_siswa)
```
**Pertanyaan untuk dipahami**:
- Kenapa pakai `@app.route('/')`?
- Apa fungsi `siswa=data_siswa`?
- Bagaimana data sampai ke HTML?

**Bagian CREATE (Menambah Data)**:
```python
@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        nama = request.form['nama']
        kelas = request.form['kelas']
        
        siswa_baru = {
            'id': len(data_siswa) + 1,
            'nama': nama,
            'kelas': kelas
        }
        data_siswa.append(siswa_baru)
        return redirect('/')
    
    return render_template('tambah.html')
```
**Pertanyaan untuk dipahami**:
- Kenapa ada `methods=['GET', 'POST']`?
- Apa bedanya GET dan POST?
- Kenapa ada `if request.method == 'POST'`?
- Dari mana `request.form['nama']` datangnya?
- Kenapa pakai `redirect('/')`?

### C. Perbedaan GET vs POST (15 menit)

#### Analogi Surat

**GET** seperti "kartu pos":
- Semua orang bisa baca isinya
- Terbatas jumlah tulisannya
- Untuk minta informasi
- Contoh: Melihat halaman web

**POST** seperti "surat dalam amplop":
- Isinya rahasia/tersembunyi
- Bisa kirim banyak data
- Untuk kirim informasi
- Contoh: Kirim form, upload file

#### Kapan Pakai GET?
- Melihat halaman
- Mencari data
- Tidak mengubah data di server

#### Kapan Pakai POST?
- Kirim form
- Upload file
- Mengubah data di server

### D. Visualisasi Alur Kerja (45 menit)

#### Latihan: Membuat Flowchart

Mari buat diagram alur untuk proses "Tambah Data Siswa":

```
[User buka /tambah] 
        ↓
[Server kirim form HTML]
        ↓
[User isi form & submit]
        ↓
[Browser kirim POST ke /tambah]
        ↓
[Server terima data form]
        ↓
[Server simpan ke data_siswa]
        ↓
[Server redirect ke /]
        ↓
[Browser buka halaman utama]
        ↓
[User lihat data baru]
```

#### Latihan: Trace Kode

Ikuti langkah demi langkah apa yang terjadi ketika:
1. User membuka `http://localhost:5000/`
2. User klik "Tambah Siswa"
3. User isi form dan klik "Submit"
4. User kembali ke halaman utama

### E. Latihan Mengubah Fungsi Dasar (30 menit)

#### Tantangan 1: Ubah Pesan Konfirmasi
Tambahkan pesan "Data berhasil ditambahkan!" setelah user menambah data.

**Petunjuk**: Gunakan flash message
```python
from flask import flash

# Setelah data ditambahkan:
flash('Data siswa berhasil ditambahkan!')
```

#### Tantangan 2: Validasi Input
Pastikan nama siswa tidak boleh kosong.

**Petunjuk**:
```python
if request.method == 'POST':
    nama = request.form['nama']
    if not nama:  # Jika nama kosong
        flash('Nama tidak boleh kosong!')
        return render_template('tambah.html')
    # Lanjutkan proses normal...
```

#### Tantangan 3: Konfirmasi Hapus
Ubah fungsi hapus agar user harus konfirmasi dua kali.

**Petunjuk**: Tambahkan parameter konfirmasi di URL
```python
@app.route('/hapus/<int:id>')
@app.route('/hapus/<int:id>/<konfirmasi>')
def hapus(id, konfirmasi=None):
    if konfirmasi != 'ya':
        # Tampilkan halaman konfirmasi
        return render_template('konfirmasi_hapus.html', id=id)
    # Lanjutkan hapus data...
```

## Rangkuman

### Konsep Penting yang Dipelajari:
1. **Client-Server Architecture** = Pola komunikasi antara browser dan server
2. **Flask (Server)** = Backend yang memproses request dan mengirim response
3. **Browser (Client)** = Frontend yang mengirim request dan menerima response
4. **HTTP Methods** = GET untuk meminta data, POST untuk mengirim data
5. **Database MySQL** = Tempat penyimpanan data yang diakses oleh server
6. **Request-Response Cycle** = Alur komunikasi lengkap client-server-database

### Alur Kerja Client-Server dalam CRUD:
1. **CREATE**: Client kirim form (POST) → Server proses → Database simpan → Response ke client
2. **READ**: Client request data (GET) → Server query database → Response dengan data
3. **UPDATE**: Client kirim perubahan (POST) → Server update database → Response konfirmasi
4. **DELETE**: Client request hapus → Server hapus dari database → Response konfirmasi

### Tips Debugging:
1. Baca error message dengan teliti
2. Cek apakah route sudah benar
3. Pastikan method HTTP sesuai
4. Periksa nama variabel di form dan kode
5. Gunakan `print()` untuk debug

---

## Persiapan Pertemuan Selanjutnya

Di pertemuan berikutnya, kita akan:
1. Membangun aplikasi client-server dengan MySQL database
2. Fokus pada komunikasi HTTP dan integrasi database
3. Mengimplementasikan API endpoints untuk client-server communication

**Tugas Rumah**:
1. Coba jalankan kembali aplikasi CRUD yang pernah dibuat
2. Eksperimen dengan mengubah pesan atau warna
3. Buat catatan tentang bagian yang masih membingungkan

**Bahan yang Perlu Disiapkan**:
- Laptop dengan Python dan Flask terinstall
- Text editor (VS Code, Notepad++, dll.)
- Browser untuk testing
- Kertas dan pulpen untuk membuat diagram