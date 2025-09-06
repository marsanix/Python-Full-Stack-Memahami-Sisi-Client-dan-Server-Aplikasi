# Quiz Pertemuan 3: Integrasi Data & Validasi dengan MySQL

**Nama**: ___________________  
**Tanggal**: ___________________  
**Durasi**: 30 menit

---

## Petunjuk Pengerjaan
1. Quiz ini menguji pemahaman tentang validasi data dan integrasi database MySQL
2. Boleh melihat kode yang sudah dibuat sebagai referensi
3. Fokus pada pemahaman konsep dan implementasi praktis
4. Berikan penjelasan yang jelas dan logis
5. Tanyakan jika ada soal yang tidak jelas

---

## BAGIAN A: PILIHAN GANDA (40 poin)
*Pilih jawaban yang paling tepat!*

### 1. Apa perbedaan utama antara client-side validation dan server-side validation?

a) Client-side lebih aman, server-side lebih cepat  
b) Client-side lebih cepat, server-side lebih aman  
c) Tidak ada perbedaan, keduanya sama  
d) Client-side untuk database, server-side untuk tampilan  

**Jawaban**: ___

### 2. Mengapa validasi server-side tetap diperlukan meskipun sudah ada client-side validation?

a) Untuk backup jika client-side gagal  
b) Karena client-side validation bisa dibypass oleh user  
c) Untuk mempercepat proses validasi  
d) Untuk menghemat bandwidth  

**Jawaban**: ___

### 3. Dalam regex pattern `r'^[a-zA-Z\s.,]+$'`, apa yang divalidasi?

a) Hanya huruf kecil  
b) Huruf besar dan kecil saja  
c) Huruf, spasi, titik, dan koma  
d) Semua karakter kecuali angka  

**Jawaban**: ___

### 4. Fungsi `strip()` dalam validasi digunakan untuk:

a) Menghapus karakter khusus  
b) Menghapus spasi di awal dan akhir string  
c) Mengubah huruf menjadi kecil  
d) Memvalidasi format email  

**Jawaban**: ___

### 5. Dalam MySQL, apa kegunaan AUTO_INCREMENT pada kolom ID?

a) Menyimpan data siswa  
b) Membuat ID unik secara otomatis untuk setiap record baru  
c) Menyimpan konfigurasi aplikasi  
d) Menyimpan backup data  

**Jawaban**: ___

### 6. Dalam MySQL, constraint UNIQUE berguna untuk:

a) Mempercepat proses penyimpanan  
b) Menghemat ukuran file  
c) Memastikan tidak ada duplikasi data pada kolom tersebut  
d) Mencegah error saat membaca file  

**Jawaban**: ___

### 7. Dalam MySQL, error 1062 menandakan:

a) Koneksi database gagal  
b) Tabel tidak ditemukan  
c) Pelanggaran UNIQUE constraint (duplicate entry)  
d) Data terlalu panjang untuk kolom  

**Jawaban**: ___

### 8. Flash message dengan kategori 'error' biasanya ditampilkan dengan warna:

a) Hijau  
b) Biru  
c) Kuning  
d) Merah  

**Jawaban**: ___

---

## BAGIAN B: ANALISIS KODE VALIDASI (35 poin)
*Analisis kode berikut dan jawab pertanyaan!*

### 9. Perhatikan fungsi validasi berikut:

```python
def validasi_email(email):
    if not email or not email.strip():
        return False, "Email tidak boleh kosong"
    
    email = email.strip().lower()
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False, "Format email tidak valid"
    
    if len(email) > 100:
        return False, "Email terlalu panjang"
    
    return True, email
```

**a) Jelaskan langkah-langkah validasi yang dilakukan fungsi ini! (10 poin)**

```
1. ________________________________________________
2. ________________________________________________
3. ________________________________________________
4. ________________________________________________
5. ________________________________________________
```

**b) Apa yang dikembalikan fungsi ini jika email valid? (5 poin)**

**Jawaban**: ________________________________________________

**c) Mengapa email diubah menjadi lowercase? (5 poin)**

**Jawaban**: ________________________________________________

### 10. Perhatikan kode database operation berikut:

```python
def add_siswa(self, siswa_data):
    try:
        cursor = self.connection.cursor()
        query = """
        INSERT INTO siswa (nama, umur, email, kelas) 
        VALUES (%(nama)s, %(umur)s, %(email)s, %(kelas)s)
        """
        cursor.execute(query, siswa_data)
        self.connection.commit()
        
        new_id = cursor.lastrowid
        cursor.close()
        return new_id
    except mysql.connector.Error as e:
        self.connection.rollback()
        print(f"MySQL Error: {e}")
        return None
```

