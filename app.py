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
<h3 style="color:#f9c00f">⬆️ UPLOADER - ESP
