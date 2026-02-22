from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)

# URL API NETSHORT
BASE_URL = "https://hrdyckorclwpeyorzpry.supabase.co/functions/v1/api-proxy"

BASE_LAYOUT = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ALBEDONEXT-SHORT</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        body { background-color: #0b0e14; color: #e2e8f0; font-family: sans-serif; }
        .glass { background: rgba(15, 23, 42, 0.9); backdrop-filter: blur(10px); }
    </style>
</head>
<body>
    <nav class="glass sticky top-0 p-4 border-b border-white/10 flex justify-between items-center z-50">
        <a href="/" class="text-xl font-bold italic text-white">ALBEDO<span class="text-rose-500">NEXT</span></a>
    </nav>
    <main class="p-4 md:p-8">{{ content | safe }}</main>
</body>
</html>
"""

@app.route('/')
def home():
    page = request.args.get('page', 1)
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fforyou&page={page}").json()
    items = res.get('data', {}).get('contentInfos', [])
    
    html = '<div class="grid grid-cols-2 md:grid-cols-5 gap-6">'
    for i in items:
        html += f'''
        <a href="/drama/{i['shortPlayId']}" class="block group">
            <img src="{i['shortPlayCover']}" class="rounded-xl w-full aspect-[3/4] object-cover border border-white/5">
            <p class="text-sm font-bold mt-2 truncate text-white">{i['shortPlayName']}</p>
        </a>'''
    html += '</div>'
    return render_template_string(BASE_LAYOUT, content=html)

@app.route('/drama/<id>')
def detail(id):
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fallepisode&shortPlayId={id}").json()
    data = res.get('data', {})
    eps = data.get('shortPlayEpisodeInfos', [])
    
    html = f'<h1 class="text-2xl font-bold mb-4">{data.get("shortPlayName")}</h1>'
    html += '<div class="grid grid-cols-5 md:grid-cols-10 gap-2">'
    for e in eps:
        html += f'<a href="/watch/{id}/{e["episodeNo"]}" class="bg-white/10 p-2 text-center rounded hover:bg-rose-600">{e["episodeNo"]}</a>'
    html += '</div>'
    return render_template_string(BASE_LAYOUT, content=html)

@app.route('/watch/<id>/<int:no>')
def watch(id, no):
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fallepisode&shortPlayId={id}").json()
    data = res.get('data', {})
    curr = next((e for e in data.get('shortPlayEpisodeInfos', []) if e['episodeNo'] == no), None)
    
    html = f'''
    <div class="max-w-md mx-auto">
        <video controls autoplay class="w-full aspect-[9/16] bg-black rounded-2xl border border-white/10">
            <source src="{curr['playVoucher']}" type="video/mp4">
        </video>
        <div class="flex justify-between mt-4">
            <a href="/watch/{id}/{no-1}" class="px-4 py-2 bg-white/5 rounded">Prev</a>
            <span class="font-bold">Eps {no}</span>
            <a href="/watch/{id}/{no+1}" class="px-4 py-2 bg-rose-600 rounded">Next</a>
        </div>
    </div>'''
    return render_template_string(BASE_LAYOUT, content=html)

# Penting untuk Vercel
def handler(event, context):
    return app(event, context)