**a) Apa yang terjadi jika `commit()` gagal? (5 poin)**

**Jawaban**: ________________________________________________

**b) Mengapa menggunakan `rollback()` dalam except block? (5 poin)**

**Jawaban**: ________________________________________________

**c) Apa kegunaan `cursor.lastrowid` dan parameterized query? (5 poin)**

**Jawaban**: ________________________________________________

---

## BAGIAN C: IMPLEMENTASI VALIDASI (30 poin)
*Tulis kode untuk menyelesaikan masalah berikut!*

### 11. Buatlah fungsi validasi untuk nomor HP Indonesia dengan MySQL constraint! (15 poin)

**Requirement**:
- Format: 08xxxxxxxxxx (dimulai 08, total 11-13 digit)
- Hanya boleh angka
- Tidak boleh kosong
- Cek duplikasi di database MySQL

```python
def validasi_hp_mysql(hp, db_connection, exclude_id=None):
    """Validasi nomor HP Indonesia dengan MySQL check"""
    if not hp or not hp.strip():
        return ________________________________
    
    hp = hp.strip()
    
    # Cek apakah dimulai dengan 08
    if not ________________________________:
        return False, "Nomor HP harus dimulai dengan 08"
    
    # Cek apakah hanya angka
    if not ________________________________:
        return False, "Nomor HP hanya boleh berisi angka"
    
    # Cek panjang (11-13 digit)
    if ________________________________:
        return False, "Nomor HP harus 11-13 digit"
    
    # Cek duplikasi di MySQL
    if check_hp_exists_mysql(db_connection, hp, exclude_id):
        return False, "Nomor HP sudah terdaftar (UNIQUE constraint)"
    
    return ________________________________
```

### 12. Buatlah fungsi untuk validasi alamat sesuai MySQL schema! (15 poin)

**Requirement**:
- Minimal 10 karakter
- Maksimal sesuai VARCHAR(255) di MySQL
- Tidak boleh kosong (NOT NULL constraint)
- Boleh mengandung huruf, angka, spasi, dan tanda baca

```python
def validasi_alamat_mysql(alamat):
    """Validasi alamat siswa untuk MySQL"""
    if ________________________________:
        return False, "Alamat tidak boleh kosong (NOT NULL constraint)"
    
    alamat = alamat.strip()
    
    if ________________________________:
        return False, "Alamat minimal 10 karakter"
    
    if ________________________________:
        return False, "Alamat maksimal 255 karakter (VARCHAR(255))"
    
    # Cek karakter yang diizinkan (huruf, angka, spasi, tanda baca)
    if not re.match(r'^[a-zA-Z0-9\s.,/-]+$', alamat):
        return ________________________________
    
    return ________________________________
```

---

## BAGIAN D: PROBLEM SOLVING DATABASE (25 poin)
*Analisis masalah dan berikan solusi!*

### 13. Debugging Challenge! (15 poin)

Seorang siswa membuat kode untuk mencari siswa berdasarkan email di MySQL:

```python
def cari_siswa_by_email_mysql(email, connection):
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM siswa WHERE email = %s"
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    cursor.close()
    return result

# Penggunaan
result = cari_siswa_by_email_mysql("AHMAD@EMAIL.COM", db_connection)
if result:
    print(f"Ditemukan: {result['nama']}")
else:
    print("Siswa tidak ditemukan")
```

**Masalah**: Meskipun ada siswa dengan email "ahmad@email.com" di database MySQL, fungsi ini mengembalikan None.

**a) Apa penyebab masalah ini? (5 poin)**

**Jawaban**: ________________________________________________

**b) Bagaimana cara memperbaikinya? (5 poin)**

**Jawaban**: ________________________________________________

**c) Tulis kode yang sudah diperbaiki! (5 poin)**

```python
def cari_siswa_by_email_mysql(email, connection):
    ________________________________________________
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM siswa WHERE ________________________________________________"
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    cursor.close()
    return result
```

### 14. Design Challenge! (10 poin)

Anda diminta menambahkan fitur "History Perubahan" yang mencatat setiap kali data siswa diubah.

**a) Struktur data apa yang diperlukan untuk menyimpan history? (5 poin)**

**Jawaban**: ________________________________________________

**b) Kapan saja history harus dicatat? (5 poin)**

**Jawaban**: ________________________________________________

---

