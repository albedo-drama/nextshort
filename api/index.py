from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# Referral Code: 2025-12-17
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
    <style>
        body { background: #000; color: #fff; font-family: sans-serif; margin: 0; padding-bottom: 80px; }
        .bottom-nav { position: fixed; bottom: 0; left: 0; right: 0; height: 70px; background: rgba(15,15,15,0.95); display: flex; justify-content: space-around; align-items: center; border-top: 1px solid #222; z-index: 100; }
        .nav-item { display: flex; flex-direction: column; align-items: center; font-size: 10px; color: #777; text-decoration: none; }
        .nav-item.active { color: #ff004c; }
        .drama-card { border-radius: 8px; overflow: hidden; background: #111; position: relative; border: 1px solid #222; }
        .drama-card img { width: 100%; aspect-ratio: 3/4; object-fit: cover; }
        #video-full { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #000; z-index: 9999; }
        video { width: 100%; height: 100%; object-fit: contain; }
    </style>
</head>
<body>
    <nav class="p-4 flex items-center bg-black border-b border-white/5 sticky top-0 z-[50]">
        <h1 class="font-bold text-rose-600 mr-4">ALBEDONEXT-SHORT</h1>
        <form action="/search" class="flex-1"><input name="q" placeholder="Cari..." class="w-full bg-white/10 rounded-full px-4 py-1 text-xs outline-none"></form>
    </nav>
    <main>{{ content | safe }}</main>
    <div class="bottom-nav">
        <a href="/" class="nav-item">🏠<br>Home</a>
        <a href="/favorites" class="nav-item">❤️<br>Favorit</a>
        <a href="/history" class="nav-item">🕒<br>Riwayat</a>
    </div>
    <script>
        function saveH(id, name, img) {
            let h = JSON.parse(localStorage.getItem('albedo_h') || '[]');
            h = h.filter(x => x.id !== id);
            h.unshift({id, name, img});
            localStorage.setItem('albedo_h', JSON.stringify(h.slice(0, 40)));
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
    html = '<div class="p-2 grid grid-cols-4 gap-2">'
    for i in items:
        html += f'<a href="/drama/{i["shortPlayId"]}" class="drama-card"><img src="{i["shortPlayCover"]}"><div class="absolute bottom-0 p-1 text-[7px] bg-black/70 w-full truncate">{i["shortPlayName"]}</div></a>'
    html += f'</div><a href="/?page={page+1}" class="block text-center p-6 text-rose-500 font-bold">MUAT LAGI</a>'
    return render_template_string(BASE_LAYOUT, content=html)

@app.route('/drama/<id>')
def detail(id):
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fallepisode&shortPlayId={id}", headers=HEADERS).json()
    data = res.get('data', {})
    html = f'<div class="p-4"><div class="flex gap-4 mb-6"><img src="{data["shortPlayCover"]}" class="w-24 rounded shadow-lg"><h1 class="font-bold text-sm">{data["shortPlayName"]}</h1></div>'
    html += '<div class="grid grid-cols-5 gap-2">'
    for e in data.get('shortPlayEpisodeInfos', []):
        html += f'<a href="/watch/{id}/{e["episodeNo"]}" class="bg-white/10 py-4 text-center rounded text-xs">{e["episodeNo"]}</a>'
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
    <div id="video-full">
        <video id="main-video" controls autoplay playsinline>
            <source src="{curr['playVoucher']}" type="video/mp4">
        </video>
        <div style="position:absolute; bottom:40px; right:20px; z-index:100; display:flex; flex-direction:column; gap:15px;">
            {f'<a id="next-ep" href="/watch/{id}/{no+1}" style="background:#e11d48; width:50px; height:50px; border-radius:50%; display:flex; align-items:center; justify-content:center; text-decoration:none; color:white; font-weight:bold;">▶</a>' if no < data.get('totalEpisode', 0) else ''}
            <a href="/drama/{id}" style="background:rgba(255,255,255,0.2); width:50px; height:50px; border-radius:50%; display:flex; align-items:center; justify-content:center; text-decoration:none; color:white;">☰</a>
        </div>
        <div style="position:absolute; top:20px; left:20px; background:rgba(0,0,0,0.5); padding:4px 10px; border-radius:4px; font-size:10px;">EPS {no}</div>
    </div>
    <script>
        saveH('{id}', `{data['shortPlayName']}`, '{data['shortPlayCover']}');
        
        const v = document.getElementById('main-video');
        
        // AUTO FULLSCREEN SAAT KLIK/PLAY
        function openFull() {{
            if (v.requestFullscreen) v.requestFullscreen();
            else if (v.webkitEnterFullscreen) v.webkitEnterFullscreen();
            else if (v.webkitRequestFullscreen) v.webkitRequestFullscreen();
        }}

        v.addEventListener('play', openFull);
        
        // AUTO NEXT
        v.addEventListener('ended', () => {{
            const next = document.getElementById('next-ep');
            if(next) window.location.href = next.href;
        }});

        // Coba paksa fullscreen setelah video siap
        v.onloadedmetadata = () => {{
            v.play().catch(e => console.log("Autoplay blocked"));
        }};
    </script>
    '''
    return render_template_string(BASE_LAYOUT, content=html)

@app.route('/history')
def history():
    return render_template_string(BASE_LAYOUT, content='<div class="p-4"><h1 class="text-xs font-bold mb-4">RIWAYAT</h1><div id="hl" class="grid grid-cols-4 gap-2"></div></div><script>let h=JSON.parse(localStorage.getItem("albedo_h")||"[]");let c=document.getElementById("hl");h.forEach(i=>{c.innerHTML+=`<a href="/drama/${i.id}" class="drama-card"><img src="${i.img}"><div class="p-1 text-[7px] truncate">${i.name}</div></a>`});</script>')

@app.route('/favorites')
def favorites():
    return render_template_string(BASE_LAYOUT, content='<div class="p-4"><h1 class="text-xs font-bold mb-4">FAVORIT</h1><div id="fl" class="grid grid-cols-4 gap-2"></div></div><script>let f=JSON.parse(localStorage.getItem("albedo_f")||"[]");let c=document.getElementById("fl");f.forEach(i=>{c.innerHTML+=`<a href="/drama/${i.id}" class="drama-card"><img src="${i.img}"><div class="p-1 text-[7px] truncate">${i.name}</div></a>`});</script>')

@app.route('/search')
def search():
    q = request.args.get('q', '')
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fsearch&query={q}", headers=HEADERS).json()
    items = res.get('data', {}).get('searchCodeSearchResult', [])
    html = f'<div class="p-4"><h2 class="text-xs mb-4 italic">Hasil: {q}</h2><div class="grid grid-cols-4 gap-2">'
    for i in items:
        html += f'<a href="/drama/{i["shortPlayId"]}" class="drama-card"><img src="{i["shortPlayCover"]}"><div class="p-1 text-[7px] truncate">{i["shortPlayName"]}</div></a>'
    html += '</div></div>'
    return render_template_string(BASE_LAYOUT, content=html)
