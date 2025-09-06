# Quiz Pertemuan 2: Membangun Ulang dari Nol

**Nama**: ___________________  
**Tanggal**: ___________________  
**Durasi**: 25 menit

---

## Petunjuk Pengerjaan
1. Quiz ini menguji pemahaman tentang membangun aplikasi Flask dari nol
2. Boleh melihat kode yang sudah dibuat sebagai referensi
3. Fokus pada pemahaman konsep, bukan hafalan syntax
4. Berikan penjelasan yang jelas dan logis
5. Tanyakan jika ada soal yang tidak jelas

---

## BAGIAN A: PILIHAN GANDA (35 poin)
*Pilih jawaban yang paling tepat!*

### 1. Ketika membangun aplikasi Flask dari nol, apa langkah pertama yang harus dilakukan?

a) Membuat database  
b) Membuat file HTML  
c) Import Flask dan membuat instance app  
d) Membuat route untuk semua halaman  

**Jawaban**: ___

### 2. Dalam kode `app.secret_key = 'rahasia'`, apa fungsi dari secret_key?

a) Password untuk login  
b) Kunci untuk enkripsi database  
c) Diperlukan untuk flash message dan session  
d) Nama aplikasi  

**Jawaban**: ___

### 3. Jika ingin membuat route yang bisa menerima parameter ID dari URL, format yang benar adalah:

a) `@app.route('/edit?id=<id>')`  
b) `@app.route('/edit/<id>')`  
c) `@app.route('/edit/<int:id>')`  
d) `@app.route('/edit/{id}')`  

**Jawaban**: ___

### 4. Dalam implementasi CREATE (tambah data), kenapa perlu mengecek `request.method == 'POST'`?

a) Untuk keamanan aplikasi  
b) Untuk membedakan antara menampilkan form (GET) dan memproses form (POST)  
c) Untuk validasi data  
d) Untuk redirect ke halaman lain  

**Jawaban**: ___

### 5. Ketika membuat ID baru untuk data, kenapa menggunakan `max([buku['id'] for buku in buku_list]) + 1`?

a) Untuk membuat ID yang unik dan berurutan  
b) Untuk menghitung jumlah data  
c) Untuk validasi data  
d) Untuk sorting data  

**Jawaban**: ___

### 6. Apa perbedaan utama antara `render_template()` dan `redirect()`?

a) render_template lebih cepat  
b) render_template menampilkan halaman, redirect mengarahkan ke URL lain  
c) redirect hanya untuk error  
d) Tidak ada perbedaan  

**Jawaban**: ___

### 7. Dalam validasi form, jika data tidak valid, tindakan yang tepat adalah:

a) Langsung redirect ke halaman utama  
b) Tampilkan pesan error dan form kembali  
c) Hapus semua data  
d) Restart aplikasi  

**Jawaban**: ___

---

## BAGIAN B: ANALISIS KODE (30 poin)
*Analisis kode berikut dan jawab pertanyaan!*

### 8. Perhatikan kode berikut:

```python
@app.route('/tambah', methods=['GET', 'POST'])
def tambah_siswa():
    if request.method == 'POST':
        nama = request.form['nama']
        if not nama:
            flash('Nama tidak boleh kosong!', 'error')
            return render_template('tambah.html')
        
        siswa_baru = {'id': len(data_siswa) + 1, 'nama': nama}
        data_siswa.append(siswa_baru)
        flash('Data berhasil ditambahkan!', 'success')
        return redirect('/')
    
    return render_template('tambah.html')
```

**a) Jelaskan alur kerja kode ini step by step! (10 poin)**

```
1. ________________________________________________
2. ________________________________________________
3. ________________________________________________
4. ________________________________________________
5. ________________________________________________
```

**b) Apa masalah potensial dengan cara membuat ID `len(data_siswa) + 1`? (5 poin)**

**Jawaban**: ________________________________________________

**c) Bagaimana cara memperbaiki masalah tersebut? (5 poin)**

**Jawaban**: ________________________________________________

### 9. Perhatikan kode template HTML berikut:

```html
{% for buku in daftar_buku %}
<tr>
    <td>{{ buku.judul }}</td>
    <td>{{ buku.pengarang }}</td>
    <td>
        {% if buku.status == 'tersedia' %}
            <span style="color: green;">Tersedia</span>
        {% else %}
            <span style="color: red;">Dipinjam</span>
        {% endif %}
    </td>
</tr>
{% endfor %}
```

**a) Jelaskan apa yang dilakukan kode ini! (5 poin)**

**Jawaban**: ________________________________________________

**b) Dari mana variabel `daftar_buku` berasal? (5 poin)**

**Jawaban**: ________________________________________________