## BAGIAN E: KONSEP LANJUTAN (20 poin)

### 15. Jelaskan konsep "Separation of Concerns" dalam konteks validasi data! (10 poin)

**a) Apa maksud dari konsep ini?**

**Jawaban**: ________________________________________________

**b) Berikan contoh penerapannya dalam aplikasi Flask!**

**Jawaban**: ________________________________________________

### 16. Bandingkan kelebihan dan kekurangan menggunakan file JSON vs database SQL! (10 poin)

**JSON:**
- **Kelebihan**: ________________________________________________
- **Kekurangan**: ________________________________________________

**SQL Database:**
- **Kelebihan**: ________________________________________________
- **Kekurangan**: ________________________________________________

---

## BAGIAN F: REFLEKSI PEMBELAJARAN (10 poin)

### 17. Refleksi pengalaman Pertemuan 3! (10 poin)

**a) Konsep validasi mana yang paling sulit dipahami? Mengapa?**

**Jawaban**: ________________________________________________

**b) Apa manfaat praktis dari belajar validasi data?**

**Jawaban**: ________________________________________________

**c) Bagaimana pengalaman menggunakan database JSON dibanding list biasa?**

**Jawaban**: ________________________________________________

**d) Fitur apa yang ingin ditambahkan ke aplikasi di pertemuan berikutnya?**

**Jawaban**: ________________________________________________

---

## KUNCI JAWABAN

### Bagian A (Pilihan Ganda):
1. b) Client-side lebih cepat, server-side lebih aman
2. b) Karena client-side validation bisa dibypass oleh user
3. c) Huruf, spasi, titik, dan koma
4. b) Menghapus spasi di awal dan akhir string
### 5. b) Membuat ID unik secara otomatis untuk setiap record baru
6. c) Memastikan tidak ada duplikasi data pada kolom tersebut
7. c) Pelanggaran UNIQUE constraint (duplicate entry)
8. d) Merah

### Bagian B (Analisis Kode):

**9a) Langkah validasi email:**
1. Cek apakah email kosong atau hanya spasi
2. Bersihkan spasi dan ubah ke lowercase
3. Validasi format dengan regex pattern
4. Cek panjang email tidak lebih dari 100 karakter
5. Return True dan email yang sudah dibersihkan jika valid

**9b) Return jika valid:**
Tuple (True, email) dimana email sudah dalam format lowercase dan bersih

**9c) Alasan lowercase:**
Untuk memastikan konsistensi data dan mencegah duplikasi email dengan case berbeda

**10a) Jika commit() gagal:**
Transaksi akan di-rollback dan fungsi return None, data tidak tersimpan

**10b) Alasan rollback():**
Untuk membatalkan transaksi yang gagal dan mengembalikan database ke state sebelumnya

**10c) Kegunaan lastrowid dan parameterized query:**
- lastrowid: Mendapatkan ID yang baru saja di-generate oleh AUTO_INCREMENT
- parameterized query: Mencegah SQL injection dengan binding parameter safely

### Bagian C (Implementasi):

**11. Validasi HP MySQL:**
```python
def validasi_hp_mysql(hp, db_connection, exclude_id=None):
    if not hp or not hp.strip():
        return False, "Nomor HP tidak boleh kosong"
    
    hp = hp.strip()
    
    if not hp.startswith('08'):
        return False, "Nomor HP harus dimulai dengan 08"
    
    if not hp.isdigit():
        return False, "Nomor HP hanya boleh berisi angka"
    
    if len(hp) < 11 or len(hp) > 13:
        return False, "Nomor HP harus 11-13 digit"
    
    if check_hp_exists_mysql(db_connection, hp, exclude_id):
        return False, "Nomor HP sudah terdaftar (UNIQUE constraint)"
    
    return True, hp
```

**12. Validasi Alamat MySQL:**
```python
def validasi_alamat_mysql(alamat):
    if not alamat or not alamat.strip():
        return False, "Alamat tidak boleh kosong (NOT NULL constraint)"
    
    alamat = alamat.strip()
    
    if len(alamat) < 10:
        return False, "Alamat minimal 10 karakter"
    
    if len(alamat) > 255:
        return False, "Alamat maksimal 255 karakter (VARCHAR(255))"
    
    if not re.match(r'^[a-zA-Z0-9\s.,/-]+$', alamat):
        return False, "Alamat mengandung karakter tidak valid"
    
    return True, alamat
```

### Bagian D (Problem Solving):

**13a) Penyebab masalah:**
Perbandingan case-sensitive. "AHMAD@EMAIL.COM" tidak sama dengan "ahmad@email.com"

