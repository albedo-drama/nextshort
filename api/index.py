# ==========================================
# ALBEDONEXT-SHORT - PREMIUM STREAMING SCRIPT
# ==========================================
REFERRAL_CODE = "ALBEDONEXT-SHORT-2026" 

from flask import Flask, request, render_template_string
import requests

app = Flask(__name__)
BASE_URL = "https://hrdyckorclwpeyorzpry.supabase.co/functions/v1/api-proxy"

# --- UI LAYOUT DENGAN FITUR ANTI-CLOSE & AUTO-NEXT ---
BASE_LAYOUT = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>ALBEDONEXT-SHORT | Premium Short Drama</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'Plus Jakarta Sans', sans-serif; background-color: #0b0e14; color: #e2e8f0; overflow-x: hidden; }
        .glass { background: rgba(15, 23, 42, 0.8); backdrop-filter: blur(12px); border-bottom: 1px solid rgba(255,255,255,0.05); }
        .drama-card { transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); }
        .drama-card:hover { transform: translateY(-8px); border-color: #f43f5e; }
        .btn-rose { background: linear-gradient(135deg, #fb7185 0%, #e11d48 100%); transition: all 0.3s; }
        .btn-rose:hover { transform: scale(1.05); shadow: 0 10px 15px -3px rgba(225, 29, 72, 0.4); }
        .video-wrapper { position: relative; width: 100%; max-width: 450px; margin: auto; aspect-ratio: 9/16; background: #000; border-radius: 24px; overflow: hidden; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5); }
        video { width: 100%; h-height: 100%; object-fit: contain; }
    </style>
</head>
<body class="pb-10">
    <nav class="sticky top-0 z-50 glass px-6 py-4 flex items-center justify-between">
        <a href="/" class="flex items-center gap-2">
            <span class="text-2xl font-black tracking-tighter text-white uppercase italic">Albedo<span class="text-rose-500 underline">Next</span></span>
        </a>
        <form action="/search" method="GET" class="hidden md:flex items-center bg-white/5 rounded-full px-4 py-1.5 border border-white/10 focus-within:border-rose-500">
            <input type="text" name="q" placeholder="Cari drama CEO..." class="bg-transparent border-none outline-none text-sm w-64 text-white">
            <button type="submit">🔍</button>
        </form>
        <div class="px-3 py-1 rounded-full bg-rose-500/10 border border-rose-500/30 text-[10px] font-bold text-rose-500">
            REF: {{ ref }}
        </div>
    </nav>

    <main class="max-w-7xl mx-auto p-4 md:p-8">
        {% block content %}{% endblock %}
    </main>

    <div class="md:hidden fixed bottom-0 left-0 w-full glass p-3 flex justify-around border-t border-white/10 z-50">
        <a href="/" class="text-xs flex flex-col items-center gap-1 text-rose-500 font-bold"><span>🏠</span> Home</a>
        <button onclick="window.history.back()" class="text-xs flex flex-col items-center gap-1 text-slate-400"><span>⬅️</span> Kembali</button>
    </div>

    <script>
        // Mencegah User Langsung Keluar Website saat tekan Back
        (function() {
            window.history.pushState(null, null, window.location.pathname);
            window.addEventListener('popstate', function (event) {
                // Jika berada di halaman player, kembali ke halaman detail drama saja
                if (window.location.pathname.includes('/watch/')) {
                    window.history.pushState(null, null, window.location.pathname);
                    const backUrl = document.getElementById('btn-back-detail')?.href || "/";
                    if(confirm("Berhenti menonton dan kembali ke daftar episode?")) {
                        window.location.href = backUrl;
                    }
                } else if (window.location.pathname !== "/") {
                    window.location.href = "/";
                } else {
                    window.history.pushState(null, null, window.location.pathname);
                    alert("Gunakan menu navigasi untuk menjelajah ALBEDONEXT.");
                }
            });
        })();

        // Fitur Auto-Next Episode
        document.addEventListener('DOMContentLoaded', () => {
            const video = document.getElementById('player');
            if (video) {
                video.onended = function() {
                    const nextBtn = document.getElementById('next-episode-btn');
                    if (nextBtn) {
                        console.log("Episode selesai, memutar selanjutnya dalam 2 detik...");
                        setTimeout(() => { nextBtn.click(); }, 2000);
                    }
                };
            }
        });
    </script>
</body>
</html>
"""

# --- ROUTES ---

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fforyou&page={page}").json()
    items = res.get('data', {}).get('contentInfos', [])
    
    content = """
    <div class="flex items-center justify-between mb-8">
        <div>
            <h1 class="text-3xl font-black text-white">EXPLORE DRAMA</h1>
            <p class="text-slate-500 text-sm">Update harian drama pendek premium.</p>
        </div>
    </div>

    <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-4 md:gap-8">
        {% for item in items %}
        <a href="/drama/{{ item.shortPlayId }}" class="group drama-card border border-white/5 rounded-3xl p-2 bg-white/5">
            <div class="relative aspect-[3/4] rounded-2xl overflow-hidden shadow-2xl">
                <img src="{{ item.shortPlayCover }}" class="w-full h-full object-cover group-hover:scale-110 duration-700">
                <div class="absolute inset-0 bg-gradient-to-t from-black via-transparent"></div>
                <div class="absolute bottom-3 left-3">
                    <p class="text-[10px] font-bold text-rose-400 uppercase tracking-widest">{{ item.heatScoreShow }} 🔥</p>
                    <h3 class="text-sm font-bold text-white leading-tight truncate w-32 md:w-40">{{ item.shortPlayName }}</h3>
                </div>
            </div>
        </a>
        {% endfor %}
    </div>

    <div class="flex justify-center items-center gap-4 mt-12">
        {% if page > 1 %}
        <a href="/?page={{ page - 1 }}" class="px-6 py-3 rounded-full border border-white/10 font-bold text-sm hover:bg-white/5">← Prev</a>
        {% endif %}
        <span class="text-slate-500 font-bold">Halaman {{ page }}</span>
        <a href="/?page={{ page + 1 }}" class="btn-rose px-10 py-3 rounded-full font-bold text-sm shadow-xl">Next Page →</a>
    </div>
    """
    return render_template_string(BASE_LAYOUT, content=content, items=items, page=page, ref=REFERRAL_CODE)

@app.route('/drama/<play_id>')
def detail(play_id):
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fallepisode&shortPlayId={play_id}").json()
    info = res.get('data', {})
    
    content = """
    <div class="flex flex-col md:flex-row gap-10">
        <div class="w-full md:w-80 shrink-0">
            <img src="{{ info.shortPlayCover }}" class="w-full rounded-[40px] shadow-2xl border-4 border-white/5">
        </div>
        <div class="flex-1 py-4">
            <h1 class="text-5xl font-black text-white italic tracking-tighter">{{ info.shortPlayName }}</h1>
            <div class="flex flex-wrap gap-2 mt-6">
                {% for label in info.shortPlayLabels %}
                <span class="px-4 py-1 rounded-full bg-white/5 border border-white/10 text-[10px] font-bold text-slate-300">{{ label }}</span>
                {% endfor %}
            </div>
            <p class="mt-8 text-slate-400 text-lg leading-relaxed">{{ info.shotIntroduce }}</p>
        </div>
    </div>

    <div class="mt-16">
        <h2 class="text-2xl font-bold mb-8 flex items-center gap-3"><span class="w-2 h-8 bg-rose-500 rounded-full"></span> EPISODES</h2>
        <div class="grid grid-cols-4 sm:grid-cols-6 md:grid-cols-12 gap-3">
            {% for ep in info.shortPlayEpisodeInfos %}
            <a href="/watch/{{ info.shortPlayId }}/{{ ep.episodeNo }}" class="aspect-square flex items-center justify-center rounded-2xl bg-white/5 border border-white/5 font-black hover:bg-rose-500 hover:text-white transition-all text-sm shadow-lg">
                {{ ep.episodeNo }}
            </a>
            {% endfor %}
        </div>
    </div>
    """
    return render_template_string(BASE_LAYOUT, content=content, info=info, ref=REFERRAL_CODE)

@app.route('/watch/<play_id>/<int:ep_no>')
def watch(play_id, ep_no):
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fallepisode&shortPlayId={play_id}").json()
    info = res.get('data', {})
    episodes = info.get('shortPlayEpisodeInfos', [])
    curr = next((e for e in episodes if e['episodeNo'] == ep_no), None)
    
    if not curr: return "Episode not found", 404
    sub = curr['subtitleList'][0]['url'] if curr['subtitleList'] else ""

    content = f"""
    <div class="max-w-4xl mx-auto">
        <div class="video-wrapper">
            <video id="player" controls autoplay playsinline>
                <source src="{curr['playVoucher']}" type="video/mp4">
                <track label="Indonesia" kind="subtitles" srclang="id" src="{sub}" default>
            </video>
        </div>
        
        <div class="mt-10 flex flex-col md:flex-row items-center justify-between gap-6">
            <a id="btn-back-detail" href="/drama/{play_id}" class="text-slate-400 font-bold hover:text-white">← Daftar Episode</a>
            
            <div class="flex items-center gap-4">
                {'<a href="/watch/'+play_id+'/'+str(ep_no-1)+'" class="px-6 py-3 rounded-full bg-white/5 font-bold text-xs">PREV</a>' if ep_no > 1 else ''}
                <span class="text-xl font-black text-rose-500 tracking-widest px-4">EPS {ep_no}</span>
                {'<a id="next-episode-btn" href="/watch/'+play_id+'/'+str(ep_no+1)+'" class="btn-rose px-8 py-3 rounded-full font-bold text-xs">NEXT EPS</a>' if ep_no < info['totalEpisode'] else ''}
            </div>
            
            <p class="text-[10px] font-bold text-slate-600 uppercase">Auto-Next Active</p>
        </div>
    </div>
    """
    return render_template_string(BASE_LAYOUT, content=content, ref=REFERRAL_CODE)

@app.route('/search')
def search():
    q = request.args.get('q', '')
    res = requests.get(f"{BASE_URL}?path=%2Fnetshort%2Fsearch&query={q}").json()
    items = res.get('data', {}).get('searchCodeSearchResult', [])
    
    content = f"""
    <h2 class="text-2xl font-bold mb-10 italic">Pencarian: <span class="text-rose-500 underline uppercase italic">{q}</span></h2>
    <div class="grid grid-cols-2 md:grid-cols-5 gap-6">
        {"".join([f'<a href="/drama/{item["shortPlayId"]}" class="group bg-white/5 p-2 rounded-2xl border border-white/5"><div class="aspect-[3/4] overflow-hidden rounded-xl relative"><img src="{item["shortPlayCover"]}" class="w-full h-full object-cover transition-transform group-hover:scale-110"><div class="absolute bottom-2 left-2 right-2"><h3 class="text-xs font-bold text-white truncate drop-shadow-lg">{item["shortPlayName"]}</h3></div></div></a>' for item in items])}
    </div>
    """
    return render_template_string(BASE_LAYOUT, content=content, ref=REFERRAL_CODE)

if __name__ == "__main__":
    app.run(debug=True)
