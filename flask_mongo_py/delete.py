from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# Replace MONGO_URI with your actual MongoDB connection string
MONGO_URI = "mongodb+srv://guselvaraanni:selvaraanni24@cluster0.03ahigd.mongodb.net/motor"
client = MongoClient(MONGO_URI)
db = client["motor"]

# Specify the collections
collections = ["steel", "magnet", "copper", "copper_iron"]

@app.route('/')
def index():
    return render_template('delete.html', collections=collections)

@app.route('/delete', methods=['POST'])
def delete_document():
    try:
        collection_name = request.form['collection']
        document_id = request.form['document_id']

        # Check if the specified collection is valid
        if collection_name not in collections:
            return jsonify({'error': 'Invalid collection name'}), 400

        # Delete document by ID
        collection = db[collection_name]
        obj_id = ObjectId(document_id)
        result = collection.delete_one({'_id': obj_id})

        if result.deleted_count > 0:
            return jsonify({'message': 'Document deleted successfully'})
        else:
            return jsonify({'error': 'Document not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
