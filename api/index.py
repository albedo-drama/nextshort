# REFERRAL CODE: 2025-12-17
REFERRAL_CODE = "ALBEDO-777"

from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

BASE_URL = "https://hrdyckorclwpeyorzpry.supabase.co/functions/v1/api-proxy"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
}

# --- THEMA PREMIUM DARK ---
BASE_LAYOUT = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>ALBEDONEXT-SHORT</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;700;800&display=swap" rel="stylesheet">
    <style>
        :root { --crimson: #e11d48; --dark-bg: #030303; }
        body { background: var(--dark-bg); color: #fff; font-family: 'Plus Jakarta Sans', sans-serif; margin: 0; padding-bottom: 100px; }
        
        /* Glass Navbar */
        .glass-nav { background: rgba(3,3,3,0.8); backdrop-filter: blur(20px); border-bottom: 1px solid rgba(255,255,255,0.05); }
        
        /* Grid 4 System */
        .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; padding: 12px; }
        .drama-card { position: relative; border-radius: 12px; overflow: hidden; background: #111; border: 1px solid #1a1a1a; transition: 0.3s; }
        .drama-card:active { transform: scale(0.92); }
        .drama-card img { width: 100%; aspect-ratio: 3/4; object-fit: cover; }
        .card-overlay { position: absolute; bottom: 0; width: 100%; background: linear-gradient(transparent, rgba(0,0,0,0.9)); padding: 8px 4px 4px; }
        
        /* Status Bar Bawah */
        .status-bar { position: fixed; bottom: 0; left: 0; right: 0; height: 80px; background: rgba(10,10,10,0.95); backdrop-filter: blur(25px); border-top: 1px solid rgba(255,255,255,0.1); display: flex; justify-content: space-around; align-items: center; z-index: 1000; padding-bottom: env(safe-area-inset-bottom); }
        .nav-link { display: flex; flex-direction: column; align-items: center; font-size: 10px; color: #555; text-decoration: none; font-weight: 800; transition: 0.3s; }
        .nav-link.active { color: var(--crimson); }
        .nav-link svg { width: 22px; height: 22px; margin-bottom: 4px; }

        /* Video Player Bawaan */
        .player-container { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: #000; z-index: 9999; display: none; }
        .player-container.active { display: block; }
        video { width: 100%; height: 100%; background: #000; }

        /* Button Pagination */
        .btn-nav-page { background: #111; border: 1px solid #222; padding: 12px 24px; border-radius: 10px; color: var(--crimson); font-size: 11px; font-weight: 800; letter-spacing: 1px; }
    </style>
</head>
<body>
    <nav class="glass-nav sticky top-0 z-[500] px-5 py-4 flex items-center justify-between">
        <h1 class="text-sm font-black italic tracking-tighter">ALBEDO<span class="text-rose-600">NEXT-SHORT</span></h1>
        <form action="/search" method="GET" class="flex-1 max-w-[150px] ml-4">
            <input type="text" name="q" placeholder="Cari drama..." class="w-full bg-white/5 border border-white/10 rounded-full py-1.5 px-4 text-[10px] outline-none focus:border-rose-600 transition-all">
        </form>
    </nav>

    <main id="content-area">{{ content | safe }}</main>

    <div class="status-bar">
        <a href="/" class="nav-link" id="h-home"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>HOME</a>
        <a href="javascript:history.back()" class="nav-link"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg>KEMBALI</a>
        <a href="/favorites" class="nav-link" id="h-fav"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>FAVORIT</a>
        <a href="/history" class="nav-link" id="h-hist"><svg fill="currentColor" viewBox="0 0 24 24"><path d="M13 3a9 9 0 0 0-9 9H1l3.89 3.89.07.14L9 12H6a7 7 0 1 1 7 7 7.07 7.07 0 0 1-6-3.15L5.45 17.4A9 9 0 1 0 13 3z"/></svg>HISTORY</a>
    </div>

    <script>
        function saveHist(id, name, img) {
            let h = JSON.parse(localStorage.getItem('alb_history') || '[]');
            h = h.filter(x => x.id !== id);
            h.unshift({id, name, img});
            localStorage.setItem('alb_history', JSON.stringify(h.slice(0, 48)));
        }
        // Active effect
        const path = window.location.pathname;
        if(path === '/') document.getElementById('h-home').classList.add('active');
        if(path === '/favorites') document.getElementById('h-fav').classList.add('active');
        if(path === '/history') document.getElementById('h-hist').classList.add('active');
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fforyou&page={page}", headers=HEADERS).json()
    items = res.get('data', {}).get('contentInfos', [])
    
    html = '<div class="grid-4">'
    for i in items:
        html += f'''
        <a href="/drama/{i['shortPlayId']}" class="drama-card">
            <img src="{i['shortPlayCover']}" loading="lazy">
            <div class="card-overlay">
                <div class="text-[7px] font-bold truncate opacity-80">{i['shortPlayName']}</div>
            </div>
        </a>'''
    html += '</div>'
    
    # NEXT PREV NAVIGATION
    html += f'''
    <div class="flex justify-center items-center gap-6 p-10">
        {f'<a href="/?page={page-1}" class="btn-nav-page">PREV</a>' if page > 1 else ''}
        <span class="text-xs font-bold text-gray-600">PAGE {page}</span>
        <a href="/?page={page+1}" class="btn-nav-page">NEXT</a>
    </div>'''
    return render_template_string(BASE_LAYOUT, content=html)

@app.route('/drama/<id>')
def detail(id):
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fallepisode&shortPlayId={id}", headers=HEADERS).json()
    data = res.get('data', {})
    
    # GAMBAR DITENGAH SESUAI INSTRUKSI
    html = f'''
    <div class="p-8 text-center">
        <div class="flex justify-center mb-6">
            <img src="{data['shortPlayCover']}" class="w-56 rounded-3xl shadow-[0_20px_50px_rgba(225,29,72,0.3)] border border-white/10">
        </div>
        <h1 class="text-lg font-extrabold mb-2 leading-tight uppercase tracking-tight">{data['shortPlayName']}</h1>
        <p class="text-[10px] text-gray-500 mb-8">{data.get('totalEpisode')} EPISODES TOTAL</p>
        
        <button onclick="alert('Disimpan ke Favorit!')" class="w-full bg-rose-600 py-3 rounded-2xl text-[10px] font-black tracking-widest mb-12 shadow-lg">❤️ TAMBAH FAVORIT</button>
        
        <div class="grid grid-cols-5 gap-3 text-left">
    '''
    for e in data.get('shortPlayEpisodeInfos', []):
        html += f'<a href="/watch/{id}/{e["episodeNo"]}" class="bg-white/5 border border-white/5 py-4 text-center rounded-xl text-xs font-bold active:bg-rose-600 transition-all">{e["episodeNo"]}</a>'
    html += '</div></div>'
    return render_template_string(BASE_LAYOUT, content=html)

@app.route('/watch/<id>/<int:no>')
def watch(id, no):
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fallepisode&shortPlayId={id}", headers=HEADERS).json()
    data = res.get('data', {})
    eps = data.get('shortPlayEpisodeInfos', [])
    curr = next((e for e in eps if e['episodeNo'] == no), None)
    if not curr: return "Error", 404
    
    html = f'''
    <div class="player-container active">
        <video id="vid" src="{curr['playVoucher']}" controls autoplay playsinline webkit-playsinline></video>
        
        <div style="position:absolute; bottom:50px; right:20px; z-index:10001; display:flex; flex-direction:column; gap:25px;">
            {f'<a id="nx" href="/watch/{id}/{no+1}" style="background:#e11d48; width:60px; height:60px; border-radius:50%; display:flex; align-items:center; justify-content:center; text-decoration:none; color:white; font-size:28px; box-shadow:0 0 30px rgba(225,29,72,0.5);">▶</a>' if no < data.get('totalEpisode', 0) else ''}
            <a href="/drama/{id}" style="background:rgba(255,255,255,0.1); backdrop-filter:blur(10px); width:60px; height:60px; border-radius:50%; display:flex; align-items:center; justify-content:center; text-decoration:none; color:white; font-size:20px; border:1px solid rgba(255,255,255,0.2);">✕</a>
        </div>
        <div style="position:absolute; top:40px; left:20px; background:rgba(0,0,0,0.6); padding:6px 15px; border-radius:10px; font-size:12px; font-weight:800; border:1px solid rgba(255,255,255,0.1);">EPS {no}</div>
    </div>
    <script>
        saveHist('{id}', `{data['shortPlayName']}`, '{data['shortPlayCover']}');
        const v = document.getElementById('vid');
        
        // AUTO FULLSCREEN SAAT PLAY
        v.addEventListener('play', () => {{
            if (v.requestFullscreen) v.requestFullscreen();
            else if (v.webkitEnterFullscreen) v.webkitEnterFullscreen();
        }});

        // AUTO NEXT
        v.addEventListener('ended', () => {{
            const n = document.getElementById('nx');
            if(n) window.location.href = n.href;
            else if(document.exitFullscreen) document.exitFullscreen();
        }});
    </script>
    '''
    return render_template_string(BASE_LAYOUT, content=html)

@app.route('/history')
def history():
    return render_template_string(BASE_LAYOUT, content='<div class="p-6"><h1 class="text-xs font-black tracking-widest text-rose-600 mb-8 uppercase">Riwayat Nonton</h1><div id="h-list" class="grid-4 !p-0"></div></div><script>let h=JSON.parse(localStorage.getItem("alb_history")||"[]");let c=document.getElementById("h-list");if(h.length==0)c.innerHTML="<p class=\'col-span-4 py-20 text-center opacity-20 text-xs\'>KOSONG</p>";h.forEach(i=>{c.innerHTML+=`<a href="/drama/${i.id}" class="drama-card"><img src="${i.img}"><div class="card-overlay"><div class="text-[7px] font-bold truncate">${i.name}</div></div></a>`});</script>')

@app.route('/favorites')
def favorites():
    return render_template_string(BASE_LAYOUT, content='<div class="p-6"><h1 class="text-xs font-black tracking-widest text-rose-600 mb-8 uppercase">Favorit Saya</h1><div id="f-list" class="grid-4 !p-0"></div></div><script>let f=JSON.parse(localStorage.getItem("alb_fav")||"[]");let c=document.getElementById("f-list");if(f.length==0)c.innerHTML="<p class=\'col-span-4 py-20 text-center opacity-20 text-xs\'>KOSONG</p>";f.forEach(i=>{c.innerHTML+=`<a href="/drama/${i.id}" class="drama-card"><img src="${i.img}"><div class="card-overlay"><div class="text-[7px] font-bold truncate">${i.name}</div></div></a>`});</script>')

@app.route('/search')
def search():
    q = request.args.get('q', '')
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fsearch&query={q}", headers=HEADERS).json()
    items = res.get('data', {}).get('searchCodeSearchResult', [])
    html = f'<div class="p-6 text-[10px] italic opacity-40 uppercase tracking-widest">Hasil Pencarian: {q}</div><div class="grid-4 !pt-0">'
    for i in items:
        html += f'<a href="/drama/{i["shortPlayId"]}" class="drama-card"><img src="{i["shortPlayCover"]}"><div class="card-overlay"><div class="text-[7px] font-bold truncate">{i["shortPlayName"]}</div></div></a>'
    html += '</div>'
    return render_template_string(BASE_LAYOUT, content=html)
