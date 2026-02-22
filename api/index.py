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
        .grid-4 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 6px; padding: 8px; }
        .card { position: relative; border-radius: 6px; overflow: hidden; background: #111; border: 1px solid #222; }
        .card img { width: 100%; aspect-ratio: 3/4; object-fit: cover; }
        .card-title { position: absolute; bottom: 0; width: 100%; background: rgba(0,0,0,0.8); font-size: 7px; padding: 3px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        
        /* Navigasi Bawah 3 Tombol */
        .status-bar { position: fixed; bottom: 0; left: 0; right: 0; height: 70px; background: #050505; border-top: 1px solid #222; display: flex; justify-content: space-around; align-items: center; z-index: 1000; padding-bottom: env(safe-area-inset-bottom); }
        .nav-item { text-align: center; font-size: 10px; color: #777; text-decoration: none; font-weight: bold; }
        
        /* Video Fullscreen Mode */
        #player-box { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: #000; z-index: 99999; display: none; }
        #player-box.active { display: block; }
        video { width: 100%; height: 100%; object-fit: contain; }
        
        /* Detail Page */
        .ep-grid { display: grid; grid-template-columns: repeat(7, 1fr); gap: 5px; } /* Episode Kecil */
        .ep-btn { background: #1a1a1a; padding: 8px 0; text-align: center; border-radius: 4px; font-size: 10px; font-weight: bold; border: 1px solid #333; }
        .ep-btn:active { background: #e11d48; }
    </style>
</head>
<body>
    <nav class="p-4 bg-black flex items-center justify-between sticky top-0 z-50 border-b border-white/10">
        <h1 class="text-xs font-black italic tracking-tighter text-rose-600">ALBEDONEXT-SHORT</h1>
        <form action="/search" class="flex-1 max-w-[140px] ml-4">
            <input name="q" placeholder="Cari..." class="w-full bg-white/10 rounded-full px-4 py-1.5 text-[10px] outline-none border border-white/5 focus:border-rose-600">
        </form>
    </nav>

    <main>{{ content | safe }}</main>

    <div class="status-bar">
        <a href="/" class="nav-item">🏠<br>HOME</a>
        <a href="javascript:history.back()" class="nav-item">⬅️<br>KEMBALI</a>
        <a href="/favorites" class="nav-item">❤️<br>FAVORIT</a>
    </div>

    <script>
        function saveF(id, name, img) {
            let f = JSON.parse(localStorage.getItem('al_fav') || '[]');
            if(!f.find(x => x.id === id)) {
                f.push({id, name, img});
                localStorage.setItem('al_fav', JSON.stringify(f));
                alert("Berhasil disimpan!");
            } else { alert("Sudah di favorit"); }
        }
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
        <a href="/drama/{i['shortPlayId']}" class="card">
            <img src="{i['shortPlayCover']}">
            <div class="card-title">{i['shortPlayName']}</div>
        </a>'''
    html += '</div>'
    html += f'''
    <div class="flex justify-center gap-10 p-10">
        {f'<a href="/?page={page-1}" class="text-xs font-bold text-gray-500">PREV</a>' if page > 1 else ''}
        <span class="text-xs font-bold text-rose-600">HAL {page}</span>
        <a href="/?page={page+1}" class="text-xs font-bold text-rose-500">NEXT</a>
    </div>'''
    return render_template_string(BASE_LAYOUT, content=html)

@app.route('/drama/<id>')
def detail(id):
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fallepisode&shortPlayId={id}", headers=HEADERS).json()
    data = res.get('data', {})
    html = f'''
    <div class="p-6 text-center">
        <img src="{data['shortPlayCover']}" class="w-48 mx-auto rounded-xl shadow-2xl mb-4">
        <h1 class="text-sm font-bold mb-6 uppercase">{data['shortPlayName']}</h1>
        <button onclick="saveF('{id}', `{data['shortPlayName']}`, '{data['shortPlayCover']}')" class="bg-white/10 px-6 py-2 rounded-full text-[10px] font-bold mb-10 border border-white/20">❤️ FAVORITKAN</button>
        
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
    if not curr: return "End of Episodes", 404
    
    html = f'''
    <div id="player-box" class="active">
        <video id="vid" src="{curr['playVoucher']}" controls autoplay playsinline webkit-playsinline></video>
        
        <div style="position:absolute; bottom:60px; right:20px; z-index:100000; display:flex; flex-direction:column; gap:20px;">
            {f'<a id="autoNext" href="/watch/{id}/{no+1}" style="background:#e11d48; width:50px; height:50px; border-radius:50%; display:flex; align-items:center; justify-content:center; text-decoration:none; color:white; font-weight:bold; font-size:20px;">▶</a>' if no < data.get('totalEpisode', 0) else ''}
            <a href="/drama/{id}" style="background:rgba(255,255,255,0.2); width:50px; height:50px; border-radius:50%; display:flex; align-items:center; justify-content:center; text-decoration:none; color:white; font-size:18px;">✕</a>
        </div>
        <div style="position:absolute; top:30px; left:20px; background:rgba(0,0,0,0.5); padding:4px 8px; border-radius:4px; font-size:10px; font-weight:bold;">EPS {no}</div>
    </div>
    <script>
        const v = document.getElementById('vid');
        
        // AUTO FULLSCREEN SAAT PLAY
        v.addEventListener('play', () => {{
            if (v.requestFullscreen) v.requestFullscreen();
            else if (v.webkitEnterFullscreen) v.webkitEnterFullscreen();
            else if (v.webkitRequestFullscreen) v.webkitRequestFullscreen();
        }});

        // LOGIKA AUTO NEXT EPISODE
        v.addEventListener('ended', () => {{
            const nxt = document.getElementById('autoNext');
            if(nxt) {{
                window.location.href = nxt.href;
            }} else {{
                if(document.exitFullscreen) document.exitFullscreen();
            }}
        }});
    </script>
    '''
    return render_template_string(BASE_LAYOUT, content=html)

@app.route('/favorites')
def favorites():
    return render_template_string(BASE_LAYOUT, content='<div class="p-4"><h1 class="text-xs font-bold text-rose-600 mb-6">FAVORIT SAYA</h1><div id="fl" class="grid-4 !p-0"></div></div><script>let f=JSON.parse(localStorage.getItem("al_fav")||"[]");let c=document.getElementById("fl");f.forEach(i=>{c.innerHTML+=`<a href="/drama/${i.id}" class="card"><img src="${i.img}"><div class="card-title">${i.name}</div></a>`});</script>')

@app.route('/search')
def search():
    q = request.args.get('q', '')
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fsearch&query={q}", headers=HEADERS).json()
    items = res.get('data', {}).get('searchCodeSearchResult', [])
    html = f'<div class="p-4 text-[10px] opacity-50">CARI: {q}</div><div class="grid-4">'
    for i in items:
        html += f'<a href="/drama/{i["shortPlayId"]}" class="card"><img src="{i["shortPlayCover"]}"><div class="card-title">{i["shortPlayName"]}</div></a>'
    html += '</div>'
    return render_template_string(BASE_LAYOUT, content=html)
