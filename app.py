from flask import Flask, jsonify, request, send_from_directory
import json, os, uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
SONGS_FILE = "songs.json"
PRAY_FILE = "prayers.json"
AMEN_FILE = "amens.json"

def load_json(f, default):
    if not os.path.exists(f): return default
    try:
        with open(f,"r",encoding="utf-8") as x: return json.load(x)
    except: return default
def save_json(f, data):
    with open(f,"w",encoding="utf-8") as x: json.dump(data,x,ensure_ascii=False,indent=2)

def load_songs(): return load_json(SONGS_FILE, [{"id":"1","title":"AIMEZ PRECHER JESUS","artist":"Jean Farakamano","type":"SINGLE","cover_file":"","cover_url":"https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=500","file":"","plays":1240,"prayers":0}])
def get_cover(s):
    if s.get("cover_file"): return f"/uploads/{s['cover_file']}"
    return s.get("cover_url") or s.get("cover") or "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=500"

@app.route("/")
def home():
    return """
<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>GOSPEL224 WORLD - ROYAUME 4D</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}body{background:#000;color:#fff;font-family:Arial;padding-bottom:95px;overflow-x:hidden}
.header{background:linear-gradient(180deg,#f9c00f 0%, #ff8c00 40%, #000 100%);padding:22px 15px;text-align:center}
.topbar{display:flex;gap:10px;padding:12px;background:#121212;position:sticky;top:0;z-index:20}
.topbar input{flex:1;padding:10px 15px;border-radius:25px;background:#2a2a2a;border:none;color:#fff}
.nav{display:flex;gap:8px;overflow-x:auto;padding:0 15px 12px;background:#121212;position:sticky;top:54px;z-index:10}
.nav button{background:#2a2a2a;color:#fff;border:none;padding:7px 16px;border-radius:20px;white-space:nowrap;font-size:13px}
.nav button.active{background:#f9c00f;color:#000;font-weight:bold}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px;padding:15px}
.card{background:#181818;padding:10px;border-radius:12px;cursor:pointer;position:relative;overflow:hidden}
.card:hover{background:#282828} .card img{width:100%;height:150px;object-fit:cover;border-radius:8px}
.card h4{margin:8px 0 2px;font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.badge{font-size:10px;background:#f9c00f;color:#000;padding:2px 6px;border-radius:10px;font-weight:bold}
.ad{background:linear-gradient(90deg,#ff8c00,#f9c00f);color:#000;padding:10px;text-align:center;margin:12px 15px;border-radius:10px;font-weight:bold;font-size:13px}
.uploadBox{background:#121212;margin:15px;padding:18px;border-radius:15px;border:2px dashed #f9c00f}
input,select{width:100%;padding:10px;margin:6px 0;border-radius:8px;border:none;background:#2a2a2a;color:#fff}
.file-label{display:block;background:#2a2a2a;padding:10px;border-radius:8px;margin:6px 0;text-align:center;border:1px dashed #555;cursor:pointer}
.player{position:fixed;bottom:0;left:0;right:0;background:#181818;border-top:1px solid #333;padding:10px 15px;display:flex;align-items:center;gap:12px;z-index:50}
.player img{width:52px;height:52px;border-radius:6px}
/* ROYAUME IMMERSIVE */
#royaumeMode{position:fixed;top:0;left:0;right:0;bottom:0;background:#000;z-index:200;display:none;overflow:hidden}
.royaume-bg{position:absolute;top:0;left:0;right:0;bottom:0;background-size:cover;background-position:center;filter:brightness(0.5);animation:zoomSlow 20s infinite alternate}
@keyframes zoomSlow{from{transform:scale(1)}to{transform:scale(1.15)}}
.particles{position:absolute;top:0;left:0;right:0;bottom:0;pointer-events:none}
.particle{position:absolute;width:4px;height:4px;background:#f9c00f;border-radius:50%;animation:floatUp linear infinite;opacity:0.8}
@keyframes floatUp{from{transform:translateY(100vh) scale(0)}to{transform:translateY(-10vh) scale(1.5)}}
.cross-glow{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-size:200px;color:#f9c00f;opacity:0.15;animation:pulse 2s infinite}
@keyframes pulse{0%,100%{transform:translate(-50%,-50%) scale(1);opacity:0.15}50%{transform:translate(-50%,-50%) scale(1.2);opacity:0.3}}
.royaume-content{position:relative;z-index:2;padding:20px;text-align:center;height:100%;display:flex;flex-direction:column;justify-content:center}
.verse-pop{font-size:28px;font-weight:bold;color:#f9c00f;text-shadow:0 0 20px #f9c00f, 0 0 40px #ff8c00;animation:verseHit 0.8s; margin:15px 0}
@keyframes verseHit{0%{transform:scale(0) rotate(-10deg)}60%{transform:scale(1.3) rotate(5deg)}100%{transform:scale(1) rotate(0)}}
/* MAP GUINEE */
.map-guinee{display:grid;grid-template-columns:repeat(3,1fr);gap:8px;margin:15px 0}
.city{padding:10px;background:#1e1e1e;border-radius:8px;text-align:center;font-size:12px;border:1px solid #333;transition:0.5s}
.city.on{background:linear-gradient(#ff8c00,#f9c00f);color:#000;font-weight:bold;box-shadow:0 0 15px #f9c00f;transform:scale(1.05)}
/* ARMOR */
.armor-bar{display:flex;gap:6px;overflow-x:auto;padding:10px 0}
.armor-piece{min-width:70px;padding:8px;background:#1e1e1e;border-radius:10px;text-align:center;font-size:10px;border:1px solid #333}
.armor-piece.unlocked{background:#f9c00f;color:#000;font-weight:bold;box-shadow:0 0 10px #f9c00f}
/* AMEN WALL */
.amen-wall{max-height:120px;overflow-y:auto;background:#0f0f0f;border-radius:10px;padding:10px;margin:10px 0}
.amen-bubble{background:#2a2a2a;padding:6px 10px;border-radius:15px;margin:5px;display:inline-block;font-size:12px;animation:amenRise 0.5s}
@keyframes amenRise{from{transform:translateY(20px);opacity:0}to{transform:translateY(0);opacity:1}}
.modal{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.92);z-index:100;display:none;overflow-y:auto;padding:20px}
.modal-content{background:#121212;border-radius:15px;padding:20px;max-width:600px;margin:20px auto}
</style></head><body>
<div class="header"><h1>🎤 GOSPEL224 WORLD</h1><p>⚔️ ROYAUME 4D - JAMAIS VU AU MONDE 🇬🇳</p></div>
<div class="topbar"><input id="search" placeholder="🔍 Rechercher..." oninput="doSearch()"><span id="count" style="font-size:12px;color:#aaa"></span></div>
<div class="nav">
<button class="active" onclick="filterType('ALL',this)">TOUT</button>
<button onclick="filterType('SINGLE',this)">SINGLE</button>
<button onclick="filterType('EP',this)">EP</button>
<button onclick="filterType('COVER',this)">COVER</button>
<button onclick="filterType('MIXTAPE',this)">MIXTAPE</button>
<button onclick="filterType('ALBUM',this)">ALBUM</button>
</div>

<!-- ARMURE DE DIEU BAR -->
<div style="padding:0 15px;background:#121212"><p style="font-size:11px;color:#f9c00f;font-weight:bold">⚔️ ARMURE DE DIEU - EPHESIENS 6</p><div class="armor-bar" id="armorBar"></div></div>

<!-- CARTE GUINEE EN FEU -->
<div style="margin:12px 15px;background:#121212;padding:12px;border-radius:12px"><p style="font-size:12px;font-weight:bold;color:#f9c00f">🗺️ GUINÉE EN FEU - ÉCOUTES EN DIRECT</p><div class="map-guinee" id="guineeMap"></div><p style="font-size:10px;color:#aaa;text-align:center">Chaque écoute allume une ville 🔥</p></div>

<div class="ad">📢 <span id="livePrayers">🔥 0 guerriers prient maintenant</span> - Rejoins la chaîne!</div>
<div class="grid" id="grid"></div>

<div class="uploadBox">
<h3 style="color:#f9c00f">⬆️ UPLOADER - ESPACE CHANTRES</h3>
<input id="title" placeholder="Titre ex: ROYAUME"><input id="artist" placeholder="Artiste">
<select id="type"><option>SINGLE</option><option>EP</option><option>COVER</option><option>MIXTAPE</option><option>ALBUM</option></select>
<label class="file-label">📀 AUDIO MP3<input id="file" type="file" accept="audio/*"></label>
<label class="file-label">🖼️ COVER IMAGE<input id="coverFile" type="file" accept="image/*"></label>
<input id="cover" placeholder="Ou lien image https://...">
<button onclick="upload()" style="width:100%;background:#f9c00f;padding:14px;border-radius:25px;font-weight:bold;margin-top:10px;border:none;color:#000">PUBLIER 🚀</button>
<p id="status" style="margin-top:8px;font-size:13px;text-align:center"></p>
</div>

<div class="player" id="player" style="display:none">
<img id="pCover" src=""><div style="flex:1;min-width:0"><b id="pTitle" style="font-size:13px;display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis"></b><small id="pArtist" style="color:#aaa"></small>
<audio id="audio" controls style="width:100%;height:26px;margin-top:4px"></audio>
<div style="display:flex;gap:4px;margin-top:5px;flex-wrap:wrap">
<button onclick="enterRoyaume()" style="font-size:11px;padding:4px 10px;border-radius:15px;border:none;background:linear-gradient(#f9c00f,#ff8c00);color:#000;font-weight:bold">👑 MODE ROYAUME 4D</button>
<button onclick="pray()" style="font-size:11px;padding:4px 10px;border-radius:15px;border:none;background:#8B0000;color:#fff">🙏 PRIER</button>
<button onclick="amen()" style="font-size:11px;padding:4px 10px;border-radius:15px;border:none;background:#333;color:#fff">AMEN 🔥</button>
<button onclick="shareTo('whatsapp')" style="font-size:11px;padding:4px 8px;border-radius:15px;border:none;background:#25D366;color:#fff">WA</button>
</div>
<div id="amenWall" class="amen-wall" style="display:none"></div>
</div></div>

<!-- MODE ROYAUME IMMERSIF -->
<div id="royaumeMode">
<div class="royaume-bg" id="royaumeBg"></div><div class="cross-glow">✝️</div><div class="particles" id="particles"></div>
<div class="royaume-content">
<button onclick="exitRoyaume()" style="position:absolute;top:20px;right:20px;background:#000;color:#fff;border:1px solid #f9c00f;padding:8px 15px;border-radius:20px">X FERMER</button>
<img id="rCover" src="" style="width:180px;height:180px;border-radius:15px;margin:0 auto;box-shadow:0 0 40px #f9c00f;border:3px solid #f9c00f">
<h1 id="rTitle" style="margin:15px 0 5px;font-size:26px;color:#f9c00f"></h1><p id="rArtist" style="color:#fff"></p>
<div id="verseContainer" style="min-height:80px;margin:20px 0"></div>
<button onclick="declareWar()" style="background:linear-gradient(90deg,#f9c00f,#ff8c00);color:#000;padding:15px 30px;border-radius:30px;border:none;font-weight:bold;font-size:16px;box-shadow:0 0 30px #f9c00f;animation:pulse 1s infinite">⚔️ DÉCLARER LA GUERRE SPIRITUELLE ⚔️</button>
<p style="margin-top:15px;font-size:12px;color:#aaa">Tape pour faire exploser la lumière du Royaume!</p>
<div style="margin-top:20px"><p style="font-size:11px;color:#f9c00f">🔥 <span id="rPrayers">0</span> GUERRIERS DANS CE COMBAT</p></div>
</div>
</div>

<div class="modal" id="artistModal"><div class="modal-content"><button onclick="closeArtist()" style="float:right;background:#333;color:#fff;border:none;padding:5px 12px;border-radius:15px">X</button><div id="artistContent"></div></div></div>

<script>
let allSongs=[]; let currentSong=null; let currentFile=''; let verses=["JE SUIS DU ROYAUME! 👑","LE ROYAUME A VAINCU! ✝️","AUCUNE ARME NE PROSPÉRERA! 🛡️","JE SUIS PLUS QUE VAINQUEUR! 🔥","LUMIÈRE CONTRE TÉNÈBRES! ⚡","CHRIST EST ROI! 👑"];
let cities=["Conakry","Kindia","Labé","Kankan","Nzérékoré","Boké","Mamou","Faranah"]; let cityState={};
async function load(){ let r=await fetch('/api/songs'); allSongs=await r.json(); document.getElementById('count').innerText=allSongs.length+' chants'; render(allSongs); initMap(); initArmor(); setInterval(updateLive,3000); }
function getCover(s){ if(s.cover_file) return '/uploads/'+s.cover_file; return s.cover_url||s.cover||'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=500'; }
function render(list){
 let h=''; list.forEach(s=>{
  let cover=getCover(s);
  h+=`<div class="card"><div onclick="playSong('${s.id}')"><img src="${cover}"><h4>${s.title}</h4></div><p onclick="openArtist('${s.artist.replace(/'/g,"\\\\'")}')" style="color:#aaa;font-size:11px">${s.artist}</p><div style="display:flex;justify-content:space-between;margin-top:5px"><span style="font-size:10px;color:#aaa">▶️ ${s.plays||0} | 🙏 ${s.prayers||0}</span><span class="badge">${s.type||'SINGLE'}</span></div></div>`;
 }); document.getElementById('grid').innerHTML=h||'<p style="padding:20px;color:#aaa">Aucun</p>';
}
function initMap(){ let h=''; cities.forEach(c=>{ cityState[c]=false; h+=`<div class="city" id="city-${c}">${c}<br><small>0</small></div>`; }); document.getElementById('guineeMap').innerHTML=h; }
function lightCity(){ let c=cities[Math.floor(Math.random()*cities.length)]; let el=document.getElementById('city-'+c); if(!el) return; el.classList.add('on'); let countEl=el.querySelector('small'); countEl.innerText=parseInt(countEl.innerText||0)+1+' écoutes'; setTimeout(()=>el.classList.remove('on'),2500); }
function initArmor(){
 let pieces=[{id:'ceinture',name:'CEINTURE',icon:'🎗️',need:1},{id:'cuirasse',name:'CUIRASSE',icon:'🛡️',need:3},{id:'chaussures',name:'CHAUSSURES',icon:'👟',need:5},{id:'bouclier',name:'BOUCLIER',icon:'🛡️',need:8},{id:'casque',name:'CASQUE',icon:'⛑️',need:12},{id:'epee',name:'ÉPÉE',icon:'⚔️',need:20}];
 let total=parseInt(localStorage.getItem('gospel_plays')||0);
 let h=''; pieces.forEach(p=>{ let unlocked=total>=p.need; h+=`<div class="armor-piece ${unlocked?'unlocked':''}">${p.icon}<br>${p.name}<br><small>${unlocked?'✅':total+'/'+p.need}</small></div>`; });
 h+=`<div style="min-width:80px;padding:8px;background:#000;border-radius:10px;text-align:center;font-size:10px;border:1px dashed #f9c00f">TOTAL<br><b>${total} écoutes</b></div>`;
 document.getElementById('armorBar').innerHTML=h;
 if(total>=20 && !localStorage.getItem('warrior_alert')){ alert('🎉 TU ES DEVENU GUERRIER DU ROYAUME! Armure complète débloquée! 👑⚔️'); localStorage.setItem('warrior_alert','1'); }
}
async function playSong(id){
 let s=allSongs.find(x=>x.id==id); if(!s) return; currentSong=s; currentFile=s.file;
 document.getElementById('player').style.display='flex'; document.getElementById('pCover').src=getCover(s);
 document.getElementById('pTitle').innerText=s.title; document.getElementById('pArtist').innerText=s.artist;
 if(s.file){ document.getElementById('audio').src='/uploads/'+s.file; document.getElementById('audio').play(); }
 fetch('/api/play/'+id,{method:'POST'}).then(()=>{ s.plays=(s.plays||0)+1; });
 let tp=parseInt(localStorage.getItem('gospel_plays')||0)+1; localStorage.setItem('gospel_plays',tp); initArmor(); lightCity(); loadAmens(id);
}
function doSearch(){ let q=document.getElementById('search').value.toLowerCase(); if(!q) return render(allSongs); render(allSongs.filter(s=> (s.title+s.artist).toLowerCase().includes(q))); }
function filterType(t,btn){ document.querySelectorAll('.nav button').forEach(b=>b.classList.remove('active')); btn.classList.add('active'); if(t=='ALL') render(allSongs); else render(allSongs.filter(s=>(s.type||'SINGLE')==t)); }
// PRIERE ET AMEN
async function pray(){ if(!currentSong) return; let r=await fetch('/api/pray/'+currentSong.id,{method:'POST'}); let j=await r.json(); alert('🙏 Tu as rejoint la chaîne de prière! '+j.total+' guerriers prient sur ce chant!'); currentSong.prayers=j.total; render(allSongs); }
async function amen(){ if(!currentSong) return; let name=prompt('Ton prénom pour le Mur d\\'AMEN?')||'Guerrier Anonyme'; let r=await fetch('/api/amen/'+currentSong.id,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name})}); loadAmens(currentSong.id); // effet visuel
 let wall=document.getElementById('amenWall'); wall.style.display='block'; let b=document.createElement('span'); b.className='amen-bubble'; b.innerText='🔥 AMEN - '+name; wall.appendChild(b); wall.scrollTop=wall.scrollHeight;
}
async function loadAmens(id){ let r=await fetch('/api/amens/'+id); let list=await r.json(); let wall=document.getElementById('amenWall'); if(list.length==0){ wall.style.display='none'; return; } wall.style.display='block'; wall.innerHTML=list.slice(-20).map(a=>`<span class="amen-bubble">🔥 ${a.name} - AMEN</span>`).join(''); }
async function updateLive(){ let r=await fetch('/api/live'); let j=await r.json(); document.getElementById('livePrayers').innerText=`🔥 ${j.prayers} guerriers prient maintenant - ${j.totalPlays} écoutes totales`; if(document.getElementById('royaumeMode').style.display=='block'){ document.getElementById('rPrayers').innerText=j.prayers; } }
// ROYAUME MODE
function enterRoyaume(){ if(!currentSong) return; document.getElementById('royaumeMode').style.display='block'; document.getElementById('royaumeBg').style.backgroundImage=`url('${getCover(currentSong)}')`; document.getElementById('rCover').src=getCover(currentSong); document.getElementById('rTitle').innerText=currentSong.title; document.getElementById('rArtist').innerText=currentSong.artist; createParticles(); showVerse(); }
function exitRoyaume(){ document.getElementById('royaumeMode').style.display='none'; }
function createParticles(){ let cont=document.getElementById('particles'); cont.innerHTML=''; for(let i=0;i<30;i++){ let p=document.createElement('div'); p.className='particle'; p.style.left=Math.random()*100+'%'; p.style.animationDuration=(3+Math.random()*4)+'s'; p.style.animationDelay=Math.random()*2+'s'; cont.appendChild(p); } }
function showVerse(){ let v=verses[Math.floor(Math.random()*verses.length)]; let c=document.getElementById('verseContainer'); c.innerHTML=`<div class="verse-pop">${v}</div>`; }
function declareWar(){
 showVerse(); // explosion
 let bg=document.getElementById('royaumeBg'); bg.style.filter='brightness(1.5)'; setTimeout(()=>bg.style.filter='brightness(0.5)',300);
 // vibration si mobile
 if(navigator.vibrate) navigator.vibrate(200);
 // particules explosion
 for(let i=0;i<50;i++){ let p=document.createElement('div'); p.className='particle'; p.style.left='50%'; p.style.top='50%'; p.style.background='#fff'; p.style.animation='floatUp 1s ease-out'; document.getElementById('particles').appendChild(p); setTimeout(()=>p.remove(),1000); }
 fetch('/api/pray/'+currentSong.id,{method:'POST'});
}
function openArtist(artist){
 let songs=allSongs.filter(s=>s.artist.toLowerCase()==artist.toLowerCase());
 let html=`<div style="text-align:center"><img src="${getCover(songs[0])}" style="width:100px;height:100px;border-radius:50%;object-fit:cover;border:3px solid #f9c00f"><h2 style="margin:10px 0">${artist}</h2><p style="color:#aaa">${songs.length} chants • ${songs.reduce((a,b)=>a+(b.plays||0),0)} écoutes</p></div><hr style="border:0;border-top:1px solid #333;margin:15px 0">`;
 songs.forEach(s=>{ html+=`<div style="display:flex;gap:10px;padding:10px;background:#1e1e1e;border-radius:8px;margin:8px 0" onclick="playSong('${s.id}');closeArtist()"><img src="${getCover(s)}" style="width:45px;height:45px;border-radius:5px"><div><b>${s.title}</b><br><small>${s.type} • ▶️ ${s.plays||0}</small></div></div>`; });
 document.getElementById('artistContent').innerHTML=html; document.getElementById('artistModal').style.display='block';
}
function closeArtist(){ document.getElementById('artistModal').style.display='none'; }
function shareTo(p){ let url=encodeURIComponent(location.href); let text=encodeURIComponent('🎤 Écoute '+document.getElementById('pTitle').innerText+' sur GOSPEL224 WORLD 👑⚔️'); if(p=='whatsapp') window.open('https://wa.me/?text='+text+'%20'+url); }
async function upload(){
 let title=document.getElementById('title').value; let artist=document.getElementById('artist').value; let type=document.getElementById('type').value;
 if(!title||!artist) return alert('Titre et artiste requis'); document.getElementById('status').innerText='⏳ Envoi...';
 let fd=new FormData(); fd.append('title',title); fd.append('artist',artist); fd.append('type',type); fd.append('cover_url',document.getElementById('cover').value);
 let f=document.getElementById('file').files[0]; if(f) fd.append('file',f); let cf=document.getElementById('coverFile').files[0]; if(cf) fd.append('coverFile',cf);
 let r=await fetch('/upload',{method:'POST',body:fd}); let j=await r.json(); document.getElementById('status').innerText=j.message; if(j.success) load();
}
load();
</script></body></html>
    """

