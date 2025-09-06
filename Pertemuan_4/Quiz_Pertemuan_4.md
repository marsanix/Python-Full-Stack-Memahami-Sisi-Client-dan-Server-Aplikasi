# Quiz Pertemuan 4: Proyek Mandiri & Improvisasi dengan MySQL

**Nama**: ___________________  
**Tanggal**: ___________________  
**Durasi**: 35 menit

---

## Petunjuk Pengerjaan
1. Quiz ini menguji pemahaman tentang pengembangan proyek mandiri dengan MySQL integration
2. Jawab berdasarkan pengalaman mengerjakan proyek mandiri dengan database MySQL
3. Fokus pada refleksi pembelajaran MySQL dan problem solving database
4. Berikan penjelasan yang jelas dan personal tentang pengalaman MySQL
5. Tidak ada jawaban "salah" untuk pertanyaan refleksi - yang penting jujur dan thoughtful

---

## BAGIAN A: PROJECT OVERVIEW (25 poin)
*Ceritakan tentang proyek yang kamu buat!*

### 1. Informasi Proyek (10 poin)

**a) Nama aplikasi yang kamu buat:**

**Jawaban**: ________________________________________________

**b) Tema/kategori aplikasi (contoh: lifestyle, education, entertainment):**

**Jawaban**: ________________________________________________

**c) Target user aplikasi ini:**

**Jawaban**: ________________________________________________

**d) Masalah apa yang diselesaikan oleh aplikasimu?**

**Jawaban**: ________________________________________________
________________________________________________

### 2. Fitur Aplikasi (15 poin)

**a) Sebutkan 3 fitur utama aplikasimu:**

```
1. ________________________________________________
2. ________________________________________________
3. ________________________________________________
```

**b) Fitur unik/kreatif apa yang membedakan aplikasimu dari yang lain?**

**Jawaban**: ________________________________________________
________________________________________________

**c) Tabel dan field apa saja yang ada dalam database MySQL aplikasimu? (minimal 3 field per tabel)**

```
Tabel 1: ________________________________________________
- Field 1: ________________________________________________
- Field 2: ________________________________________________
- Field 3: ________________________________________________

Tabel 2: ________________________________________________
- Field 1: ________________________________________________
- Field 2: ________________________________________________
- Field 3: ________________________________________________
```

---

## BAGIAN B: TECHNICAL IMPLEMENTATION (30 poin)
*Tunjukkan pemahamanmu tentang implementasi teknis!*

### 3. Analisis Kode (15 poin)

Perhatikan struktur route berikut dari proyekmu:

```python
@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        # Ambil data dari form
        nama = request.form.get('nama', '')
        
        # Validasi
        if not nama.strip():
            flash('Nama tidak boleh kosong', 'error')
            return render_template('add.html')
        
        # Simpan ke database
        data = load_data()
        new_item = {
            'id': get_next_id(data),
            'nama': nama,
            'tanggal': datetime.now().strftime('%Y-%m-%d')
        }
        data['items'].append(new_item)
        save_data(data)
        
        flash('Data berhasil disimpan!', 'success')
        return redirect(url_for('home'))
    
    return render_template('add.html')
```

**a) Jelaskan alur kerja route ini step by step! (8 poin)**

```
Step 1: ________________________________________________
Step 2: ________________________________________________
Step 3: ________________________________________________
Step 4: ________________________________________________
Step 5: ________________________________________________
```

**b) Mengapa perlu ada validasi `if not nama.strip()`? (4 poin)**

**Jawaban**: ________________________________________________

**c) Apa fungsi `flash()` dalam kode ini? (3 poin)**

**Jawaban**: ________________________________________________

### 4. MySQL Database Operations (15 poin)

**a) Jelaskan struktur tabel MySQL yang kamu gunakan dalam proyekmu! (5 poin)**

