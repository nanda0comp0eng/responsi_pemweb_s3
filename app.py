from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Database connection using environment variables
def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        port=int(os.getenv('DB_PORT', 3307))
    )

# Home page
@app.route('/')
def index():
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tbl_mahasiswa")
    mahasiswa = cursor.fetchall()
    cursor.close()
    db.close()
    return render_template('index.html', mahasiswa=mahasiswa)

# Tambah data
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nim = request.form['nim']
        nama = request.form['nama']
        asal = request.form['asal']
        
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO tbl_mahasiswa (nim, nama, asal) VALUES (%s, %s, %s)", 
                      (nim, nama, asal))
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for('index'))
    return render_template('add.html')

# Edit data
@app.route('/edit/<nim>', methods=['GET', 'POST'])
def edit(nim):
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tbl_mahasiswa WHERE nim = %s", (nim,))
    mahasiswa = cursor.fetchone()
    
    if request.method == 'POST':
        nama = request.form['nama']
        asal = request.form['asal']
        cursor.execute("UPDATE tbl_mahasiswa SET nama = %s, asal = %s WHERE nim = %s", 
                      (nama, asal, nim))
        db.commit()
        cursor.close()
        db.close()
        return redirect(url_for('index'))
        
    cursor.close()
    db.close()
    return render_template('edit.html', mahasiswa=mahasiswa)

# Hapus data
@app.route('/delete/<nim>')
def delete(nim):
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("DELETE FROM tbl_mahasiswa WHERE nim = %s", (nim,))
    db.commit()
    cursor.close()
    db.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=os.getenv('FLASK_DEBUG', 'False').lower() == 'true')