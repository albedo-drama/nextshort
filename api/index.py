from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

BASE_URL = "https://hrdyckorclwpeyorzpry.supabase.co/functions/v1/api-proxy"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
}

# --- UI LAYOUT DENGAN VIDEO.JS & BOTTOM NAV ---
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
        body { background-color: #000; color: #fff; font-family: 'Plus Jakarta Sans', sans-serif; }
        .vjs-theme-city .vjs-big-play-button { border: none; background-color: #e11d48; }
        .video-container { width: 100vw; height: calc(100vh - 70px); position: relative; background: #000; }
        .bottom-nav { position: fixed; bottom: 0; left: 0; right: 0; height: 70px; background: rgba(10,10,10,0.95); backdrop-filter: blur(10px); display: flex; justify-content: space-around; items-center: center; border-top: 1px solid rgba(255,255,255,0.1); z-index: 100; }
        .nav-item { display: flex; flex-direction: column; align-items: center; font-size: 10px; color: #666; font-weight: 600; }
        .nav-item.active { color: #e11d48; }
        .nav-item svg { width: 24px; height: 24px; margin-bottom: 4px; }
        /* Make Video Full */
        .video-js { width: 100% !important; height: 100% !important; }
        .drama-card { border-radius: 12px; overflow: hidden; background: #111; border: 1px solid #222; }
    </style>
</head>
<body class="pb-[80px]">

    <main id="main-content">
        {{ content | safe }}
    </main>

    <div class="bottom-nav">
        <a href="/" class="nav-item active">
            <svg fill="currentColor" viewBox="0 0 24 24"><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"/></svg>
            Home
        </a>
        <button onclick="window.history.back()" class="nav-item">
            <svg fill="currentColor" viewBox="0 0 24 24"><path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z"/></svg>
            Back
        </button>
        <a href="/favorites" class="nav-item">
            <svg fill="currentColor" viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>
            Favorite
        </a>
        <a href="/history" class="nav-item">
            <svg fill="currentColor" viewBox="0 0 24 24"><path d="M13 3a9 9 0 0 0-9 9H1l3.89 3.89.07.14L9 12H6a7 7 0 1 1 7 7 7.07 7.07 0 0 1-6-3.15L5.45 17.4A9 9 0 1 0 13 3z"/></svg>
            History
        </a>
    </div>

    <script src="https://vjs.zencdn.net/8.10.0/video.min.js"></script>
    <script>
        // HISTORY & FAVORITE LOGIC
        function saveHistory(id, name, img) {
            let history = JSON.parse(localStorage.getItem('albedo_history') || '[]');
            history = history.filter(item => item.id !== id);
            history.unshift({id, name, img, time: new Date().getTime()});
            localStorage.setItem('albedo_history', JSON.stringify(history.slice(0, 20)));
        }

        function toggleFavorite(id, name, img) {
            let favs = JSON.parse(localStorage.getItem('albedo_favs') || '[]');
            const index = favs.findIndex(item => item.id === id);
            if(index > -1) {
                favs.splice(index, 1);
                alert("Dihapus dari Favorit");
            } else {
                favs.push({id, name, img});
                alert("Ditambah ke Favorit");
            }
            localStorage.setItem('albedo_favs', JSON.stringify(favs));
        }

        // AUTO-NEXT & PLAYER INITIALIZATION
        document.addEventListener('DOMContentLoaded', () => {
            const videoEl = document.querySelector('.video-js');
            if (videoEl) {
                const player = videojs(videoEl, {
                    fluid: false,
                    autoplay: true,
                    playbackRates: [0.5, 1, 1.5, 2]
                });
                
                player.on('ended', () => {
                    const nextBtn = document.getElementById('next-btn');
                    if(nextBtn) window.location.href = nextBtn.href;
                });
            }
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    page = request.args.get('page', 1, type=int)
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fforyou&page={page}", headers=HEADERS).json()
    items = res.get('data', {}).get('contentInfos', [])
    
    html = '<div class="p-4"><h1 class="text-xl font-bold mb-4 text-rose-500 italic">ALBEDONEXT</h1>'
    html += '<div class="grid grid-cols-2 md:grid-cols-5 gap-3">'
    for i in items:
        html += f'''
        <a href="/drama/{i['shortPlayId']}" class="drama-card block">
            <img src="{i['shortPlayCover']}" class="w-full aspect-[3/4] object-cover">
            <div class="p-2 truncate text-[11px] font-bold">{i['shortPlayName']}</div>
        </a>'''
    html += f'</div><a href="/?page={page+1}" class="block text-center bg-rose-600 p-3 mt-6 rounded-xl font-bold text-sm">LIHAT LAGI</a></div>'
    return render_template_string(BASE_LAYOUT, content=html)

@app.route('/drama/<id>')
def detail(id):
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fallepisode&shortPlayId={id}", headers=HEADERS).json()
    data = res.get('data', {})
    
    html = f'''
    <div class="p-4">
        <div class="flex gap-4 mb-6">
            <img src="{data['shortPlayCover']}" class="w-32 rounded-lg shadow-lg">
            <div>
                <h1 class="text-lg font-bold">{data['shortPlayName']}</h1>
                <button onclick="toggleFavorite('{id}', '{data['shortPlayName']}', '{data['shortPlayCover']}')" class="mt-2 text-xs bg-white/10 px-3 py-1 rounded-full border border-white/20">❤️ Tambah Favorit</button>
            </div>
        </div>
        <div class="grid grid-cols-5 gap-2">
    '''
    for e in data.get('shortPlayEpisodeInfos', []):
        html += f'<a href="/watch/{id}/{e["episodeNo"]}" class="bg-white/5 py-3 text-center rounded-lg text-sm border border-white/5">{e["episodeNo"]}</a>'
    html += '</div></div>'
    return render_template_string(BASE_LAYOUT, content=html)

@app.route('/watch/<id>/<int:no>')
def watch(id, no):
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fallepisode&shortPlayId={id}", headers=HEADERS).json()
    data = res.get('data', {})
    eps = data.get('shortPlayEpisodeInfos', [])
    curr = next((e for e in eps if e['episodeNo'] == no), None)
    
    if not curr: return "Not Found", 404
    sub = curr['subtitleList'][0]['url'] if curr.get('subtitleList') else ""

    # Pemicu simpan history di client-side
    save_script = f"<script>saveHistory('{id}', '{data['shortPlayName']}', '{data['shortPlayCover']}')</script>"
    
    html = f'''
    <div class="video-container">
        <video id="my-video" class="video-js vjs-theme-city vjs-big-play-centered" controls preload="auto" playsinline>
            <source src="{curr['playVoucher']}" type="video/mp4">
            <track label="Indonesia" kind="subtitles" src="{sub}" default>
        </video>
        <div class="absolute bottom-10 right-4 flex flex-col gap-4 z-50">
            {f'<a id="next-btn" href="/watch/{id}/{no+1}" class="bg-rose-600 p-4 rounded-full shadow-lg">▶</a>' if no < data.get('totalEpisode', 0) else ''}
            <a href="/drama/{id}" class="bg-white/20 p-4 rounded-full backdrop-blur-md">☰</a>
        </div>
        <div class="absolute top-4 left-4 z-50 bg-black/40 px-3 py-1 rounded text-[10px] font-bold">EPS {no} / {data['totalEpisode']}</div>
    </div>
    {save_script}
    '''
    return render_template_string(BASE_LAYOUT, content=html)

@app.route('/history')
def history():
    return render_template_string(BASE_LAYOUT, content='''
    <div class="p-4">
        <h1 class="text-xl font-bold mb-6 text-rose-500 italic">RIWAYAT NONTON</h1>
        <div id="history-list" class="grid grid-cols-2 gap-3"></div>
    </div>
    <script>
        const hist = JSON.parse(localStorage.getItem('albedo_history') || '[]');
        const container = document.getElementById('history-list');
        if(hist.length === 0) container.innerHTML = '<p class="text-xs text-gray-500 col-span-2">Belum ada riwayat.</p>';
        hist.forEach(item => {
            container.innerHTML += `
            <a href="/drama/${item.id}" class="drama-card block">
                <img src="${item.img}" class="w-full aspect-[3/4] object-cover">
                <div class="p-2 truncate text-[11px] font-bold">${item.name}</div>
            </a>`;
        });
    </script>
    ''')

@app.route('/favorites')
def favorites():
    return render_template_string(BASE_LAYOUT, content='''
    <div class="p-4">
        <h1 class="text-xl font-bold mb-6 text-rose-500 italic">FAVORIT SAYA</h1>
        <div id="fav-list" class="grid grid-cols-2 gap-3"></div>
    </div>
    <script>
        const favs = JSON.parse(localStorage.getItem('albedo_favs') || '[]');
        const container = document.getElementById('fav-list');
        if(favs.length === 0) container.innerHTML = '<p class="text-xs text-gray-500 col-span-2">Belum ada favorit.</p>';
        favs.forEach(item => {
            container.innerHTML += `
            <a href="/drama/${item.id}" class="drama-card block">
                <img src="${item.img}" class="w-full aspect-[3/4] object-cover">
                <div class="p-2 truncate text-[11px] font-bold">${item.name}</div>
            </a>`;
        });
    </script>
    ''')

@app.route('/search')
def search():
    q = request.args.get('q', '')
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fsearch&query={q}", headers=HEADERS).json()
    items = res.get('data', {}).get('searchCodeSearchResult', [])
    html = f'<div class="p-4"><h2 class="text-xs font-bold mb-4 uppercase">Hasil: {q}</h2><div class="grid grid-cols-2 gap-3">'
    for i in items:
        html += f'<a href="/drama/{i["shortPlayId"]}" class="drama-card block"><img src="{i["shortPlayCover"]}" class="w-full aspect-[3/4] object-cover"><div class="p-2 truncate text-[10px] font-bold">{i["shortPlayName"]}</div></a>'
    html += '</div></div>'
    return render_template_string(BASE_LAYOUT, content=html)
