from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime

connection_string ='mongodb+srv://AnnidaAuliyaZahwa:Annida276@cluster0.pniqosj.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(connection_string)
db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({},{'_id':False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form.get('title_give')
    content_receive = request.form.get('content_give')

    today = datetime.now()
    time = today.strftime('%Y-%m-%d-%H-%M-%S')

    file = request.files['file_give']
    extension = file.filename.split('.')[-1]
    filename = f'static/post-{time}.{extension}'
    file.save(filename)

    profile = request.files['profile_give']
    extension = profile.filename.split('.')[-1]
    profilename = f'static/profile-{time}.{extension}'
    profile.save(profilename)
    
    doc = {
        'file' : filename,
        'profile' : profilename,
        'title': title_receive,
        'content': content_receive,
        'time': today.strftime('%Y-%m-%d')
    }
    db.diary.insert_one(doc)
    return jsonify({'message': 'data was saved!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)