```sql
CREATE TABLE table_name (
    id INT PRIMARY KEY AUTO_INCREMENT,
    ________________________________________________,
    ________________________________________________,
    ________________________________________________,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**b) Apa keuntungan menggunakan MySQL dibandingkan JSON file? (5 poin)**

**Jawaban**: ________________________________________________
________________________________________________

**c) Bagaimana cara mengatasi jika MySQL connection error atau query gagal? (5 poin)**

**Jawaban**: ________________________________________________
________________________________________________

---

## BAGIAN C: PROBLEM SOLVING & DEBUGGING (25 poin)
*Ceritakan pengalaman problem solving selama mengerjakan proyek!*

### 5. Debugging Experience (15 poin)

**a) Error apa yang paling sering kamu temui saat mengerjakan proyek? (5 poin)**

**Jawaban**: ________________________________________________

**b) Bagaimana cara kamu mengatasi error tersebut? (5 poin)**

**Jawaban**: ________________________________________________
________________________________________________

**c) Tools atau strategi apa yang kamu gunakan untuk debugging? (5 poin)**

**Jawaban**: ________________________________________________

### 6. Creative Problem Solving (10 poin)

**a) Tantangan teknis apa yang paling sulit dalam mengimplementasikan fitur kreatifmu? (5 poin)**

**Jawaban**: ________________________________________________
________________________________________________

**b) Solusi kreatif apa yang kamu temukan untuk mengatasi keterbatasan? (5 poin)**

**Jawaban**: ________________________________________________
________________________________________________

---

## BAGIAN D: CODE ANALYSIS & IMPROVEMENT (30 poin)
*Analisis dan perbaikan kode!*

### 7. Code Review (15 poin)

Perhatikan kode MySQL berikut yang bermasalah:

```python
@app.route('/search')
def search():
    query = request.args.get('q')
    cursor = mysql.connection.cursor()
    cursor.execute(f"SELECT * FROM items WHERE nama LIKE '%{query}%'")
    results = cursor.fetchall()
    cursor.close()
    
    return render_template('search.html', results=results)
```

**a) Identifikasi 3 masalah potensial dalam kode ini! (9 poin)**

```
Masalah 1: ________________________________________________
Masalah 2: ________________________________________________
Masalah 3: ________________________________________________
```

**b) Tulis kode yang sudah diperbaiki! (6 poin)**

```python
@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    if not query:
        return render_template('search.html', results=[])
    
    try:
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM items WHERE nama LIKE %s", (f"%{query}%",))
        results = cursor.fetchall()
        cursor.close()
        return render_template('search.html', results=results)
    except Exception as e:
        flash('Error dalam pencarian', 'error')
        return render_template('search.html', results=[])
```

### 8. Feature Enhancement (15 poin)

**a) Jika diberi waktu tambahan 30 menit, fitur apa yang ingin kamu tambahkan? Mengapa? (8 poin)**

**Jawaban**: ________________________________________________
________________________________________________
________________________________________________

**b) Tulis pseudocode untuk implementasi fitur tersebut! (7 poin)**

```python
# Pseudocode untuk fitur baru
def new_feature():
    # Step 1: ________________________________________________
    # Step 2: ________________________________________________
    # Step 3: ________________________________________________
    # Step 4: ________________________________________________
    # Step 5: ________________________________________________
```

---

## BAGIAN E: INTEGRATION & CONCEPTS (25 poin)
*Tunjukkan pemahaman integrasi konsep dari 4 pertemuan!*

### 9. Concept Integration (15 poin)

**a) Bagaimana kamu menggunakan konsep MySQL CRUD dalam proyekmu? (5 poin)**

**Jawaban**: ________________________________________________

**b) Bagaimana kamu menerapkan MySQL connection dan query optimization? (5 poin)**

**Jawaban**: ________________________________________________

**c) Validasi data dan MySQL constraints apa yang kamu implementasikan? (5 poin)**

**Jawaban**: ________________________________________________

### 10. Architecture Understanding (10 poin)

**a) Gambar diagram sederhana yang menunjukkan alur data dalam aplikasimu! (5 poin)**

```
User Input → [_______] → [_______] → [_______] → [_______] → Display
             (Form)     (Validation) (MySQL)     (Processing) (Template)
