# Quiz Pertemuan 1: Memahami Arsitektur Client-Server dalam Aplikasi Web

**Nama**: ___________________  
**Tanggal**: ___________________  
**Durasi**: 20 menit

---

## Petunjuk Pengerjaan
1. Baca setiap soal dengan teliti
2. Pilih jawaban yang paling tepat untuk soal pilihan ganda
3. Berikan penjelasan lengkap untuk soal essay
4. Boleh melihat kode yang sudah dibuat sebagai referensi
5. Tanyakan jika ada soal yang tidak jelas

---

## BAGIAN A: PILIHAN GANDA (40 poin)
*Pilih jawaban yang paling tepat!*

### 1. Apa fungsi utama dari Flask dalam pengembangan web?

a) Membuat database  
b) Framework untuk membuat aplikasi web dengan Python  
c) Text editor untuk menulis kode  
d) Browser untuk menjalankan aplikasi  

**Jawaban**: ___

### 2. Dalam kode `@app.route('/tambah')`, apa arti dari `/tambah`?

a) Nama file Python  
b) Nama fungsi  
c) Alamat URL yang bisa diakses user  
d) Nama template HTML  

**Jawaban**: ___

### 3. Apa perbedaan utama antara method GET dan POST?

a) GET untuk menampilkan halaman, POST untuk mengirim data  
b) GET lebih cepat dari POST  
c) POST hanya bisa digunakan dengan Flask  
d) Tidak ada perbedaan  

**Jawaban**: ___

### 4. Dalam kode `return render_template('index.html', data=siswa_list)`, apa fungsi dari `data=siswa_list`?

a) Menyimpan data ke database  
b) Mengirim data ke template HTML  
c) Membuat file HTML baru  
d) Menghapus data siswa  

**Jawaban**: ___

### 5. Kenapa perlu menggunakan `redirect('/')` setelah menambah data?

a) Untuk menghapus data  
b) Untuk menutup aplikasi  
c) Untuk mengarahkan user ke halaman utama yang sudah terupdate  
d) Untuk membuat backup data  

**Jawaban**: ___

### 6. Dalam kode `request.form['nama']`, dari mana data `nama` berasal?

a) Dari database  
b) Dari file Python  
c) Dari form HTML yang disubmit user  
d) Dari browser  

**Jawaban**: ___

### 7. Apa yang terjadi jika kita tidak menambahkan `methods=['POST']` pada route yang menerima data form?

a) Aplikasi akan crash  
b) Data tidak bisa diterima  
c) Flask akan error "Method Not Allowed"  
d) Tidak ada masalah  

**Jawaban**: ___

### 8. Dalam aplikasi CRUD, apa kepanjangan dari CRUD?

a) Create, Read, Update, Delete  
b) Copy, Run, Upload, Download  
c) Connect, Receive, Use, Disconnect  
d) Code, Review, Upload, Deploy  

**Jawaban**: ___

---

## BAGIAN B: ESSAY SINGKAT (40 poin)
*Berikan penjelasan singkat dan jelas!*

### 9. Jelaskan alur kerja yang terjadi ketika user mengklik tombol "Tambah Data" sampai data muncul di halaman utama! (10 poin)

**Jawaban**:
```
1. ________________________________________________
2. ________________________________________________
3. ________________________________________________
4. ________________________________________________
5. ________________________________________________
```

### 10. Sebutkan 3 kelemahan menyimpan data dalam list Python (seperti `data_siswa = []`) dan berikan solusinya! (10 poin)

**Kelemahan 1**: ________________________________  
**Solusi**: ____________________________________

**Kelemahan 2**: ________________________________  
**Solusi**: ____________________________________

**Kelemahan 3**: ________________________________  
**Solusi**: ____________________________________

### 11. Jelaskan dengan bahasa sendiri apa yang dilakukan oleh kode berikut: (10 poin)

```python
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_siswa(id):
    if request.method == 'POST':
        # update data
        return redirect('/')
    return render_template('edit.html')
```

**Jawaban**:
________________________________________________
________________________________________________
________________________________________________
________________________________________________

### 12. Jika kamu ingin menambahkan fitur "Cari Siswa berdasarkan Nama", jelaskan langkah-langkah yang perlu dilakukan! (10 poin)

**Jawaban**:
```
1. ________________________________________________
2. ________________________________________________
3. ________________________________________________
4. ________________________________________________
```

---

## BAGIAN C: PRAKTIK KODE (20 poin)
*Tulis kode untuk menyelesaikan masalah berikut!*

### 13. Buatlah route Flask untuk menampilkan detail siswa berdasarkan ID! (20 poin)

**Contoh**: Jika user mengakses `/detail/1`, maka akan menampilkan detail siswa dengan ID 1.

