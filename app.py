from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection
db = mysql.connector.connect(
    host="876ke.h.filess.io",
    database="dbkuliah_honormice",
    user="dbkuliah_honormice",
    password="e3a960a71b43773752b6f42a4099582c62f0f9fa",
    port=3307
)

# Home page
@app.route('/')
def index():
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tbl_mahasiswa")
    mahasiswa = cursor.fetchall()
    return render_template('index.html', mahasiswa=mahasiswa)

# Tambah data
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nim = request.form['nim']
        nama = request.form['nama']
        asal = request.form['asal']
        cursor = db.cursor()
        cursor.execute("INSERT INTO tbl_mahasiswa (nim, nama, asal) VALUES (%s, %s, %s)", (nim, nama, asal))
        db.commit()
        return redirect(url_for('index'))
    return render_template('add.html')

# Edit data
@app.route('/edit/<nim>', methods=['GET', 'POST'])
def edit(nim):
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tbl_mahasiswa WHERE nim = %s", (nim,))
    mahasiswa = cursor.fetchone()
    if request.method == 'POST':
        nama = request.form['nama']
        asal = request.form['asal']
        cursor = db.cursor()
        cursor.execute("UPDATE tbl_mahasiswa SET nama = %s, asal = %s WHERE nim = %s", (nama, asal, nim))
        db.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', mahasiswa=mahasiswa)

# Hapus data
@app.route('/delete/<nim>')
def delete(nim):
    cursor = db.cursor()
    cursor.execute("DELETE FROM tbl_mahasiswa WHERE nim = %s", (nim,))
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)