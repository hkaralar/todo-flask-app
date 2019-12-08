import os
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = "çok gizli key"

# Veri tabanı bağlantısı
uri = os.getenv("MONGO_ATLAS_URI")
client = MongoClient(uri)
db = client.tododb.todos
# tododb: veri tabanı ismi, todos: collection name

@app.route('/')
def index():
    # veri tabanından kayıtları al ve listeye doldur
    yapilacaklar = []
    for yap in db.find():
         yapilacaklar.append({'_id': str(yap['_id']), 'isim': yap['isim'], 'durum': yap['durum']})
    
    # index.html dosyasına listeyi gönder  
    return render_template('index.html', yapilacaklar = yapilacaklar)

@app.route('/ekle', methods=['GET', 'POST'])
def ekle():
    if request.method == 'GET':
        return redirect('/')
    try:
        if request.method == 'POST':
            # index.html formundan isim gelecek
            isim = request.form.get('isim')
            db.insert_one({'isim': isim, 'durum':'False'})
            return redirect('/')
    except expression as identifier:
        return redirect('/')
  
@app.route('/guncelle/<id>')
def guncelle(id):
   try:
       yap = db.find_one({'_id':ObjectId(id)})
       durum = not yap['durum']
       db.find_one_and_update({'_id':ObjectId(id)},{'$set':{'durum': durum}})
       # ana sayfaya dönelim
       return redirect('/')
   except :
       return redirect('/') 

@app.route('/sil/<id>')
def sil(id):
    try:
        db.find_one_and_delete({'_id':ObjectId(id)})
        return redirect('/')
    except expression as identifier:
        return redirect('/') 

# Hatalı ya da olmayan url istekleri gelirse
# hata vermesin, ana sayfaya gitsin
@app.errorhandler(404) 
def not_found(e): 
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
