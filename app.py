from flask import Flask, jsonify, request, send_from_directory
import json, os, uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('static', exist_ok=True)

SONGS_FILE = "songs.json"

def load_songs():
    if not os.path.exists(SONGS_FILE):
        # Chanson de depart
        return [{
            "id": "1",
            "title": "AIMEZ PRECHER JESUS",
            "artist": "Jean Farakamano - Gospel224",
            "file": "",
            "youtube": "https://youtu.be/"
        }]
    try:
        with open(SONGS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def save_songs(songs):
    with open(SONGS_FILE, "w", encoding="utf-8") as f:
        json.dump(songs, f, ensure_ascii=False, indent=2)

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>GOSPEL224 WORLD - Plateforme des Chantres de Guinée</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',Arial;background:#0f0f0f;color:#fff}
.header{background:linear-gradient(135deg,#f9c00f,#ff8c00);padding:20px;text-align:center;color:#000}
.header h1{font-size:28px;letter-spacing:2px}
.header p{margin-top:5px;font-weight:bold}
.container{max-width:900px;margin:20px auto;padding:0 15px}
.card{background:#1e1e1e;border-radius:15px;padding:20px;margin-bottom:20px;border:1px solid #333}
.card h2{color:#f9c00f;margin-bottom:15px}
.song-item{background:#2a2a2a;padding:15px;border-radius:10px;margin:10px 0;display:flex;justify-content:space-between;align-items:center}
.song-item strong{color:#f9c00f}
.btn{background:#f9c00f;color:#000;border:none;padding:10px 20px;border-radius:25px;font-weight:bold;cursor:pointer}
.btn:hover{background:#fff}
input, textarea{width:100%;padding:12px;margin:8px 0;border-radius:8px;border:none;background:#2a2a2a;color:#fff}
audio{width:100%;margin-top:10px}
.upload-area{border:2px dashed #f9c00f;padding:20px;border-radius:10px;text-align:center}
.live-badge{background:#00ff00;color:#000;padding:5px 10px;border-radius:20px;font-size:12px;font-weight:bold}
</style>
</head>
<body>
<div class="header">
<h1>🎤 GOSPEL224 WORLD</h1>
<p>La Plateforme Officielle des Chantres de Guinée - Conakry</p>
<span class="live-badge">● LIVE MONDIAL</span>
</div>

<div class="container">
<div class="card">
<h2>🎵 À LA UNE</h2>
<div class="song-item">
<div><strong>AIMEZ PRECHER JESUS</strong><br><small>Jean Farakamano</small></div>
<audio controls><source src=""></audio>
</div>
<p style="margin-top:10px">Partage l'Evangile en musique! 🙏</p>
</div>

<div class="card">
<h2>📀 Tous les Chants</h2>
<div id="songsList">Chargement...</div>
</div>

<div class="card">
<h2>⬆️ Uploader un Chant (Pour Chantres)</h2>
<div class="upload-area">
<input type="text" id="title" placeholder="Titre du chant ex: Gloire à Dieu">
<input type="text" id="artist" placeholder="Nom de l'artiste ex: Soeur Marie">
<input type="file" id="audioFile" accept="audio/*">
<button class="btn" onclick="uploadSong()">Publier le Chant</button>
<p id="uploadStatus" style="margin-top:10px"></p>
</div>
</div>

<div class="card" style="text-align:center">
<p>🔗 Lien officiel: <b>gospel224-world-1.onrender.com</b></p>
<p>📱 Contact WhatsApp: Gospel224</p>
<p style="margin-top:10px;color:#f9c00f">JESUS REVIENT BIENTOT!</p>
</div>
</div>

<script>
async function loadSongs(){
  let res = await fetch('/api/songs');
  let songs = await res.json();
  let html = '';
  songs.forEach(s=>{
    html+=`<div class="song-item"><div><strong>${s.title}</strong><br><small>${s.artist}</small></div>
    ${s.file?`<audio controls src="/uploads/${s.file}"></audio>`:''}
    </div>`;
  });
  if(songs.length==0) html='<p>Aucun chant encore. Sois le premier!</p>';
  document.getElementById('songsList').innerHTML=html;
}

async function uploadSong(){
  let title=document.getElementById('title').value;
  let artist=document.getElementById('artist').value;
  let file=document.getElementById('audioFile').files[0];
  if(!title||!artist){alert('Titre et Artiste obligatoires');return;}
  document.getElementById('uploadStatus').innerText='Envoi en cours...';
  let form=new FormData();
  form.append('title',title); form.append('artist',artist);
  if(file) form.append('file',file);
  let res=await fetch('/upload',{method:'POST',body:form});
  let data=await res.json();
  document.getElementById('uploadStatus').innerText=data.message;
  if(data.success){loadSongs(); document.getElementById('title').value=''; document.getElementById('artist').value='';}
}
loadSongs();
</script>
</body>
</html>
    """

@app.route("/api/songs")
def api_songs():
    return jsonify(load_songs())

@app.route("/uploads/<filename>")
def serve_upload(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/upload", methods=["POST"])
def upload():
    title = request.form.get("title", "").strip()
    artist = request.form.get("artist", "").strip()
    if not title or not artist:
        return jsonify({"success": False, "message": "Titre et artiste requis"})
    
    filename = ""
    if "file" in request.files:
        file = request.files["file"]
        if file and file.filename:
            ext = os.path.splitext(secure_filename(file.filename))[1]
            filename = f"{uuid.uuid4().hex}{ext}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    songs = load_songs()
    new_song = {
        "id": uuid.uuid4().hex[:8],
        "title": title,
        "artist": artist,
        "file": filename
    }
    songs.insert(0, new_song)
    save_songs(songs)
    return jsonify({"success": True, "message": f"✅ Chant '{title}' publié avec succès!"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
