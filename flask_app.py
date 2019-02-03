from flask import Flask, url_for, render_template, request
from sqlalchemy import Column, Integer, DateTime
import os
import requests
import json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import ssl
from flask_sqlalchemy import SQLAlchemy
import datetime

app = Flask(__name__)
project_dir = os.path.dirname(os.path.abspath(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///{}".format(os.path.join(project_dir, "hashdatabase.db"))
db_user = SQLAlchemy(app)

class Hash(db_user.Model):
    file_hash = db_user.Column(db_user.String(80), unique=True, nullable=False, primary_key=True)
    timestamp = db_user.Column(DateTime, default=datetime.datetime.utcnow)
    def __init__(self, file_hash, timestamp):
        self.file_hash = file_hash
        self.timestamp = timestamp        
    def __repr__(self):
        return '<file_hash %r>' % self.file_hash

@app.route("/")
def hello():
    return render_template('base.html',url_for = url_for)

@app.route("/start_daemon")
def start_daemon():
    os.system("ipfs daemon")
    return "Starting daemon"

@app.route("/is_daemon_running")
def is_daemon_running():
    try:
        request = requests.get('http://127.0.0.1:5001/webui')
        if request.status_code == 200:
            return "IPFS Daemon is running"
        else:
            return "IPFS Daemon is not running"
    except requests.ConnectionError:
        return "IPFS Daemon is not running"
@app.route("/pin_from_database")
def pins_from_database():
    context = ssl._create_unverified_context()
    while True:
        post_fields = {'connect_key':98702002992116,'query':'get_users'}
        request = Request('https://endereum.io/internal-queries/', urlencode(post_fields).encode())
        jsony = urlopen(request,context=context).read().decode()
        jsony = json.loads(jsony)
        print("user details obtained from PHP server")
        data = None
        for record in jsony:
            if record['user_id'] == 'MjY':
                data = record
        data = data['user_hash']
        str1 = ""
        hash_file = open("hashes", "r")
        hashes = hash_file.read().split()
        hash_file.close()
        print("Before pinning")
        for hash in data:
            if hash not in hashes :
                print(hash)
                status = os.system("ipfs pin add " + hash)
                if status == 0:
                    file_hash = Hash(hash, datetime.datetime.now())
                    db_user.session.add(file_hash)
                    db_user.session.commit()
                    hashes.append(hash)
                if status != 0:
                    str1 = str1 + hash + " " + "Not pinned yet \n"
        hash_file = open("hashes","w")
        for hash in hashes:
            hash_file.write(hash)
            hash_file.write(" ")
        hash_file.close()
    return "Please continue running the application for continuous pinning"

@app.route('/pin', methods=["GET", "POST"])
def Pin():
    if request.method == 'POST':
        hash = request.form['Hash']
        if hash is not None:
            os.system("ipfs pin add " + hash)
            file_hash = Hash(hash, datetime.datetime.now())
            db_user.session.add(file_hash)
            db_user.session.commit()
            return "pinned"
        else:
            return "no hash"
    return "Not a post request"

@app.route('/local_files')
def view_local_files():
    os.system("ipfs pin ls | findstr recursive > hash")
    local_files = open("hash", "r").read()
    return local_files

@app.route('/files_pinned_dyanamically')
def view_dyanamic_files():
    str1 = ""
    hash_read = open("hashes", "r").read().split()
    for hash in hash_read:
        str1 = str1 + hash + "\n"
    if str1 == "":
        return "Files not yet pinned"
    else:
        return "displaying files that are pinned to local node from website\n" + str1

@app.route('/view_token_of_pinned_files')
def view_tokens():
    output = ""
    max = 0
    for hash in Hash.query.all():
        f_hash = hash.file_hash
        time = hash.timestamp
        token = datetime.datetime.now() - time
        token1 = (token.total_seconds() / 60) * 5
        if max < token1:
            max = token1
        output = output + f_hash + " \n"
    return output + " " + str(round(max,0)) + " ENDRS so far"

if __name__ == "__main__":
    app.run()
