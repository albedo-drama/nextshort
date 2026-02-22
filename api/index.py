from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# API Proxy Target
BASE_URL = "https://hrdyckorclwpeyorzpry.supabase.co/functions/v1/api-proxy"

# Header Browser Terkini
HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Accept": "application/json"
}

# --- UI LAYOUT PREMIUM ---
BASE_LAYOUT = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>ALBEDONEXT</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
    <style>
        body { background-color: #05070a; color: #afb3b8; font-family: 'Plus Jakarta Sans', sans-serif; -webkit-tap-highlight-color: transparent; }
        .nav-glass { background: rgba(5, 7, 10, 0.8); backdrop-filter: blur(20px); border-bottom: 1px solid rgba(255,255,255,0.05); }
        .drama-card img { transition: transform 0.5s ease; border-radius: 12px; }
        .drama-card:hover img { transform: scale(1.03); }
        .btn-rose { background: #e11d48; color: white; transition: all 0.3s ease; border-radius: 8px; font-weight: 600; }
        .btn-rose:hover { background: #be123c; transform: translateY(-1px); }
        .video-container { width: 100%; max-width: 400px; margin: auto; aspect-ratio: 9/16; background: #000; border-radius: 16px; overflow: hidden; box-shadow: 0 20px 50px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1); }
        input::placeholder { color: #4b5563; }
        .episode-grid a { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.05); transition: 0.2s; }
        .episode-grid a:hover { background: #e11d48; border-color: #e11d48; color: white; }
    </style>
</head>
<body class="pb-10">
    <nav class="nav-glass sticky top-0 p-4 flex justify-between items-center z-50">
        <a href="/" class="text-lg font-bold tracking-tighter text-white">ALBEDO<span class="text-rose-600">NEXT</span></a>
        <form action="/search" method="GET" class="flex bg-white/5 rounded-lg px-3 py-1 border border-white/10">
            <input type="text" name="q" placeholder="Cari drama..." class="bg-transparent border-none outline-none text-xs w-28 md:w-56 text-white py-1">
            <button type="submit" class="text-xs">🔍</button>
        </form>
    </nav>

    <main class="max-w-5xl mx-auto p-4 md:p-6">
        {{ content | safe }}
    </main>

    <script>
        // ANTI-EXIT LOGIC
        (function() {
            window.history.pushState(null, null, window.location.pathname);
            window.addEventListener('popstate', function () {
                if (window.location.pathname.includes('/watch/')) {
                    if(confirm("Kembali ke daftar episode?")) {
                        window.location.href = document.getElementById('btn-back-link')?.href || "/";
                    } else {
                        window.history.pushState(null, null, window.location.pathname);
                    }
                } else if (window.location.pathname !== "/") {
                    window.location.href = "/";
                } else {
                    window.history.pushState(null, null, window.location.pathname);
                }
            });
        })();

        // AUTO-NEXT LOGIC
        document.addEventListener('DOMContentLoaded', () => {
            const player = document.getElementById('main-player');
            if (player) {
                player.onended = () => {
                    const next = document.getElementById('next-btn-link');
                    if (next) {
                        setTimeout(() => { window.location.href = next.href; }, 1000);
                    }
                };
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
    
    html = '<h2 class="text-sm font-bold tracking-widest text-slate-500 mb-6 uppercase">Rekomendasi Terkini</h2>'
    html += '<div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4 md:gap-6">'
    for i in items:
        html += f'''
        <a href="/drama/{i['shortPlayId']}" class="drama-card group block">
            <div class="overflow-hidden rounded-xl bg-white/5 border border-white/5">
                <img src="{i['shortPlayCover']}" class="w-full aspect-[3/4] object-cover">
            </div>
            <h3 class="text-xs font-semibold text-white mt-3 truncate group-hover:text-rose-500">{i['shortPlayName']}</h3>
            <p class="text-[10px] text-slate-600 mt-1 italic">{i.get('heatScoreShow', 'Trending')}</p>
        </a>'''
    html += '</div>'
    html += f'''
    <div class="mt-12 flex justify-center items-center gap-6">
        {"<a href='/?page="+str(page-1)+"' class='text-xs font-bold hover:text-white'>PREV</a>" if page > 1 else ""}
        <span class="text-[10px] bg-white/5 px-3 py-1 rounded border border-white/10 uppercase tracking-widest">Hal {page}</span>
        <a href="/?page={page+1}" class="btn-rose px-6 py-2 text-xs">NEXT PAGE</a>
    </div>'''
    return render_template_string(BASE_LAYOUT, content=html)

@app.route('/drama/<id>')
def detail(id):
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fallepisode&shortPlayId={id}", headers=HEADERS).json()
    data = res.get('data', {})
    
    html = f'''
    <div class="flex flex-col md:flex-row gap-6 md:gap-10 mb-10">
        <img src="{data.get('shortPlayCover')}" class="w-40 md:w-52 mx-auto md:mx-0 rounded-2xl shadow-2xl border border-white/10">
        <div class="flex-1 text-center md:text-left pt-2">
            <h1 class="text-xl md:text-2xl font-bold text-white mb-4 tracking-tight">{data.get('shortPlayName')}</h1>
            <p class="text-xs text-slate-500 leading-relaxed max-w-2xl mx-auto md:mx-0">{data.get('shotIntroduce', '')}</p>
            <div class="mt-6 flex flex-wrap justify-center md:justify-start gap-2">
                {" ".join([f'<span class="text-[9px] border border-white/10 px-2 py-1 rounded text-slate-400 font-bold uppercase tracking-tighter">{l}</span>' for l in data.get('shortPlayLabels', [])])}
            </div>
        </div>
    </div>
    <div class="border-t border-white/5 pt-8">
        <h3 class="text-xs font-bold text-rose-500 mb-6 uppercase tracking-widest">Pilih Episode</h3>
        <div class="grid grid-cols-5 sm:grid-cols-8 md:grid-cols-12 gap-2 episode-grid">
    '''
    for e in data.get('shortPlayEpisodeInfos', []):
        html += f'<a href="/watch/{id}/{e["episodeNo"]}" class="aspect-square flex items-center justify-center rounded-lg text-xs font-bold">{e["episodeNo"]}</a>'
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

    html = f'''
    <div class="max-w-md mx-auto">
        <div class="video-container">
            <video id="main-player" controls autoplay playsinline>
                <source src="{curr['playVoucher']}" type="video/mp4">
                <track label="Indonesia" kind="subtitles" src="{sub}" default>
            </video>
        </div>
        <div class="mt-8 bg-white/5 p-4 rounded-xl border border-white/10 flex justify-between items-center">
            <a id="btn-back-link" href="/drama/{id}" class="text-[10px] font-bold text-slate-500 hover:text-white uppercase">Daftar Episode</a>
            <div class="flex items-center gap-3">
                {f'<a href="/watch/{id}/{no-1}" class="text-xs font-bold px-3 py-1 border border-white/10 rounded">PREV</a>' if no > 1 else ''}
                <span class="text-xs font-bold text-white px-2 italic">Eps {no}</span>
                {f'<a id="next-btn-link" href="/watch/{id}/{no+1}" class="btn-rose px-5 py-1 text-xs uppercase">Next</a>' if no < data.get('totalEpisode', 0) else ''}
            </div>
        </div>
        <p class="text-center text-[9px] text-slate-600 mt-6 uppercase tracking-[0.2em]">Auto-Next Episode Active</p>
    </div>
    '''
    return render_template_string(BASE_LAYOUT, content=html)

@app.route('/search')
def search():
    q = request.args.get('q', '')
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fsearch&query={q}", headers=HEADERS).json()
    items = res.get('data', {}).get('searchCodeSearchResult', [])
    
    html = f'<h2 class="text-xs font-bold text-slate-500 mb-8 uppercase tracking-widest">Hasil Pencarian: <span class="text-white italic">"{q}"</span></h2>'
    html += '<div class="grid grid-cols-2 md:grid-cols-5 gap-6">'
    for i in items:
        html += f'''
        <a href="/drama/{i['shortPlayId']}" class="drama-card block">
            <img src="{i['shortPlayCover']}" class="w-full aspect-[3/4] object-cover rounded-xl border border-white/5 shadow-lg">
            <h3 class="text-xs font-bold text-white mt-3 truncate">{i['shortPlayName']}</h3>
        </a>'''
    html += '</div>'
    return render_template_string(BASE_LAYOUT, content=html)