```

**b) Jelaskan peran masing-masing komponen dalam diagram tersebut! (5 poin)**

**Jawaban**: ________________________________________________
________________________________________________

---

## BAGIAN F: REFLECTION & LEARNING (35 poin)
*Refleksi mendalam tentang pengalaman belajar!*

### 11. Learning Journey (20 poin)

**a) Bandingkan kemampuan codingmu sebelum dan sesudah 4 pertemuan ini! (5 poin)**

**Sebelum**: ________________________________________________
**Sesudah**: ________________________________________________

**b) Konsep mana yang awalnya sulit tapi sekarang sudah dipahami? (5 poin)**

**Jawaban**: ________________________________________________

**c) Skill non-teknis apa yang berkembang selama mengerjakan proyek? (5 poin)**

**Jawaban**: ________________________________________________

**d) Apa yang paling membanggakan dari hasil proyekmu? (5 poin)**

**Jawaban**: ________________________________________________

### 12. Future Planning (15 poin)

**a) Bagaimana rencana pengembangan aplikasimu ke depan? (5 poin)**

**Jawaban**: ________________________________________________
________________________________________________

**b) Teknologi atau skill apa yang ingin dipelajari selanjutnya? (5 poin)**

**Jawaban**: ________________________________________________

**c) Apakah tertarik melanjutkan belajar programming? Mengapa? (5 poin)**

**Jawaban**: ________________________________________________
________________________________________________

---

## BAGIAN G: PRESENTATION SKILLS (20 poin)
*Persiapan dan evaluasi presentasi!*

### 13. Presentation Preparation (10 poin)

**a) Bagaimana kamu mempersiapkan presentasi proyekmu? (5 poin)**

**Jawaban**: ________________________________________________

**b) Apa yang paling ingin kamu highlight dalam presentasi? (5 poin)**

**Jawaban**: ________________________________________________

### 14. Communication & Feedback (10 poin)

**a) Bagaimana perasaanmu saat mempresentasikan proyek? (5 poin)**

**Jawaban**: ________________________________________________

**b) Feedback apa yang kamu terima dan bagaimana responmu? (5 poin)**

**Jawaban**: ________________________________________________

---

## BAGIAN H: CREATIVE THINKING (15 poin)
*Evaluasi kreativitas dan inovasi!*

### 15. Innovation Assessment (15 poin)

**a) Dari mana ide aplikasimu berasal? Ceritakan proses brainstorming! (5 poin)**

**Jawaban**: ________________________________________________
________________________________________________

**b) Bagaimana kamu memutuskan fitur mana yang prioritas untuk diimplementasikan? (5 poin)**

**Jawaban**: ________________________________________________

**c) Jika harus membuat aplikasi lain, ide apa yang ingin kamu coba? (5 poin)**

**Jawaban**: ________________________________________________

---

## KUNCI JAWABAN & RUBRIK PENILAIAN

### Bagian A - Project Overview (25 poin)

**Kriteria Penilaian:**
- **Excellent (23-25)**: Proyek jelas, terarah, dan memiliki value proposition yang baik
- **Good (18-22)**: Proyek cukup jelas dengan beberapa fitur menarik
- **Fair (13-17)**: Proyek basic tapi fungsional
- **Needs Work (0-12)**: Proyek tidak jelas atau tidak lengkap

**Sample Answer untuk 1d:**
"Aplikasi Habit Tracker ini membantu siswa SMP untuk membangun kebiasaan baik seperti belajar rutin, olahraga, atau membaca. Masalahnya banyak siswa yang sulit konsisten dengan target mereka karena tidak ada tracking yang mudah dan menyenangkan."

### Bagian B - Technical Implementation (30 poin)

**3a) Alur kerja route:**
1. Cek apakah request method adalah POST
2. Ambil data nama dari form
3. Validasi apakah nama tidak kosong
4. Jika tidak valid, tampilkan error dan kembali ke form
5. Jika valid, buat item baru dan simpan ke database
6. Tampilkan success message dan redirect ke home

**3b) Validasi strip():**
Untuk memastikan input tidak hanya berisi spasi kosong. `strip()` menghilangkan spasi di awal dan akhir, sehingga input yang hanya spasi akan menjadi string kosong.

**3c) Fungsi flash():**
Untuk menampilkan pesan sementara kepada user (success, error, info) yang akan muncul di halaman berikutnya.

**4b) Keuntungan metadata:**
- Menyimpan informasi tentang database (total items, last ID)
- Memudahkan generate ID baru
- Tracking statistik database
- Informasi versi atau timestamp

**4c) Mengatasi JSON corrupted:**
- Gunakan try-except untuk handle JSONDecodeError
- Buat backup file secara berkala
- Return default structure jika file rusak
- Log error untuk debugging

### Bagian C - Problem Solving (25 poin)

**Sample Answers:**

**5a) Error yang sering:**
- TemplateNotFound: Lupa buat file HTML atau salah nama
- KeyError: Field form tidak sesuai dengan yang diambil di Python
- JSONDecodeError: File JSON rusak atau format salah

**5b) Cara mengatasi:**
- Baca error message dengan teliti
- Cek struktur folder dan nama file
- Gunakan print() untuk debug
- Tanya teman atau guru jika stuck

### Bagian D - Code Analysis (30 poin)

**7a) Masalah dalam kode search:**
1. Tidak ada handling jika query None atau kosong
2. Case sensitive search (tidak user-friendly)
3. Tidak ada error handling jika load_data() gagal

**7b) Kode yang diperbaiki:**
```python
@app.route('/search')
def search():
    query = request.args.get('q', '').strip()
    
    if not query:
        flash('Masukkan kata kunci pencarian', 'info')
        return redirect(url_for('home'))
    
    data = load_data()
    results = []
    
    for item in data['items']:
        if query.lower() in item['nama'].lower():
            results.append(item)
    
    return render_template('search.html', results=results, query=query)