@app.route("/api/songs")
def api(): return jsonify(load_songs())

@app.route("/api/live")
def live():
    songs=load_songs()
    total=sum(s.get("plays",0) for s in songs)
    prayers=sum(s.get("prayers",0) for s in songs)
    return jsonify({"totalPlays":total,"prayers":prayers})

@app.route("/api/play/<song_id>", methods=["POST"])
def play(song_id):
    songs=load_songs()
    for s in songs:
        if s["id"]==song_id:
            s["plays"]=s.get("plays",0)+1
            break
    save_json(SONGS_FILE,songs)
    return jsonify({"ok":True})

@app.route("/api/pray/<song_id>", methods=["POST"])
def pray(song_id):
    songs=load_songs()
    total=0
    for s in songs:
        if s["id"]==song_id:
            s["prayers"]=s.get("prayers",0)+1
            total=s["prayers"]
            break
    save_json(SONGS_FILE,songs)
    return jsonify({"ok":True,"total":total})

@app.route("/api/amens/<song_id>")
def get_amens(song_id):
    all_amens=load_json(AMEN_FILE,{})
    return jsonify(all_amens.get(song_id,[]))

@app.route("/api/amen/<song_id>", methods=["POST"])
def add_amen(song_id):
    data=request.get_json() or {}
    name=data.get("name","Guerrier")[:30]
    all_amens=load_json(AMEN_FILE,{})
    if song_id not in all_amens: all_amens[song_id]=[]
    all_amens[song_id].append({"name":name,"id":uuid.uuid4().hex[:4]})
    # garde 50 derniers
    all_amens[song_id]=all_amens[song_id][-50:]
    save_json(AMEN_FILE,all_amens)
    return jsonify({"ok":True})

