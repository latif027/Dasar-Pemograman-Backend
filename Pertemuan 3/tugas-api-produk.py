from flask import Flask, jsonify, request
from flasgger import Swagger

app = Flask(__name__)
swagger = Swagger(app)

# Data produk (contoh awal)
snack_data = [
    {"id": 1, "nama": "Keripik Singkong", "harga": 10000},
    {"id": 2, "nama": "Kacang Goreng", "harga": 12000},
    {"id": 3, "nama": "Kerupuk Ikan", "harga": 8000},
]

drink_data = [
    {"id": 1, "nama": "Es Teh Manis", "harga": 5000},
    {"id": 2, "nama": "Jus Jeruk", "harga": 15000},
    {"id": 3, "nama": "Kopi Hitam", "harga": 10000},
]


@app.route('/')
def home():
    """
    Home Page
    ---
    responses:
      200:
        description: Selamat Datang
    """
    return jsonify({"message": "Selamat Datang Di Produk UMKM"})


# ==================== SNACK CRUD ====================

@app.route('/produk/snack', methods=['GET'])
def semua_snack():
    """
    Get Semua Snack
    ---
    responses:
      200:
        description: Daftar produk snack
    """
    return jsonify({"message": "Halaman Produk Semua Snack..", "data": snack_data})


@app.route('/produk/snack/<int:id>', methods=['GET'])
def snack_by_id(id):
    """
    Get Snack by ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    responses:
      200:
        description: Detail produk snack
    """
    produk = next((item for item in snack_data if item["id"] == id), None)
    if produk:
        return jsonify({"message": f"Halaman Produk Snack dengan id = {id}", "data": produk})
    return jsonify({"error": "Produk Snack tidak ditemukan"}), 404


@app.route('/produk/snack', methods=['POST'])
def tambah_snack():
    """
    Tambah Produk Snack
    ---
    parameters:
      - name: body
        in: body
        schema:
          properties:
            id:
              type: integer
            nama:
              type: string
            harga:
              type: integer
    responses:
      201:
        description: Snack berhasil ditambahkan
    """
    data = request.get_json()
    snack_data.append(data)
    return jsonify({"message": "Produk Snack berhasil ditambahkan", "data": data}), 201


@app.route('/produk/snack/<int:id>', methods=['PUT'])
def update_snack(id):
    """
    Update Produk Snack
    ---
    parameters:
      - name: id
        in: path
        type: integer
      - name: body
        in: body
        schema:
          properties:
            nama:
              type: string
            harga:
              type: integer
    responses:
      200:
        description: Snack berhasil diupdate
    """
    data = request.get_json()
    for item in snack_data:
        if item["id"] == id:
            item["nama"] = data.get("nama", item["nama"])
            item["harga"] = data.get("harga", item["harga"])
            return jsonify({"message": "Produk Snack berhasil diupdate", "data": item})
    return jsonify({"error": "Produk Snack tidak ditemukan"}), 404


@app.route('/produk/snack/<int:id>', methods=['DELETE'])
def hapus_snack(id):
    """
    Hapus Produk Snack
    ---
    parameters:
      - name: id
        in: path
        type: integer
    responses:
      200:
        description: Snack berhasil dihapus
    """
    global snack_data
    snack_data = [item for item in snack_data if item["id"] != id]
    return jsonify({"message": f"Produk Snack dengan id={id} berhasil dihapus"})


# ==================== DRINK CRUD ====================

@app.route('/produk/drink', methods=['GET'])
def semua_drink():
    """
    Get Semua Drink
    ---
    responses:
      200:
        description: Daftar produk minuman
    """
    return jsonify({"message": "Halaman Produk Semua Soft Drink..", "data": drink_data})


@app.route('/produk/drink/<int:id>', methods=['GET'])
def drink_by_id(id):
    """
    Get Drink by ID
    ---
    parameters:
      - name: id
        in: path
        type: integer
    responses:
      200:
        description: Detail produk minuman
    """
    produk = next((item for item in drink_data if item["id"] == id), None)
    if produk:
        return jsonify({"message": f"Halaman Produk Soft Drink dengan id = {id}", "data": produk})
    return jsonify({"error": "Produk Soft Drink tidak ditemukan"}), 404


@app.route('/produk/drink', methods=['POST'])
def tambah_drink():
    """
    Tambah Produk Drink
    ---
    parameters:
      - name: body
        in: body
        schema:
          properties:
            id:
              type: integer
            nama:
              type: string
            harga:
              type: integer
    responses:
      201:
        description: Drink berhasil ditambahkan
    """
    data = request.get_json()
    drink_data.append(data)
    return jsonify({"message": "Produk Drink berhasil ditambahkan", "data": data}), 201


@app.route('/produk/drink/<int:id>', methods=['PUT'])
def update_drink(id):
    """
    Update Produk Drink
    ---
    parameters:
      - name: id
        in: path
        type: integer
      - name: body
        in: body
        schema:
          properties:
            nama:
              type: string
            harga:
              type: integer
    responses:
      200:
        description: Drink berhasil diupdate
    """
    data = request.get_json()
    for item in drink_data:
        if item["id"] == id:
            item["nama"] = data.get("nama", item["nama"])
            item["harga"] = data.get("harga", item["harga"])
            return jsonify({"message": "Produk Drink berhasil diupdate", "data": item})
    return jsonify({"error": "Produk Drink tidak ditemukan"}), 404


@app.route('/produk/drink/<int:id>', methods=['DELETE'])
def hapus_drink(id):
    """
    Hapus Produk Drink
    ---
    parameters:
      - name: id
        in: path
        type: integer
    responses:
      200:
        description: Drink berhasil dihapus
    """
    global drink_data
    drink_data = [item for item in drink_data if item["id"] != id]
    return jsonify({"message": f"Produk Drink dengan id={id} berhasil dihapus"})


if __name__ == '__main__':
    app.run(debug=True)
