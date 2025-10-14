from flask import Flask, jsonify, request
import json, os

app = Flask(__name__)

# ------------------------
# Fungsi bantu untuk load & save JSON
# ------------------------
def load_data(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as f:
            return json.load(f)
    return []

def save_data(file_name, data):
    with open(file_name, 'w') as f:
        json.dump(data, f, indent=2)


# ------------------------
# Route Utama
# ------------------------
@app.route('/', methods=['GET'])
def index():
    return jsonify({"pesan": "Selamat Datang Di Produk UMKM"}), 200


# ------------------------
# CRUD Snack
# ------------------------
@app.route('/produk/snack', methods=['GET', 'POST'])
def semua_snack():
    snacks = load_data("snacks.json")
    if request.method == 'GET':
        return jsonify({"pesan": "Halaman Produk Semua Snack..", "data": snacks}), 200
    elif request.method == 'POST':
        data = request.get_json()
        new_id = len(snacks) + 1
        produk = {"id": new_id, "nama": data['nama'], "harga": data['harga']}
        snacks.append(produk)
        save_data("snacks.json", snacks)
        return jsonify({"pesan": "Snack berhasil ditambahkan", "data": produk}), 201


@app.route('/produk/snack/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def snack_by_id(id):
    snacks = load_data("snacks.json")
    produk = next((item for item in snacks if item["id"] == id), None)
    if not produk:
        return jsonify({"error": "Snack tidak ditemukan"}), 404

    if request.method == 'GET':
        return jsonify({"pesan": f"Halaman Produk Snack dengan id = {id}", "data": produk}), 200
    
    elif request.method == 'PUT':
        data = request.get_json()
        produk["nama"] = data.get("nama", produk["nama"])
        produk["harga"] = data.get("harga", produk["harga"])
        save_data("snacks.json", snacks)
        return jsonify({"pesan": "Snack berhasil diupdate", "data": produk}), 200

    elif request.method == 'DELETE':
        snacks.remove(produk)
        save_data("snacks.json", snacks)
        return jsonify({"pesan": f"Snack dengan id {id} berhasil dihapus"}), 200


# ------------------------
# CRUD Drink
# ------------------------
@app.route('/produk/drink', methods=['GET', 'POST'])
def semua_drink():
    drinks = load_data("drinks.json")
    if request.method == 'GET':
        return jsonify({"pesan": "Halaman Produk Semua Soft Drink..", "data": drinks}), 200
    elif request.method == 'POST':
        data = request.get_json()
        new_id = len(drinks) + 1
        produk = {"id": new_id, "nama": data['nama'], "harga": data['harga']}
        drinks.append(produk)
        save_data("drinks.json", drinks)
        return jsonify({"pesan": "Soft Drink berhasil ditambahkan", "data": produk}), 201


@app.route('/produk/drink/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def drink_by_id(id):
    drinks = load_data("drinks.json")
    produk = next((item for item in drinks if item["id"] == id), None)
    if not produk:
        return jsonify({"error": "Soft Drink tidak ditemukan"}), 404

    if request.method == 'GET':
        return jsonify({"pesan": f"Halaman Produk Soft Drink dengan id = {id}", "data": produk}), 200
    
    elif request.method == 'PUT':
        data = request.get_json()
        produk["nama"] = data.get("nama", produk["nama"])
        produk["harga"] = data.get("harga", produk["harga"])
        save_data("drinks.json", drinks)
        return jsonify({"pesan": "Soft Drink berhasil diupdate", "data": produk}), 200

    elif request.method == 'DELETE':
        drinks.remove(produk)
        save_data("drinks.json", drinks)
        return jsonify({"pesan": f"Soft Drink dengan id {id} berhasil dihapus"}), 200


# ------------------------
if __name__ == '__main__':
    app.run(debug=True)
