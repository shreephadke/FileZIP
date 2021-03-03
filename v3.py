from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():
  if request.method == 'POST':
    uploaded_json = request.get_json()
    filename = uploaded_json["file name"]
    updateList(filename)
    fileID = generateID(filename)
    return jsonify({'You uploaded:': uploaded_json, 'fileID:': fileID})

def updateList(filename):
  file1 = open("uploaded.txt","a")
  file1.write(filename + '\n')
  file1.close()

def generateID(filename):
  count = 0
  with open("uploaded.txt", "r") as f:
    for line in f:
      stripped_line = line.strip()
      count += 1
      if stripped_line == filename:
        return count

if __name__ == '__main__':
    app.run(debug=True)
