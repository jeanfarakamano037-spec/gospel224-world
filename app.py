from flask import Flask, jsonify, request, send_from_directory
import json, os, uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

SONGS_FILE = "songs.json"

def load_songs():
    if not os.path.exists(SONGS_FILE):
        return [{
            "id":"1","title":"AIMEZ PRECHER JESUS","artist":"Jean Farakamano","type":"SINGLE","cover":"https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=300","file":"","plays":1240
        }]
    try:
        with open(SONGS_FILE,"r",encoding="utf-8") as f: return json.load(f)
    except: return []

def save_songs(s): 
    with open(SONGS_FILE,"w",encoding="utf-8") as f: json.dump(s,f,ensure_ascii=False,indent=2)

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>GOSPEL224 WORLD - Spotify Guinée</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}body{background:#000;color:#fff;font-family:Arial;padding-bottom:90px}
.header{background:linear-gradient(#f9c00f,#000);padding:25px;text-align:center}
.nav{display:flex;gap:10px;overflow-x:auto;padding:15px;background:#121212;position:sticky;top:0;z-index:10}
.nav button{background:#2a2a2a;color:#fff;border:none;padding:8px 18px;border-radius:20px;white-space:nowrap}
.nav button.active{background:#f9c00f;color:#000;font-weight:bold}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:15px;padding:15px}
.card{background:#181818;padding:12px;border-radius:10px;transition:0.2s;cursor:pointer}
.card:hover{background:#282828}
.card img{width:100%;height:150px;object-fit:cover;border-radius:8px}
.card h4{margin:8px 0 3px;color:#fff;font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.card p{color:#aaa;font-size:12px}
.actions{display:flex;gap:8px;margin-top:8px;flex-wrap:wrap}
.btn-mini{font-size:11px;padding:5px 10px;border-radius:15px;border:none;cursor:pointer}
.btn-play{background:#1DB954;color:#000;font-weight:bold}
.btn-down{background:#333;color:#fff}
.btn-share{background:#f9c00f;color:#000}
.player{position:fixed;bottom:0;left:0;right:0;background:#181818;border-top:1px solid #333;padding:10px 15px;display:flex;align-items:center;gap:15px}
.player img{width:50px;height:50px;border-radius:5px}
.progress{flex:1}
.ad{background:linear-gradient(90deg,#ff8c00,#f9c00f);color:#000;padding:10px;text-align:center;margin:15px;border-radius:8px;font-weight:bold}
.uploadBox{background:#121212;margin:15px;padding:20px;border-radius:15px;border:1px dashed #f9c00f}
input,select{width:100%;padding:10px;margin:5px 0;border-radius:8px;border:none;background:#2a2a2a;color:#fff}
</style></head><body>
<div class="header"><h1>🎤 GOSPEL224 WORLD</h1><p>LE SPOTIFY GOSPEL DE GUINÉE 🇬🇳</p></div>

<div class="nav">
<button class="active" onclick="filterType('ALL',this)">TOUT</button>
<button onclick="filterType('SINGLE',this)">SINGLE</button>
<button onclick="filterType('EP',this)">EP</button>
<button onclick="filterType('COVER',this)">COVER</button>
<button onclick="filterType('MIXTAPE',this)">MIXTAPE</button>
<button onclick="filterType('ALBUM',this)">ALBUM</button>
</div>

<div class="ad">📢 PUB: Promouvez votre chant ici! Contact Gospel224 WhatsApp - 50 000 GNF / semaine!</div>

<div class="grid" id="grid">Chargement...</div>

<div class="uploadBox">
<h3 style="color:#f9c00f">⬆️ UPLOADER (Chantres)</h3>
<input id="title" placeholder="Titre">
<input id="artist" placeholder="Artiste">
<select id="type"><option>SINGLE</option><option>EP</option><option>COVER</option><option>MIXTAPE</option><option>ALBUM</option></select>
<input id="file" type="file" accept="audio/*"><input id="cover" placeholder="Lien image cover (optionnel)">
<button onclick="upload()" style="width:100%;background:#f9c00f;padding:12px;border-radius:25px;font-weight:bold;margin-top:10px;border:none">PUBLIER MAINTENANT</button>
<p id="status"></p>
</div>

<div class="player" id="player" style="display:none">
<img id="pCover" src=""><div><b id="pTitle"></b><br><small id="pArtist"></small></div>
<div class="progress"><audio id="audio" controls style="width:100%"></audio><div style="display:flex;gap:5px;margin-top:5px">
<button class="btn-mini btn-share" onclick="share()">PARTAGER ↗️</button>
<button class="btn-mini btn-down" onclick="download()">TÉLÉCHARGER ⬇️</button>
<button class="btn-mini btn-down" onclick="shareTo('facebook')">Facebook</button>
<button class="btn-mini btn-down" onclick="shareTo('whatsapp')">WhatsApp</button>
</div></div></div>

<script>
let allSongs=[]; let currentFile='';
async function load(){
 let r=await fetch('/api/songs'); allSongs=await r.json(); render(allSongs);
}
function render(list){
 let h=''; list.forEach(s=>{
  h+=`<div class="card" onclick="playSong('${s.id}')">
  <img src="${s.cover||'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=300'}">
  <h4>${s.title}</h4><p>${s.artist} • ${s.type}</p>
  <div class="actions"><span style="font-size:11px;color:#aaa">▶️ ${s.plays||0}</span><span style="font-size:11px;background:#f9c00f;color:#000;padding:2px 6px;border-radius:10px">${s.type}</span></div>
  </div>`;
 }); document.getElementById('grid').innerHTML=h||'<p style="padding:20px">Aucun chant dans cette catégorie</p>';
}
function filterType(t,btn){
 document.querySelectorAll('.nav button').forEach(b=>b.classList.remove('active')); btn.classList.add('active');
 if(t=='ALL') render(allSongs); else render(allSongs.filter(s=>s.type==t));
}
function playSong(id){
 let s=allSongs.find(x=>x.id==id); if(!s) return;
 document.getElementById('player').style.display='flex';
 document.getElementById('pCover').src=s.cover||'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=300';
 document.getElementById('pTitle').innerText=s.title; document.getElementById('pArtist').innerText=s.artist;
 currentFile=s.file; if(s.file){ document.getElementById('audio').src='/uploads/'+s.file; document.getElementById('audio').play(); }
}
function share(){ if(navigator.share){navigator.share({title:document.getElementById('pTitle').innerText,text:'Écoute sur Gospel224 WORLD',url:location.href})} else {alert('Lien copié: '+location.href); navigator.clipboard.writeText(location.href)} }
function download(){ if(!currentFile) return alert('Pas de fichier à télécharger'); window.location='/uploads/'+currentFile; }
function shareTo(p){ let url=encodeURIComponent(location.href); let text=encodeURIComponent('Écoute '+document.getElementById('pTitle').innerText+' sur Gospel224 WORLD 🔥'); if(p=='whatsapp') window.open('https://wa.me/?text='+text+'%20'+url); if(p=='facebook') window.open('https://www.facebook.com/sharer/sharer.php?u='+url); }
async function upload(){
 let title=document.getElementById('title').value; let artist=document.getElementById('artist').value; let type=document.getElementById('type').value;
 if(!title||!artist) return alert('Titre et artiste requis'); document.getElementById('status').innerText='Envoi...';
 let fd=new FormData(); fd.append('title',title); fd.append('artist',artist); fd.append('type',type);
 fd.append('cover',document.getElementById('cover').value); let f=document.getElementById('file').files[0]; if(f) fd.append('file',f);
 let r=await fetch('/upload',{method:'POST',body:fd}); let j=await r.json(); document.getElementById('status').innerText=j.message; if(j.success) load();
}
load();
</script></body></html>
    """

@app.route("/api/songs")
def api(): return jsonify(load_songs())

@app.route("/uploads/<path:filename>")
def up(filename): return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/upload", methods=["POST"])
def upload():
    title=request.form.get("title","").strip(); artist=request.form.get("artist","").strip()
    type_ = request.form.get("type","SINGLE"); cover=request.form.get("cover","").strip()
    if not title or not artist: return jsonify({"success":False,"message":"Titre et artiste requis"})
    filename=""; 
    if "file" in request.files:
        file=request.files["file"]
        if file and file.filename:
            ext=os.path.splitext(secure_filename(file.filename))[1]
            filename=f"{uuid.uuid4().hex}{ext}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    songs=load_songs()
    songs.insert(0,{"id":uuid.uuid4().hex[:8],"title":title,"artist":artist,"type":type_,"cover":cover,"file":filename,"plays":0})
    save_songs(songs)
    return jsonify({"success":True,"message":f"✅ {type_} '{title}' publié!"})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",5000)))
