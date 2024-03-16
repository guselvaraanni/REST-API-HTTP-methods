from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

app = Flask(__name__)

MONGO_URI = "mongodb+srv://guselvaraanni:selvaraanni24@cluster0.03ahigd.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["motor"]
collections = {
    "steel": db["steel"],
    "magnet": db["magnet"],
    "copper": db["copper"],
    "copper_iron": db["copper_iron"],
}


#steel
@app.route('/steel')
def display_collection_steel():
    collection_name = 'steel'
    collection = collections.get(collection_name)
    if collection is None:
        return jsonify({"error": f"Collection {collection_name} not found"}), 404

    data = []
    for record in collection.find():
        data.append({
            "_id": str(record['_id']),
            "b_sat": record.get("b_sat", ""),
            "grade": record.get("grade", ""),
            "thickness": record.get("thickness", ""),
            "density": record.get("density", ""),
            "rs_per_g": record.get("rs_per_g", ""),
            "hyst_factor": record.get("hyst_factor", ""),
            "eddy_factor": record.get("eddy_factor", ""),
            "extra_factor": record.get("extra_factor", "")
        })

    if collection_name == 'steel':
        html_file = 'index.html'
    elif collection_name == 'magnet':
        html_file = 'magnet.html'
    elif collection_name == 'copper':
        html_file = 'copper.html'
    elif collection_name == 'copper_iron':
        html_file = 'copperIron.html'
    else:
        return jsonify({"error": "Invalid collection name"}), 400

    return render_template(html_file, data=data)

@app.route('/post_data', methods=['POST'])
def post_data():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request, data missing"}), 400

    collection_name = data.get('collection')
    collection = collections.get(collection_name)
    if collection is None:
        return jsonify({"error": f"Collection {collection_name} not found"}), 404

    new_data = {
        "b_sat": float(data.get('b_sat', 0.0)),
        "grade": data.get('grade', ''),
        "thickness": float(data.get('thickness', 0.0)),
        "density": float(data.get('density', 0.0)),
        "rs_per_g": float(data.get('rs_per_g', 0.0)),
        "hyst_factor": float(data.get('hyst_factor', 0.0)),
        "eddy_factor": float(data.get('eddy_factor', 0.0)),
        "extra_factor": float(data.get('extra_factor', 0.0))
    }

    result = collection.insert_one(new_data)

    inserted_data = {
        "_id": str(result.inserted_id),
        "b_sat": new_data["b_sat"],
        "grade": new_data["grade"],
        "thickness": new_data["thickness"],
        "density": new_data["density"],
        "rs_per_g": new_data["rs_per_g"],
        "hyst_factor": new_data["hyst_factor"],
        "eddy_factor": new_data["eddy_factor"],
        "extra_factor": new_data["extra_factor"],
    }

    print(f"Data inserted successfully: {inserted_data}")
    return jsonify({"message": "Data inserted successfully", "data": inserted_data})



#magnet
@app.route('/magnet')
def display_collection_magnet():
    collection_name = 'magnet'
    collection = collections.get(collection_name)
    
    if collection is None:
        return jsonify({"error": f"Collection {collection_name} not found"}), 404

    data = []
    for record in collection.find():
        data.append({
            "_id": str(record['_id']),
            "b_r": record.get("b_r", ""),
            "k_pm": record.get("k_pm", ""),
            "mu_ra": record.get("mu_ra", ""),
            "density": record.get("density", ""),
            "rs_per_g": record.get("rs_per_g", ""),
        })

    return render_template('magnet.html', data=data, collection_name=collection_name)

