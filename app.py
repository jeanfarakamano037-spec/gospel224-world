from flask import Flask, request, redirect
import os, json, time
from werkzeug.utils import secure_filename
app = Flask(__name__)
DB="songs.json"
def load_songs():
    try:
        return json.load(open(DB,encoding='utf-8'))
    except:
        return [{"title":"AIMEZ PRECHER JESUS MASTER FINAL","artist":"Mission Part I","file":"AIMEZ PRECHER JESUS MASTER FINAL.mp3","likes":128,"time":time.time()}]
def save_songs(s):
    json.dump(s, open(DB,"w",encoding='utf-8'), ensure_ascii=False, indent=2)

@app.route("/")
def home():
    songs=load_songs()
    files=[x for x in os.listdir("static") if x.lower().endswith(".mp3")]
    for f in files:
        if not any(s["file"]==f for s in songs):
            songs.append({"title":f.replace(".mp3","").replace("_"," "),"artist":"Chantre GN","file":f,"likes":0,"time":time.time()})
    if files:
        save_songs(songs)
    songs_sorted=sorted(songs, key=lambda x: x.get("time",0), reverse=True)
    cards=""
    for i,s in enumerate(songs_sorted):
        t=s["title"].replace("'","")
        a=s["artist"].replace("'","")
        f=s["file"]
        cards+=f"<div style='background:#111;border-radius:20px;padding:15px;border:1px solid #222'><img src='https://picsum.photos/seed/{i}/400/400' style='width:100%;height:200px;object-fit:cover;border-radius:15px'><h3 style='font-weight:bold;margin-top:10px'>{t}</h3><p style='font-size:12px;opacity:0.5'>{a}</p><button onclick=\"playSong('{t}','{a}','/static/{f}')\" style='margin-top:10px;background:#FFD700;color:black;padding:8px 15px;border-radius:20px;font-weight:bold;width:100%'>PLAY ▶</button></div>"
    html = """
<!DOCTYPE html>
<html><head><meta charset='UTF-8'><meta name='viewport' content='width=device-width,initial-scale=1'>
<title>GOSPEL224 WORLD</title>
<script src='https://cdn.tailwindcss.com'></script>
<link rel='stylesheet' href='https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css'>
</head><body style='background:#050505;color:white;font-family:sans-serif'>
<header style='position:fixed;top:0;width:100%;background:rgba(0,0,0,0.9);border-bottom:1px solid rgba(255,215,0,0.2);padding:15px;z-index:50;display:flex;justify-content:space-between;align-items:center'>
<div><b>GOSPEL224<span style='color:gold'>.WORLD</span></b> 🇬🇳</div>
<button onclick="document.getElementById('modal').classList.remove('hidden')" style='background:gold;color:black;padding:8px 20px;border-radius:20px;font-weight:bold'>+ UPLOADER</button>
</header>
<section style='padding-top:100px;padding-left:20px;padding-right:20px;max-width:1200px;margin:0 auto'>
<h1 style='font-size:60px;font-weight:900;line-height:0.9'>AIMEZ.<br><span style='background:linear-gradient(135deg,#FFD700,#FF8C00);-webkit-background-clip:text;-webkit-text-fill-color:transparent'>PRECHEZ</span><br>JESUS.</h1>
<p style='opacity:0.5;margin-top:20px'>Plateforme la plus stylée de Guinée - Design Spotify, âme guinéenne</p>
</section>
<section style='padding:20px;max-width:1200px;margin:20px auto;display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:20px;padding-bottom:120px'>
CARDS_PLACEHOLDER
</section>
<div style='position:fixed;bottom:0;width:100%;background:rgba(0,0,0,0.95);border-top:1px solid rgba(255,215,0,0.2);padding:15px;display:flex;align-items:center;gap:15px;z-index:40'>
<div style='flex:1'><h4 id='ptitle' style='font-weight:bold'>Choisis un chant</h4><p id='partist' style='font-size:12px;opacity:0.5'>GOSPEL224 WORLD</p><div style='width:100%;background:rgba(255,255,255,0.1);height:4px;border-radius:10px;margin-top:5px'><div id='prog' style='height:4px;background:gold;width:0%'></div></div></div>
<button id='playBtn' style='width:50px;height:50px;background:white;color:black;border-radius:50%'><i class='fa-solid fa-play'></i></button>
<audio id='audio'></audio>
</div>
<div id='modal' style='display:none;position:fixed;inset:0;background:rgba(0,0,0,0.9);z-index:100;align-items:center;justify-content:center;padding:20px' class='hidden flex'>
<div style='background:#111;border:1px solid rgba(255,215,0,0.3);border-radius:25px;padding:30px;max-width:400px;width:100%'>
<h3 style='font-size:24px;font-weight:900;margin-bottom:20px'>Publier ton chant</h3>
<form method='post' action='/upload' enctype='multipart/form-data' style='display:flex;flex-direction:column;gap:15px'>
<input name='chantre' placeholder='Nom chantre' required style='background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:10px;padding:12px'>
<input name='titre' placeholder='Titre chant' required style='background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:10px;padding:12px'>
<input type='file' name='file' accept='.mp3' required>
<button style='background:gold;color:black;font-weight:900;padding:15px;border-radius:10px'>PUBLIER 🔥</button>
</form>
<button onclick="document.getElementById('modal').classList.add('hidden');document.getElementById('modal').style.display='none'" style='margin-top:15px;opacity:0.5;width:100%'>Fermer</button>
</div></div>
<script>
const audio=document.getElementById('audio');const playBtn=document.getElementById('playBtn');
function playSong(t,a,s){document.getElementById('ptitle').innerText=t;document.getElementById('partist').innerText=a;audio.src=s;audio.play();playBtn.innerHTML='<i class="fa-solid fa-pause"></i>';document.getElementById('modal').style.display='none';}
playBtn.onclick=()=>{if(audio.paused){audio.play();playBtn.innerHTML='<i class="fa-solid fa-pause"></i>';}else{audio.pause();playBtn.innerHTML='<i class="fa-solid fa-play"></i>';}};
audio.ontimeupdate=()=>{if(audio.duration){document.getElementById('prog').style.width=audio.currentTime/audio.duration*100+'%';}};
</script>
</body></html>
"""
    return html.replace("CARDS_PLACEHOLDER", cards)

@app.route("/upload",methods=["POST"])
def upload():
    f=request.files.get("file")
    chantre=request.form.get("chantre","Anonyme")
    titre=request.form.get("titre","Sans titre")
    if f and f.filename:
        safe=secure_filename(f"{chantre}_{titre}.mp3".replace(" ","_"))
        f.save(os.path.join("static",safe))
        songs=load_songs()
        songs.append({"title":titre,"artist":chantre,"file":safe,"likes":0,"time":time.time()})
        save_songs(songs)
    return redirect("/")

if __name__=="__main__":
    os.makedirs("static",exist_ok=True)
    app.run(host="0.0.0.0",port=5000,debug=True)
