from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# Referral Code: 2025-12-17 (Hardcoded as requested)
REFERRAL_CODE = "ALBEDO-777"

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
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap" rel="stylesheet">
    <link href="https://vjs.zencdn.net/8.10.0/video-js.css" rel="stylesheet" />
    <style>
        :root { --accent: #e11d48; }
        body { background-color: #050505; color: #fff; font-family: 'Plus Jakarta Sans', sans-serif; padding-bottom: 90px; margin: 0; }
        .glass-nav { background: rgba(5,5,5,0.8); backdrop-filter: blur(20px); border-bottom: 1px solid rgba(255,255,255,0.05); }
        .bottom-nav { position: fixed; bottom: 0; left: 0; right: 0; height: 75px; background: rgba(10,10,10,0.9); backdrop-filter: blur(25px); display: flex; justify-content: space-around; align-items: center; border-top: 1px solid rgba(255,255,255,0.08); z-index: 100; padding-bottom: env(safe-area-inset-bottom); }
        .nav-item { display: flex; flex-direction: column; align-items: center; font-size: 10px; color: #555; font-weight: 600; text-decoration: none; transition: 0.3s; }
        .nav-item.active { color: var(--accent); }
        .nav-item svg { width: 24px; height: 24px; margin-bottom: 4px; }
        .drama-card { position: relative; border-radius: 12px; overflow: hidden; background: #111; border: 1px solid rgba(255,255,255,0.05); transition: 0.3s; }
        .drama-card img { width: 100%; aspect-ratio: 3/4; object-fit: cover; }
        .drama-card:active { transform: scale(0.96); filter: brightness(1.2); }
        .btn-play-float { background: var(--accent); box-shadow: 0 0 25px rgba(225,29,72,0.6); }
        
        /* Fullscreen Video Fix */
        #video-box { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: #000; z-index: 9999; display: none; }
        #video-box.active { display: block; }
        .video-js { width: 100% !important; height: 100% !important; }
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar { width: 0px; }
    </style>
</head>
<body>
    <nav class="glass-nav sticky top-0 p-4 z-50 flex items-center justify-between">
        <h1 class="text-sm font-extrabold tracking-tighter italic text-white">ALBEDO<span class="text-rose-600 underline">NEXT</span></h1>
        <form action="/search" method="GET" class="flex items-center bg-white/5 rounded-full px-4 py-1.5 border border-white/10 ml-4 flex-1">
            <input type="text" name="q" placeholder="Cari..." class="bg-transparent border-none outline-none text-[11px] w-full text-white">
            <button type="submit" class="opacity-50">🔍</button>
        </form>
    </nav>

    <main>{{ content | safe }}</main>

    <div class="bottom-nav">
        <a href="/" class="nav-item">
            <svg fill="currentColor" viewBox="0 0 24 24"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>Home
        </a>
        <a href="/favorites" class="nav-item">
            <svg fill="currentColor" viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>Favorit
        </a>
        <a href="/history" class="nav-item">
            <svg fill="currentColor" viewBox="0 0 24 24"><path d="M13 3a9 9 0 0 0-9 9H1l3.89 3.89.07.14L9 12H6a7 7 0 1 1 7 7 7.07 7.07 0 0 1-6-3.15L5.45 17.4A9 9 0 1 0 13 3z"/></svg>Riwayat
        </a>
    </div>

    <script src="https://vjs.zencdn.net/8.10.0/video.min.js"></script>
    <script>
        function saveToHistory(id, name, img) {
            let h = JSON.parse(localStorage.getItem('albedo_h') || '[]');
            h = h.filter(x => x.id !== id);
            h.unshift({id, name, img, t: Date.now()});
            localStorage.setItem('albedo_h', JSON.stringify(h.slice(0, 40)));
        }

        function toggleFav(id, name, img) {
            let f = JSON.parse(localStorage.getItem('albedo_f') || '[]');
            let i = f.findIndex(x => x.id === id);
            if(i > -1) { f.splice(i, 1); alert("Dihapus"); }
            else { f.push({id, name, img}); alert("Ditambah ke Favorit"); }
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
    html = '<div class="p-4"><div class="grid grid-cols-4 gap-2.5">'
    for i in items:
        html += f'''
        <a href="/drama/{i['shortPlayId']}" class="drama-card">
            <img src="{i['shortPlayCover']}">
            <div class="absolute bottom-0 left-0 right-0 p-1 bg-gradient-to-t from-black text-[8px] font-bold truncate opacity-80">{i['shortPlayName']}</div>
        </a>'''
    html += f'</div><a href="/?page={page+1}" class="block text-center bg-white/5 border border-white/10 p-3 mt-8 rounded-xl text-[10px] font-bold tracking-widest uppercase">Muat Lebih Banyak</a></div>'
    return render_template_string(BASE_LAYOUT, content=html)

@app.route('/drama/<id>')
def detail(id):
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fallepisode&shortPlayId={id}", headers=HEADERS).json()
    data = res.get('data', {})
    html = f'''
    <div class="p-5">
        <div class="flex gap-5 items-center mb-8">
            <img src="{data['shortPlayCover']}" class="w-28 rounded-2xl shadow-2xl border border-white/10">
            <div class="flex-1">
                <h1 class="text-base font-bold mb-3 leading-tight">{data['shortPlayName']}</h1>
                <div class="flex gap-2">
                    <button onclick="toggleFav('{id}','{data['shortPlayName']}','{data['shortPlayCover']}')" class="text-[10px] bg-white/5 border border-white/10 px-4 py-2 rounded-lg">❤️ Simpan</button>
                </div>
            </div>
        </div>
        <h3 class="text-[10px] font-bold text-rose-500 mb-4 uppercase tracking-widest">Daftar Episode</h3>
        <div class="grid grid-cols-5 gap-2">
    '''
    for e in data.get('shortPlayEpisodeInfos', []):
        html += f'<a href="/watch/{id}/{e["episodeNo"]}" class="bg-white/5 py-4 text-center rounded-xl text-xs font-bold border border-white/5 active:bg-rose-600">{e["episodeNo"]}</a>'
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
    <div id="video-box" style="position:fixed; top:0; left:0; width:100vw; height:100vh; background:#000; z-index:10000; overflow:hidden;">
        <video id="vid" class="video-js vjs-theme-city" preload="auto" playsinline style="width:100%; height:100%; object-fit: cover;">
            <source src="{curr['playVoucher']}" type="video/mp4">
            <track label="Indo" kind="subtitles" src="{sub}" default>
        </video>
        
        <div id="video-ui" style="position:absolute; bottom:40px; right:20px; z-index:10001; display:flex; flex-direction:column; gap:20px; align-items:center;">
            {f'<a id="nx" href="/watch/{id}/{no+1}" class="btn-play-float" style="width:55px; height:55px; border-radius:50%; display:flex; align-items:center; justify-content:center; text-decoration:none; color:white; font-size:20px;">▶</a>' if no < data.get('totalEpisode', 0) else ''}
            <a href="/drama/{id}" style="background:rgba(255,255,255,0.1); width:55px; height:55px; border-radius:50%; display:flex; align-items:center; justify-content:center; backdrop-filter:blur(15px); text-decoration:none; color:white; font-size:20px;">☰</a>
        </div>
        
        <div id="eps-info" style="position:absolute; top:40px; left:20px; z-index:10001; background:rgba(0,0,0,0.4); padding:6px 15px; border-radius:10px; font-size:11px; font-weight:800; border: 1px solid rgba(255,255,255,0.1); letter-spacing:1px;">EPS {no} / {data['totalEpisode']}</div>
    </div>

    <script>
        saveToHistory('{id}', `{data['shortPlayName']}`, '{data['shortPlayCover']}');
        
        const player = videojs('vid', {{
            autoplay: true,
            controls: true,
            fluid: false,
            userActions: {{ doubleClick: true }}
        }});

        function requestFull() {{
            const el = document.getElementById('video-box');
            if (el.requestFullscreen) el.requestFullscreen();
            else if (el.webkitRequestFullscreen) el.webkitRequestFullscreen();
            else if (el.webkitEnterFullscreen) el.webkitEnterFullscreen(); // iOS fix
        }}

        // Langsung Fullscreen saat metadata dimuat (lebih cepat)
        player.on('loadedmetadata', requestFull);
        player.on('play', requestFull);

        player.on('ended', () => {{
            const n = document.getElementById('nx');
            if(n) window.location.href = n.href;
            else if(document.exitFullscreen) document.exitFullscreen();
        }});
        
        // Sembunyikan UI saat video di play agar tidak mengganggu
        player.on('userinactive', () => {{
            document.getElementById('video-ui').style.opacity = '0';
            document.getElementById('eps-info').style.opacity = '0';
        }});
        player.on('useractive', () => {{
            document.getElementById('video-ui').style.opacity = '1';
            document.getElementById('eps-info').style.opacity = '1';
        }});
    </script>
    '''
    return render_template_string(BASE_LAYOUT, content=html)

@app.route('/history')
def history():
    return render_template_string(BASE_LAYOUT, content='<div class="p-4"><h1 class="text-xs font-bold text-rose-500 uppercase mb-6 tracking-widest">Riwayat Menonton</h1><div id="hl" class="grid grid-cols-4 gap-2.5"></div></div><script>let h=JSON.parse(localStorage.getItem("albedo_h")||"[]");let c=document.getElementById("hl");if(h.length==0)c.innerHTML="<p class=\'col-span-4 py-20 text-center opacity-20 text-xs\'>Kosong</p>";h.forEach(i=>{c.innerHTML+=`<a href="/drama/${i.id}" class="drama-card"><img src="${i.img}"><div class="absolute bottom-0 p-1 text-[7px] font-bold truncate w-full bg-black/60">${i.name}</div></a>`});</script>')

@app.route('/favorites')
def favorites():
    return render_template_string(BASE_LAYOUT, content='<div class="p-4"><h1 class="text-xs font-bold text-rose-500 uppercase mb-6 tracking-widest">Koleksi Favorit</h1><div id="fl" class="grid grid-cols-4 gap-2.5"></div></div><script>let f=JSON.parse(localStorage.getItem("albedo_f")||"[]");let c=document.getElementById("fl");if(f.length==0)c.innerHTML="<p class=\'col-span-4 py-20 text-center opacity-20 text-xs\'>Kosong</p>";f.forEach(i=>{c.innerHTML+=`<a href="/drama/${i.id}" class="drama-card"><img src="${i.img}"><div class="absolute bottom-0 p-1 text-[7px] font-bold truncate w-full bg-black/60">${i.name}</div></a>`});</script>')

@app.route('/search')
def search():
    q = request.args.get('q', '')
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fsearch&query={q}", headers=HEADERS).json()
    items = res.get('data', {}).get('searchCodeSearchResult', [])
    html = f'<div class="p-4"><h2 class="text-[10px] uppercase opacity-40 mb-5 italic tracking-widest">Hasil Pencarian: {q}</h2><div class="grid grid-cols-4 gap-2.5">'
    for i in items:
        html += f'<a href="/drama/{i["shortPlayId"]}" class="drama-card"><img src="{i["shortPlayCover"]}"><div class="absolute bottom-0 p-1 text-[7px] font-bold truncate w-full bg-black/60">{i["shortPlayName"]}</div></a>'
    html += '</div></div>'
    return render_template_string(BASE_LAYOUT, content=html)
