# REFERRAL CODE: 2025-12-17
REFERRAL_CODE = "ALBEDO-777"

from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

BASE_URL = "https://hrdyckorclwpeyorzpry.supabase.co/functions/v1/api-proxy"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
}

BASE_LAYOUT = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>ALBEDONEXT-SHORT</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background: #000; color: #fff; font-family: sans-serif; margin: 0; padding-bottom: 90px; }
        .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; padding: 10px; }
        .card { position: relative; border-radius: 6px; overflow: hidden; background: #111; border: 1px solid #222; }
        .card img { width: 100%; aspect-ratio: 3/4; object-fit: cover; }
        .card-title { position: absolute; bottom: 0; width: 100%; background: rgba(0,0,0,0.8); font-size: 7px; padding: 3px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        
        /* Navigasi Bawah 3 Tombol */
        .status-bar { position: fixed; bottom: 0; left: 0; right: 0; height: 70px; background: #050505; border-top: 1px solid #222; display: flex; justify-content: space-around; align-items: center; z-index: 1000; padding-bottom: env(safe-area-inset-bottom); }
        .nav-item { text-align: center; font-size: 10px; color: #777; text-decoration: none; font-weight: bold; }
        
        /* Video Player Absolute - Subtitle Aman */
        video { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #000; z-index: 9999; object-fit: contain; }
        .v-nav { position: fixed; bottom: 85px; right: 20px; z-index: 10000; display: flex; flex-direction: column; gap: 15px; }
        .btn-circle { background: #e11d48; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #fff; text-decoration: none; font-weight: bold; font-size: 20px; box-shadow: 0 4px 15px rgba(225,29,72,0.4); }

        /* Episode Grid Kecil */
        .ep-grid { display: grid; grid-template-columns: repeat(8, 1fr); gap: 4px; }
        .ep-btn { background: #1a1a1a; border: 1px solid #333; padding: 8px 0; text-align: center; border-radius: 4px; font-size: 9px; font-weight: bold; }
    </style>
</head>
<body>
    <nav class="p-4 bg-black flex items-center justify-between sticky top-0 z-50 border-b border-white/10">
        <h1 class="text-xs font-black italic text-rose-600">ALBEDONEXT-SHORT</h1>
        <form action="/search" class="flex-1 max-w-[140px] ml-4">
            <input name="q" placeholder="Cari..." class="w-full bg-white/10 rounded-full px-4 py-1.5 text-[10px] outline-none border border-white/5">
        </form>
    </nav>

    <main>{{ content | safe }}</main>

    <div class="status-bar">
        <a href="/" class="nav-item">🏠<br>HOME</a>
        <a href="javascript:history.back()" class="nav-item">⬅️<br>KEMBALI</a>
        <a href="/favorites" class="nav-item">❤️<br>FAVORIT</a>
    </div>
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
        html += f'<a href="/drama/{i["shortPlayId"]}" class="card"><img src="{i["shortPlayCover"]}"><div class="card-title">{i["shortPlayName"]}</div></a>'
    html += '</div>'
    html += f'<div class="flex justify-center gap-10 p-10"><a href="/?page={page-1}" class="text-xs font-bold text-gray-500">PREV</a><span class="text-xs font-bold text-rose-600">HAL {page}</span><a href="/?page={page+1}" class="text-xs font-bold text-rose-500">NEXT</a></div>'
    return render_template_string(BASE_LAYOUT, content=html)

@app.route('/drama/<id>')
def detail(id):
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fallepisode&shortPlayId={id}", headers=HEADERS).json()
    data = res.get('data', {})
    
    # CEK API: Views & Sinopsis
    views = data.get('playVolume', '0')
    sinopsis = data.get('shortPlayDescription', 'Sinopsis tidak tersedia untuk judul ini.')
    
    html = f'''
    <div class="p-6 text-center">
        <div class="flex justify-center mb-4">
            <img src="{data['shortPlayCover']}" class="w-48 rounded-2xl shadow-2xl border border-white/10">
        </div>
        
        <h1 class="text-sm font-black mb-1 uppercase tracking-tighter">{data['shortPlayName']}</h1>
        
        <div class="text-[9px] text-rose-500 font-bold mb-4 uppercase tracking-widest">👁️ {views} VIEWS</div>
        
        <div class="bg-white/5 border border-white/5 p-4 rounded-xl mb-6 text-left">
            <h2 class="text-[8px] font-black text-gray-500 uppercase mb-1">Sinopsis</h2>
            <p class="text-[10px] text-gray-300 leading-relaxed italic">{sinopsis}</p>
        </div>

        <button onclick="alert('Ditambahkan ke Favorit!')" class="w-full bg-rose-600 py-3 rounded-full text-[10px] font-black mb-8 shadow-lg">❤️ FAVORITKAN</button>
        
        <div class="ep-grid">
    '''
    for e in data.get('shortPlayEpisodeInfos', []):
        html += f'<a href="/watch/{id}/{e["episodeNo"]}" class="ep-btn">{e["episodeNo"]}</a>'
    html += '</div></div>'
    return render_template_string(BASE_LAYOUT, content=html)

@app.route('/watch/<id>/<int:no>')
def watch(id, no):
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fallepisode&shortPlayId={id}", headers=HEADERS).json()
    data = res.get('data', {})
    eps = data.get('shortPlayEpisodeInfos', [])
    curr = next((e for e in eps if e['episodeNo'] == no), None)
    if not curr: return "End", 404
    
    html = f'''
    <video id="v" src="{curr['playVoucher']}" controls autoplay playsinline webkit-playsinline></video>
    
    <div class="v-nav">
        {f'<a id="nxt" href="/watch/{id}/{no+1}" class="btn-circle">▶</a>' if no < data.get('totalEpisode', 0) else ''}
        <a href="/drama/{id}" class="btn-circle" style="background:rgba(255,255,255,0.1); font-size:16px;">✕</a>
    </div>

    <script>
        const v = document.getElementById('v');
        
        // AUTO FULLSCREEN & PLAY
        v.play();
        v.addEventListener('play', () => {{
            if (v.webkitEnterFullscreen) v.webkitEnterFullscreen();
            else if (v.requestFullscreen) v.requestFullscreen();
        }});

        // AUTO NEXT EPISODE (FIXED)
        v.addEventListener('ended', () => {{
            const nxt = document.getElementById('nxt');
            if(nxt) window.location.href = nxt.href;
        }});
    </script>
    '''
    return render_template_string(BASE_LAYOUT, content=html)

@app.route('/favorites')
def favorites():
    return render_template_string(BASE_LAYOUT, content='<div class="p-4 text-center text-xs opacity-50 py-20">Fitur Favorit memerlukan LocalStorage.</div>')

@app.route('/search')
def search():
    q = request.args.get('q', '')
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fsearch&query={q}", headers=HEADERS).json()
    items = res.get('data', {}).get('searchCodeSearchResult', [])
    html = f'<div class="p-4 text-[10px] opacity-40 uppercase">Hasil: {q}</div><div class="grid-4">'
    for i in items:
        html += f'<a href="/drama/{i["shortPlayId"]}" class="card"><img src="{i["shortPlayCover"]}"><div class="card-title">{i["shortPlayName"]}</div></a>'
    html += '</div>'
    return render_template_string(BASE_LAYOUT, content=html)
