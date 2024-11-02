from flask import Flask, request, jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

# Contoh data roti
breads = [
    {"id": "1", "name": "Roti Tawar", "description": "Roti tawar lembut dan segar", "price": 15000, "available": True},
    {"id": "2", "name": "Croissant", "description": "Croissant mentega yang renyah", "price": 20000, "available": True},
]

# Endpoint untuk menampilkan daftar produk
class BreadList(Resource):
    def get(self):
        return {
            "error": False,
            "message": "success",
            "count": len(breads),
            "breads": breads
        }

# Endpoint untuk menampilkan detail produk
class BreadDetail(Resource):
    def get(self, bread_id):
        bread = next((b for b in breads if b["id"] == bread_id), None)
        if bread:
            return {
                "error": False,
                "message": "success",
                "bread": bread
            }
        return {"error": True, "message": "Bread not found"}, 404

# Endpoint untuk menambahkan produk baru
class AddBread(Resource):
    def post(self):
        data = request.get_json()
        new_bread = {
            "id": str(len(breads) + 1),  # ID unik berdasarkan urutan
            "name": data.get("name"),
            "description": data.get("description"),
            "price": data.get("price"),
            "available": data.get("available", True)
        }
        breads.append(new_bread)
        return {
            "error": False,
            "message": "success",
            "bread": new_bread
        }, 201

# Endpoint untuk memperbarui detail produk
class UpdateBread(Resource):
    def put(self, bread_id):
        bread = next((b for b in breads if b["id"] == bread_id), None)
        if bread:
            data = request.get_json()
            bread["name"] = data.get("name", bread["name"])
            bread["description"] = data.get("description", bread["description"])
            bread["price"] = data.get("price", bread["price"])
            bread["available"] = data.get("available", bread["available"])
            return {
                "error": False,
                "message": "success",
                "bread": bread
            }
        return {"error": True, "message": "Bread not found"}, 404

# Endpoint untuk menghapus produk
class DeleteBread(Resource):
    def delete(self, bread_id):
        global breads
        bread = next((b for b in breads if b["id"] == bread_id), None)
        if bread:
            breads = [b for b in breads if b["id"] != bread_id]
            return {
                "error": False,
                "message": "success",
                "deleted_bread": bread
            }
        return {"error": True, "message": "Bread not found"}, 404

# Menambahkan endpoint ke API
api.add_resource(BreadList, '/breads')
api.add_resource(BreadDetail, '/breads/<string:bread_id>')
api.add_resource(AddBread, '/breads/add')
api.add_resource(UpdateBread, '/breads/update/<string:bread_id>')
api.add_resource(DeleteBread, '/breads/delete/<string:bread_id>')

if __name__ == '__main__':
    app.run(debug=True)
