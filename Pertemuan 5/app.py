from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "mapaswangi_secret"

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'latif'
app.config['MYSQL_DB'] = 'crud_db'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM stok ORDER BY id DESC")
    items = cur.fetchall()
    cur.close()
    return render_template('index.html', items=items)

@app.route('/search')
def search():
    q = request.args.get('q', '')
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM stok WHERE nama LIKE %s OR kategori LIKE %s ORDER BY id DESC", (f"%{q}%", f"%{q}%"))
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nama = request.form['nama']
        kategori = request.form['kategori']
        jumlah = request.form['jumlah']
        harga = request.form['harga']
        if not nama.strip():
            flash('Nama barang wajib diisi.', 'danger')
            return redirect(url_for('add'))
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO stok (nama, kategori, jumlah, harga) VALUES (%s, %s, %s, %s)", (nama, kategori, jumlah, harga))
        mysql.connection.commit()
        cur.close()
        flash('Barang berhasil ditambahkan!', 'success')
        return redirect(url_for('index'))
    return render_template('form.html', action='add', title='Tambah Barang')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM stok WHERE id=%s", (id,))
    item = cur.fetchone()
    if not item:
        flash('Data tidak ditemukan.', 'warning')
        return redirect(url_for('index'))
    if request.method == 'POST':
        nama = request.form['nama']
        kategori = request.form['kategori']
        jumlah = request.form['jumlah']
        harga = request.form['harga']
        cur.execute("UPDATE stok SET nama=%s, kategori=%s, jumlah=%s, harga=%s WHERE id=%s", (nama, kategori, jumlah, harga, id))
        mysql.connection.commit()
        flash('Data berhasil diperbarui!', 'success')
        return redirect(url_for('index'))
    cur.close()
    return render_template('form.html', action='edit', item=item, title='Edit Barang')

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM stok WHERE id=%s", (id,))
    mysql.connection.commit()
    cur.close()
    flash('Data berhasil dihapus!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
