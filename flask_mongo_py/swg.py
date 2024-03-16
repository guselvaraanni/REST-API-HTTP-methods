from flask import Flask, render_template, request
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb+srv://guselvaraanni:selvaraanni24@cluster0.03ahigd.mongodb.net/')
db = client['motor']
collection = db['swg']

@app.route('/')
def index():
    return render_template('swg_output.html')

@app.route('/retrieve', methods=['POST'])
def retrieve():
    swg_key = request.form['swg_key']

    
    result = collection.find_one({str(swg_key): {"$exists": True}})

    if result:
        value = result[str(swg_key)]
        return render_template('swg_output.html', swg_key=swg_key, value=value),print("SWG value of" , swg_key , "is" , result)
    else:
        return render_template('swg_output.html', swg_key=swg_key, error_message="No matching value found in the database.")

if __name__ == '__main__':
    app.run(debug=True)