@app.route("/uploads/<path:filename>")
def up(filename): return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/upload", methods=["POST"])
def upload():
    title=request.form.get("title","").strip(); artist=request.form.get("artist","").strip()
    type_ = request.form.get("type","SINGLE"); cover_url=request.form.get("cover_url","").strip()
    if not title or not artist: return jsonify({"success":False,"message":"Titre et artiste requis"})
    audio_filename=""; cover_filename="";
    if "file" in request.files:
        file=request.files["file"]
        if file and file.filename:
            ext=os.path.splitext(secure_filename(file.filename))[1]
            audio_filename=f"{uuid.uuid4().hex}{ext}"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], audio_filename))
    if "coverFile" in request.files:
        cfile=request.files["coverFile"]
        if cfile and cfile.filename:
            ext=os.path.splitext(secure_filename(cfile.filename))[1]
            cover_filename=f"cover_{uuid.uuid4().hex}{ext}"
            cfile.save(os.path.join(app.config['UPLOAD_FOLDER'], cover_filename))
    songs=load_songs()
    songs.insert(0,{"id":uuid.uuid4().hex[:8],"title":title,"artist":artist,"type":type_,
                     "cover_file":cover_filename,"cover_url":cover_url,"file":audio_filename,"plays":0,"prayers":0})
    save_json(SONGS_FILE,songs)
    return jsonify({"success":True,"message":f"✅ {type_} '{title}' publié! 👑"})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",5000)))
