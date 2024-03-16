from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# Replace MONGO_URI with your actual MongoDB connection string
MONGO_URI = "mongodb+srv://guselvaraanni:selvaraanni24@cluster0.03ahigd.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["motor"]
steel_collection = db["steel"]
magnet_collection = db["magnet"]
copper_collection = db["copper"]
copper_iron_collection = db["copper_iron"]

@app.route('/update/steel')
def steel():
    return render_template('update_steel.html', document={})

@app.route('/update/magnet')
def magnet():
    return render_template('update_magnet.html', document={})

@app.route('/update/copper')
def copper():
    return render_template('update_copper.html', document={})

@app.route('/update/copper_iron')
def copper_iron():
    return render_template('update_copper_iron.html', document={})

@app.route('/update_steel/<string:document_id>', methods=['GET'])
def get_steel_document(document_id):
    return get_document(document_id, steel_collection, 'update_steel.html')

@app.route('/update_magnet/<string:document_id>', methods=['GET'])
def get_magnet_document(document_id):
    return get_document(document_id, magnet_collection, 'update_magnet.html')

@app.route('/update_copper/<string:document_id>', methods=['GET'])
def get_copper_document(document_id):
    return get_document(document_id, copper_collection, 'update_copper.html')

@app.route('/update_copper_iron/<string:document_id>', methods=['GET'])
def get_copper_iron_document(document_id):
    return get_document(document_id, copper_iron_collection, 'update_copper_iron.html')

def get_document(document_id, collection, template):
    try:
        obj_id = ObjectId(document_id)
        document = collection.find_one({'_id': obj_id})
        if document:
            return render_template(template, document=document)
        else:
            return jsonify({'error': 'Document not found'}), 404
    except Exception as e:
        return jsonify({'error': 'Invalid document ID'}), 400

@app.route('/update_steel', methods=['PATCH'])
def update_steel_document():
    return update_document(steel_collection)

@app.route('/update_magnet', methods=['PATCH'])
def update_magnet_document():
    return update_document(magnet_collection)

@app.route('/update_copper', methods=['PATCH'])
def update_copper_document():
    return update_document(copper_collection)

@app.route('/update_copper_iron', methods=['PATCH'])
def update_copper_iron_document():
    return update_document(copper_iron_collection)


def update_document(collection):
    data = request.form.to_dict()
    document_id = data.get('_id')

    try:
        obj_id = ObjectId(document_id)
    except Exception as e:
        return jsonify({'error': 'Invalid document ID'}), 400

    # Convert numeric fields to appropriate data types
    numeric_fields = ['b_r', 'k_pm', 'mu_ra', 'density', 'rs_per_g','b_sat','grade','thickness','density','rs_per_g','hyst_factor','eddy_factor','extra_factor','wire_diameter','resistivity','temp_coeff_resistivity','htc']
    for field in numeric_fields:
        if field in data:
            data[field] = float(data[field])

    update_query = {'$set': {key: value for key, value in data.items() if key != '_id'}}

    try:
        result = collection.update_one({'_id': obj_id}, update_query)
        if result.modified_count > 0:
            return jsonify({'message': 'Document updated successfully'})
        else:
            return jsonify({'error': 'Document not found or no changes made'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
