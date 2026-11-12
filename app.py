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
            "id":"1","title":"AIMEZ PRECHER JESUS","artist":"Jean Farakamano","type":"SINGLE",
            "cover_file":"","cover_url":"https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=500","file":"","plays":1240
        }]
    try:
        with open(SONGS_FILE,"r",encoding="utf-8") as f: return json.load(f)
    except: return []

def save_songs(s): 
    with open(SONGS_FILE,"w",encoding="utf-8") as f: json.dump(s,f,ensure_ascii=False,indent=2)

def get_cover_url(song):
    if song.get("cover_file"):
        return f"/uploads/{song['cover_file']}"
    return song.get("cover_url") or song.get("cover") or "https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=500"

@app.route("/")
def home():
    return """
<!DOCTYPE html>
<html lang="fr"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>GOSPEL224 WORLD</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}body{background:#000;color:#fff;font-family:Arial;padding-bottom:95px}
.header{background:linear-gradient(180deg,#f9c00f 0%, #ff8c00 40%, #000 100%);padding:25px 15px;text-align:center}
.header h1{font-size:28px;letter-spacing:1px;color:#000} .header p{color:#000;font-weight:bold;margin-top:5px;font-size:13px}
.topbar{display:flex;gap:10px;padding:12px;background:#121212;position:sticky;top:0;z-index:20;align-items:center}
.topbar input{flex:1;padding:10px 15px;border-radius:25px;background:#2a2a2a;border:none;color:#fff}
.nav{display:flex;gap:8px;overflow-x:auto;padding:0 15px 12px;background:#121212;position:sticky;top:54px;z-index:10}
.nav button{background:#2a2a2a;color:#fff;border:none;padding:7px 16px;border-radius:20px;white-space:nowrap;font-size:13px}
.nav button.active{background:#f9c00f;color:#000;font-weight:bold}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px;padding:15px}
.card{background:#181818;padding:10px;border-radius:12px;cursor:pointer}
.card:hover{background:#282828;transform:translateY(-3px)} .card img{width:100%;height:150px;object-fit:cover;border-radius:8px}
.card h4{margin:8px 0 2px;font-size:14px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.card p{color:#aaa;font-size:12px} .badge{font-size:10px;background:#f9c00f;color:#000;padding:2px 6px;border-radius:10px;font-weight:bold}
.ad{background:linear-gradient(90deg,#ff8c00,#f9c00f);color:#000;padding:10px;text-align:center;margin:12px 15px;border-radius:10px;font-weight:bold;font-size:13px}
.uploadBox{background:#121212;margin:15px;padding:18px;border-radius:15px;border:2px dashed #f9c00f}
input,select{width:100%;padding:10px;margin:6px 0;border-radius:8px;border:none;background:#2a2a2a;color:#fff}
.file-label{display:block;background:#2a2a2a;padding:12px;border-radius:8px;margin:6px 0;text-align:center;border:1px dashed #555;cursor:pointer}
.file-label span{color:#f9c00f;font-weight:bold}
.player{position:fixed;bottom:0;left:0;right:0;background:#181818;border-top:1px solid #333;padding:10px 15px;display:flex;align-items:center;gap:12px;z-index:50}
.player img{width:52px;height:52px;border-radius:6px}
.modal{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.9);z-index:100;display:none;overflow-y:auto;padding:20px}
.modal-content{background:#121212;border-radius:15px;padding:20px;max-width:600px;margin:20px auto}
.close{float:right;background:#333;color:#fff;border:none;padding:5px 12px;border-radius:15px;cursor:pointer}
</style></head><body>
<div class="header"><h1>🎤 GOSPEL224 WORLD</h1><p>LA PLATEFORME OFFICIELLE DES CHANTRES DE GUINÉE 🇬🇳</p></div>
<div class="topbar"><input id="search" placeholder="🔍 Rechercher un chant, un artiste..." oninput="doSearch()"><span id="count" style="font-size:12px;color:#aaa"></span></div>
<div class="nav">
<button class="active" onclick="filterType('ALL',this)">TOUT</button>
<button onclick="filterType('SINGLE',this)">SINGLE</button>
<button onclick="filterType('EP',this)">EP</button>
<button onclick="filterType('COVER',this)">COVER</button>
<button onclick="filterType('MIXTAPE',this)">MIXTAPE</button>
<button onclick="filterType('ALBUM',this)">ALBUM</button>
</div>
<div class="ad">📢 PROMO: Mets ton chant en avant ici! Contact Gospel224 WhatsApp</div>
<div class="grid" id="grid"></div>

<div class="uploadBox">
<h3 style="color:#f9c00f;margin-bottom:10px">⬆️ UPLOADER - Espace Chantres</h3>
<input id="title" placeholder="Titre du chant ex: ROYAUME">
<input id="artist" placeholder="Nom de l'artiste ex: Jean Farakamano">
<select id="type"><option>SINGLE</option><option>EP</option><option>COVER</option><option>MIXTAPE</option><option>ALBUM</option></select>

<label class="file-label">📀 <span>Choisir le fichier AUDIO (MP3/WAV)</span><br><input id="file" type="file" accept="audio/*" style="margin-top:8px"></label>
<label class="file-label">🖼️ <span>Choisir la COVER (Image ROYAUME)</span><br><input id="coverFile" type="file" accept="image/*" style="margin-top:8px"><br><small style="color:#aaa">Laisse vide si tu veux utiliser un lien</small></label>
<input id="cover" placeholder="Ou colle un lien image https://... (optionnel)">

<button onclick="upload()" style="width:100%;background:#f9c00f;padding:14px;border-radius:25px;font-weight:bold;margin-top:10px;border:none;color:#000;font-size:15px">PUBLIER MAINTENANT 🚀</button>
<p id="status" style="margin-top:10px;font-size:13px;text-align:center"></p>
</div>

<div class="player" id="player" style="display:none">
<img id="pCover" src=""><div style="flex:1;min-width:0"><b id="pTitle" style="font-size:14px;display:block;white-space:nowrap;overflow:hidden;text-overflow:ellipsis"></b><small id="pArtist" style="color:#aaa"></small><br>
<audio id="audio" controls style="width:100%;height:28px;margin-top:4px"></audio>
<div style="display:flex;gap:5px;margin-top:6px;flex-wrap:wrap">
<button onclick="share()" style="font-size:11px;padding:4px 10px;border-radius:15px;border:none;background:#f9c00f;color:#000">PARTAGER ↗️</button>
<button onclick="download()" style="font-size:11px;padding:4px 10px;border-radius:15px;border:none;background:#333;color:#fff">TÉLÉCHARGER ⬇️</button>
<button onclick="shareTo('whatsapp')" style="font-size:11px;padding:4px 10px;border-radius:15px;border:none;background:#25D366;color:#fff">WhatsApp</button>
<button onclick="shareTo('facebook')" style="font-size:11px;padding:4px 10px;border-radius:15px;border:none;background:#1877F2;color:#fff">Facebook</button>
</div></div></div>

<div class="modal" id="artistModal"><div class="modal-content"><button class="close" onclick="closeArtist()">X Fermer</button><div id="artistContent"></div></div></div>

<script>
let allSongs=[]; let currentSong=null; let currentFile='';
async function load(){
 let r=await fetch('/api/songs'); allSongs=await r.json();
 document.getElementById('count').innerText=allSongs.length+' chants'; render(allSongs);
}
function getCover(s){ if(s.cover_file) return '/uploads/'+s.cover_file; return s.cover_url||s.cover||'https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=500'; }
function render(list){
 let h=''; list.forEach(s=>{
  let cover=getCover(s);
  h+=`<div class="card"><div onclick="playSong('${s.id}')"><img src="${cover}"><h4>${s.title}</h4></div>
  <p onclick="openArtist('${s.artist.replace(/'/g,"\\\\'")}')">${s.artist}</p>
  <div style="display:flex;justify-content:space-between;align-items:center;margin-top:6px"><span style="font-size:11px;color:#aaa">▶️ ${s.plays||0}</span><span class="badge">${s.type||'SINGLE'}</span></div></div>`;
 }); document.getElementById('grid').innerHTML=h||'<p style="padding:20px;color:#aaa">Aucun résultat</p>';
}
function doSearch(){ let q=document.getElementById('search').value.toLowerCase(); if(!q) return render(allSongs); render(allSongs.filter(s=> (s.title+s.artist).toLowerCase().includes(q))); }
function filterType(t,btn){ document.querySelectorAll('.nav button').forEach(b=>b.classList.remove('active')); btn.classList.add('active'); if(t=='ALL') render(allSongs); else render(allSongs.filter(s=>(s.type||'SINGLE')==t)); }
async function playSong(id){
 let s=allSongs.find(x=>x.id==id); if(!s) return; currentSong=s; currentFile=s.file;
 document.getElementById('player').style.display='flex';
 document.getElementById('pCover').src=getCover(s);
 document.getElementById('pTitle').innerText=s.title; document.getElementById('pArtist').innerText=s.artist;
 if(s.file){ document.getElementById('audio').src='/uploads/'+s.file; document.getElementById('audio').play(); }
 fetch('/api/play/'+id,{method:'POST'}).then(()=>{ s.plays=(s.plays||0)+1; });
}
function share(){ if(navigator.share){navigator.share({title:currentSong.title,text:'Écoute sur GOSPEL224 WORLD',url:location.href})} else {navigator.clipboard.writeText(location.href); alert('Lien copié!');} }
function download(){ if(!currentFile) return alert('Pas de fichier audio - uploade un MP3 d\\'abord'); window.location='/uploads/'+currentFile; }
function shareTo(p){ let url=encodeURIComponent(location.href); let text=encodeURIComponent('🎤 Écoute '+document.getElementById('pTitle').innerText+' sur GOSPEL224 WORLD 🔥'); if(p=='whatsapp') window.open('https://wa.me/?text='+text+'%20'+url); if(p=='facebook') window.open('https://www.facebook.com/sharer/sharer.php?u='+url); }
function openArtist(artist){
 let songs=allSongs.filter(s=>s.artist.toLowerCase()==artist.toLowerCase());
 let html=`<div style="text-align:center;padding:20px 0"><img src="${getCover(songs[0])}" style="width:120px;height:120px;border-radius:50%;object-fit:cover"><h2 style="margin:15px 0 5px">${artist}</h2><p style="color:#aaa">${songs.length} chants • ${(songs.reduce((a,b)=>a+(b.plays||0),0))} écoutes totales</p></div><hr style="border:0;border-top:1px solid #333;margin:15px 0"><h3>Chants de ${artist}</h3><div style="margin-top:10px">`;
 songs.forEach(s=>{ html+=`<div style="display:flex;gap:10px;padding:10px;background:#1e1e1e;border-radius:8px;margin:8px 0" onclick="playSong('${s.id}');closeArtist()"><img src="${getCover(s)}" style="width:50px;height:50px;border-radius:5px;object-fit:cover"><div><b>${s.title}</b><br><small style="color:#aaa">${s.type} • ▶️ ${s.plays||0}</small></div></div>`; });
 html+=`</div>`; document.getElementById('artistContent').innerHTML=html; document.getElementById('artistModal').style.display='block';
}
function closeArtist(){ document.getElementById('artistModal').style.display='none'; }
async function upload(){
 let title=document.getElementById('title').value; let artist=document.getElementById('artist').value; let type=document.getElementById('type').value;
 if(!title||!artist) return alert('Titre et artiste requis'); 
 document.getElementById('status').innerText='⏳ Envoi en cours... Ne ferme pas!';
 let fd=new FormData(); fd.append('title',title); fd.append('artist',artist); fd.append('type',type);
 fd.append('cover_url',document.getElementById('cover').value);
 let f=document.getElementById('file').files[0]; if(f) fd.append('file',f);
 let cf=document.getElementById('
