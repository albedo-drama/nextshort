from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

BASE_URL = "https://hrdyckorclwpeyorzpry.supabase.co/functions/v1/api-proxy"

# Header User-Agent agar tidak diblokir server
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

BASE_LAYOUT = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>ALBEDONEXT-SHORT</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #0b0e14; color: #e2e8f0; font-family: sans-serif; }
        .glass { background: rgba(15, 23, 42, 0.9); backdrop-filter: blur(10px); }
        video { width: 100%; height: 100%; object-fit: contain; border-radius: 20px; }
    </style>
</head>
<body class="pb-20">
    <nav class="glass sticky top-0 p-4 border-b border-white/10 flex justify-between items-center z-50">
        <a href="/" class="text-xl font-black italic text-rose-500 underline">ALBEDONEXT</a>
        <form action="/search" method="GET" class="flex bg-white/5 rounded-full px-4 py-1 border border-white/10">
            <input type="text" name="q" placeholder="Cari drama..." class="bg-transparent border-none outline-none text-sm w-32 md:w-64 text-white">
            <button type="submit">🔍</button>
        </form>
    </nav>
    <main class="max-w-6xl mx-auto p-4 md:p-8">{{ content | safe }}</main>
</body>
</html>
"""

@app.route('/')
def home():
    page = request.args.get('page', 1)
    url = f"{BASE_URL}?path=%2Fnetshort%2Fforyou&page={page}"
    res = requests.get(url, headers=HEADERS).json()
    items = res.get('data', {}).get('contentInfos', [])
    
    html = '<h2 class="text-2xl font-bold mb-6 italic underline uppercase">Rekomendasi</h2>'
    html += '<div class="grid grid-cols-2 md:grid-cols-5 gap-6">'
    for i in items:
        html += f'''
        <a href="/drama/{i['shortPlayId']}" class="block bg-white/5 rounded-2xl overflow-hidden border border-white/5 shadow-xl">
            <img src="{i['shortPlayCover']}" class="w-full aspect-[3/4] object-cover">
            <div class="p-3"><p class="text-xs font-bold truncate">{i['shortPlayName']}</p></div>
        </a>'''
    html += '</div>'
    html += f'<div class="mt-12 flex justify-center"><a href="/?page={int(page)+1}" class="bg-rose-600 px-10 py-3 rounded-full font-bold">NEXT PAGE</a></div>'
    return render_template_string(BASE_LAYOUT, content=html)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    url = f"{BASE_URL}?path=%2Fnetshort%2Fsearch&query={query}"
    res = requests.get(url, headers=HEADERS).json()
    items = res.get('data', {}).get('searchCodeSearchResult', [])
    
    html = f'<h2 class="text-xl font-bold mb-6 italic">Hasil: "{query}"</h2>'
    html += '<div class="grid grid-cols-2 md:grid-cols-5 gap-6">'
    for i in items:
        html += f'''
        <a href="/drama/{i['shortPlayId']}" class="block bg-white/5 rounded-2xl overflow-hidden border border-white/5">
            <img src="{i['shortPlayCover']}" class="w-full aspect-[3/4] object-cover">
            <div class="p-3"><p class="text-xs font-bold truncate">{i['shortPlayName']}</p></div>
        </a>'''
    html += '</div>'
    return render_template_string(BASE_LAYOUT, content=html)

@app.route('/drama/<id>')
def detail(id):
    url = f"{BASE_URL}?path=%2Fnetshort%2Fallepisode&shortPlayId={id}"
    res = requests.get(url, headers=HEADERS).json()
    data = res.get('data', {})
    eps = data.get('shortPlayEpisodeInfos', [])
    
    html = f'''
    <div class="flex flex-col md:flex-row gap-8 mb-10 text-center md:text-left">
        <img src="{data.get('shortPlayCover')}" class="w-48 mx-auto md:mx-0 rounded-3xl shadow-2xl">
        <div class="flex-1">
            <h1 class="text-4xl font-black italic">{data.get('shortPlayName')}</h1>
            <p class="mt-4 text-slate-400">{data.get('shotIntroduce', '')}</p>
        </div>
    </div>
    <div class="grid grid-cols-4 md:grid-cols-10 gap-2">
    '''
    for e in eps:
        html += f'<a href="/watch/{id}/{e["episodeNo"]}" class="bg-white/10 p-3 text-center rounded-xl font-bold hover:bg-rose-600 transition">{e["episodeNo"]}</a>'
    html += '</div>'
    return render_template_string(BASE_LAYOUT, content=html)

@app.route('/watch/<id>/<int:no>')
def watch(id, no):
    url = f"{BASE_URL}?path=%2Fnetshort%2Fallepisode&shortPlayId={id}"
    res = requests.get(url, headers=HEADERS).json()
    data = res.get('data', {})
    eps = data.get('shortPlayEpisodeInfos', [])
    curr = next((e for e in eps if e['episodeNo'] == no), None)
    
    if not curr: return "Episode Not Found", 404
    
    sub = curr['subtitleList'][0]['url'] if curr.get('subtitleList') else ""

    html = f'''
    <div class="max-w-md mx-auto">
        <div class="aspect-[9/16] bg-black rounded-3xl overflow-hidden border border-white/10">
            <video controls autoplay playsinline>
                <source src="{curr['playVoucher']}" type="video/mp4">
                <track label="Indo" kind="subtitles" src="{sub}" default>
            </video>
        </div>
        <div class="mt-8 flex justify-between items-center bg-white/5 p-4 rounded-2xl">
            <a href="/watch/{id}/{no-1}" class="font-bold {'opacity-20 pointer-events-none' if no <= 1 else ''}">PREV</a>
            <h2 class="text-2xl font-black text-rose-500">EPS {no}</h2>
            <a href="/watch/{id}/{no+1}" class="bg-rose-600 px-6 py-2 rounded-xl font-bold {'hidden' if no >= data.get('totalEpisode', 100) else ''}">NEXT</a>
        </div>
        <a href="/drama/{id}" class="block text-center mt-6 text-slate-500 text-sm">Kembali ke Daftar Episode</a>
    </div>
    '''
    return render_template_string(BASE_LAYOUT, content=html)
