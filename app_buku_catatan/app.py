from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# Data catatan (sementara disimpan di memory)
catatan_list = []

@app.route('/')
def lihat_catatan():
    """Menampilkan semua catatan (READ)"""
    return render_template('index.html', catatan=catatan_list)

@app.route('/tambah', methods=['GET', 'POST'])
def tambah_catatan():
    """Menambah catatan baru (CREATE)"""
    if request.method == 'POST':
        judul = request.form['judul']
        isi = request.form['isi']
        
        catatan_baru = {
            'id': len(catatan_list) + 1,
            'judul': judul,
            'isi': isi
        }
        catatan_list.append(catatan_baru)
        return redirect('/')
    
    return render_template('tambah.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_catatan(id):
    """Mengedit catatan (UPDATE)"""
    # Cari catatan berdasarkan ID
    catatan = None
    for c in catatan_list:
        if c['id'] == id:
            catatan = c
            break
    
    if not catatan:
        return redirect('/')  # Jika catatan tidak ditemukan, kembali ke halaman utama
    
    if request.method == 'POST':
        # Update data catatan
        catatan['judul'] = request.form['judul']
        catatan['isi'] = request.form['isi']
        return redirect('/')
    
    return render_template('edit.html', catatan=catatan)

@app.route('/hapus/<int:id>')
def hapus_catatan(id):
    """Menghapus catatan (DELETE)"""
    global catatan_list
    catatan_list = [c for c in catatan_list if c['id'] != id]
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)