---

## BAGIAN C: IMPLEMENTASI KODE (25 poin)
*Tulis kode untuk menyelesaikan masalah berikut!*

### 10. Buatlah route Flask untuk mencari buku berdasarkan judul! (15 poin)

**Requirement**:
- Route: `/cari`
- Method: GET dan POST
- Jika GET: tampilkan form pencarian
- Jika POST: cari buku yang judulnya mengandung kata kunci (case-insensitive)

```python
@app.route('/_________________________', methods=['_______', '_______'])
def cari_buku():
    if request.method == '_______':
        kata_kunci = request.form['_____________'].lower()
        hasil_cari = []
        
        for buku in buku_list:
            if ________________________________:
                hasil_cari.append(buku)
        
        return render_template('_____________', 
                             hasil=hasil_cari, 
                             kata_kunci=kata_kunci)
    
    return render_template('_____________')
```

### 11. Buatlah fungsi untuk menghitung statistik perpustakaan! (10 poin)

**Requirement**: Hitung total buku, buku tersedia, dan buku dipinjam

```python
@app.route('/statistik')
def statistik():
    total_buku = ________________________________
    
    buku_tersedia = 0
    buku_dipinjam = 0
    
    for buku in buku_list:
        if ________________________________:
            buku_tersedia += 1
        else:
            buku_dipinjam += 1
    
    stats = {
        'total': total_buku,
        'tersedia': buku_tersedia,
        'dipinjam': buku_dipinjam
    }
    
    return render_template('statistik.html', ________________)
```

---

## BAGIAN D: PROBLEM SOLVING (20 poin)
*Analisis masalah dan berikan solusi!*

### 12. Debugging Challenge! (10 poin)

Seorang siswa membuat kode berikut tapi mendapat error:

```python
@app.route('/edit/<int:id>')
def edit_buku(id):
    buku = None
    for b in buku_list:
        if b['id'] == id:
            buku = b
    
    buku['judul'] = request.form['judul']
    return redirect('/')
```

**Error yang muncul**: "AttributeError: 'NoneType' object has no attribute '__setitem__'"

**a) Apa penyebab error ini?**

**Jawaban**: ________________________________________________

**b) Bagaimana cara memperbaikinya?**

**Jawaban**: ________________________________________________

### 13. Design Challenge! (10 poin)

Anda diminta menambahkan fitur "Kategori Buku" (misal: Novel, Pelajaran, Komik) ke aplikasi perpustakaan.

**a) Perubahan apa yang perlu dilakukan pada struktur data?**

**Jawaban**: ________________________________________________

**b) Route apa saja yang perlu dimodifikasi?**

**Jawaban**: ________________________________________________

**c) Fitur tambahan apa yang bisa dibuat dengan kategori ini?**

**Jawaban**: ________________________________________________

---

## BAGIAN E: REFLEKSI PEMBELAJARAN (10 poin)

### 14. Bandingkan pengalaman Pertemuan 1 vs Pertemuan 2! (10 poin)

**a) Apa perbedaan utama antara "membongkar kode" vs "membangun dari nol"?**

**Jawaban**: ________________________________________________

**b) Mana yang lebih sulit? Kenapa?**

**Jawaban**: ________________________________________________

**c) Konsep apa yang lebih mudah dipahami setelah coding session?**

**Jawaban**: ________________________________________________

**d) Apa tantangan terbesar saat membangun aplikasi dari nol?**

**Jawaban**: ________________________________________________

---

## KUNCI JAWABAN

### Bagian A (Pilihan Ganda):
1. c) Import Flask dan membuat instance app
2. c) Diperlukan untuk flash message dan session
3. c) `@app.route('/edit/<int:id>')`
4. b) Untuk membedakan antara menampilkan form (GET) dan memproses form (POST)
5. a) Untuk membuat ID yang unik dan berurutan
6. b) render_template menampilkan halaman, redirect mengarahkan ke URL lain
7. b) Tampilkan pesan error dan form kembali

### Bagian B (Analisis Kode):

**8a) Alur kerja:**
1. Cek apakah request method adalah POST
2. Jika POST, ambil data nama dari form
3. Validasi: jika nama kosong, tampilkan error dan form kembali
4. Jika valid, buat data siswa baru dan tambahkan ke list
5. Berikan pesan sukses dan redirect ke halaman utama
6. Jika GET, tampilkan form tambah

**8b) Masalah dengan ID:**
Jika ada data yang dihapus, ID bisa duplikat. Misal: ada 3 data (ID 1,2,3), hapus ID 2, tambah data baru akan dapat ID 3 (duplikat).

**8c) Solusi:**
Gunakan `max([siswa['id'] for siswa in data_siswa]) + 1` atau simpan counter ID terpisah.

