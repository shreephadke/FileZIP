from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
  if request.method == 'POST':
    uploaded_json = request.get_json()
    filename = uploaded_json["file name"]
    return jsonify({'You uploaded:': uploaded_json})

if __name__ == '__main__':
    app.run(debug=True)
