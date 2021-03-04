from flask import Flask, jsonify, request
from flask_restful import Resource, Api
import zipfile, os
from datetime import date
#import wget
#import threading

app = Flask(__name__)
api = Api(app)
today = date.today()

@app.route('/', methods=['POST'])
def index():
  """ POST API Call that receives input json from the user, adds file to list of uploaded files,
      generates a unique fileID, and gives the user the name of the file that has been appended
      to uploaded.txt as well as its unique identifier
  """
  if request.method == 'POST':
    uploaded_json = request.get_json()
    originalName = uploaded_json["file name"]
    filename = duplicateName(originalName)
    # if the new file name is different than the original (it has been modified),
    # then rename the original to the new file name and update the list accordingly
    if originalName != filename:
      os.rename(originalName,filename)
    updateList(filename)
    fileID = generateID(filename)
    # background process to output the fileID to the user
    print(f"Filename: {filename}, FileID: {fileID}, File Size: {file_size(filename)}")
    #zip_thread = threading.Thread(target=zip, args=(filename))
    #zip_thread.start()
    #print(f"You uploaded {filename} with a fileID of {fileID}")
    #return jsonify({'You uploaded:': filename, 'fileID:': fileID})
    return zip(filename, fileID)

class Download(Resource):
  def get(self, fileID):
    """ GET API Call that receives fileID as input and returns the correct zip file as output
    """
    count = 0
    with open("uploaded.txt", "r") as f:
      for line in f:
        count += 1
        if count == fileID:
          stripped_line = line.strip()
          name = stripped_line.split(',')
          filename = name[0]
          zipFile = str("zipped/" + filename[:ind(filename)] + '.zip')
          #wget.download(zipFile)
          return zipFile
    return "Error: File has not yet been zipped."

def zip(filename, fileID):
  """ In charge of zipping the file and adding it to the folder titled "zipped".
      Uses Lempel-Ziv-Markov-Chain Algorithm for lossless compression
  """
  zipName = filename[:ind(filename)] + '.zip'
  zip_file = zipfile.ZipFile('zipped/' + zipName,'w')
  zip_file.write(filename, compress_type=zipfile.ZIP_DEFLATED)
  zip_file.close()
  return f"The file {filename} with fileID {fileID} and file size {file_size(filename)} has been zipped!" + '\n'

def ind(filename):
  """ find the index where the file extension begins
  """
  for i in range(len(filename)-1,-1,-1):
    if filename[i] == '.':
      return i

def duplicateName(filename):
  """ Handles filename collisions, calls changeBase function to rename the base of the file
      before returning it back to the user.
  """
  base = filename[:ind(filename)]
  # reads file
  with open("uploaded.txt", "r") as f:
    # if there already exists a file with that base, append _# to the base
    for line in f:
      stripped_line = line.strip()
      name = stripped_line.split(',')
      if name[0] == filename:
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
      name = stripped_line.split(',')
      # if the filename is the same as the one in uploaded.txt or has a similar suffix, rename
      if name[0] == filename or (base + '_') in stripped_line:
        count += 1
    return base + '_' + str(count) + filename[ind(filename):]
  return filename

def updateList(filename):
  """ Adds appropriate filename to uploaded.txt after collisions have been handled, etc.
  """
  date_uploaded = today.strftime("%b-%d-%Y")
  file1 = open("uploaded.txt", "a")
  file1.write(filename + ',' + str(file_size(filename)) + ',' + str(date_uploaded) + '\n')
  file1.close()

def file_size(filename):
    if os.path.isfile(filename):
        file_info = os.stat(filename)
        return byteConvert(file_info.st_size)

def byteConvert(num):
    for i in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, i)
        num /= 1024.0

def generateID(filename):
  """ Generates a unique file identifier for each file using a simple increment method within
      a persistent data structure.
  """
  count = 0
  with open("uploaded.txt", "r") as f:
    for line in f:
      stripped_line = line.strip()
      name = stripped_line.split(',')
      count += 1
      if name[0] == filename:
        return count

api.add_resource(Download, '/get/<int:fileID>')

if __name__ == '__main__':
    app.run(debug=True)