```

### Bagian E - Integration (25 poin)

**9a) Konsep CRUD:**
"Saya implementasikan Create (tambah habit), Read (lihat daftar), Update (edit habit), Delete (hapus habit) sesuai dengan yang dipelajari di Pertemuan 1."

**9b) Build from scratch:**
"Saya mulai dari template kosong, setup Flask, buat struktur folder, dan build step by step seperti yang dipelajari di Pertemuan 2."

**9c) Validasi data:**
"Saya pakai validasi required field, length validation, dan format validation untuk memastikan data yang masuk valid."

### Bagian F - Reflection (35 poin)

**Kriteria Penilaian:**
- **Excellent (32-35)**: Refleksi mendalam, honest, dan menunjukkan growth mindset
- **Good (25-31)**: Refleksi cukup baik dengan beberapa insight
- **Fair (18-24)**: Refleksi basic tapi menunjukkan pembelajaran
- **Needs Work (0-17)**: Refleksi superficial atau tidak jelas

**Sample Answers:**

**11a) Perbandingan kemampuan:**
- **Sebelum**: "Tidak tahu apa-apa tentang web development, takut dengan coding"
- **Sesudah**: "Bisa buat aplikasi web sederhana, paham konsep client-server, lebih percaya diri"

**11c) Skill non-teknis:**
"Problem solving, time management, presentation skills, creative thinking, persistence"

**12c) Minat lanjutan:**
"Ya, karena ternyata coding itu menyenangkan dan bisa dipakai untuk solve masalah real. Ingin belajar mobile app development."

### Bagian G - Presentation (20 poin)

**Sample Answers:**

**13a) Persiapan presentasi:**
"Saya latihan demo aplikasi, siapkan poin-poin yang mau dijelaskan, dan pastikan aplikasi berjalan lancar."

**14a) Perasaan presentasi:**
"Awalnya nervous, tapi setelah mulai demo jadi excited karena bangga dengan hasil karya sendiri."

### Bagian H - Creative Thinking (15 poin)

**15a) Asal ide:**
"Ide datang dari masalah pribadi - saya sering lupa target belajar harian. Jadi kepikiran bikin app yang bisa remind dan track progress."

**15b) Prioritas fitur:**
"Saya fokus ke core functionality dulu (add, view, mark complete), baru tambah fitur fun seperti streak counter dan statistics."

---

## RUBRIK PENILAIAN KESELURUHAN

| Aspek | Bobot | Excellent (A) | Good (B) | Fair (C) | Needs Work (D) |
|-------|-------|---------------|----------|----------|-----------------|
| **Project Quality** | 25% | Aplikasi lengkap, kreatif, fungsional | Aplikasi baik dengan beberapa fitur menarik | Aplikasi basic tapi jalan | Aplikasi tidak lengkap/bermasalah |
| **Technical Understanding** | 30% | Paham konsep mendalam, implementasi benar | Paham konsep utama, implementasi cukup | Paham basic, implementasi sederhana | Pemahaman terbatas |
| **Problem Solving** | 20% | Excellent debugging & creative solutions | Good problem solving skills | Basic problem solving | Kesulitan mengatasi masalah |
| **Integration & Concepts** | 15% | Mengintegrasikan semua konsep dengan baik | Menggunakan sebagian besar konsep | Menggunakan beberapa konsep | Integrasi konsep terbatas |
| **Reflection & Growth** | 10% | Refleksi mendalam, growth mindset jelas | Refleksi baik, menunjukkan pembelajaran | Refleksi cukup | Refleksi superficial |

### Skala Nilai:
- **A (Excellent)**: 85-100 - Outstanding work, exceeds expectations
- **B (Good)**: 70-84 - Good work, meets expectations well
- **C (Fair)**: 55-69 - Acceptable work, meets basic expectations
- **D (Needs Work)**: 40-54 - Below expectations, needs improvement
- **F (Fail)**: 0-39 - Does not meet minimum requirements

---

## FEEDBACK TEMPLATE UNTUK GURU

### Strengths (Yang sudah baik):
- ________________________________________________
- ________________________________________________
- ________________________________________________

### Areas for Improvement (Yang perlu diperbaiki):
- ________________________________________________
- ________________________________________________
- ________________________________________________

### Recommendations (Saran untuk pengembangan):
- ________________________________________________
- ________________________________________________
- ________________________________________________

### Overall Comment:
________________________________________________
________________________________________________
________________________________________________

---

## SELF-REFLECTION CHECKLIST

**Setelah mengerjakan quiz, centang yang sudah kamu capai:**

### Technical Skills:
- [ ] Bisa membuat aplikasi Flask dari nol
- [ ] Paham konsep CRUD operations
- [ ] Bisa implementasi validasi data
- [ ] Bisa handle error dan debugging
- [ ] Bisa mengintegrasikan HTML dengan Flask
- [ ] Paham struktur database JSON

### Soft Skills:
- [ ] Bisa brainstorming ide kreatif
- [ ] Bisa manage waktu dalam project
- [ ] Bisa present hasil karya dengan percaya diri
- [ ] Bisa problem solving secara mandiri
- [ ] Bisa belajar dari kesalahan
- [ ] Bisa bekerja dengan minimal guidance

### Mindset:
- [ ] Growth mindset dalam belajar coding
- [ ] Tidak takut mencoba hal baru
- [ ] Persistent dalam mengatasi masalah
- [ ] Excited tentang teknologi dan programming
- [ ] Confident untuk terus belajar
- [ ] Melihat coding sebagai tool untuk solve problems

---

## NEXT STEPS & RECOMMENDATIONS

### Immediate Actions (1-2 minggu ke depan):
1. **Polish your project**: Perbaiki bug, tambah fitur kecil
2. **Share with friends**: Tunjukkan ke teman dan keluarga
3. **Document your journey**: Tulis blog post atau diary
4. **Join communities**: Gabung grup programming Indonesia

### Short-term Goals (1-3 bulan):
1. **Learn new framework**: Coba Django atau FastAPI
2. **Frontend skills**: Belajar JavaScript dan CSS framework
3. **Database upgrade**: Belajar SQL dan database relational
4. **Version control**: Belajar Git dan GitHub

### Long-term Vision (6-12 bulan):
1. **Build portfolio**: Kumpulkan 3-5 proyek untuk portfolio
2. **Contribute to open source**: Mulai kontribusi ke proyek open source
3. **Participate in competitions**: Ikut hackathon atau coding competition
4. **Consider career path**: Eksplorasi karir di bidang tech

---

**🎉 CONGRATULATIONS! 🎉**

**Kamu telah menyelesaikan perjalanan 4 pertemuan Python Full-Stack!**

**Remember:**
- Every expert was once a beginner
- Your first project might be simple, but your growth mindset is powerful
- The skills you've learned will serve you well in any field
- Keep coding, keep creating, keep dreaming big!

**🚀 The journey doesn't end here - it's just the beginning! 🚀**

---

**Catatan Guru:**
________________________________________________
________________________________________________
________________________________________________

**Nilai Akhir**: _____ / 205 poin = _____ %

**Grade**: _____ (A/B/C/D/F)

**Tanggal**: ___________________
**Tanda Tangan Guru**: ___________________