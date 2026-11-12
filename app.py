from flask import Flask, jsonify, request, send_from_directory, Response
import json, os, uuid
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
SONGS_FILE = "songs.json"
AMEN_FILE = "amens.json"

def load_json(f, default):
    if not os.path.exists(f): return default
    try:
        with open(f,"r",encoding="utf-8") as x: return json.load(x)
    except: return default
def save_json(f, data):
    with open(f,"w",encoding="utf-8") as x: json.dump(data,x,ensure_ascii=False,indent=2)
def load_songs(): return load_json(SONGS_FILE, [{"id":"1","title":"ROYAUME","artist":"Jean Farakamano","type":"ALBUM","cover_file":"","cover_url":"","file":"","plays":1240,"prayers":89}])
def get_cover(s):
    if s.get("cover_file"): return f"/uploads/{s['cover_file']}"
    return s.get("cover_url") or s.get("cover") or "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600"

@app.route("/manifest.json")
def manifest():
    return jsonify({
        "name": "GOSPEL224 WORLD",
        "short_name": "GOSPEL224",
        "description": "La plateforme officielle des chantres de Guinée",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#000000",
        "theme_color": "#f9c00f",
        "orientation": "portrait",
        "icons": [
            {"src": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=192", "sizes": "192x192", "type": "image/png"},
            {"src": "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=512", "sizes": "512x512", "type": "image/png"}
        ]
    })

@app.route("/sw.js")
def sw():
    js = """
    self.addEventListener('install', e => self.skipWaiting());
    self.addEventListener('activate', e => self.clients.claim());
    self.addEventListener('fetch', e => {
      e.respondWith(fetch(e.request).catch(() => caches.match(e.request)));
    });
    """
    return Response(js, mimetype="application/javascript")

@app.route("/")
def home():
    return """
<!DOCTYPE html><html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>GOSPEL224 WORLD</title>
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#f9c00f">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="GOSPEL224">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}body{background:#050505;color:#fff;font-family:'Inter',Arial;padding-bottom:110px;overflow-x:hidden}
.header{background:radial-gradient(ellipse at top, #2a2100 0%, #000 70%);padding:32px 15px;text-align:center;border-bottom:1px solid #1a1a1a}
.header h1{font-size:34px;font-weight:900;letter-spacing:3px;background:linear-gradient(#f9c00f,#ff8c00);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.header p{color:#555;font-size:10px;letter-spacing:5px;margin-top:8px;text-transform:uppercase}
.topbar{display:flex;gap:10px;padding:14px;background:#0a0a0a;position:sticky;top:0;z-index:20;border-bottom:1px solid #151515}
.topbar input{flex:1;padding:12px 18px;border-radius:30px;background:#151515;border:1px solid #222;color:#fff;outline:none}
.nav{display:flex;gap:8px;overflow-x:auto;padding:0 15px 14px;background:#0a0a0a;position:sticky;top:58px;z-index:10}
.nav button{background:#151515;color:#888;border:1px solid #222;padding:8px 18px;border-radius:25px;white-space:nowrap;font-size:12px;font-weight:700}
.nav button.active{background:#f9c00f;color:#000;border-color:#f9c00f}
.install-banner{display:none;background:linear-gradient(90deg,#f9c00f,#ff8c00);color:#000;padding:14px 16px;margin:12px 14px;border-radius:14px;justify-content:space-between;align-items:center;font-weight:900;font-size:13px}
.install-banner.show{display:flex}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:14px;padding:16px}
.card{background:#101010;border-radius:18px;overflow:hidden;border:1px solid #1a1a1a;cursor:pointer;transition:0.3s}
.card:hover{transform:translateY(-6px);border-color:#f9c00f}
.card img{width:100%;height:165px;object-fit:cover}
.card-info{padding:12px}
.card h4{font-size:13px;font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.card p{color:#666;font-size:11px;margin-top:3px}
.card-meta{display:flex;justify-content:space-between;margin-top:8px;font-size:10px;color:#555}
.badge{font-size:9px;background:#f9c00f;color:#000;padding:3px 8px;border-radius:20px;font-weight:900}
.section{background:#0a0a0a;margin:14px;border-radius:18px;padding:16px;border:1px solid #151515}
.section-title{font-size:11px;letter-spacing:2px;color:#f9c00f;font-weight:900;margin-bottom:12px;text-transform:uppercase}
.map-guinee{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.city{padding:12px 5px;background:#111;border-radius:12px;text-align:center;font-size:11px;border:1px solid #1e1e1e;transition:0.6s}
.city.on{background:linear-gradient(135deg,#f9c00f,#ff8c00);color:#000;font-weight:900;box-shadow:0 0 20px #f9c00f;transform:scale(1.08)}
.armor-bar{display:flex;gap:8px;overflow-x:auto}
.armor-piece{min-width:78px;padding:10px;background:#111;border-radius:14px;text-align:center;font-size:10px;border:1px solid #1e1e1e}
.armor-piece.unlocked{background:linear-gradient(135deg,#f9c00f,#ff8c00);color:#000;font-weight:900}
.uploadBox{background:#0a0a0a;margin:14px;padding:20px;border-radius:18px;border:1px dashed #222}
.file-label{display:block;background:#111;padding:14px;border-radius:12px;margin:8px 0;text-align:center;border:1px dashed #333;cursor:pointer;font-size:12px}
.file-label span{color:#f9c00f;font-weight:900}
input,select{width:100%;padding:12px;margin:7px 0;border-radius:12px;border:1px solid #222;background:#111;color:#fff;outline:none}
.player{position:fixed;bottom:0;left:0;right:0;background:rgba(10,10,10,0.97);backdrop-filter:blur(20px);border-top:1px solid #222;padding:12px 15px;display:flex;align-items:center;gap:14px;z-index:50}
.player img{width:56px;height:56px;border-radius:10px}
.btn{font-size:11px;padding:7px 14px;border-radius:20px;border:none;font-weight:700;cursor:pointer}
.btn-down{background:#f9c00f;color:#000}
.btn-dark{background:#1e1e1e;color:#fff;border:1px solid #333}
.btn-immersif{background:linear-gradient(135deg,#f9c00f,#ff8c00);color:#000}
.amen-wall{max-height:90px;overflow-y:auto;background:#050505;border-radius:12px;padding:8px;margin-top:8px;display:flex;flex-wrap:wrap;gap:6px}
.amen-bubble{background:#1a1a1a;padding:5px 10px;border-radius:20px;font-size:11px;border:1px solid #222}
#royaumeMode{position:fixed;top:0;left:0;right:0;bottom:0;background:#000;z-index:200;display:none;overflow:hidden}
.royaume-bg{position:absolute;top:0;left:0;right:0;bottom:0;background-size:cover;background-position:center;filter:brightness(0.35);animation:zoomSlow 25s infinite alternate}
@keyframes zoomSlow{from{transform:scale(1)}to{transform:scale(1.2)}}
.particles{position:absolute;top:0;left:0;right:0;bottom:0;pointer-events:none}
.particle{position:absolute;width:3px;height:3px;background:#f9c00f;border-radius:50%;animation:floatUp linear infinite}
@keyframes floatUp{from{transform:translateY(100vh)}to{transform:translateY(-10vh)}}
.cross-glow{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-size:180px;color:#f9c00f;opacity:0.12;animation:pulse 3s infinite}
@keyframes pulse{0%,100%{transform:translate(-50%,-50%) scale(1)}50%{transform:translate(-50%,-50%) scale(1.15)}}
.royaume-content{position:relative;z-index:2;padding:20px;text-align:center;height:100%;display:flex;flex-direction:column;justify-content:center}
.verse-pop{font-size:30px;font-weight:900;color:#f9c00f;text-shadow:0 0 30px #f9c00f;animation:verseHit 0.8s;margin:20px 0}
@keyframes verseHit{0%{transform:scale(0)}60%{transform:scale(1.25)}100%{transform:scale(1)}}
.modal{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.94);z-index:100;display:none;overflow-y:auto;padding:20px}
.modal-content{background:#0f0f0f;border-radius:20px;padding:22px;max-width:600px;margin:20px auto;border:1px solid #222}
.liveDot{display:inline-block;width:8px;height:8px;background:#ff3b3b;border-radius:50%;margin-right:6px;animation:blink 1s infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:0.3}}
</style></head><body>
<div class="header"><h1>GOSPEL224 WORLD</h1><p>Plateforme Officielle</p></div>

<div class="install-banner" id="installBanner">
<span>📲 Installer GOSPEL224 WORLD sur ton téléphone?</span>
<div><button onclick="installApp()" style="background:#000;color:#f9c00f;padding:8px 16px;border-radius:20px;border:none;font-weight:900;margin-right:8px">INSTALLER</button>
<button onclick="hideBanner()" style="background:transparent;color:#000;border:1px solid #000;padding:6px 12px;border-radius:20px">Plus tard</button></div>
</div>

<div class="topbar"><input id="search" placeholder="Rechercher un chant, un artiste..." oninput="doSearch()"><span id="count" style="font-size:11px;color:#555"></span></div>
<div class="nav">
<button class="active" onclick="filterType('ALL',this)">TOUT</button>
<button onclick="filterType('SINGLE',this)">SINGLE</button>
<button onclick="filterType('EP',this)">EP</button>
<button onclick="filterType('COVER',this)">COVER</button>
<button onclick="filterType('MIXTAPE',this)">MIXTAPE</button>
<button onclick="filterType('ALBUM',this)">ALBUM</button>
</div>
<div class="section"><div class="section-title">Armure • Ephesiens 6</div><div class="armor-bar" id="armorBar"></div></div>
<div class="section"><div class="section-title"><span class="liveDot"></span>Guinée en Direct</div><div class="map-guinee" id="guineeMap"></div></div>
<div style="margin:0 14px;background:linear-gradient(90deg,#111,#1a1500);border:1px solid #2a2200;padding:12px;border-radius:14px;display:flex;justify-content:space-between;align-items:center"><span style="font-size:11px;color:#f9c00f;font-weight:700" id="liveStats">Chargement...</span><span style="font-size:10px;color:#555">LIVE</span></div>
<div class="grid" id="grid"></div>
<div class="uploadBox">
<div class="section-title">Espace Chantres</div>
<input id="title" placeholder="Titre du chant"><input id="artist" placeholder="Nom de l'artiste">
<select id="type"><option>SINGLE</option><option>EP</option><option>COVER</option><option>MIXTAPE</option><option>ALBUM</option></select>
<label class="file-label">📀 Audio MP3 / WAV <input id="file" type="file" accept="audio/*"></label>
<label class="file-label">🖼️ Cover Image <input id="coverFile" type="file" accept="image/*"></label>
<input id="cover" placeholder="Ou lien image https://...">
<button onclick="upload()" style="width:100%;background:#f9c00f;padding:14px;border-radius:30px;font-weight:900;margin-top:12px;border:none;color:#000">PUBLIER</button>
<p id="status" style="margin-top:10px;font-size:12px;text-align:center;color:#888"></p>
</div>
<div class="player" id="player" style="display:none">
<img id="pCover" src=""><div style="flex:1;min-width:0"><b id="pTitle" style="font-size:13px;display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis"></b><small id="pArtist" style="color:#666;font-size:11px"></small>
<audio id="audio" controls style="width:100%;height:28px;margin-top:6px"></audio>
<div style="display:flex;gap:6px;margin-top:8px;flex-wrap:wrap">
<button onclick="download()" class="btn btn-down">⬇️ TÉLÉCHARGER</button>
<button onclick="enterRoyaume()" class="btn btn-immersif">👑 IMMERSIF</button>
<button onclick="pray()" class="btn btn-dark">🙏 PRIER</button>
<button onclick="amen()" class="btn btn-dark">AMEN 🔥</button>
</div><div id="amenWall" class="amen-wall" style="display:none"></div></div></div>
<div id="royaumeMode">
<div class="royaume-bg" id="royaumeBg"></div><div class="cross-glow">✝️</div><div class="particles" id="particles"></div>
<div class="royaume-content">
<button onclick="exitRoyaume()" style="position:absolute;top:20px;right:20px;background:rgba(0,0,0,0.6);color:#fff;border:1px solid #333;padding:8px 16px;border-radius:25px">✕</button>
<img id="rCover" src="" style="width:200px;height:200px;border-radius:20px;margin:0 auto;box-shadow:0 0 50px rgba(249,192,15,0.5);border:2px solid #f9c00f;object-fit:cover">
<h1 id="rTitle" style="margin:18px 0 6px;font-size:28px;font-weight:900;color:#f9c00f"></h1><p id="rArtist" style="color:#888;font-size:13px"></p>
<div id="verseContainer" style="min-height:90px;margin:25px 0"></div>
<div style="display:flex;gap:10px;justify-content:center;flex-wrap:wrap">
<button onclick="declareWar()" style="background:linear-gradient(135deg,#f9c00f,#ff8c00);color:#000;padding:14px 28px;border-radius:30px;border:none;font-weight:900;font-size:13px">⚔️ DÉCLARER</button>
<button onclick="download()" style="background:#fff;color:#000;padding:14px 28px;border-radius:30px;border:none;font-weight:900;font-size:13px">⬇️ TÉLÉCHARGER</button>
</div>
<p style="margin-top:20px;font-size:10px;color:#555;letter-spacing:2px"><span id="rPrayers">0</span> EN PRIÈRE • GOSPEL224 WORLD</p>
</div></div>
<div class="modal" id="artistModal"><div class="modal-content"><button onclick="closeArtist()" style="float:right;background:#1a1a1a;color:#fff;border:1px solid #333;padding:6px 14px;border-radius:20px">✕</button><div id="artistContent"></div></div></div>

<script>
let deferredPrompt;
window.addEventListener('beforeinstallprompt', (e) => {
  e.preventDefault(); deferredPrompt = e;
  document.getElementById('installBanner').classList.add('show');
});
function installApp(){ if(deferredPrompt){ deferredPrompt.prompt(); deferredPrompt.userChoice.then(() => { deferredPrompt = null; hideBanner(); }); } }
function hideBanner(){ document.getElementById('installBanner').classList.remove('show'); }

if('serviceWorker' in navigator){ navigator.serviceWorker.register('/sw.js'); }

let allSongs=[]; let currentSong=null; let currentFile='';
let verses=["JE SUIS DU ROYAUME","LE ROYAUME A VAINCU","AUCUNE ARME NE PROSPÉRERA","PLUS QUE VAINQUEUR","CHRIST EST ROI","LUMIÈRE DANS LES TÉNÈBRES"];
let cities=["Conakry","Kindia","Labé","Kankan","Nzérékoré","Boké","Mamou","Faranah"];
async function load(){ let r=await fetch('/api/songs'); allSongs=await r.json(); document.getElementById('count').innerText=allSongs.length; render(allSongs); initMap(); initArmor(); setInterval(updateLive,4000); updateLive(); }
function getCover(s){ if(s.cover_file) return '/uploads/'+s.cover_file; return s.cover_url||s.cover||'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=600'; }
function render(list){
 let h=''; list.forEach(s=>{
  let cover=getCover(s);
  h+=`<div class="card"><div onclick="playSong('${s.id}')"><img src="${cover}"><div class="card-info"><h4>${s.title}</h4><p>${s.artist}</p><div class="card-meta"><span>▶️ ${s.plays||0}</span><span>🙏 ${s.prayers||0}</span><span class="badge">${s.type||'SINGLE'}</span></div></div></div></div>`;
 }); document.getElementById('grid').innerHTML=h||'<p style="padding:20px;color:#555">Aucun chant</p>';
}
function initMap(){ let h=''; cities.forEach(c=>{ h+=`<div class="city" id="city-${c}"><b>${c}</b><br><small style="font-size:9px;color:#666">0</small></div>`; }); document.getElementById('guineeMap').innerHTML=h; }
function lightCity(){ let c=cities[Math.floor(Math.random()*cities.length)]; let el=document.getElementById('city-'+c); if(!el) return; el.classList.add('on'); let sm=el.querySelector('small'); sm.innerText=parseInt(sm.innerText||0)+1; setTimeout(()=>el.classList.remove('on'),3000); }
function initArmor(){
 let pieces=[{icon:'🎗️',name:'CEINTURE',need:1},{icon:'🛡️',name:'CUIRASSE',need:3},{icon:'👟',name:'MARCHE',need:6},{icon:'🛡️',name:'BOUCLIER',need:10},{icon:'⛑️',name:'CASQUE',need:15},{icon:'⚔️',name:'ÉPÉE',need:25}];
 let total=parseInt(localStorage.getItem('gospel_plays')||0);
 let h=''; pieces.forEach(p=>{ let u=total>=p.need; h+=`<div class="armor-piece ${u?'unlocked':''}"><div style="font-size:18px">${p.icon}</div>${p.name}<br><small style="font-size:9px">${u?'✓':total+'/'+p.need}</small></div>`; });
 h+=`<div style="min-width:70px;padding:10px;background:#000;border-radius:14px;text-align:center;border:1px dashed #222"><small>TOTAL</small><br><b style="color:#f9c00f">${total}</b></div>`;
 document.getElementById('armorBar').innerHTML=h;
}
async function playSong(id){
 let s=allSongs.find(x=>x.id==id); if(!s) return; currentSong=s; currentFile=s.file;
 document.getElementById('player').style.display='flex'; document.getElementById('pCover').src=getCover(s);
 document.getElementById('pTitle').innerText=s.title; document.getElementById('pArtist').innerText=s.artist;
 if(s.file){ document.getElementById('audio').src='/uploads/'+s.file; document.getElementById('audio').play(); }
 fetch('/api/play/'+id,{method:'POST'}); let tp=parseInt(localStorage.getItem('gospel_plays')||0)+1; localStorage.setItem('gospel_plays',tp); initArmor(); lightCity(); loadAmens(id);
}
function doSearch(){ let q=document.getElementById('search').value.toLowerCase(); if(!q) return render(allSongs); render(allSongs.filter(s=> (s.title+s.artist).toLowerCase().includes(q))); }
function filterType(t,btn){ document.querySelectorAll('.nav button').forEach(b=>b.classList.remove('active')); btn.classList.add('active'); if(t=='ALL') render(allSongs); else render(allSongs.filter(s=>(s.type||'SINGLE')==t)); }
function download(){
 if(!currentFile || currentFile==""){ alert('⚠️ Pas de fichier MP3 pour ce chant. Uploade le MP3!'); return; }
 let a=document.createElement('a'); a.href='/uploads/'+currentFile; a.download=currentSong.title+'.mp3'; document.body.appendChild(a); a.click(); document.body.removeChild(a);
}
async function pray(){ if(!currentSong) return; let r=await fetch('/api/pray/'+currentSong.id,{method:'POST'}); let j=await r.json(); currentSong.prayers=j.total; render(allSongs); updateLive(); }
async function amen(){ if(!currentSong) return; let name=prompt('Ton prénom?')||'Guerrier'; await fetch('/api/amen/'+currentSong.id,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name})}); loadAmens(currentSong.id); let wall=document.getElementById('amenWall'); wall.style.display='flex'; }
async function loadAmens(id){ let r=await fetch('/api/amens/'+id); let list=await r.json(); let wall=document.getElementById('amenWall'); if(list.length==0){ wall.style.display='none'; return; } wall.style.display='flex'; wall.innerHTML=list.slice(-30).map(a=>`<span class="amen-bubble">🔥 ${a.name}</span>`).join(''); }
async function updateLive(){ let r=await fetch('/api/live'); let j=await r.json(); document.getElementById('liveStats').innerText=`🔥 ${j.prayers} en prière • ${j.totalPlays} écoutes totales`; document.getElementById('rPrayers').innerText=j.prayers; }
function enterRoyaume(){ if(!currentSong) return; document.getElementById('royaumeMode').style.display='block'; document.getElementById('royaumeBg').style.backgroundImage=`url('${getCover(currentSong)}')`; document.getElementById('rCover').src=getCover(currentSong); document.getElementById('rTitle').innerText=currentSong.title; document.getElementById('rArtist').innerText=currentSong.artist; createParticles(); showVerse(); }
function exitRoyaume(){ document.getElementById('royaumeMode').style.display='none'; }
function createParticles(){ let cont=document.getElementById('particles'); cont.innerHTML=''; for(let i=0;i<35;i++){ let p=document.createElement('div'); p.className='particle'; p.style.left=Math.random()*100+'%'; p.style.animationDuration=(4+Math.random()*6)+'s'; p.style.animationDelay=Math.random()*3+'s'; cont.appendChild(p); } }
function showVerse(){ let v=verses[Math.floor(Math.random()*verses.length)]; document.getElementById('verseContainer').innerHTML=`<div class="verse-pop">${v}</div>`; }
function declareWar(){ showVerse(); let bg=document.getElementById('royaumeBg'); bg.style.filter='brightness(1.2)'; setTimeout(()=>bg.style.filter='brightness(0.35)',400); fetch('/api/pray/'+currentSong.id,{method:'POST'}); }
function openArtist(artist){ let songs=allSongs.filter(s=>s.artist.toLowerCase()==artist.toLowerCase()); let html=`<div style="text-align:center"><img src="${getCover(songs[0])}" style="width:110px;height:110px;border-radius:50%;object-fit:cover;border:3px solid #f9c00f"><h2 style="margin:12px 0 5px">${artist}</h2><p style="color:#666;font-size:12px">${songs.length} chants • ${songs.reduce((a,b)=>a+(b.plays||0),0)} écoutes</p></div><hr style="border:0;border-top:1px solid #1a1a1a;margin:16px 0">`; songs.forEach(s=>{ html+=`<div style="display:flex;gap:12px;padding:12px;background:#0a0a0a;border-radius:12px;margin:8px 0;border:1px solid #151515" onclick="playSong('${s.id}');closeArtist()"><img src="${getCover(s)}" style="width:48px;height:48px;border-radius:8px"><div><b style="font-size:13px">${s.title}</b><br><small style="color:#666">${s.type} • ▶️ ${s.plays||0}</small></div></div>`; }); document.getElementById('artistContent').innerHTML=html; document.getElementById('artistModal').style.display='block'; }
function closeArtist(){ document.getElementById('artistModal').style.display='none'; }
async function upload(){ let title=document.getElementById('title').value; let artist=document.getElementById('artist').value; let type=document.getElementById('type').value; if(!title||!artist) return alert('Titre et artiste requis'); document.getElementById('status').innerText='Envoi...'; let fd=new FormData(); fd.append('title',title); fd.append('artist',artist); fd.append('type',type); fd.append('cover_url',document.getElementById('cover').value); let f=document.getElementById('file').files[0]; if(f) fd.append('file',f); let cf=document.getElementById('coverFile').files[0]; if(cf) fd.append('coverFile',cf); let r=await fetch('/upload',{method:'POST',body:fd}); let j=await r.json(); document.getElementById('status').innerText=j.message; if(j.success) load(); }
load();
</script></body></html>
    """

@app.route("/api/songs")
def api(): return jsonify(load_songs())
@app.route("/api/live")
def live():
    songs=load_songs(); return jsonify({"totalPlays":sum(s.get("plays",0) for s in songs),"prayers":sum(s.get("prayers",0) for s in songs)})
@app.route("/api/play/<song_id>", methods=["POST"])
def play(song_id):
    songs=load_songs()
    for s in songs:
        if s["id"]==song_id: s["plays"]=s.get("plays",0)+1
    save_json(SONGS_FILE,songs); return jsonify({"ok":True})
@app.route("/api/pray/<song_id>", methods=["POST"])
def pray(song_id):
    songs=load_songs(); total=0
    for s in songs:
        if s["id"]==song_id: s["prayers"]=s.get("prayers",0)+1; total=s["prayers"]
    save_json(SONGS_FILE,songs); return jsonify({"ok":True,"total":total})
@app.route("/api/amens/<song_id>")
def get_amens(song_id): return jsonify(load_json(AMEN_FILE,{}).get(song_id,[]))
@app.route("/api/amen/<song_id>", methods=["POST"])
def add_amen(song_id):
    data=request.get_json() or {}; name=data.get("name","Guerrier")[:30]
    all_amens=load_json(AMEN_FILE,{}); all_amens.setdefault(song_id,[]).append({"name":name}); all_amens[song_id]=all_amens[song_id][-50:]
    save_json(AMEN_FILE,all_amens); return jsonify({"ok":True})
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
    return jsonify({"success":True,"message":f"✅ {type_} '{title}' publié!"})

if __name__=="__main__":
    app.run(host="0.0.0.0",port=int(os.environ.get("PORT",5000)))
