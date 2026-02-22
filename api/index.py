from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# Referral Code: 2025-12-17
REFERRAL_CODE = "ALBEDO-777"

BASE_URL = "https://hrdyckorclwpeyorzpry.supabase.co/functions/v1/api-proxy"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Accept": "application/json"
}

BASE_LAYOUT = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
    <title>ALBEDONEXT-SHORT</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;700;800&display=swap" rel="stylesheet">
    <link href="https://vjs.zencdn.net/8.10.0/video-js.css" rel="stylesheet" />
    <style>
        :root { --accent: #ff004c; --bg: #030303; }
        body { background: var(--bg); color: #fff; font-family: 'Plus Jakarta Sans', sans-serif; margin: 0; -webkit-font-smoothing: antialiased; }
        
        /* Glass Navigation */
        .glass-header { background: rgba(3,3,3,0.7); backdrop-filter: blur(20px); border-bottom: 1px solid rgba(255,255,255,0.05); }
        .bottom-nav { position: fixed; bottom: 0; left: 0; right: 0; height: 75px; background: rgba(10,10,10,0.85); backdrop-filter: blur(20px); border-top: 1px solid rgba(255,255,255,0.08); z-index: 1000; padding-bottom: env(safe-area-inset-bottom); display: flex; justify-content: space-around; align-items: center; }
        
        /* Modern Cards */
        .drama-grid { display: grid; grid-template-cols: repeat(4, 1fr); gap: 10px; padding: 15px; }
        .drama-card { position: relative; border-radius: 12px; overflow: hidden; background: #111; border: 1px solid rgba(255,255,255,0.05); transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
        .drama-card:active { transform: scale(0.94); filter: brightness(1.2); }
        .drama-card img { width: 100%; aspect-ratio: 3/4; object-fit: cover; }
        .card-overlay { position: absolute; bottom: 0; left: 0; right: 0; padding: 20px 6px 6px; background: linear-gradient(to top, rgba(0,0,0,0.9), transparent); }
        
        /* Player Immersive */
        #player-wrapper { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: #000; z-index: 99999; }
        .video-js { width: 100% !important; height: 100% !important; }
        .vjs-big-play-button { background-color: var(--accent) !important; border: none !important; width: 60px !important; height: 60px !important; line-height: 60px !important; border-radius: 50% !important; left: 50% !important; top: 50% !important; transform: translate(-50%, -50%) !important; }
        
        /* Nav Item Styles */
        .nav-link { display: flex; flex-direction: column; align-items: center; text-decoration: none; color: #666; font-size: 10px; font-weight: 700; transition: 0.3s; }
        .nav-link.active { color: var(--accent); }
        .nav-link svg { width: 22px; height: 22px; margin-bottom: 4px; }
        
        input::placeholder { color: #444; }
    </style>
</head>
<body class="pb-24">
    <nav class="glass-header sticky top-0 z-[100] px-4 py-3 flex items-center justify-between">
        <a href="/" class="text-lg font-extrabold tracking-tighter text-white">ALBEDO<span class="text-[#ff004c]">NEXT</span></a>
        <form action="/search" method="GET" class="flex-1 max-w-[200px] ml-4">
            <div class="relative">
                <input type="text" name="q" placeholder="Cari drama..." class="w-full bg-white/5 border border-white/10 rounded-full py-1.5 px-4 text-[11px] outline-none focus:border-[#ff004c]/50 transition-all">
            </div>
        </form>
    </nav>

    <main id="app-content">
        {{ content | safe }}
    </main>

    <div class="bottom-nav">
        <a href="/" class="nav-link active" id="nav-home">
            <svg fill="currentColor" viewBox="0 0 24 24"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>Home
        </a>
        <a href="/favorites" class="nav-link" id="nav-fav">
            <svg fill="currentColor" viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>Favorit
        </a>
        <a href="/history" class="nav-link" id="nav-hist">
            <svg fill="currentColor" viewBox="0 0 24 24"><path d="M13 3a9 9 0 0 0-9 9H1l3.89 3.89.07.14L9 12H6a7 7 0 1 1 7 7 7.07 7.07 0 0 1-6-3.15L5.45 17.4A9 9 0 1 0 13 3z"/></svg>Riwayat
        </a>
    </div>

    <script src="https://vjs.zencdn.net/8.10.0/video.min.js"></script>
    <script>
        function saveHistory(id, name, img) {
            let h = JSON.parse(localStorage.getItem('albedo_hist') || '[]');
            h = h.filter(x => x.id !== id);
            h.unshift({id, name, img});
            localStorage.setItem('albedo_hist', JSON.stringify(h.slice(0, 48)));
        }

        function toggleFav(id, name, img) {
            let f = JSON.parse(localStorage.getItem('albedo_fav') || '[]');
            let i = f.findIndex(x => x.id === id);
            if(i > -1) { f.splice(i, 1); alert("Dihapus dari Favorit"); }
            else { f.push({id, name, img}); alert("Ditambah ke Favorit"); }
            localStorage.setItem('albedo_fav', JSON.stringify(f));
        }

        // Active Nav Highlighter
        const path = window.location.pathname;
        document.querySelectorAll('.nav-link').forEach(el => el.classList.remove('active'));
        if(path === '/') document.getElementById('nav-home').classList.add('active');
        if(path === '/favorites') document.getElementById('nav-fav').classList.add('active');
        if(path === '/history') document.getElementById('nav-hist').classList.add('active');
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fforyou&page={page}", headers=HEADERS).json()
    items = res.get('data', {}).get('contentInfos', [])
    html = '<div class="drama-grid">'
    for i in items:
        html += f'''
        <a href="/drama/{i['shortPlayId']}" class="drama-card">
            <img src="{i['shortPlayCover']}" loading="lazy">
            <div class="card-overlay">
                <div class="text-[8px] font-bold truncate opacity-90">{i['shortPlayName']}</div>
            </div>
        </a>'''
    html += '</div>'
    html += f'<div class="px-4 pb-10"><a href="/?page={page+1}" class="block text-center py-4 bg-white/5 rounded-2xl text-[10px] font-bold tracking-[0.2em] border border-white/5 active:scale-95 transition-all">MUAT LEBIH BANYAK</a></div>'
    return render_template_string(BASE_LAYOUT, content=html)

@app.route('/drama/<id>')
def detail(id):
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fallepisode&shortPlayId={id}", headers=HEADERS).json()
    data = res.get('data', {})
    html = f'''
    <div class="p-6">
        <div class="flex gap-5 items-center mb-10">
            <div class="w-32 flex-shrink-0">
                <img src="{data['shortPlayCover']}" class="w-full rounded-2xl shadow-2xl border border-white/10">
            </div>
            <div class="flex-1">
                <h1 class="text-lg font-bold leading-tight mb-4">{data['shortPlayName']}</h1>
                <button onclick="toggleFav('{id}',`{data['shortPlayName']}`,'{data['shortPlayCover']}')" class="bg-[#ff004c] text-white px-5 py-2 rounded-full text-[10px] font-bold shadow-lg shadow-[#ff004c]/30">❤️ SIMPAN KE FAVORIT</button>
            </div>
        </div>
        <div class="mb-4 flex items-center justify-between">
            <h3 class="text-[10px] font-black tracking-widest opacity-40 uppercase">Pilih Episode</h3>
            <span class="text-[9px] bg-white/10 px-2 py-0.5 rounded text-gray-400">{data.get('totalEpisode')} Episode</span>
        </div>
        <div class="grid grid-cols-5 gap-2.5">
    '''
    for e in data.get('shortPlayEpisodeInfos', []):
        html += f'<a href="/watch/{id}/{e["episodeNo"]}" class="bg-white/5 border border-white/10 py-4 text-center rounded-xl text-xs font-bold active:bg-[#ff004c] active:border-[#ff004c] transition-all">{e["episodeNo"]}</a>'
    html += '</div></div>'
    return render_template_string(BASE_LAYOUT, content=html)

@app.route('/watch/<id>/<int:no>')
def watch(id, no):
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fallepisode&shortPlayId={id}", headers=HEADERS).json()
    data = res.get('data', {})
    eps = data.get('shortPlayEpisodeInfos', [])
    curr = next((e for e in eps if e['episodeNo'] == no), None)
    if not curr: return "404", 404
    
    html = f'''
    <div id="player-wrapper">
        <video id="vjs-player" class="video-js vjs-big-play-centered" playsinline>
            <source src="{curr['playVoucher']}" type="video/mp4">
        </video>
        
        <div id="ui-layer" style="position:absolute; inset:0; pointer-events:none; z-index:10;">
            <div style="position:absolute; top:40px; left:20px; pointer-events:auto;">
                <a href="/drama/{id}" style="text-decoration:none; color:white; font-size:18px; background:rgba(0,0,0,0.4); width:40px; height:40px; display:flex; align-items:center; justify-content:center; border-radius:50%; backdrop-filter:blur(10px);">✕</a>
            </div>
            <div style="position:absolute; top:45px; left:50%; transform:translateX(-50%); text-align:center;">
                <div style="font-size:10px; font-weight:800; opacity:0.6; letter-spacing:2px; text-transform:uppercase;">EPISODE {no}</div>
            </div>
            <div style="position:absolute; bottom:50px; right:20px; display:flex; flex-direction:column; gap:20px; pointer-events:auto;">
                {f'<a id="btn-next" href="/watch/{id}/{no+1}" style="background:#ff004c; width:55px; height:55px; border-radius:50%; display:flex; align-items:center; justify-content:center; box-shadow:0 0 30px rgba(255,0,76,0.5); text-decoration:none; color:white; font-size:24px;">▶</a>' if no < data.get('totalEpisode', 0) else ''}
            </div>
        </div>
    </div>
    <script>
        saveHistory('{id}', `{data['shortPlayName']}`, '{data['shortPlayCover']}');
        
        const player = videojs('vjs-player', {{
            autoplay: true,
            controls: true,
            muted: false,
            userActions: {{ doubleClick: true }}
        }});

        function launchFullscreen() {{
            const el = document.getElementById('player-wrapper');
            if (el.requestFullscreen) el.requestFullscreen();
            else if (el.webkitRequestFullscreen) el.webkitRequestFullscreen();
            else if (el.webkitEnterFullscreen) el.webkitEnterFullscreen();
        }}

        player.on('play', launchFullscreen);
        
        player.on('ended', () => {{
            const nextLink = document.getElementById('btn-next');
            if(nextLink) window.location.href = nextLink.href;
            else if(document.exitFullscreen) document.exitFullscreen();
        }});

        // Auto play handler
        player.ready(() => {{
            let playPromise = player.play();
            if (playPromise !== undefined) {{
                playPromise.catch(() => {{
                    console.log("Menunggu interaksi user...");
                }});
            }}
        }});
    </script>
    '''
    return render_template_string(BASE_LAYOUT, content=html)

@app.route('/history')
def history():
    return render_template_string(BASE_LAYOUT, content='<div class="p-6"><div class="flex items-center justify-between mb-8"><h1 class="text-xs font-black tracking-[0.3em] text-white opacity-40 uppercase">Riwayat Nonton</h1><button onclick="localStorage.removeItem(\'albedo_hist\');location.reload();" class="text-[8px] border border-white/20 px-2 py-1 rounded opacity-40">HAPUS SEMUA</button></div><div id="hist-list" class="drama-grid !p-0"></div></div><script>let h=JSON.parse(localStorage.getItem("albedo_hist")||"[]");let c=document.getElementById("hist-list");if(h.length==0)c.innerHTML="<div class=\'col-span-4 py-20 text-center text-[10px] opacity-20\'>KOSONG</div>";h.forEach(i=>{c.innerHTML+=`<a href="/drama/${i.id}" class="drama-card"><img src="${i.img}"><div class="card-overlay"><div class="text-[8px] font-bold truncate opacity-90">${i.name}</div></div></a>`});</script>')

@app.route('/favorites')
def favorites():
    return render_template_string(BASE_LAYOUT, content='<div class="p-6"><h1 class="text-xs font-black tracking-[0.3em] text-white opacity-40 uppercase mb-8">Daftar Favorit</h1><div id="fav-list" class="drama-grid !p-0"></div></div><script>let f=JSON.parse(localStorage.getItem("albedo_fav")||"[]");let c=document.getElementById("fav-list");if(f.length==0)c.innerHTML="<div class=\'col-span-4 py-20 text-center text-[10px] opacity-20\'>KOSONG</div>";f.forEach(i=>{c.innerHTML+=`<a href="/drama/${i.id}" class="drama-card"><img src="${i.img}"><div class="card-overlay"><div class="text-[8px] font-bold truncate opacity-90">${i.name}</div></div></a>`});</script>')

@app.route('/search')
def search():
    q = request.args.get('q', '')
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fsearch&query={q}", headers=HEADERS).json()
    items = res.get('data', {}).get('searchCodeSearchResult', [])
    html = f'<div class="p-6"><h2 class="text-[10px] uppercase opacity-30 mb-8 tracking-widest italic font-bold">Hasil: {q}</h2><div class="drama-grid !p-0">'
    for i in items:
        html += f'<a href="/drama/{i["shortPlayId"]}" class="drama-card"><img src="{i["shortPlayCover"]}"><div class="card-overlay"><div class="text-[8px] font-bold truncate opacity-90">{i["shortPlayName"]}</div></div></a>'
    html += '</div></div>'
    return render_template_string(BASE_LAYOUT, content=html)
