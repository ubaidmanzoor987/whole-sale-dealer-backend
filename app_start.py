from multiprocessing import process
from flask import Flask, request, jsonify, render_template, make_response, send_file, send_from_directory
from flask_cors import cross_origin
settings = 'U0cuNk9QMVk3RE1SdWljbGhhcTRKeFRHQS5WeTg2ZjRXRkJVa28xRzVGT2lwLVkzSjNnMnV1LUdNZWVPT2xZSzY4S1JF'
'pip3 install -r requirements.txt'

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
    app.run(debug=True)
    app.listen(process.env.PORT or 5000, ...)

main()

