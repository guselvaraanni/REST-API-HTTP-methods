from flask import Flask, request ,jsonify
import pymongo
import json

app = Flask(__name__)

myclient = pymongo.MongoClient("mongodb+srv://guselvaraanni:selvaraanni24@cluster0.03ahigd.mongodb.net/")

mydb = myclient["motor"]
mycol=mydb["steel"]
@app.route('/')
def hello_world():
    output=dict()
    for x in mycol.find():
        output[str(x['_id'])]={
                            "b_sat":x["b_sat"],
                            "grade":x["grade"],
                            "thickness":x["thickness"]
                            }
    output = json.dumps(output)
    print(output)

    return jsonify(output)


if __name__ == '__main__':
	app.run()




