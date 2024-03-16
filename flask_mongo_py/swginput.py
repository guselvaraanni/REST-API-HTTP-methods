from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient('mongodb+srv://guselvaraanni:selvaraanni24@cluster0.03ahigd.mongodb.net/')
db = client['motor']
collection = db['swg1']


@app.route('/')
def index():
    return render_template('swg_input.html')

@app.route('/insert', methods=['POST'])
def insert():
    key = request.form['swg_key']
    value = request.form['diameter_value']

    # Convert the value to the corresponding data type
    try:
        key = float(key)
        value = float(value)
    except ValueError:
        # Handle the case where the value is not a valid float
        return "Invalid value. Please enter a valid numeric value."

    data = {str(key): value}
    
    # Debugging: Print values before insertion
    print(f"Inserting data: {data}")

    collection.insert_one(data)

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)