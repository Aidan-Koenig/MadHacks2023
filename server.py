from flask import Flask, jsonify, request
from flask_cors import CORS

import backend

app = Flask(__name__)
CORS(app)
logins = {}
@app.route('/signup/<username>/<password>/<email>/<isGrad>', methods=['GET'])
def signup(username, password, email, isGrad):
    return backend.signup(username, password, email, isGrad)

@app.route('/login/<username>/<password>', methods=['GET'])
def login(username, password):
    if backend.login(username, password) == "Success":
        logins[request.remote_addr] = username
        print(f"{request.remote_addr} logged in as {username}")
        return "Success"
    else:
        return "Failed login"

@app.route('/logout', methods=['GET'])
def logout():
    del logins[request.remote_addr]
@app.route('/addFriend/<friendname>', methods=['GET'])
def addFriend(friendname):
    if request.remote_addr not in logins:
        return "Not logged in"
    return backend.addFriend(logins[request.remote_addr], friendname)

@app.route('/findFriendClasses', methods=['GET'])
def findFriendClasses():
    if request.remote_addr not in logins:
        return "Not logged in"
    return str(backend.findFriendClasses(logins[request.remote_addr]))

@app.route('/getFriends', methods=['GET'])
def getFriends():
    if request.remote_addr not in logins:
        return "Not logged in"
    return backend.getFriends(logins[request.remote_addr])

@app.route('/getHighlights', methods=['GET'])
def getHighlights():
    if request.remote_addr not in logins:
        return "Not logged in"
    return backend.getHighlights(logins[request.remote_addr])

@app.route('/create_dars', methods=['POST'])
def create_dars():
    if request.remote_addr not in logins:
        return "Not logged in"
    data = request.get_json()
    
    username = logins[request.remote_addr]
    taken = data.get('taken')
    required = data.get('required')

    result = backend.createDARS(username, taken, required)

    return result

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