@app.route('/post_magnet', methods=['POST'])
def post_magnet():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request, data missing"}), 400

    collection_name = data.get('collection_name')
    collection = collections.get(collection_name)
    if collection is None:
        return jsonify({"error": f"Collection {collection_name} not found"}), 404

    new_data = {
        "b_r": float(data.get('b_r', 0.0)),
        "k_pm":float(data.get('k_pm', 0.0)),
        "mu_ra":float(data.get('mu_ra', 0.0)),
        "density":float(data.get('density', 0.0)),
        "rs_per_g":float(data.get('rs_per_g', 0.0)),
        
    }

    result = collection.insert_one(new_data)

    inserted_data = {
        "_id": str(result.inserted_id),
        "b_r": new_data["b_r"],
        "k_pm": new_data["k_pm"],
        "mu_ra": new_data["mu_ra"],
        "density": new_data["density"],
        "rs_per_g": new_data["rs_per_g"],
        
    }

    print(f"Data inserted successfully: {inserted_data}")
    return jsonify({"message": "Data inserted successfully", "data": inserted_data})


# Copper routes

@app.route('/copper')
def display_collection_copper():
    collection_name = 'copper'
    collection = collections.get(collection_name)

    if collection is None:
        return jsonify({"error": f"Collection {collection_name} not found"}), 404

    data = []
    for record in collection.find():
        data.append({
            "_id": str(record['_id']),
            "wire_diameter": record.get("wire_diameter", ""),
            "resistivity": record.get("resistivity", ""),
            "temp_coeff_resistivity": record.get("temp_coeff_resistivity", ""),
            "density": record.get("density", ""),
            "rs_per_g": record.get("rs_per_g", ""),
        })

    return render_template('copper.html', data=data, collection_name=collection_name)

@app.route('/post_copper', methods=['POST'])
def post_copper():
    data = request.get_json()
    print("Received JSON data for copper:", data)  # Debugging statement

    if not data:
        return jsonify({"error": "Invalid request, data missing"}), 400

    collection_name = 'copper'
    collection = collections.get(collection_name)

    if collection is None:
        return jsonify({"error": f"Collection {collection_name} not found"}), 404

    new_data = {
        "wire_diameter": float(data.get('wire_diameter', 0.0)),
        "resistivity": float(data.get('resistivity', 0.0)),
        "temp_coeff_resistivity": float(data.get('temp_coeff_resistivity', 0.0)),
        "density": float(data.get('density', 0.0)),
        "rs_per_g": float(data.get('rs_per_g', 0.0)),
    }

    result = collection.insert_one(new_data)

    inserted_data = {
        "_id": str(result.inserted_id),
        "wire_diameter": new_data["wire_diameter"],
        "resistivity": new_data["resistivity"],
        "temp_coeff_resistivity": new_data["temp_coeff_resistivity"],
        "density": new_data["density"],
        "rs_per_g": new_data["rs_per_g"],
    }

    print(f"Data inserted successfully: {inserted_data}")
    return jsonify({"message": "Data inserted successfully", "data": inserted_data})




#copper_iron
@app.route('/copper_iron')
def display_collection_copper_iron():
    collection_name = 'copper_iron'
    collection = collections.get(collection_name)
    
    if collection is None:
        return jsonify({"error": f"Collection {collection_name} not found"}), 404

    data = []
    for record in collection.find():
        data.append({
            "_id": str(record['_id']),
            "htc": record.get("htc", ""),
        })

    return render_template('copperIron.html', data=data, collection_name=collection_name)

@app.route('/post_copper_iron', methods=['POST'])
def post_copper_iron():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request, data missing"}), 400

    collection_name = data.get('collection_name')
    collection = collections.get(collection_name)
    if collection is None:
        return jsonify({"error": f"Collection {collection_name} not found"}), 404

    new_data = {
        "htc": float(data.get('htc', 0.0)),
    }

    result = collection.insert_one(new_data)

    inserted_data = {
        "_id": str(result.inserted_id),
        "htc": new_data["htc"],
    }

    print(f"Data inserted successfully: {inserted_data}")
    return jsonify({"message": "Data inserted successfully", "data": inserted_data})


if __name__ == '__main__':
    app.run(debug=True, threaded=False)
