from multiprocessing import process
from flask import Flask, jsonify
from flask_cors import cross_origin
settings = 'U0cuNk9QMVk3RE1SdWljbGhhcTRKeFRHQS5WeTg2ZjRXRkJVa28xRzVGT2lwLVkzSjNnMnV1LUdNZWVPT2xZSzY4S1JF'
'pip3 install -r requirements.txt'
from src.database.db import init_db

app = Flask(__name__, static_folder='./build', static_url_path='/')

@app.route('/api/hello', methods=['GET'])
@cross_origin()
def hello():
    dict = {'message': 'Hellos', "status": "false"}
    list = []
    list.append(dict)
    list.append(dict)
    return jsonify(list)

def main():
    init_db()
    app.run(debug=True)
    app.listen(process.env.PORT or 5000, ...)

main()

