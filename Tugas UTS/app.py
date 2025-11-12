from flask import Flask, render_template, jsonify, request, abort

app = Flask(__name__)

cars = [
    {"id": 1, "nama": "Lamborghini Aventador", "harga": 1500000000, "gambar": "https://i.imgur.com/oyC7Iqs.jpg"},
    {"id": 2, "nama": "Ferrari 488 GTB", "harga": 1300000000, "gambar": "https://i.imgur.com/4G7cKxg.jpg"},
    {"id": 3, "nama": "Nissan GTR R35", "harga": 950000000, "gambar": "https://i.imgur.com/WlC3VZ1.jpg"}
]

def find_car(cid):
    for c in cars:
        if c['id'] == cid:
            return c
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/mobil', methods=['GET'])
def list_cars():
    return jsonify(cars)

@app.route('/api/mobil/<int:cid>', methods=['GET'])
def get_car(cid):
    car = find_car(cid)
    if not car:
        abort(404)
    return jsonify(car)

@app.route('/api/mobil', methods=['POST'])
def create_car():
    data = request.get_json() or {}
    nama = data.get('nama')
    harga = data.get('harga')
    gambar = data.get('gambar','')
    if not nama or harga is None:
        return jsonify({'error':'nama dan harga wajib'}),400
    new_id = max([c['id'] for c in cars] or [0]) + 1
    car = {'id': new_id, 'nama': nama, 'harga': int(harga), 'gambar': gambar}
    cars.append(car)
    return jsonify(car), 201

@app.route('/api/mobil/<int:cid>', methods=['PUT'])
def update_car(cid):
    car = find_car(cid)
    if not car:
        abort(404)
    data = request.get_json() or {}
    nama = data.get('nama', car['nama'])
    harga = data.get('harga', car['harga'])
    gambar = data.get('gambar', car.get('gambar',''))
    car.update({'nama': nama, 'harga': int(harga), 'gambar': gambar})
    return jsonify(car)

@app.route('/api/mobil/<int:cid>', methods=['DELETE'])
def delete_car(cid):
    global cars
    car = find_car(cid)
    if not car:
        abort(404)
    cars = [c for c in cars if c['id'] != cid]
    return jsonify({'deleted': True})

if __name__ == '__main__':
    app.run(debug=True)