```python
@app.route('/_________________________')
def detail_siswa(_______________):
    # Cari siswa berdasarkan ID
    siswa_ditemukan = None
    for siswa in data_siswa:
        if ________________________________:
            siswa_ditemukan = siswa
            break
    
    # Jika siswa tidak ditemukan
    if not siswa_ditemukan:
        return "_________________________________"
    
    # Jika ditemukan, tampilkan detail
    return render_template('_______________', siswa=siswa_ditemukan)
```

---

## BAGIAN D: ANALISIS MASALAH (Bonus: 10 poin)
*Untuk siswa yang ingin tantangan lebih!*

### 14. Perhatikan kode error berikut:

```python
@app.route('/tambah', methods=['GET'])
def tambah_siswa():
    if request.method == 'POST':
        nama = request.form['nama']
        # ... kode lainnya
    return render_template('tambah.html')
```

**Masalah**: Ketika user submit form, muncul error "Method Not Allowed"

**Pertanyaan**: 
a) Apa penyebab error ini?  
b) Bagaimana cara memperbaikinya?

**Jawaban**:
a) ________________________________________________
b) ________________________________________________

---

## KUNCI JAWABAN

### Bagian A (Pilihan Ganda):
1. b) Framework untuk membuat aplikasi web dengan Python
2. c) Alamat URL yang bisa diakses user
3. a) GET untuk menampilkan halaman, POST untuk mengirim data
4. b) Mengirim data ke template HTML
5. c) Untuk mengarahkan user ke halaman utama yang sudah terupdate
6. c) Dari form HTML yang disubmit user
7. c) Flask akan error "Method Not Allowed"
8. a) Create, Read, Update, Delete

### Bagian B (Essay Singkat):

**9. Alur kerja tambah data:**
1. User mengklik tombol "Tambah Data"
2. Browser mengirim request GET ke `/tambah`
3. Server mengirim form HTML ke browser
4. User mengisi form dan klik submit
5. Browser mengirim POST request dengan data form
6. Server memproses data dan menyimpan ke list
7. Server mengirim redirect ke halaman utama
8. Browser memuat halaman utama yang sudah terupdate

**10. Kelemahan menyimpan data dalam list:**
- **Kelemahan 1**: Data hilang saat aplikasi restart
  **Solusi**: Gunakan database (SQLite, MySQL, dll.)
- **Kelemahan 2**: Tidak bisa diakses oleh multiple user secara bersamaan
  **Solusi**: Gunakan database dengan sistem concurrent access
- **Kelemahan 3**: Sulit untuk query data kompleks
  **Solusi**: Gunakan database dengan SQL query

**11. Penjelasan kode:**
Kode ini membuat route `/edit/<id>` yang bisa menerima GET dan POST. Parameter `<int:id>` mengambil ID dari URL. Jika method POST (user submit form), data akan diupdate dan redirect ke halaman utama. Jika method GET (user buka halaman), akan menampilkan form edit.

**12. Langkah menambah fitur cari:**
1. Buat route `/cari` dengan method GET dan POST
2. Buat template HTML dengan form pencarian
3. Di fungsi, ambil kata kunci dari form
4. Loop data siswa dan cari yang namanya mengandung kata kunci
5. Tampilkan hasil pencarian di template

### Bagian C (Praktik Kode):

```python
@app.route('/detail/<int:id>')
def detail_siswa(id):
    siswa_ditemukan = None
    for siswa in data_siswa:
        if siswa['id'] == id:
            siswa_ditemukan = siswa
            break
    
    if not siswa_ditemukan:
        return "Siswa tidak ditemukan!"
    
    return render_template('detail.html', siswa=siswa_ditemukan)
```

### Bagian D (Analisis Masalah):
a) **Penyebab**: Route hanya menerima method GET, tapi form mengirim POST
b) **Solusi**: Ubah `methods=['GET']` menjadi `methods=['GET', 'POST']`

---

## RUBRIK PENILAIAN

| Bagian | Skor Maksimal | Kriteria |
|--------|---------------|----------|
| A (Pilihan Ganda) | 40 | 5 poin per jawaban benar |
| B (Essay) | 40 | Penjelasan logis dan lengkap |
| C (Praktik) | 20 | Kode sintaks benar dan logika tepat |
| D (Bonus) | 10 | Analisis masalah yang tepat |
| **Total** | **110** | **A = 90-110, B = 70-89, C = 50-69** |

---

## REFLEKSI PEMBELAJARAN

**Setelah mengerjakan quiz ini, jawab pertanyaan berikut:**

1. **Bagian mana yang paling mudah?** ___________________
2. **Bagian mana yang paling sulit?** ___________________
3. **Konsep apa yang masih membingungkan?** ___________________
4. **Apa yang ingin dipelajari lebih lanjut?** ___________________

**Catatan Guru:**
________________________________________________
________________________________________________
________________________________________________