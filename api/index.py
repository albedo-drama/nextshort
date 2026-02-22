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
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>ALBEDONEXT</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
    <link href="https://vjs.zencdn.net/8.10.0/video-js.css" rel="stylesheet" />
    <style>
        body { background-color: #000; color: #fff; font-family: 'Plus Jakarta Sans', sans-serif; padding-bottom: 80px; }
        .glass-nav { background: rgba(10,10,10,0.8); backdrop-filter: blur(15px); border-bottom: 1px solid rgba(255,255,255,0.05); }
        .bottom-nav { position: fixed; bottom: 0; left: 0; right: 0; height: 70px; background: rgba(10,10,10,0.95); backdrop-filter: blur(10px); display: flex; justify-content: space-around; align-items: center; border-top: 1px solid rgba(255,255,255,0.1); z-index: 100; }
        .nav-item { display: flex; flex-direction: column; align-items: center; font-size: 9px; color: #666; transition: 0.3s; text-decoration: none; }
        .nav-item.active { color: #e11d48; }
        .nav-item svg { width: 22px; height: 22px; margin-bottom: 4px; }
        .drama-card { border-radius: 8px; overflow: hidden; background: #111; border: 1px solid #1a1a1a; }
        .drama-card img { width: 100%; aspect-ratio: 3/4; object-fit: cover; }
    </style>
</head>
<body>
    <nav class="glass-nav sticky top-0 p-4 z-50">
        <form action="/search" method="GET" class="flex items-center bg-white/5 rounded-full px-4 py-2 border border-white/10">
            <input type="text" name="q" placeholder="Cari drama..." class="bg-transparent border-none outline-none text-xs w-full text-white" required>
            <button type="submit">🔍</button>
        </form>
    </nav>

    <main>{{ content | safe }}</main>

    <div class="bottom-nav">
        <a href="/" class="nav-item">
            <svg fill="currentColor" viewBox="0 0 24 24"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>Home
        </a>
        <a href="/favorites" class="nav-item">
            <svg fill="currentColor" viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>Favorite
        </a>
        <a href="/history" class="nav-item">
            <svg fill="currentColor" viewBox="0 0 24 24"><path d="M13 3a9 9 0 0 0-9 9H1l3.89 3.89.07.14L9 12H6a7 7 0 1 1 7 7 7.07 7.07 0 0 1-6-3.15L5.45 17.4A9 9 0 1 0 13 3z"/></svg>History
        </a>
    </div>

    <script src="https://vjs.zencdn.net/8.10.0/video.min.js"></script>
    <script>
        // GLOBAL FUNCTIONS
        function saveToHistory(id, name, img) {
            let h = JSON.parse(localStorage.getItem('albedo_h') || '[]');
            h = h.filter(x => x.id !== id);
            h.unshift({id, name, img, t: Date.now()});
            localStorage.setItem('albedo_h', JSON.stringify(h.slice(0, 40)));
            console.log("Saved to history:", name);
        }

        function toggleFav(id, name, img) {
            let f = JSON.parse(localStorage.getItem('albedo_f') || '[]');
            let i = f.findIndex(x => x.id === id);
            if(i > -1) { f.splice(i, 1); alert("Dihapus dari Favorite"); }
            else { f.push({id, name, img}); alert("Disimpan ke Favorite"); }
            localStorage.setItem('albedo_f', JSON.stringify(f));
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
    html = '<div class="p-3"><div class="grid grid-cols-4 gap-2">'
    for i in items:
        html += f'<a href="/drama/{i["shortPlayId"]}" class="drama-card"><img src="{i["shortPlayCover"]}"><div class="p-1 truncate text-[9px] opacity-70 font-bold">{i["shortPlayName"]}</div></a>'
    html += f'</div><a href="/?page={page+1}" class="block text-center bg-rose-600 p-3 mt-6 rounded-lg text-xs font-bold">MUAT LAGI</a></div>'
    return render_template_string(BASE_LAYOUT, content=html)

@app.route('/drama/<id>')
def detail(id):
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fallepisode&shortPlayId={id}", headers=HEADERS).json()
    data = res.get('data', {})
    html = f'''
    <div class="p-4">
        <div class="flex gap-4 items-center mb-6">
            <img src="{data["shortPlayCover"]}" class="w-24 rounded shadow-xl">
            <div class="flex-1">
                <h1 class="text-sm font-bold mb-2">{data["shortPlayName"]}</h1>
                <button onclick="toggleFav('{id}','{data["shortPlayName"]}','{data["shortPlayCover"]}')" class="text-[10px] bg-white/10 px-4 py-2 rounded-full border border-white/10">❤️ Favorite</button>
            </div>
        </div>
        <div class="grid grid-cols-5 gap-2">
    '''
    for e in data.get('shortPlayEpisodeInfos', []):
        html += f'<a href="/watch/{id}/{e["episodeNo"]}" class="bg-white/5 py-4 text-center rounded text-xs border border-white/5">{e["episodeNo"]}</a>'
    html += '</div></div>'
    return render_template_string(BASE_LAYOUT, content=html)

@app.route('/watch/<id>/<int:no>')
def watch(id, no):
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fallepisode&shortPlayId={id}", headers=HEADERS).json()
    data = res.get('data', {})
    eps = data.get('shortPlayEpisodeInfos', [])
    curr = next((e for e in eps if e['episodeNo'] == no), None)
    if not curr: return "404", 404
    sub = curr['subtitleList'][0]['url'] if curr.get('subtitleList') else ""
    
    html = f'''
    <div id="video-box" style="position:fixed; top:0; left:0; width:100vw; height:100vh; background:#000; z-index:1000;">
        <video id="vid" class="video-js vjs-theme-city" controls preload="auto" playsinline style="width:100%; height:100%;">
            <source src="{curr['playVoucher']}" type="video/mp4">
            <track label="Indo" kind="subtitles" src="{sub}" default>
        </video>
        <div style="position:absolute; bottom:30px; right:20px; z-index:1001; display:flex; flex-direction:column; gap:15px;">
            {f'<a id="nx" href="/watch/{id}/{no+1}" style="background:#e11d48; width:50px; height:50px; border-radius:50%; display:flex; align-items:center; justify-content:center; box-shadow:0 0 20px rgba(225,29,72,0.5);">▶</a>' if no < data.get('totalEpisode', 0) else ''}
            <a href="/drama/{id}" style="background:rgba(255,255,255,0.1); width:50px; height:50px; border-radius:50%; display:flex; align-items:center; justify-content:center; backdrop-filter:blur(10px);">☰</a>
        </div>
        <div style="position:absolute; top:20px; left:20px; z-index:1001; background:rgba(0,0,0,0.5); padding:5px 12px; border-radius:5px; font-size:10px; font-weight:bold; border: 1px solid rgba(255,255,255,0.1);">EPS {no} / {data['totalEpisode']}</div>
    </div>
    <script>
        // Eksekusi Simpan History Langsung
        saveToHistory('{id}', `{data['shortPlayName']}`, '{data['shortPlayCover']}');

        const p = videojs('vid', {{ autoplay: true }});
        
        function goFull() {{
            const el = document.getElementById('video-box');
            if (el.requestFullscreen) el.requestFullscreen();
            else if (el.webkitRequestFullscreen) el.webkitRequestFullscreen();
        }}

        p.on('play', goFull);
        p.on('ended', () => {{
            const n = document.getElementById('nx');
            if(n) window.location.href = n.href;
        }});
    </script>
    '''
    return render_template_string(BASE_LAYOUT, content=html)

@app.route('/history')
def history():
    return render_template_string(BASE_LAYOUT, content='''
    <div class="p-3">
        <div class="flex justify-between items-center mb-4">
            <h1 class="text-xs font-bold text-rose-500 uppercase italic">Riwayat Nonton</h1>
            <button onclick="localStorage.removeItem('albedo_h'); location.reload();" class="text-[8px] opacity-50 border border-white/20 px-2 py-1 rounded">Hapus Semua</button>
        </div>
        <div id="hl" class="grid grid-cols-4 gap-2"></div>
    </div>
    <script>
        let h = JSON.parse(localStorage.getItem("albedo_h") || "[]");
        let c = document.getElementById("hl");
        if(h.length === 0) {{
            c.innerHTML = '<div class="col-span-4 py-20 text-center opacity-30 text-[10px]">Belum ada riwayat</div>';
        }} else {{
            h.forEach(i => {{
                c.innerHTML += `<a href="/drama/${i.id}" class="drama-card"><img src="${i.img}"><div class="p-1 truncate text-[8px] font-bold">${i.name}</div></a>`;
            }});
        }}
    </script>
    ''')

@app.route('/favorites')
def favorites():
    return render_template_string(BASE_LAYOUT, content='''
    <div class="p-3">
        <h1 class="text-xs font-bold mb-4 text-rose-500 uppercase italic">Favorit Saya</h1>
        <div id="fl" class="grid grid-cols-4 gap-2"></div>
    </div>
    <script>
        let f = JSON.parse(localStorage.getItem("albedo_f") || "[]");
        let c = document.getElementById("fl");
        if(f.length === 0) {{
            c.innerHTML = '<div class="col-span-4 py-20 text-center opacity-30 text-[10px]">Belum ada favorit</div>';
        }} else {{
            f.forEach(i => {{
                c.innerHTML += `<a href="/drama/${i.id}" class="drama-card"><img src="${i.img}"><div class="p-1 truncate text-[8px] font-bold">${i.name}</div></a>`;
            }});
        }}
    </script>
    ''')

@app.route('/search')
def search():
    q = request.args.get('q', '')
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fsearch&query={q}", headers=HEADERS).json()
    items = res.get('data', {}).get('searchCodeSearchResult', [])
    html = f'<div class="p-3"><h2 class="text-[10px] uppercase opacity-50 mb-4 italic">Search: {q}</h2><div class="grid grid-cols-4 gap-2">'
    for i in items:
        html += f'<a href="/drama/{i["shortPlayId"]}" class="drama-card"><img src="{i["shortPlayCover"]}"><div class="p-1 truncate text-[8px] font-bold">{i["shortPlayName"]}</div></a>'
    html += '</div></div>'
    return render_template_string(BASE_LAYOUT, content=html)