**9a) Penjelasan kode HTML:**
Kode ini membuat loop untuk setiap buku dalam daftar_buku, menampilkan judul dan pengarang dalam tabel, serta menampilkan status dengan warna berbeda (hijau untuk tersedia, merah untuk dipinjam).

**9b) Asal variabel:**
Variabel `daftar_buku` berasal dari parameter yang dikirim melalui `render_template()` di route Python.

### Bagian C (Implementasi Kode):

**10. Route pencarian:**
```python
@app.route('/cari', methods=['GET', 'POST'])
def cari_buku():
    if request.method == 'POST':
        kata_kunci = request.form['kata_kunci'].lower()
        hasil_cari = []
        
        for buku in buku_list:
            if kata_kunci in buku['judul'].lower():
                hasil_cari.append(buku)
        
        return render_template('hasil_cari.html', 
                             hasil=hasil_cari, 
                             kata_kunci=kata_kunci)
    
    return render_template('cari.html')
```

**11. Fungsi statistik:**
```python
total_buku = len(buku_list)

for buku in buku_list:
    if buku['status'] == 'tersedia':
        buku_tersedia += 1
    else:
        buku_dipinjam += 1

return render_template('statistik.html', stats=stats)
```

### Bagian D (Problem Solving):

**12a) Penyebab error:**
Buku dengan ID tersebut tidak ditemukan, sehingga variabel `buku` tetap `None`. Ketika mencoba mengakses `buku['judul']`, terjadi error karena `None` tidak punya atribut.

**12b) Solusi:**
Tambahkan pengecekan apakah buku ditemukan:
```python
if buku is None:
    flash('Buku tidak ditemukan!', 'error')
    return redirect('/')
```

**13a) Perubahan struktur data:**
Tambahkan field 'kategori' pada setiap dictionary buku.

**13b) Route yang dimodifikasi:**
Semua route yang menangani form (tambah, edit) perlu ditambahkan field kategori.

**13c) Fitur tambahan:**
Filter berdasarkan kategori, statistik per kategori, pencarian dalam kategori tertentu.

### Bagian E (Refleksi):

**14a) Perbedaan:**
Membongkar kode = menganalisis yang sudah ada, membangun dari nol = mengimplementasikan dari pemahaman.

**14b) Yang lebih sulit:**
Membangun dari nol lebih sulit karena harus mengingat dan menerapkan konsep tanpa panduan kode.

**14c) Konsep yang lebih mudah:**
Alur data dari form ke Python, hubungan route dengan template, pattern CRUD.

**14d) Tantangan terbesar:**
Mengingat syntax, debugging error, memahami alur logika aplikasi.

---

## RUBRIK PENILAIAN

| Bagian | Skor Maksimal | Kriteria Penilaian |
|--------|---------------|--------------------|
| A (Pilihan Ganda) | 35 | 5 poin per jawaban benar |
| B (Analisis Kode) | 30 | Pemahaman alur dan konsep |
| C (Implementasi) | 25 | Syntax benar dan logika tepat |
| D (Problem Solving) | 20 | Analisis masalah dan solusi |
| E (Refleksi) | 10 | Pemahaman pembelajaran |
| **Total** | **120** | **A = 100-120, B = 80-99, C = 60-79** |

---

## FEEDBACK PEMBELAJARAN

**Setelah mengerjakan quiz, jawab pertanyaan refleksi berikut:**

### Pemahaman Konsep:
1. **Konsep mana yang sudah dikuasai dengan baik?**
   ________________________________________________

2. **Konsep mana yang masih perlu diperdalam?**
   ________________________________________________

### Kemampuan Praktik:
3. **Bagian coding mana yang paling mudah?**
   ________________________________________________

4. **Error apa yang paling sering muncul saat coding?**
   ________________________________________________

### Rencana Pembelajaran:
5. **Apa yang ingin dipelajari di pertemuan berikutnya?**
   ________________________________________________

6. **Fitur apa yang ingin ditambahkan ke aplikasi?**
   ________________________________________________

**Catatan Guru:**
________________________________________________
________________________________________________
________________________________________________

---

**🎯 Tujuan Quiz Ini:**
- Mengukur pemahaman konsep Flask dan CRUD
- Menguji kemampuan membangun aplikasi dari nol
- Mengidentifikasi area yang perlu diperkuat
- Mempersiapkan untuk pembelajaran yang lebih advanced

**💡 Tips untuk Pertemuan Berikutnya:**
- Review konsep yang masih lemah
- Praktik lebih banyak dengan variasi kasus
- Fokus pada debugging dan problem solving
- Mulai berpikir tentang optimasi dan best practices