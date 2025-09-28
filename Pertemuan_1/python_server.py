from flask import Flask

app = Flask(__name__)

@app.route('/')
def halaman_utama():
    return "Halo! Ini adalah server Python!"

if __name__ == '__main__':
    app.run(debug=True)