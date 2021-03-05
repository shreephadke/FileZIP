from flask import Flask, request
from flask_restful import Resource, Api
import zipfile
from datetime import date
import os

app = Flask(__name__)
api = Api(app)
today = date.today()

@app.route('/', methods=['POST'])
def index():
  """ POST API Call that receives input json from the user, adds file to list of uploaded files,
      generates a unique fileID, and gives the user the name of the file that has been appended
      to uploaded.txt as well as its unique identifier.

      example command: curl -H "Content-Type: application/json" -d '{"file name": "hw.pdf"}' http://127.0.0.1:5000
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

        example command (returns the zip file with fileID=1): curl http://127.0.0.1:5000/get/1
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

class Listing(Resource):
  def get(self):
    """ Second GET API Call that returns the full listing of uploaded files

        example command: curl http://127.0.0.1:5000/files
    """
    lst = []
    with open("uploaded.txt", "r") as f:
      for line in f:
        lst.append(line.strip())
    if len(lst) == 0:
      return "No files have been uploaded."
    return lst

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

def updateList(filename):
  """ Adds appropriate filename to uploaded.txt after collisions have been handled, etc.
  """
  date_uploaded = today.strftime("%b-%d-%Y")
  file1 = open("uploaded.txt", "a")
  file1.write(filename + ',' + str(file_size(filename)) + ',' + str(date_uploaded) + '\n')
  file1.close()

def file_size(filename):
  """ Computes the file size of the input file and using the byteConvert function to convert
      the size to appropriate units.
  """
  if os.path.isfile(filename):
      file_info = os.stat(filename)
      return byteConvert(file_info.st_size)

def byteConvert(num):
  """ Converts the given number of bytes into proper units depending on how many bytes there are.
  """
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
api.add_resource(Listing, '/files')

""" TESTING
"""
# test checking to see if zipped file has been compressed (does not hold true for very small files)
# because ZipFile wrapper is bigger than the original file itself
assert file_size('zipped/hw.zip') < file_size("hw.pdf") # comment out before starting demo
assert file_size('zipped/temp.zip') < file_size('temp.txt') # comment out before starting demo
# in the following test, the hello.zip file (131.0 bytes) is bigger than the hello.txt file (13.0 bytes); this means that the ZipFile wrapper is 118 bytes and therefore does not reduce the size of files smaller than 118 bytes
assert file_size('zipped/hello.zip') > file_size('hello.txt') # comment out before starting demo
#print(file_size("zipped/lecture.zip"))

# test checking to see if the zip function returns the proper output for filename hw.pdf and fileID 1
assert (zip('hello.txt', 1) == "The file hello.txt with fileID 1 and file size 13.0 bytes has been zipped!" + '\n') # # comment out before starting demo
assert (zip('hw.pdf', 2) == "The file hw.pdf with fileID 2 and file size 297.4 KB has been zipped!" + '\n') # comment out before starting demo
assert (zip('temp.txt', 53) == "The file temp.txt with fileID 53 and file size 706.0 bytes has been zipped!" + '\n') # comment out before starting demo

# test checking to see if ind function returns the correct index (where the file extension begins)
assert (ind('testing.jpeg') == 7)
assert (ind('test.py') == 4)
assert (ind('test.pdf') == 4)
assert (ind('shree.phadke.png') == 12)

# hw.pdf would be renamed to hw_2.pdf in the uploaded.txt entry because there already exists a hw_1.pdf
#assert (duplicateName("hw.pdf") == "hw_2.pdf")

assert (generateID("hello.txt") == 1) # comment out before starting demo
assert (generateID("hw.pdf") == 2) # comment out before starting demo
assert (generateID("temp.txt") == 3) # comment out before starting demo

if __name__ == '__main__':
    app.run(debug=True)
