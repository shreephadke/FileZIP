from flask import Flask, jsonify, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

@app.route('/', methods=['POST'])
def index():
  """ POST API Call that receives input json from the user, adds file to list of uploaded files,
      generates a unique fileID, and gives the user the name of the file that has been appended
      to uploaded.txt as well as its unique identifier
  """
  if request.method == 'POST':
    uploaded_json = request.get_json()
    filename = uploaded_json["file name"]
    filename = duplicateName(filename)
    updateList(filename)
    fileID = generateID(filename)
    return jsonify({'You uploaded:': filename, 'fileID:': fileID})

# mention lossless compression


def duplicateName(filename):
  """ Handles filename collisions, calls changeBase function to rename the base of the file
      before returning it back to the user.
  """
  ind = 0
  # separates file name base from its extension
  for i in range(len(filename)-1,-1,-1):
    if filename[i] == '.':
      ind = i
  base = filename[:ind]
  # reads file
  with open("uploaded.txt", "r") as f:
    # if there already exists a file with that base, append _# to the base
    for line in f:
      stripped_line = line.strip()
      if stripped_line == filename:
        # calls changeBase function
        newBase = changeBase(filename, base, ind)
        return newBase
  # catch all return statement
  return filename

def changeBase(filename, base, ind):
  """ Takes filename, base, and index where extension begins as arguments.
      Iterates over uploaded.txt, line by line, and changes the file name to an appropriate one
      using incrementing.
  """
  count = 0
  with open("uploaded.txt", "r") as f:
    for line in f:
      stripped_line = line.strip()
      # if the filename is the same as the one in uploaded.txt or has a similar suffix, rename
      if stripped_line == filename or (base + '_') in stripped_line:
        count += 1
    return base + '_' + str(count) + filename[ind:]
  return filename

def updateList(filename):
  """ Adds appropriate filename to uploaded.txt after collisions have been handled, etc.
  """
  file1 = open("uploaded.txt","a")
  file1.write(filename + '\n')
  file1.close()

def generateID(filename):
  """ Generates a unique file identifier for each file using a simple increment method within
      a persistent data structure.
  """
  count = 0
  with open("uploaded.txt", "r") as f:
    for line in f:
      stripped_line = line.strip()
      count += 1
      if stripped_line == filename:
        return count

if __name__ == '__main__':
    app.run(debug=True)