**13b) Cara memperbaiki:**
Ubah kedua email ke lowercase sebelum dibandingkan

**13c) Kode diperbaiki:**
```python
def cari_siswa_by_email_mysql(email, connection):
    email = email.lower().strip()
    cursor = connection.cursor(dictionary=True)
    query = "SELECT * FROM siswa WHERE LOWER(email) = %s"
    cursor.execute(query, (email,))
    result = cursor.fetchone()
    cursor.close()
    return result
```

**14a) Struktur data history:**
List berisi dictionary dengan field: timestamp, action, old_data, new_data, user_id

**14b) Kapan mencatat history:**
Setiap operasi CREATE, UPDATE, DELETE pada data siswa

### Bagian E (Konsep Lanjutan):

**15a) Separation of Concerns:**
Memisahkan tanggung jawab berbeda ke dalam fungsi/modul terpisah

**15b) Contoh penerapan:**
- Validasi di fungsi terpisah
- Database operations di class terpisah
- Route handling di fungsi terpisah
- Template rendering terpisah dari logic

**16. Perbandingan JSON vs SQL:**

**JSON:**
- Kelebihan: Mudah dipahami, tidak perlu setup, portable, human-readable
- Kekurangan: Tidak ada relasi, performa lambat untuk data besar, tidak ada indexing, tidak ada data integrity

**MySQL Database:**
- Kelebihan: Performa tinggi, relasi antar tabel, indexing, concurrent access, ACID compliance, data integrity dengan constraints
- Kekurangan: Setup kompleks, perlu belajar SQL, membutuhkan server database, resource intensive

### Bagian F (Refleksi):

**17a) Konsep sulit:**
Regex pattern karena sintaksnya kompleks dan perlu hafalan

**17b) Manfaat praktis:**
Mencegah data rusak, meningkatkan keamanan aplikasi, user experience lebih baik

**17c) Pengalaman JSON vs list:**
JSON lebih terstruktur, mudah di-backup, tapi perlu handling error lebih hati-hati

**17d) Fitur yang diinginkan:**
Authentication, file upload, real-time notification, API endpoints

---

## RUBRIK PENILAIAN

| Bagian | Skor Maksimal | Kriteria Penilaian |
|--------|---------------|--------------------|
| A (Pilihan Ganda) | 40 | 5 poin per jawaban benar |
| B (Analisis Kode) | 35 | Pemahaman alur dan konsep validasi |
| C (Implementasi) | 30 | Syntax benar dan logika tepat |
| D (Problem Solving) | 25 | Analisis masalah dan solusi database |
| E (Konsep Lanjutan) | 20 | Pemahaman konsep advanced |
| F (Refleksi) | 10 | Refleksi pembelajaran |
| **Total** | **160** | **A = 140-160, B = 120-139, C = 100-119** |

---

## FEEDBACK PEMBELAJARAN

**Setelah mengerjakan quiz, jawab pertanyaan refleksi berikut:**

### Pemahaman Validasi:
1. **Jenis validasi mana yang sudah dikuasai dengan baik?**
   ________________________________________________

2. **Regex pattern mana yang masih sulit dipahami?**
   ________________________________________________

### Kemampuan Database:
3. **Operasi database mana yang paling mudah?**
   ________________________________________________

4. **Error handling mana yang paling sering lupa?**
   ________________________________________________

### Rencana Pengembangan:
5. **Fitur validasi apa yang ingin ditambahkan?**
   ________________________________________________

6. **Bagaimana rencana menggunakan konsep ini di proyek mandiri?**
   ________________________________________________

**Catatan Guru:**
________________________________________________
________________________________________________
________________________________________________

---

**🎯 Tujuan Quiz Ini:**
- Mengukur pemahaman konsep validasi data
- Menguji kemampuan implementasi database JSON
- Mengidentifikasi area yang perlu diperkuat
- Mempersiapkan untuk proyek mandiri

**💡 Tips untuk Pertemuan Berikutnya:**
- Review konsep validasi yang masih lemah
- Praktik lebih banyak dengan regex pattern
- Fokus pada error handling dan edge cases
- Mulai berpikir tentang fitur-fitur kreatif untuk proyek mandiri

**🚀 Persiapan Proyek Mandiri:**
- Pikirkan ide aplikasi yang ingin dibuat
- Tentukan fitur-fitur yang akan diimplementasikan
- Siapkan mental untuk coding challenge
- Bawa kreativitas dan semangat eksplorasi!