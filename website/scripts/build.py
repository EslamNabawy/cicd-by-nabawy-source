#!/usr/bin/env python3
"""Build the static CI/CD library website.
Usage: python scripts/build.py
Reads: content/books.json, ../pdf/*.html, ../GLOSSARY.md
Writes: dist/index.html, dist/read/<id>.html, dist/glossary.html
Adding a book = one manifest entry + re-run. No other files change.
"""
import glob
import pathlib
import json, os, re, html, shutil
from html.parser import HTMLParser

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KB = os.path.dirname(ROOT)
PDF = os.path.join(KB, "pdf")
DIST = os.path.join(ROOT, "dist")
READ = os.path.join(DIST, "read")
SITE_URL = "https://eslamnabawy.github.io/cicd-by-nabawy"
SITE_DESC = "39 concise technical books: CI/CD fundamentals, pipelines, artifacts, delivery, Jenkins, GitHub Actions, security, reliability \u2014 plus hands-on labs. By Nabawy."

def seo_tags(title, desc, canonical, og_type="website", image=None):
    d = html.escape(desc, quote=True)
    t = html.escape(title, quote=True)
    c = html.escape(canonical, quote=True)
    parts = [
        f'<meta name="description" content="{d}">',
        f'<meta name="theme-color" content="#0B0D10">',
        f'<link rel="canonical" href="{c}">',
        f'<meta property="og:title" content="{t}">',
        f'<meta property="og:description" content="{d}">',
        f'<meta property="og:url" content="{c}">',
        f'<meta property="og:type" content="{og_type}">',
        f'<meta property="og:site_name" content="CICD BY Nabawy">',
        f'<meta name="twitter:card" content="summary">',
        f'<meta name="twitter:title" content="{t}">',
        f'<meta name="twitter:description" content="{d}">',
    ]
    if image:
        i = html.escape(image, quote=True)
        parts.append(f'<meta property="og:image" content="{i}">')
    return "\n".join(parts)


def og_svg(title, category, color):
    t = html.escape(title[:28])
    c = html.escape(category)
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630"><rect width="1200" height="630" fill="#0B0D10"/><rect width="1200" height="14" fill="{color}"/><circle cx="120" cy="120" r="34" fill="none" stroke="#18E299" stroke-width="8"/><text x="80" y="330" font-family="monospace" font-size="44" fill="#18E299">{c}</text><text x="80" y="430" font-family="sans-serif" font-weight="bold" font-size="84" fill="#ededed">{t}</text><text x="80" y="500" font-family="sans-serif" font-size="36" fill="#a0a0a0">CICD BY Nabawy</text></svg>'

BASE_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Geist+Mono:wght@400;500;600&display=swap');
:root{--bg:#0B0D10;--bg2:#12151a;--card:#12151a;--ink:#ededed;--mut:#a0a0a0;--line:rgba(255,255,255,.1);--line-soft:rgba(255,255,255,.07);--acc:#18E299;--acc-soft:rgba(24,226,153,.12);--brand:#18E299;--warn:#c37d0d;--red:#d45656;--shadow:rgba(0,0,0,.4) 0px 2px 4px;--shadow-btn:rgba(0,0,0,.4) 0px 1px 2px;--shadow-lift:rgba(0,0,0,.5) 0px 12px 28px -8px;--radius:12px;--mono:'Geist Mono',ui-monospace,SFMono-Regular,Menlo,monospace}
[data-theme=light]{--bg:#ffffff;--bg2:#fafafa;--card:#ffffff;--ink:#0d0d0d;--mut:#666666;--line:rgba(0,0,0,.07);--line-soft:rgba(0,0,0,.05);--acc:#0b9b68;--acc-soft:#d4fae8;--brand:#18E299;--warn:#c37d0d;--red:#d45656;--shadow:rgba(0,0,0,.03) 0px 2px 4px;--shadow-btn:rgba(0,0,0,.06) 0px 1px 2px;--shadow-lift:rgba(0,0,0,.1) 0px 12px 28px -8px;--radius:12px;--mono:'Geist Mono',ui-monospace,SFMono-Regular,Menlo,monospace}
/* category accents */
[data-cat="CI/CD"]{--cat:#5B8DEF}[data-cat="Build"]{--cat:#F5A524}[data-cat="Testing"]{--cat:#2ECC71}[data-cat="Security"]{--cat:#E5484D}[data-cat="Reliability"]{--cat:#9B7BF0}[data-cat="Jenkins"]{--cat:#22B8CF}[data-cat="Delivery"]{--cat:#F472B6}[data-cat="GitHub"]{--cat:#94A3B8}[data-cat="Platforms"]{--cat:#F97316}[data-cat="Labs"]{--cat:#EAB308}[data-cat="Reference"]{--cat:#64748B}[data-cat="Series"]{--cat:#18E299}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font-family:'Inter',system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;line-height:1.5;-webkit-font-smoothing:antialiased}
a{color:var(--ink);text-decoration:none}
a:hover{color:var(--acc)}
.wrap{max-width:1200px;margin:0 auto;padding:24px 32px}
header.top{position:sticky;top:0;background:var(--bg);backdrop-filter:blur(12px);-webkit-backdrop-filter:blur(12px);border-bottom:1px solid var(--line-soft);z-index:20}
header.top .wrap{display:flex;align-items:center;gap:16px;padding:12px 32px}
.logo{display:flex;align-items:center;gap:9px;font-weight:600;letter-spacing:-.01em;font-size:16px;white-space:nowrap}
.logo svg{flex:none}
.logo span{color:var(--ink)}
.search{flex:1;display:flex;max-width:480px;margin:0 auto}
.search input{flex:1;background:var(--bg);border:1px solid rgba(255,255,255,.12);color:var(--ink);border-radius:9999px;padding:8px 16px;font-size:14px;outline:none}
[data-theme=light] .search input{border-color:rgba(0,0,0,.08)}
.search input:focus{border-color:var(--brand);box-shadow:0 0 0 1px var(--brand)}
.search input::placeholder{color:#888}
.search kbd{font-family:var(--mono);font-size:11px;color:var(--mut);border:1px solid var(--line);border-radius:6px;padding:1px 7px;margin-left:-44px;align-self:center;pointer-events:none}
.btn{background:var(--bg);border:1px solid rgba(255,255,255,.14);color:var(--ink);border-radius:9999px;padding:6px 14px;font-size:14px;font-weight:500;cursor:pointer;white-space:nowrap}
[data-theme=light] .btn{border-color:rgba(0,0,0,.08)}
.btn:hover{opacity:.75}
:focus-visible{outline:2px solid var(--brand);outline-offset:2px}
.hero{padding:64px 24px 44px;text-align:center;position:relative;background:radial-gradient(ellipse 70% 60% at 50% 0%,rgba(24,226,153,.16),transparent 70%)}
.hero .eyebrow{display:inline-block;font-family:var(--mono);font-size:12px;font-weight:600;letter-spacing:.6px;text-transform:uppercase;color:var(--brand);background:rgba(24,226,153,.14);border-radius:9999px;padding:5px 14px;margin-bottom:20px}
[data-theme=light] .hero .eyebrow{color:#0fa76e;background:#d4fae8}
.hero h1{font-size:clamp(38px,5vw,60px);font-weight:600;letter-spacing:-1px;line-height:1.15;max-width:800px;margin:0 auto}
.hero h1 span{color:var(--ink)}
.hero p{color:var(--mut);font-size:18px;line-height:1.5;max-width:640px;margin:16px auto 0}
.hero .stats{display:flex;gap:10px;margin-top:28px;flex-wrap:wrap;justify-content:center}
.hero .stats span{font-size:13px;font-weight:500;color:var(--mut);background:var(--card);border:1px solid var(--line-soft);border-radius:9999px;padding:5px 14px}
.hero .stats b{color:var(--ink);font-weight:600;font-family:var(--mono);font-size:12px}
#resume{position:fixed;right:20px;bottom:20px;z-index:40;background:var(--ink);color:var(--bg);border-radius:9999px;padding:10px 22px;font-size:14px;font-weight:500;box-shadow:var(--shadow-lift);max-width:min(420px,80vw);white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
#resume:hover{opacity:.85;color:var(--bg)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px}
.card{position:relative;background:var(--card);border:1px solid var(--line-soft);border-radius:var(--radius);padding:22px 24px 24px;display:flex;flex-direction:column;gap:9px;box-shadow:var(--shadow);overflow:hidden;transition:transform .16s ease,box-shadow .16s ease,border-color .16s ease}
.card::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;background:var(--cat,var(--brand))}
.card:hover{transform:translateY(-4px);box-shadow:var(--shadow-lift);border-color:var(--line)}
.card .num{font-family:var(--mono);color:var(--mut);font-size:10px;font-weight:500;letter-spacing:.6px;text-transform:uppercase}
.card h3{font-size:19px;font-weight:600;letter-spacing:-.2px;line-height:1.3}
.card h3 a{color:var(--ink)}
.card p{font-size:13.5px;color:var(--mut);flex:1;line-height:1.55}
.dif{display:flex;align-items:center;gap:7px;font-size:12px;font-weight:600;color:var(--ink)}
.dif i{font-style:normal;width:8px;height:8px;border-radius:50%;background:var(--cat,var(--brand));flex:none}
.meta-line{font-size:12px;color:var(--mut)}
.card a.read{margin-top:8px;align-self:flex-start;background:transparent;border:1px solid var(--cat,var(--brand));color:var(--cat,var(--brand));font-weight:500;font-size:14px;border-radius:9999px;padding:7px 22px}
.card a.read:hover{background:var(--cat,var(--brand));color:#0B0D10;opacity:1}
[data-theme=light] .card a.read:hover{color:#fff}
.card a.read::after{content:" →"}
.prog{height:5px;background:var(--bg2);border-radius:4px;overflow:hidden}
.prog b{display:block;height:100%;background:var(--brand)}
h2.sec{font-size:24px;font-weight:500;letter-spacing:-.24px;margin:64px 0 4px;color:var(--ink)}
.sub{color:var(--mut);font-size:16px;margin-bottom:24px}
footer{border-top:1px solid var(--line-soft);margin-top:64px;color:var(--mut);font-size:13px}
footer .wrap{display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap}
.empty{background:var(--card);border:1px dashed var(--line);border-radius:var(--radius);padding:30px;text-align:center;color:var(--mut)}
/* collection: shelf rows */
.collectlabel{font-family:var(--mono);font-size:11px;font-weight:600;letter-spacing:.6px;text-transform:uppercase;color:var(--mut);margin:56px 0 20px}
.jumpnav{display:flex;gap:8px;flex-wrap:wrap;margin:-6px 0 30px}
.jumpnav a{font-size:13px;font-weight:500;background:var(--card);border:1px solid var(--line-soft);border-radius:9999px;padding:5px 14px;color:var(--mut)}
.jumpnav a:hover{border-color:var(--line);color:var(--ink)}
.morewrap{text-align:center;margin:8px 0 40px}
.shelf{margin:0 0 28px}
.shelf-head{margin-bottom:10px}
.shelf-head h2{font-size:18px}
.jumpnav{margin:-2px 0 18px;gap:6px}
.jumpnav a{font-size:12px;padding:4px 11px}
.hero{padding:48px 24px 20px}
.hero h1{font-size:clamp(32px,4.5vw,52px)}
.hero p{font-size:16px;margin:10px auto 0}
.shelf-head{display:flex;align-items:baseline;gap:14px;margin-bottom:16px}
.shelf-head h2{font-size:20px;font-weight:700;letter-spacing:-.2px;padding-bottom:8px;border-bottom:2px solid var(--cat,var(--brand))}
.shelf-head span{font-family:var(--mono);font-size:11px;font-weight:500;letter-spacing:.6px;text-transform:uppercase;color:var(--mut)}
.shelf-head .arrows{margin-left:auto;display:flex;gap:8px}
.shelf-head .arrows button{width:34px;height:34px;border-radius:50%;border:1px solid var(--line);background:var(--card);color:var(--ink);font-size:15px;cursor:pointer;line-height:1}
.shelf-head .arrows button:hover{border-color:var(--brand);color:var(--brand)}
.rail{display:flex;gap:20px;overflow-x:auto;padding:4px 24px 16px 2px;scroll-snap-type:x mandatory;-webkit-overflow-scrolling:touch;scrollbar-width:thin}
.rail .card{flex:0 0 272px;scroll-snap-align:start}
.rail .card p{-webkit-line-clamp:3}
/* roadmap — dense left-aligned editorial timeline */
.route{list-style:none;position:relative;margin:0;padding:6px 0 10px 36px;display:flex;flex-direction:column;gap:8px}
.route::before{content:"";position:absolute;top:4px;bottom:4px;left:18px;width:2px;background:var(--line);opacity:.5;border-radius:2px}
.stop{position:relative;width:auto;margin:0}
.stop::before{content:attr(data-mile);position:absolute;left:-30px;top:12px;width:24px;height:24px;border-radius:50%;background:var(--card);border:1.5px solid var(--cat,var(--brand));color:var(--ink);font-family:var(--mono);font-size:9px;font-weight:600;display:flex;align-items:center;justify-content:center;z-index:2;box-shadow:0 1px 4px rgba(0,0,0,.1)}
.stop .card{margin:0;padding:13px 14px;gap:5px;border-radius:10px;display:grid;grid-template-columns:1fr auto;align-items:center}
.stop .card .num{grid-column:1 / -1}
.stop .card h3{grid-column:1;font-size:14.5px;line-height:1.25}
.stop .card p{grid-column:1;font-size:12px;line-height:1.45;-webkit-line-clamp:2;display:-webkit-box;-webkit-box-orient:vertical;overflow:hidden}
.stop .card .dif{grid-column:1}
.stop .card a.read{grid-column:2;grid-row:2 / 5;align-self:center;margin:0}
.trip{position:relative;text-align:left;margin:4px 0 6px;padding-left:36px}
.trip span{font-size:9px;padding:4px 10px}
@media(max-width:700px){
.route::before{left:22px}
.stop{width:auto;margin:0 0 14px 52px}
.stop:nth-child(even of .stop){margin-left:52px}
.stop:nth-child(odd of .stop)::before,.stop:nth-child(even of .stop)::before{left:-44px;right:auto}
.trip{text-align:left;padding-left:8px}
}
.cores-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:20px}
@media(max-width:1024px){.cores-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:600px){.cores-grid{grid-template-columns:1fr}}
/* reader */
.rlayout{display:flex;max-width:1320px;margin:0 auto;min-height:100vh}
aside.toc{width:300px;flex:none;border-right:1px solid var(--line-soft);padding:24px 16px;position:sticky;top:57px;height:calc(100vh - 57px);overflow:auto}
aside.toc h4{font-family:var(--mono);font-size:11px;font-weight:600;letter-spacing:.6px;text-transform:uppercase;color:var(--mut);margin-bottom:12px}
aside.toc a{display:block;font-size:14px;font-weight:500;color:var(--mut);text-decoration:none;padding:7px 12px;border-radius:8px;border-left:2px solid transparent;line-height:1.45}
aside.toc a:hover{color:var(--ink);background:var(--bg2)}
aside.toc a.cur{background:var(--acc-soft);color:var(--brand);font-weight:600;border-left-color:var(--brand)}
[data-theme=light] aside.toc a.cur{color:#0fa76e}
main.read{flex:1;min-width:0;padding:32px 32px 90px}
.readbody{margin:0 auto;max-width:820px}
.readbody .page{width:auto !important;min-height:0 !important;margin:0 auto 22px !important;padding:26px !important;border-radius:14px;scroll-margin-top:80px}
.readbody .page.cover{align-items:flex-start !important}
.readbody pre,.readbody .terminal{position:relative;overflow-x:auto;max-width:100%;scrollbar-width:thin}
.readbody code,.readbody .mono{overflow-wrap:anywhere}
.copybar{display:flex;justify-content:flex-end;margin:0 0 8px}
.copybtn{position:static;background:var(--bg);border:1px solid rgba(255,255,255,.14);color:var(--ink);border-radius:9999px;font-size:12px;font-weight:500;padding:4px 12px;cursor:pointer}
[data-theme=light] .copybtn{border-color:rgba(0,0,0,.08)}
.copybtn:hover{opacity:.7}
mark{background:var(--acc-soft);color:var(--ink);border-radius:3px;padding:0 2px}
.chapnav{display:flex;justify-content:space-between;gap:12px;margin-top:32px}
.chapnav a{flex:1;background:var(--card);border:1px solid var(--line-soft);border-radius:16px;padding:16px 24px;text-decoration:none;color:var(--ink);font-size:14px;font-weight:500;box-shadow:var(--shadow)}
.chapnav a:hover{border-color:var(--line)}
.chapnav a small{display:block;font-family:var(--mono);font-size:11px;font-weight:500;letter-spacing:.6px;text-transform:uppercase;color:var(--mut);margin-bottom:4px}
.chapnav a.r{text-align:right}
.drawer{display:none;position:fixed;inset:0;z-index:70}
.drawer.open{display:block}
.drawer .scrim{position:absolute;inset:0;background:rgba(0,0,0,.5)}
.drawer .panel{position:absolute;right:0;top:0;bottom:0;width:320px;background:var(--card);border-left:1px solid var(--line-soft);padding:24px 32px;overflow:auto;box-shadow:var(--shadow)}
.drawer .panel h3{font-size:20px;font-weight:600;letter-spacing:-.2px;margin-bottom:4px}
.setrow{margin:20px 0}
.setrow h5{font-family:var(--mono);font-size:11px;font-weight:600;letter-spacing:.6px;text-transform:uppercase;color:var(--mut);margin-bottom:10px}
.setrow .opts{display:flex;gap:8px;flex-wrap:wrap}
.setrow .opts .btn.on{border-color:var(--ink);background:var(--ink);color:var(--bg)}
.tocbtn{display:none}
.pdflink{display:inline-block;margin-top:12px;background:var(--ink);color:var(--bg);border-radius:9999px;padding:8px 24px;text-decoration:none;font-size:14px;font-weight:500;box-shadow:var(--shadow-btn)}
.pdflink:hover{opacity:.85;color:var(--bg)}
.crumbs{display:flex;align-items:center;gap:8px;font-size:13.5px;min-width:0}
.crumbs .here{font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:280px}
.crumbs .sep{color:var(--mut)}
@media(max-width:900px){aside.toc{position:fixed;left:0;top:0;bottom:0;background:var(--card);z-index:60;transform:translateX(-105%);transition:transform .2s;height:100vh}
aside.toc.open{transform:none}
.tocbtn{display:inline-block}
main.read{padding:20px 14px 90px}
.crumbs .here{max-width:140px}
header.top .wrap{flex-wrap:wrap}
.search{max-width:none;flex-basis:100%;order:5}
.hero{padding:36px 0 6px}
.chapnav{flex-direction:column}
.readbody table,.readbody .terminal,table.gloss{display:block;overflow-x:auto;-webkit-overflow-scrolling:touch}
.drawer .panel{width:min(320px,88vw)}}
@media(max-width:600px){
.wrap{padding:16px 14px}
.grid{grid-template-columns:1fr}
.hero .stats{gap:6px}
main.read{padding:16px 10px 90px}
.readbody .page{padding:18px !important}
.btn{min-height:40px}
.readbody pre,.readbody .terminal{font-size:11px}}


/* icon: github white on dark, black on light — no halo */
.readbody .page.cover img[src*="github"], .coverart img[src*="github"]{filter:invert(1) brightness(1.05);}

/* icon: outline/black icons white on dark covers */
.readbody .page.cover img[src*="github"], .readbody .page.cover img[src*="workflow"], .readbody .page.cover img[src*="hammer"], .readbody .page.cover img[src*="package"], .readbody .page.cover img[src*="database"], .readbody .page.cover img[src*="puzzle"], .readbody .page.cover img[src*="server"], .readbody .page.cover img[src*="terminal"], .readbody .page.cover img[src*="shield"], .readbody .page.cover img[src*="activity"], .readbody .page.cover img[src*="webhook"], .readbody .page.cover img[src*="wrench"], .readbody .page.cover img[src*="flask"], .readbody .page.cover img[src*="rocket"], .coverart img[src*="github"], .coverart img[src*="workflow"], .coverart img[src*="hammer"], .coverart img[src*="package"], .coverart img[src*="database"], .coverart img[src*="puzzle"], .coverart img[src*="server"], .coverart img[src*="terminal"], .coverart img[src*="shield"], .coverart img[src*="activity"], .coverart img[src*="webhook"], .coverart img[src*="wrench"], .coverart img[src*="flask"], .coverart img[src*="rocket"]{filter:invert(1) brightness(1.05);}

@media print{header.top,aside.toc,.drawer,.chapnav,.copybtn,.settingsbar{display:none !important}
main.read{padding:0}.readbody{max-width:none}}
table.gloss{width:100%;border-collapse:collapse;font-size:14px;margin:16px 0}
table.gloss td,table.gloss th{border:1px solid var(--line);padding:9px 11px;text-align:left}
table.gloss th{background:var(--bg2)}
/* P0: sepia theme + light leak guards + covers + filters + a11y */
[data-theme=sepia]{--bg:#f6f1e7;--bg2:#efe7d6;--card:#fffdf7;--ink:#2b2620;--mut:#6f665a;--line:rgba(43,38,32,.14);--line-soft:rgba(43,38,32,.09);--acc:#0b9b68;--acc-soft:#d4fae8;--brand:#0b9b68;--shadow:rgba(43,38,32,.06) 0px 2px 4px;--shadow-btn:rgba(43,38,32,.08) 0px 1px 2px;--shadow-lift:rgba(43,38,32,.12) 0px 12px 28px -8px}
[data-theme=sepia] .readbody{--paper:#fffdf7;--white:#fffdf7;--ink:#2b2620;--muted:#6f665a;--line:rgba(43,38,32,.14);--panel:#efe7d6;--text-light:#2b2620}
[data-theme=light] .readbody{--paper:#ffffff;--white:#ffffff;--ink:#0d0d0d;--muted:#555;--line:rgba(0,0,0,.1);--panel:#f4f4f4;--text-light:#0d0d0d}
[data-theme=light] .readbody .page,[data-theme=sepia] .readbody .page{background:var(--card) !important;color:var(--ink)}
[data-theme=light] .readbody pre,[data-theme=light] .readbody .terminal,[data-theme=sepia] .readbody pre,[data-theme=sepia] .readbody .terminal{background:var(--bg2) !important;color:var(--ink);border:1px solid var(--line)}
.coverart{height:96px;border-radius:10px 10px 0 0;margin:-22px -24px 12px;background:linear-gradient(135deg,var(--cat,#18E299),transparent 140%),repeating-linear-gradient(90deg,rgba(255,255,255,.08) 0 2px,transparent 2px 10px),var(--card);border-bottom:1px solid var(--line-soft);display:flex;align-items:flex-end;padding:10px 14px;overflow:hidden}
.coverart b{font-family:var(--mono);font-size:28px;font-weight:600;letter-spacing:-1px;color:#fff;text-shadow:0 1px 8px rgba(0,0,0,.5)}
[data-theme=light] .coverart b,[data-theme=sepia] .coverart b{color:#fff}
.filterbar{display:flex;gap:8px;flex-wrap:wrap;margin:18px 0 6px;align-items:center}
.filterbar select,.filterbar input[type=search]{background:var(--card);border:1px solid var(--line);color:var(--ink);border-radius:9999px;padding:7px 14px;font-size:13px;outline:none}
.filterbar .count{margin-left:auto;font-family:var(--mono);font-size:12px;color:var(--mut)}
.toc-l2{padding-left:14px !important}.toc-l3{padding-left:28px !important}.toc-num{font-family:var(--mono);font-size:11px;color:var(--mut);margin-right:6px}
.codehead{display:flex;align-items:center;gap:8px;font-family:var(--mono);font-size:11px;color:var(--mut);margin:12px 0 0;background:var(--bg2);border:1px solid var(--line);border-bottom:none;border-radius:8px 8px 0 0;padding:6px 12px}
.codehead .dot{width:8px;height:8px;border-radius:50%;background:var(--brand)}
.codehead button{margin-left:auto;background:transparent;border:1px solid var(--line);color:var(--ink);border-radius:9999px;font-size:11px;padding:2px 10px;cursor:pointer}
.readbody img{max-width:100%;height:auto;border-radius:8px}
.readbody img[data-broken]{display:none}
.imgfallback{display:none;background:var(--bg2);border:1px dashed var(--line);border-radius:8px;padding:12px;font-size:13px;color:var(--mut)}
@media(max-width:900px){header.top .wrap{gap:10px}.crumbs .here{max-width:110px} .search kbd{display:none}}


/* icon: github white on dark, black on light — no halo */
.readbody .page.cover img[src*="github"], .coverart img[src*="github"]{filter:invert(1) brightness(1.05);}

/* icon: outline/black icons white on dark covers */
.readbody .page.cover img[src*="github"], .readbody .page.cover img[src*="workflow"], .readbody .page.cover img[src*="hammer"], .readbody .page.cover img[src*="package"], .readbody .page.cover img[src*="database"], .readbody .page.cover img[src*="puzzle"], .readbody .page.cover img[src*="server"], .readbody .page.cover img[src*="terminal"], .readbody .page.cover img[src*="shield"], .readbody .page.cover img[src*="activity"], .readbody .page.cover img[src*="webhook"], .readbody .page.cover img[src*="wrench"], .readbody .page.cover img[src*="flask"], .readbody .page.cover img[src*="rocket"], .coverart img[src*="github"], .coverart img[src*="workflow"], .coverart img[src*="hammer"], .coverart img[src*="package"], .coverart img[src*="database"], .coverart img[src*="puzzle"], .coverart img[src*="server"], .coverart img[src*="terminal"], .coverart img[src*="shield"], .coverart img[src*="activity"], .coverart img[src*="webhook"], .coverart img[src*="wrench"], .coverart img[src*="flask"], .coverart img[src*="rocket"]{filter:invert(1) brightness(1.05);}

@media print{header.top,aside.toc,.drawer,.chapnav,.copybtn,.copybar,.codehead,.filterbar,#resume,.jumpnav,.shelf-head .arrows{display:none !important} body{background:#fff !important;color:#000 !important} .card,.readbody .page{break-inside:avoid;border:1px solid #ccc !important;background:#fff !important;color:#000 !important} main.read{padding:0}.readbody{max-width:none;font-size:12pt}}
@media(prefers-reduced-motion:reduce){*{animation:none !important;transition:none !important;scroll-behavior:auto !important}.rail{scroll-snap-type:none}}
/* P1: paths + rubric + search dropdown + bookmarks + related + labs + lightbox */
.pathgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px;margin:16px 0 8px}
.pathcard{background:var(--card);border:1px solid var(--line-soft);border-radius:var(--radius);padding:18px 20px;box-shadow:var(--shadow)}
.pathcard h3{font-size:16px;margin-bottom:4px}
.pathcard p{font-size:13px;color:var(--mut);margin-bottom:10px}
.pathcard ol{margin:0 0 10px 18px;font-size:13px;color:var(--mut)}
.pathcard ol b{color:var(--ink);font-weight:500}
.pathcard .meta{font-family:var(--mono);font-size:11px;color:var(--mut)}
.rubric{display:flex;gap:10px;flex-wrap:wrap;margin:14px 0}
.rubric div{flex:1;min-width:200px;background:var(--card);border:1px solid var(--line-soft);border-radius:10px;padding:12px 16px;font-size:13px;color:var(--mut)}
.rubric b{display:block;color:var(--ink);margin-bottom:4px}
.searchwrap{position:relative}
.searchdrop{position:absolute;top:110%;left:0;right:0;background:var(--card);border:1px solid var(--line);border-radius:12px;box-shadow:var(--shadow-lift);overflow:hidden;z-index:50;display:none;max-height:320px;overflow:auto}
.searchdrop.open{display:block}
.searchdrop a{display:block;padding:9px 16px;font-size:14px;border-bottom:1px solid var(--line-soft)}
.searchdrop a small{display:block;font-size:11px;color:var(--mut)}
.searchdrop a:hover{background:var(--bg2)}
.markbtn{background:transparent;border:1px solid var(--line);color:var(--ink);border-radius:9999px;font-size:12px;padding:4px 12px;cursor:pointer}
.markbtn.on{background:var(--acc-soft);border-color:var(--brand);color:var(--brand)}
.relatedbox{background:var(--card);border:1px solid var(--line-soft);border-radius:14px;padding:18px 22px;margin-top:28px}
.relatedbox h4{font-family:var(--mono);font-size:11px;letter-spacing:.6px;text-transform:uppercase;color:var(--mut);margin-bottom:10px}
.relatedbox ul{list-style:none;display:flex;gap:8px;flex-wrap:wrap}
.relatedbox a{font-size:13px;border:1px solid var(--line);border-radius:9999px;padding:5px 14px}
.upnext{display:flex;justify-content:space-between;gap:10px;background:var(--acc-soft);border:1px solid var(--brand);border-radius:14px;padding:14px 20px;margin-top:20px;font-size:14px}
.labcheck{list-style:none;margin:12px 0}
.labcheck li{display:flex;gap:10px;align-items:flex-start;background:var(--card);border:1px solid var(--line-soft);border-radius:10px;padding:10px 14px;margin-bottom:8px;font-size:14px}
.labcheck li.done{opacity:.6;text-decoration:line-through}
.labcheck input{margin-top:4px;accent-color:var(--brand)}
.labbanner{background:var(--acc-soft);border:1px solid var(--brand);border-radius:12px;padding:12px 18px;margin:0 auto 20px;max-width:820px;font-size:14px}
#lightbox{display:none;position:fixed;inset:0;z-index:100;background:rgba(0,0,0,.85);align-items:center;justify-content:center;padding:24px}
#lightbox.open{display:flex}
#lightbox img{max-width:94vw;max-height:90vh;border-radius:10px}
.readbody table{border-collapse:collapse}
.readbody thead th{position:sticky;top:57px;background:var(--bg2);z-index:2}
.bookhero{display:flex;gap:26px;flex-wrap:wrap;margin:30px 0}
.bookhero .coverart{height:190px;flex:0 0 220px;margin:0;border-radius:14px;align-items:center;justify-content:center}
.bookhero .coverart b{font-size:54px}
.chiprow{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}
.chiprow a,.chiprow span{font-size:12px;border:1px solid var(--line);border-radius:9999px;padding:4px 12px;color:var(--mut)}
.chiprow a:hover{color:var(--ink);border-color:var(--brand)}
.outcomes{background:var(--card);border:1px solid var(--line-soft);border-radius:12px;padding:14px 20px;margin:16px 0}
.outcomes li{margin:4px 0 4px 18px;font-size:14px}
/* P2.1: recommended-path strip — single cold-start path, distinct from shelves */
.recstrip{background:var(--card);border:1px solid var(--brand);border-radius:16px;padding:20px 22px;margin:28px 0 8px;box-shadow:var(--shadow)}
.rec-head{display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;margin-bottom:12px}
.rec-head .eyebrow{font-family:var(--mono);font-size:11px;font-weight:600;letter-spacing:.6px;text-transform:uppercase;color:var(--brand);background:var(--acc-soft);border-radius:9999px;padding:5px 14px}
.rec-meta{font-family:var(--mono);font-size:11px;color:var(--mut)}
.rec-steps{list-style:none;display:flex;gap:10px;margin:0 0 14px;padding:0;flex-wrap:wrap}
.rec-steps li{flex:1;min-width:160px;background:var(--bg2);border:1px solid var(--line-soft);border-radius:12px;padding:10px 14px;font-size:13px;color:var(--mut)}
.rec-steps li b{display:block;color:var(--ink);font-size:14px;font-weight:600;margin:2px 0}
.rec-steps li .n{font-family:var(--mono);font-size:11px;color:var(--brand)}
.rec-steps li a{color:var(--ink)}
.rec-cta{display:inline-block;background:var(--brand);color:#0B0D10;font-weight:600;font-size:14px;border-radius:9999px;padding:10px 22px}
[data-theme=light] .rec-cta{color:#fff}
.rec-cta:hover{opacity:.85;color:#0B0D10}
[data-theme=light] .rec-cta:hover{color:#fff}
@media(max-width:700px){.rec-steps{flex-direction:column}.rec-steps li{min-width:0}}
/* P2.2: reader orientation — breadcrumb + prereq + path position (existing vars only) */
.readcontext{background:var(--card);border-bottom:1px solid var(--line-soft);padding:10px 32px;font-size:13px;color:var(--mut)}
.readcontext .wrap{max-width:1320px;margin:0 auto;padding:0;display:flex;gap:10px;align-items:center;flex-wrap:wrap}
.readcontext a{color:var(--mut)}
.readcontext a:hover{color:var(--brand)}
.readcontext .here{color:var(--ink);font-weight:600}
.readcontext .pathpos{font-family:var(--mono);font-size:11px;background:var(--acc-soft);color:var(--brand);border-radius:9999px;padding:3px 12px;white-space:nowrap}
.readcontext .prereq{font-size:12px}
.readcontext .prereq a{border:1px solid var(--line);border-radius:9999px;padding:2px 10px;margin-left:6px;white-space:nowrap}
@media(max-width:700px){.readcontext{padding:8px 14px;font-size:12px}}
/* P2.4: mobile icon-chain reflow (≤480px only, desktop untouched) */
@media(max-width:480px){
.readbody .life{flex-direction:column;gap:0}
.readbody .life .lconn{transform:rotate(90deg);padding:3px 0;align-self:center}
.readbody .life .lnode{display:flex;align-items:center;gap:10px;text-align:left;padding:8px 12px}
.readbody .life .lnode img{margin:0;flex:none}
.readbody .life .lnode b{font-size:11px}
.readbody .two{grid-template-columns:1fr}
.readbody .fnode{font-size:13px}
.readbody .vflow{margin:8px 0}
}
/* P2: dim + contrast themes, font + line-height prefs, rating */
[data-theme=dim]{--bg:#000000;--bg2:#0a0a0a;--card:#0d0d0f;--ink:#e8e8e8;--mut:#9a9a9a;--line:rgba(255,255,255,.12);--line-soft:rgba(255,255,255,.08);--acc:#18E299;--acc-soft:rgba(24,226,153,.14);--brand:#18E299}
[data-theme=contrast]{--bg:#000000;--bg2:#0a0a0a;--card:#000000;--ink:#ffffff;--mut:#e0e0e0;--line:#ffffff;--line-soft:#8a8a8a;--acc:#ffe600;--acc-soft:#3a3600;--brand:#ffe600}
[data-theme=contrast] a{color:#ffe600}
[data-theme=contrast] .card,[data-theme=contrast] .pathcard{border-width:2px}
body[data-font=serif] .readbody{font-family:Georgia,'Times New Roman',serif}
body[data-font=serif] .readbody code,body[data-font=serif] .readbody pre,body[data-font=serif] .readbody .terminal{font-family:var(--mono)}
.readbody{line-height:var(--lh,1.7)}
.ratebox{display:flex;gap:8px;align-items:center;background:var(--card);border:1px solid var(--line-soft);border-radius:12px;padding:12px 18px;margin-top:22px;font-size:14px}
.ratebox button{background:transparent;border:1px solid var(--line);border-radius:9999px;font-size:14px;padding:4px 14px;cursor:pointer;color:var(--ink)}
.ratebox button.on{background:var(--acc-soft);border-color:var(--brand)}
.popsearch{font-size:12px;color:var(--mut);margin-top:6px}
.popsearch a{color:var(--mut);text-decoration:underline;cursor:pointer}
"""

BASE_JS = """
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
function getP(k,d){try{const v=JSON.parse(localStorage.getItem(k));return v??d}catch(e){return d}}
function setP(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}
"""

INDEX_JS = BASE_JS + """
const PREF='cicdlib:pref',PROG='cicdlib:prog:';
const pref=getP(PREF,{theme:'dark'});
const THEMES=['dark','light','sepia','dim','contrast'],THICON={dark:'☀',light:'☾',sepia:'◐',dim:'◑',contrast:'◉'};
function syncTheme(){const th=THEMES.includes(pref.theme)?pref.theme:'dark';document.documentElement.dataset.theme=th;const t=$('#themebtn');if(t)t.textContent=THICON[th]||'☀'}
syncTheme();
function cycleTheme(){pref.theme=THEMES[(THEMES.indexOf(pref.theme)+1)%THEMES.length]||'dark';setP(PREF,pref);syncTheme();}
function renderContinue(){
  const box=$('#continue'),items=[],done=[],hist=[];
  $$('.book[data-id]').forEach(c=>{const p=getP(PROG+c.dataset.id,null);if(!p||!p.pct)return;const e={id:c.dataset.id,title:c.dataset.title,pct:p.pct,ts:p.ts||0};hist.push(e);if(p.pct>=98)done.push(e);else if(p.pct>0)items.push(e);});
  hist.sort((a,b)=>b.ts-a.ts);
  if(!items.length&&!done.length){box.innerHTML='';}
  else{items.sort((a,b)=>b.pct-a.pct);
  box.innerHTML='<div class="collectlabel">PICK UP WHERE YOU LEFT OFF</div><div class="rail">'+items.map(i=>`<div class="card"><h3>${i.title}</h3><div class="prog"><b style="width:${i.pct}%"></b></div><a class="read" href="read/${i.id}.html">Continue — ${i.pct}%</a></div>`).join('')+'</div>'
  +(done.length?'<div class="collectlabel">COMPLETED · '+done.length+'</div><div class="chiprow">'+done.map(i=>`<a href="read/${i.id}.html">✓ ${i.title}</a>`).join('')+'</div>':'')
  +(hist.length?'<div class="collectlabel">RECENTLY VIEWED</div><div class="chiprow">'+hist.slice(0,6).map(i=>`<a href="read/${i.id}.html">${i.title} · ${i.pct}%</a>`).join('')+'</div>':'');}
  try{const marks=getP('cicdlib:marks',{}),ids=Object.keys(marks);const mr=$('#marksrow');
  if(mr){if(!ids.length)mr.innerHTML='';else{const cards=ids.map(id=>{const c=document.querySelector('.book[data-id="'+id+'"]');const t=c?c.dataset.title:id;return `<a href="read/${id}.html">★ ${t}</a>`;}).join('');mr.innerHTML='<div class="collectlabel">SAVED</div><div class="chiprow">'+cards+'</div>';}}}catch(e){}
  const top=items[0]||hist[0],rs=$('#resume');
  if(rs&&top){rs.href='read/'+top.id+'.html';rs.textContent='Resume · '+top.title+' — '+top.pct+'%';rs.style.display='';}
}
function filter(){
  const q=($('#q').value||'').toLowerCase(),cat=$('#fcat')?.value||'',dif=$('#fdif')?.value||'',sort=$('#fsort')?.value||'';
  let n=0;const visCards=[];
  $$('.book[data-id]').forEach(c=>{
    const okQ=(c.dataset.title+' '+c.dataset.desc+' '+(c.dataset.tags||'')).toLowerCase().includes(q);
    const okC=!cat||c.dataset.cat===cat, okD=!dif||c.dataset.dif===dif;
    const ok=okQ&&okC&&okD; c.style.display=ok?'':'none'; if(ok){n++;visCards.push(c);}
  });
  if(sort){$$('.shelf .rail, .shelf .cores-grid').forEach(rail=>{[...rail.children].filter(c=>c.style.display!=='none').sort((a,b)=>{
    if(sort==='az')return a.dataset.title.localeCompare(b.dataset.title);
    if(sort==='time')return (+a.dataset.time||99)-(+b.dataset.time||99);
    if(sort==='level'){const r={Beginner:0,Intermediate:1,Advanced:2};return (r[a.dataset.dif]??9)-(r[b.dataset.dif]??9);}
    return 0;}).forEach(c=>rail.appendChild(c));});}
  $$('.shelf').forEach(s=>{
    const vis=[...s.querySelectorAll('.book')].some(c=>c.style.display!=='none');
    s.style.display=vis?'':'none';
  });
  $('#empty').style.display=n?'none':'';
  const cc=$('#fcount');if(cc)cc.textContent=n+' shown';
  try{const h=new URLSearchParams();if($('#q').value)h.set('q',$('#q').value);if(cat)h.set('cat',cat);if(dif)h.set('dif',dif);history.replaceState(null,'','#'+h.toString());}catch(e){}
}
['q','fcat','fdif','fsort'].forEach(id=>{const el=document.getElementById(id);if(el)el.addEventListener('input',()=>{filter();drop();});});
function norm(s){return (s||'').toLowerCase().replace(/[-_\/]/g,' ');}
function drop(){const raw=($('#q').value||''),q=raw.toLowerCase(),box=$('#qdrop');if(!box)return;if(q.length<2){box.classList.remove('open');box.innerHTML='';return;}
const STOP=new Set(['how','does','did','can','what','when','where','which','that','this','with','from','have','has','are','was','were','been','will','would','there','their','about','into','your','you','our','the','and','for','are','but','not','all','any','can','had','her','him','his','one','our','out','day','get','has','him','how','its','may','new','now','old','see','two','way','who','boy','did','she','use','her','now','do','i','an','a','to','in','of','or','is','it','my','me','on','as','at','by','we','if','up','so']);
const qn=norm(raw);let toks=qn.split(/\s+/).filter(t=>t.length>=3&&!STOP.has(t));if(!toks.length)toks=[qn].filter(t=>t.length>=2);if(!toks.length){box.classList.remove('open');return;}
const idx=window.SEARCH_IDX||[];const res=idx.map(b=>{const secs=(b.sections||[]).join(' ');const body=(b.body||'');const hay=norm(b.title+' '+b.desc+' '+(b.tags||[]).join(' ')+' '+secs+' '+body);if(!toks.every(t=>hay.includes(t)))return null;let s=1,hit='';const secHit=(b.sections||[]).find(t=>{const tn=norm(t);return toks.every(tk=>tn.includes(tk))||tn.includes(toks[0]);});const titleHit=toks.every(t=>norm(b.title).includes(t));if(titleHit)s=3;else if(secHit){s=2;hit=secHit;}else{const bi=norm(body).indexOf(toks[0]);if(bi>=0){hit='…'+body.slice(Math.max(0,bi-30),bi+50).replace(/\s+/g,' ')+'…';}else if(b.desc){hit=b.desc.slice(0,70);}}if((b.tags||[]).some(t=>toks.some(k=>norm(t).includes(k))))s+=0.5;return {b,s,hit};}).filter(Boolean).sort((a,b2)=>b2.s-a.s).slice(0,8);
box.innerHTML=res.length?res.map(r=>`<a href="book/${r.b.id}.html"><b>${r.b.title}</b><small>${r.b.cat} · ${r.b.dif} · ${r.b.time} min${r.hit?' · § '+r.hit.slice(0,80):''}</small></a>`).join(''):'<a><b>Nothing found</b><small>Try “rollback” or “canary” — or start with Foundations</small></a>';box.classList.add('open');}
document.addEventListener('click',e=>{const box=$('#qdrop');if(box&&!e.target.closest('.searchwrap'))box.classList.remove('open');});
function logQ(q){q=(q||'').trim().toLowerCase();if(q.length<3)return;try{const L=getP('cicdlib:qlog',{});L[q]=(L[q]||0)+1;setP('cicdlib:qlog',L);}catch(e){}}
function renderPop(){try{const L=getP('cicdlib:qlog',{}),top=Object.entries(L).sort((a,b)=>b[1]-a[1]).slice(0,5);const el=$('#popsearch');if(el)el.innerHTML=top.length?('Popular: '+top.map(t=>`<a data-q="${t[0]}">${t[0]}</a>`).join(' · ')):'';$$('#popsearch a').forEach(a=>a.onclick=()=>{$('#q').value=a.dataset.q;filter();drop();});}catch(e){}}
$('#q').addEventListener('keydown',e=>{if(e.key==='Enter')logQ(e.target.value);});
renderPop();
document.addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k'){e.preventDefault();$('#q').focus()}});
$$('.shelf').forEach(s=>{const rail=s.querySelector('.rail');if(!rail)return;s.querySelectorAll('.arrows button').forEach(b=>b.onclick=()=>rail.scrollBy({left:(+b.dataset.dir)*320,behavior:'smooth'}))});
const mb=$('#morebtn');if(mb)mb.onclick=()=>{const m=$('#morecats');if(m)m.style.display='';mb.style.display='none'};
$$('.jumpnav a').forEach(a=>a.addEventListener('click',()=>{const m=$('#morecats');if(m&&m.style.display==='none'){m.style.display='';const b=$('#morebtn');if(b)b.style.display='none'}}));
$('#themebtn').onclick=()=>cycleTheme();
try{const h=new URLSearchParams(location.hash.slice(1));if(h.get('q'))$('#q').value=h.get('q');if(h.get('cat')&&$('#fcat'))$('#fcat').value=h.get('cat');if(h.get('dif')&&$('#fdif'))$('#fdif').value=h.get('dif');}catch(e){}
renderContinue();filter();
"""

READER_JS = BASE_JS + """
const BID=document.body.dataset.book,PREF='cicdlib:pref',PKEY='cicdlib:prog:'+BID;
const pref=Object.assign({theme:'dark',fs:18,width:'820px',font:'sans',lh:1.7},getP(PREF,{}));
const RTHEMES=['dark','light','sepia','dim','contrast'];
function applyPref(){document.documentElement.dataset.theme=RTHEMES.includes(pref.theme)?pref.theme:'dark';
  document.body.dataset.font=pref.font==='serif'?'serif':'sans';
  const rb=document.querySelector('.readbody');if(rb){rb.style.fontSize=pref.fs+'px';rb.style.setProperty('max-width',pref.width);rb.style.setProperty('--lh',pref.lh);}
  $$('.setrow .opts .btn').forEach(b=>b.classList.toggle('on',b.dataset.set===undefined?'':String(pref[b.dataset.k])===b.dataset.set));
  setP(PREF,pref);}
function setOpt(k,v){pref[k]=v;applyPref()}
$$('.terminal').forEach(t=>{const bar=document.createElement('div');bar.className='copybar';const b=document.createElement('button');b.className='copybtn';b.textContent='Copy';b.onclick=()=>{let txt=t.innerText.split('\\n').filter(l=>!l.match(/^\\s*(NAME|nginx-|CONTAINER|NAME\\s+READY)/)).join('\\n');navigator.clipboard.writeText(txt||t.innerText).then(()=>{b.textContent='Copied!';setTimeout(()=>b.textContent='Copy',1200)})};bar.appendChild(b);t.before(bar)});
$$('.readbody pre').forEach(p=>{if(p.closest('.terminal')||p.previousElementSibling?.classList?.contains('codehead'))return;const h=document.createElement('div');h.className='codehead';h.innerHTML='<span class=dot></span><span>code</span>';const b=document.createElement('button');b.textContent='Copy';b.onclick=()=>{navigator.clipboard.writeText(p.innerText).then(()=>{b.textContent='Copied!';setTimeout(()=>b.textContent='Copy',1200)})};const w=document.createElement('button');w.textContent='Wrap';w.style.marginLeft='6px';w.onclick=()=>{p.style.whiteSpace=p.style.whiteSpace==='pre-wrap'?'pre':'pre-wrap'};h.appendChild(b);h.appendChild(w);p.before(h)});
$$('.readbody img').forEach(im=>{im.setAttribute('loading','lazy');if(!im.getAttribute('alt'))im.setAttribute('alt','Diagram from '+BID);im.style.cursor='zoom-in';im.addEventListener('click',()=>{const lb=$('#lightbox');if(lb){lb.querySelector('img').src=im.src;lb.classList.add('open');}});im.addEventListener('error',()=>{im.dataset.broken='1';const f=document.createElement('div');f.className='imgfallback';f.style.display='block';f.textContent='Image unavailable: '+(im.getAttribute('alt')||im.src);im.after(f);});});
const _lb=$('#lightbox');if(_lb)_lb.addEventListener('click',()=>_lb.classList.remove('open'));
const MARKS='cicdlib:marks';
const _mb=$('#markbtn');function syncMark(){const m=getP(MARKS,{});const on=!!m[BID];if(_mb){_mb.textContent=on?'★ Saved':'☆ Save';_mb.classList.toggle('on',on);}}
if(_mb)_mb.onclick=()=>{const m=getP(MARKS,{});if(m[BID])delete m[BID];else m[BID]=Date.now();setP(MARKS,m);syncMark();};syncMark();
const LABKEY='cicdlib:lab:'+BID;
function labChecks(){const done=getP(LABKEY,{});$$('.readbody .step').forEach((st,i)=>{if(st.querySelector('input[type=checkbox]'))return;const lab=document.createElement('input');lab.type='checkbox';lab.checked=!!done[i];lab.setAttribute('aria-label','Mark step done');lab.onchange=()=>{const d=getP(LABKEY,{});if(lab.checked)d[i]=1;else delete d[i];setP(LABKEY,d);st.classList.toggle('done',lab.checked);};st.classList.toggle('done',!!done[i]);st.prepend(lab);});const rst=$('#labreset');if(rst)rst.onclick=()=>{setP(LABKEY,{});$$('.readbody .step').forEach(st=>{st.classList.remove('done');const c=st.querySelector('input[type=checkbox]');if(c)c.checked=false;});};}
labChecks();
function tocUpdate(){const secs=$$('.readbody .page');let cur=secs[0]&&secs[0].id;
  secs.forEach(s=>{if(s.getBoundingClientRect().top<160)cur=s.id});
  window._cur=cur;
  $$('aside.toc a').forEach(a=>a.classList.toggle('cur',a.getAttribute('href')==='#'+cur));}
const RATEKEY='cicdlib:rate:'+BID;
function syncRate(){const v=getP(RATEKEY,null);const u=$('#rateup'),d=$('#ratedown'),t=$('#ratethanks');if(u)u.classList.toggle('on',v==='up');if(d)d.classList.toggle('on',v==='down');if(t)t.textContent=v?'Thanks for the feedback!':'';}
const _ru=$('#rateup'),_rd=$('#ratedown');
if(_ru)_ru.onclick=()=>{setP(RATEKEY,getP(RATEKEY,null)==='up'?null:'up');syncRate();};
if(_rd)_rd.onclick=()=>{setP(RATEKEY,getP(RATEKEY,null)==='down'?null:'down');syncRate();};
syncRate();
window.addEventListener('scroll',()=>{tocUpdate();
  const h=document.documentElement,p=Math.min(100,Math.round(100*(h.scrollTop)/(h.scrollHeight-h.clientHeight||1)));
  setP(PKEY,{pct:p,ts:Date.now()});const bar=$('#pbar');if(bar)bar.style.width=p+'%';},{passive:true});
function findBook(q){$$('.readbody mark').forEach(m=>{m.replaceWith(document.createTextNode(m.textContent))});if(!q)return 0;
  let n=0;const walker=document.createTreeWalker(document.querySelector('.readbody'),NodeFilter.SHOW_TEXT);
  const nodes=[];while(walker.nextNode())nodes.push(walker.currentNode);
  nodes.forEach(nd=>{const i=nd.textContent.toLowerCase().indexOf(q.toLowerCase());if(i<0)return;
    if(nd.parentElement.closest('.terminal,script,style'))return;
    const r=document.createRange();r.setStart(nd,i);r.setEnd(nd,i+q.length);
    const m=document.createElement('mark');r.surroundContents(m);n++;});
  const f=document.querySelector('.readbody mark');if(f)f.scrollIntoView({block:'center'});return n;}
$('#q').addEventListener('keydown',e=>{if(e.key==='Enter'){const n=findBook(e.target.value);$('#qcount').textContent=n?n+' match'+(n>1?'es':'')+' in this book':'no matches in this book'}});
$('#q').addEventListener('input',e=>{if(!e.target.value)findBook('')});
document.addEventListener('keydown',e=>{
  if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k'){e.preventDefault();$('#q').focus()}
  if(e.key==='Escape'){$('#drawer').classList.remove('open');$('aside.toc').classList.remove('open')}
  if(e.key.toLowerCase()==='t'&&document.activeElement.tagName!=='INPUT'){$('aside.toc').classList.toggle('open')}
  if(e.key==='ArrowRight'&&document.activeElement.tagName!=='INPUT'){const n=$('#nextbook');if(n)location.href=n.href}
  if(e.key==='ArrowLeft'&&document.activeElement.tagName!=='INPUT'){const p=$('#prevbook');if(p)location.href=p.href}
  if(e.key.toLowerCase()==='c'&&document.activeElement.tagName!=='INPUT'&&window._cur){try{navigator.clipboard.writeText(location.href.split('#')[0]+'#'+window._cur);const qc=$('#qcount');if(qc)qc.textContent='section link copied';}catch(err){}}});
$('#setbtn').onclick=()=>$('#drawer').classList.add('open');
$('#drawer .scrim').onclick=()=>$('#drawer').classList.remove('open');
$('#tocbtn').onclick=()=>$('aside.toc').classList.toggle('open');
$$('aside.toc a').forEach(a=>a.onclick=()=>{if(innerWidth<=900)$('aside.toc').classList.remove('open')});
applyPref();tocUpdate();
"""


class PageGrabber(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.pages, self._buf, self._depth = [], None, 0

    def handle_starttag(self, tag, attrs):
        d = dict(attrs)
        if tag == "div" and self._buf is None and "page" in d.get("class", "").split():
            self._buf, self._depth = [self.get_starttag_text()], 1
            return
        if self._buf is not None:
            self._buf.append(self.get_starttag_text())
            if tag == "div":
                self._depth += 1

    def handle_endtag(self, tag):
        if self._buf is not None:
            self._buf.append(f"</{tag}>")
            if tag == "div":
                self._depth -= 1
                if self._depth == 0:
                    self.pages.append("".join(self._buf))
                    self._buf = None

    def handle_data(self, data):
        if self._buf is not None:
            self._buf.append(data)

    def handle_entityref(self, name):
        if self._buf is not None:
            self._buf.append(f"&{name};")

    def handle_charref(self, name):
        if self._buf is not None:
            self._buf.append(f"&#{name};")


def parse_book(path):
    src = open(path, encoding="utf-8").read()
    css = re.findall(r"<style>(.*?)</style>", src, re.S)
    g = PageGrabber()
    g.feed(src)
    return (scope_css(css[0]) if css else ""), g.pages


def scope_css(css):
    """Keep print stylesheets inside the article: bare `body{}` becomes
    `.readbody{}` (minus its page background), and `:root` variables move
    onto `.readbody` so --ink/--line/--red never leak into site chrome."""
    css = re.sub(
        r"(?<![.\w#-])body\s*\{([^}]*)\}",
        lambda m: ".readbody{" + re.sub(r"background\s*:[^;]+;?", "", m.group(1)) + "}",
        css,
    )
    return css.replace(":root", ".readbody")


def toc_of(pages):
    items = []
    n1 = n2 = n3 = 0
    for i, p in enumerate(pages):
        heads = re.findall(r"<(h2|h3|h4)[^>]*>(.*?)</\1>", p, re.S)
        if not heads:
            m = re.search(r"<h1[^>]*>(.*?)</h1>", p, re.S)
            label = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else f"Page {i+1}"
            items.append((f"p{i+1}", "Cover — " + label[:40], 1))
            continue
        for tag, htxt in heads:
            clean = re.sub(r"<[^>]+>", "", htxt).strip()
            if not clean:
                continue
            if tag == "h2":
                n1 += 1; n2 = n3 = 0; num = f"{n1}"
                lvl = 1
            elif tag == "h3":
                n2 += 1; n3 = 0; num = f"{n1}.{n2}" if n1 else f"{n2}"
                lvl = 2
            else:
                n3 += 1; num = f"{n1}.{n2}.{n3}" if n1 else f"{n2}.{n3}"
                lvl = 3
            items.append((f"p{i+1}", f"{num} {clean[:60]}", lvl))
    return items


DIFF_RANK = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}


def reader_url(b):
    """Single URL-building rule for reader pages; library cards and roadmap share it."""
    return f"read/{b['id']}.html"


def build_roadmap_page(books, output_dir):
    """Static visual map of every manifest book, grouped by category.

    Same data (books), same tokens, same card language as the library.
    Categories under 3 books merge into 'Quick topics' per homepage convention.
    """
    def slug(name):
        return "rm-" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

    groups = {}
    for b in books:
        groups.setdefault(b["category"], []).append(b)
    for bs in groups.values():
        bs.sort(key=lambda b: (DIFF_RANK.get(b["difficulty"], 9), b["title"].lower()))
    big = sorted(((c, bs) for c, bs in groups.items() if len(bs) >= 3), key=lambda t: -len(t[1]))
    small = sorted((b for c, bs in groups.items() if len(bs) < 3 for b in bs),
                   key=lambda b: (DIFF_RANK.get(b["difficulty"], 9), b["title"].lower()))
    sections = [(c, bs) for c, bs in big]
    if small:
        sections.append(("Quick topics", small))

    mile = [0]

    def rcard(b):
        mile[0] += 1
        return (
            f'<li class="stop" data-mile="{mile[0]:02d}" data-cat="{b["category"]}">'
            f'<div class="card book" data-cat="{b["category"]}" data-title="{html.escape(b["title"])}">'
            f'<span class="num">{html.escape(b["category"])}</span><h3>{html.escape(b["title"])}</h3>'
            f'<p>{html.escape(b.get("description", ""))}</p>'
            f'<div class="dif"><i></i>{b["difficulty"]}</div>'
            f'<a class="read" href="../{reader_url(b)}">Read</a></div></li>'
        )

    jump = ("<div class=\"jumpnav\">" + "".join(
        f"<a href=\"#{slug(n)}\">{n} · {len(bs)}</a>" for n, bs in sections) + "</div>")
    body = '<div class="trip"><span>START · 01</span></div>' + "".join(
        f'<section class="shelf" id="{slug(n)}"><div class="shelf-head"><h2>{n}</h2>'
        f"<span>{len(bs)} book" + ("s" if len(bs) != 1 else "") + "</span></div>"
        f"<ol class=\"route\">" + "".join(rcard(b) for b in bs) + "</ol></section>"
        for n, bs in sections) + '<div class="trip"><span>FINISH · SHIP IT</span></div>'

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Roadmap — CICD BY Nabawy</title>
{seo_tags("Roadmap — CICD BY Nabawy", "Visual map of all 39 books grouped by category — the same source as the library.", f"{SITE_URL}/roadmap/")}
<style>{BASE_CSS}</style>
</head>
<body>
<header class="top"><div class="wrap">
<a class="logo" href="../index.html" style="color:inherit"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="5" cy="12" r="2.6" stroke="#18E299" stroke-width="2"/><circle cx="19" cy="6" r="2.6" stroke="#18E299" stroke-width="2"/><circle cx="19" cy="18" r="2.6" stroke="#18E299" stroke-width="2"/><path d="M7.6 12h5.2m0 0-2.6-2.6m2.6 2.6-2.6 2.6M13.4 7.4l2.8-1M13.4 16.6l2.8 1" stroke="#18E299" stroke-width="2" stroke-linecap="round"/></svg>CICD<span> BY Nabawy</span></a>
<nav class="crumbs"><span class="sep">/</span><span class="here">Roadmap</span></nav>
<div class="search"></div>
<a class="btn" href="../index.html" style="text-decoration:none">Library</a>
<a class="btn" href="../glossary.html" style="text-decoration:none">Glossary</a>
<button class="btn" id="themebtn" aria-label="Toggle theme">☀</button>
</div></header>
<div class="wrap">
<div class="hero" style="padding:36px 24px 16px"><span class="eyebrow">MAP</span><h1>Every book, <span>one map.</span></h1>
<p>{len(books)} docs grouped by category — same source as the library, impossible to drift.</p></div>
{jump}
{body}
</div>
<footer><div class="wrap"><span>CICD BY Nabawy</span><span>Markdown source → static reader · v2.0 Sep 2026</span></div></footer>
<script>
const $=s=>document.querySelector(s);
function getP(k,d){{try{{const v=JSON.parse(localStorage.getItem(k));return v??d}}catch(e){{return d}}}}
function setP(k,v){{try{{localStorage.setItem(k,JSON.stringify(v))}}catch(e){{}}}}
const pref=getP('cicdlib:pref',{{theme:'dark'}});
const THS=['dark','light','sepia','dim','contrast'],THI={{dark:'☀',light:'☾',sepia:'◐',dim:'◑',contrast:'◉'}};
function syncTheme(){{const th=THS.includes(pref.theme)?pref.theme:'dark';document.documentElement.dataset.theme=th;const t=$('#themebtn');if(t)t.textContent=THI[th]||'☀'}}
syncTheme();
$('#themebtn').onclick=()=>{{pref.theme=THS[(THS.indexOf(pref.theme)+1)%THS.length];setP('cicdlib:pref',pref);syncTheme()}};
</script>
</body>
</html>"""
    out = os.path.join(output_dir, "roadmap")
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(page)
    print(f"BUILT roadmap: {len(books)} books in {len(sections)} sections → {out}")


def build():
    books = json.load(open(os.path.join(ROOT, "content", "books.json"), encoding="utf-8"))
    os.makedirs(READ, exist_ok=True)
    build_roadmap_page(books, DIST)
    # shared icon library: single source (KB assets) copied into dist
    shutil.rmtree(os.path.join(DIST, "assets"), ignore_errors=True)
    shutil.copytree(os.path.join(KB, "assets"), os.path.join(DIST, "assets"))
    # print editions ship with the site so reader "Open print HTML" works live
    shutil.rmtree(os.path.join(DIST, "pdf"), ignore_errors=True)
    shutil.copytree(PDF, os.path.join(DIST, "pdf"))
    stats = []

    try:
        pathdata = json.load(open(os.path.join(ROOT, "content", "paths.json"), encoding="utf-8"))
        PATH_ORDER = pathdata.get("order", [])
        PATHS = pathdata.get("paths", {})
    except Exception:
        PATH_ORDER, PATHS = [], {}
    bypath = {}
    for b in books:
        bypath.setdefault(b.get("path", "ci-core"), []).append(b)
    byid = {b["id"]: b for b in books}

    def related_books(b, n=3):
        scored = []
        for o in bypath.get(b.get("path", ""), []):
            if o["id"] == b["id"]:
                continue
            score = len(set(b.get("tags", [])) & set(o.get("tags", []))) * 2 + (o["category"] == b["category"])
            scored.append((score, o))
        scored.sort(key=lambda t: (-t[0], t[1]["title"]))
        rel = [o for _, o in scored[:n]]
        if len(rel) < n:
            for o in books:
                if o["id"] != b["id"] and o not in rel:
                    rel.append(o)
                if len(rel) >= n:
                    break
        return rel

    def path_next(b):
        seq = bypath.get(b.get("path", ""), [])
        ids = [x["id"] for x in seq]
        if b["id"] in ids and ids.index(b["id"]) + 1 < len(ids):
            return byid[ids[ids.index(b["id"]) + 1]]
        return None

    all_sections = {}
    # P2.3: book id -> markdown source (from AUDIT_STRUCTURE mapping; 3 roadmaps are pdf-only)
    MD_MAP = {"foundations": "00-foundations/cicd-overview.md", "git-branching": "01-source-control/git-branching-pull-requests.md", "pipelines": "06-ci-cd-pipelines/pipelines.md", "artifacts": "05-artifacts-and-packaging/artifact-management.md", "delivery": "07-continuous-delivery/continuous-delivery.md", "strategies": "10-deployment-strategies/deployment-strategies.md", "ci": "02-continuous-integration/continuous-integration.md", "build": "03-build-systems/build-systems.md", "testing": "04-testing/testing-strategy.md", "deployment-auto": "08-continuous-deployment/continuous-deployment.md", "envs": "09-environments-and-release/environments-release.md", "security": "11-security/cicd-security.md", "rollback": "14-reliability-and-recovery/rollback-recovery.md", "lab-01": "16-labs/01-first-pipeline.md", "lab-02": "16-labs/02-build-and-test.md", "lab-03": "16-labs/03-artifacts.md", "lab-04": "16-labs/04-deployment.md", "lab-05": "16-labs/05-rollback.md", "lab-06": "16-labs/06-jenkins-controller.md", "lab-07": "16-labs/07-jenkins-shared-library.md", "lab-08": "16-labs/08-jenkins-backup-restore.md", "cheatsheet": "17-reference/command-cheatsheet.md", "gitlab": "15-platforms-and-tools/gitlab-ci.md", "argocd": "15-platforms-and-tools/argocd-gitops.md", "iac": "12-infrastructure-and-configuration/iac-environments.md", "observability": "13-observability-and-feedback/observability-feedback.md", "jenkins-domain": "15-platforms-and-tools/jenkins/README.md", "jenkins-architecture": "15-platforms-and-tools/jenkins/jenkins-architecture.md", "jenkins-setup": "15-platforms-and-tools/jenkins/jenkins-setup.md", "jenkins-pipelines": "15-platforms-and-tools/jenkins/jenkins-pipelines.md", "groovy": "15-platforms-and-tools/jenkins/jenkins-groovy-cheatsheet.md", "jenkins-agents": "15-platforms-and-tools/jenkins/jenkins-agents.md", "jenkins-credentials": "15-platforms-and-tools/jenkins/jenkins-credentials.md", "jenkins-plugins": "15-platforms-and-tools/jenkins/jenkins-plugins.md", "jenkins-webhooks": "15-platforms-and-tools/jenkins/jenkins-webhooks.md", "jenkins-security": "15-platforms-and-tools/jenkins/jenkins-security.md", "jenkins-advanced": "15-platforms-and-tools/jenkins/jenkins-advanced.md", "jenkins-troubleshooting": "15-platforms-and-tools/jenkins/jenkins-troubleshooting.md", "github-actions": "15-platforms-and-tools/github-actions.md"}
    all_body = {}
    for idx, b in enumerate(books):
        css, pages = parse_book(os.path.join(PDF, b["file"]))
        toc = toc_of(pages)
        all_sections[b["id"]] = [t for _, t, _ in toc][:16]
        # body text for section-level search: md source preferred (full), pdf fallback
        body_txt = ""
        try:
            mp = MD_MAP.get(b["id"])
            if mp and os.path.exists(os.path.join(KB, mp)):
                raw = open(os.path.join(KB, mp), encoding="utf-8").read()
                raw = re.sub(r"^---.*?---\s*", "", raw, flags=re.S)
                raw = re.sub(r"<!--.*?-->", " ", raw, flags=re.S)
                raw = re.sub(r"```.*?```", " ", raw, flags=re.S)
                raw = re.sub(r"[`#>*|\[\]()!]", " ", raw)
                raw = re.sub(r"\s+", " ", raw).strip()
                body_txt = raw[:5000]
            else:
                praw = open(os.path.join(PDF, b["file"]), encoding="utf-8").read()
                praw = re.sub(r"<style.*?</style>", " ", praw, flags=re.S | re.I)
                praw = re.sub(r"<[^>]+>", " ", praw)
                praw = html.unescape(re.sub(r"\s+", " ", praw)).strip()
                body_txt = praw[:5000]
        except Exception:
            body_txt = ""
        all_body[b["id"]] = body_txt
        prevb = books[idx - 1] if idx > 0 else None
        nextb = books[idx + 1] if idx + 1 < len(books) else None
        rels = related_books(b)
        upnext = path_next(b)
        is_lab = b.get("path") == "labs" or b["category"] == "Labs"
        # P2.2: path position + prereq context (derived from books.json, no new fields needed)
        pseq = bypath.get(b.get("path", ""), [])
        pids = [x["id"] for x in pseq]
        ppos = pids.index(b["id"]) + 1 if b["id"] in pids else 1
        ptotal = len(pseq) if pseq else 1
        plabel = PATHS.get(b.get("path", ""), {}).get("label", b.get("path", ""))
        preqs = b.get("prereqs", [])
        if preqs:
            preq_links = "".join(
                f'<a href="{p}.html">{html.escape(byid[p]["title"])}</a>' if p in byid else f'<span>{html.escape(p)}</span>'
                for p in preqs)
            prereq_html = f'<span class="prereq">Prereq:{preq_links}</span>'
        else:
            prereq_html = '<span class="prereq">Prereq: None — start here</span>'
        contextbar = (
            f'<div class="readcontext" data-testid="reader-context"><div class="wrap">'
            f'<a href="../index.html">Library</a><span>›</span>'
            f'<a href="../index.html#{html.escape(b.get("path", ""))}">{html.escape(plabel)}</a><span>›</span>'
            f'<span class="here">{html.escape(b["title"])}</span>'
            f'<span class="pathpos">{ppos} of {ptotal} in {html.escape(plabel)}</span>'
            f'{prereq_html}</div></div>')

        # flow mode: strip print chrome (per-page headers/footers, print notes)
        # so the book reads as one document, not stacked A4 sheets
        stripped = {"phead": 0, "pfoot": 0, "printnote": 0}
        flow_pages = []
        for p in pages:
            for cls in ("phead", "pfoot", "printnote"):
                p, n = re.subn(r'<div class="' + cls + r'">.*?</div>', "", p, flags=re.S)
                stripped[cls] += n
            flow_pages.append(p)
        pages = flow_pages

        body_pages = []
        for i, p in enumerate(pages):
            body_pages.append(re.sub(r'class="page', f'id="p{i+1}" class="page', p, count=1))
        toc_html = "".join(f'<a href="#p{i}" class="toc-l{lvl}" aria-label="{html.escape(t)}">{html.escape(t)}</a>' for i, t, lvl in toc)
        # P2 Top-5 #4: chapnav follows path order, not manifest order
        pprev = pseq[ppos - 2] if ppos > 1 else None
        pnext = pseq[ppos] if ppos < ptotal else None
        prev_link = f'<a id="prevbook" href="{pprev["id"]}.html"><small>← {html.escape(plabel)}</small>{html.escape(pprev["title"])}</a>' if pprev else "<span></span>"
        next_link = f'<a id="nextbook" class="r" href="{pnext["id"]}.html"><small>{html.escape(plabel)} →</small>{html.escape(pnext["title"])}</a>' if pnext else "<span></span>"
        tocbtn_label = f'☰ Contents · {len(toc)}'
        top_upnext = f'<div class="upnext upnext-top">Up next in {html.escape(plabel)} → <a href="{upnext["id"]}.html"><b>{html.escape(upnext["title"])}</b></a></div>' if upnext else ""

        page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{html.escape(b['title'])} — CICD BY Nabawy</title>
{seo_tags(f"{b['title']} — CICD BY Nabawy", b.get("description",""), f"{SITE_URL}/read/{b['id']}.html", og_type="article", image=f"{SITE_URL}/og/{b['id']}.svg")}
{(f'<link rel="prefetch" href="{upnext["id"]}.html">' if upnext else '') + (f'<link rel="prefetch" href="{nextb["id"]}.html">' if nextb and (not upnext or nextb["id"] != upnext["id"]) else '')}
<style>{BASE_CSS}</style>
{f'<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":"TechArticle","headline":b["title"],"description":b.get("description",""),"url":SITE_URL + "/read/" + b["id"] + ".html","author":{"@type":"Person","name":"Nabawy"},"isPartOf":{"@type":"CollectionPage","name":"CICD BY Nabawy","url":SITE_URL}})}</script>'}
{f'<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Library","item":SITE_URL + "/"},{"@type":"ListItem","position":2,"name":b["title"],"item":SITE_URL + "/read/" + b["id"] + ".html"}]})}</script>'}
<style>{css}
/* reader overrides */
.readbody .page:not(.cover){{width:auto !important;min-height:0 !important;margin:0 auto !important;padding:10px 26px !important;background:transparent !important;border-radius:0;page-break-after:auto !important;overflow:visible}}
.readbody .page.cover{{align-items:flex-start !important;border-radius:16px;padding:48px 34px !important;margin:0 auto 30px !important}}
.readbody .page.opener .bignum{{margin-top:30px}}
[data-theme=dark] .readbody{{--paper:#10161d;--white:#151c25;--ink:#e6edf3;--muted:#8b949e;--line:#26303d;--panel:#0a0e14;--text-light:#e6edf3}}
[data-theme=dark] .readbody table.cmp td:first-child{{background:var(--white)}}
[data-theme=dark] .readbody .fnode.gate{{background:rgba(217,154,36,.12)}}
[data-theme=dark] .readbody .i-gr{{background:var(--muted)}}
</style>
</head>
<body data-book="{b['id']}">
<header class="top"><div class="wrap">
<button class="btn tocbtn" id="tocbtn">{tocbtn_label}</button>
<nav class="crumbs"><a class="logo" href="../index.html" style="color:inherit"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="5" cy="12" r="2.6" stroke="#18E299" stroke-width="2"/><circle cx="19" cy="6" r="2.6" stroke="#18E299" stroke-width="2"/><circle cx="19" cy="18" r="2.6" stroke="#18E299" stroke-width="2"/><path d="M7.6 12h5.2m0 0-2.6-2.6m2.6 2.6-2.6 2.6M13.4 7.4l2.8-1M13.4 16.6l2.8 1" stroke="#18E299" stroke-width="2" stroke-linecap="round"/></svg>CICD<span> BY Nabawy</span></a>
<span class="sep">/</span>
<span class="here">{html.escape(b['title'])}</span></nav>
<div class="search"><input id="q" type="search" placeholder="Find in this book…" aria-label="Find in this book"><kbd>⌘K</kbd></div>
<span id="qcount" style="font-size:12px;color:var(--mut)"></span>
<button class="markbtn" id="markbtn" aria-label="Bookmark this book">☆ Save</button>
<a class="btn" href="../book/{b['id']}.html" style="text-decoration:none">Overview</a>
<button class="btn" id="setbtn" aria-label="Reading settings">⚙ A⁺</button>
</div>
<div class="prog" style="height:3px;background:var(--line)"><b id="pbar" style="display:block;height:100%;width:0;background:var(--acc)"></b></div>
</header>
{contextbar}
<div class="rlayout">
<aside class="toc"><h4>CONTENTS · {len(pages)} PAGES · {len(toc)} SECTIONS</h4>{toc_html}
<div style="margin-top:14px"><a href="../pdf/{b['file']}">⭳ Open print HTML</a></div>
</aside>
<main class="read"><div class="readbody">
{top_upnext}
{f'<div class="labbanner">🧪 Hands-on lab · {b.get("time_minutes", 45)} min · Env: {html.escape(b.get("lab_env", "See book overview"))} · <a href="../book/' + b["id"] + '.html">Overview &amp; prereqs</a> · <button class="markbtn" id="labreset" style="margin-left:8px">Reset checks</button></div>' if is_lab else ''}
{''.join(body_pages)}
{f'<div class="upnext">Up next in {html.escape(PATHS.get(b.get("path", ""), {}).get("label", b.get("path", "")))} → <a href="{upnext["id"]}.html"><b>{html.escape(upnext["title"])}</b></a></div>' if upnext else ''}
<div class="relatedbox"><h4>Related books</h4><ul>{"".join(f'<li><a href="{r["id"]}.html">{html.escape(r["title"])}</a></li>' for r in rels)}</ul></div>
<div class="ratebox" id="ratebox"><span>Was this book useful?</span><button id="rateup" aria-label="Mark useful">👍 Yes</button><button id="ratedown" aria-label="Mark not useful">👎 No</button><span id="ratethanks" style="color:var(--mut)"></span></div>
<div class="chapnav">{prev_link}{next_link}</div>
</div></main>
<div id="lightbox" role="dialog" aria-label="Diagram viewer"><img alt="Enlarged diagram"></div>
</div>
<div class="drawer" id="drawer"><div class="scrim"></div><div class="panel">
<h3>Reading settings</h3>
<div class="setrow"><h5>THEME</h5><div class="opts">
<button class="btn" data-k="theme" data-set="dark" onclick="setOpt('theme','dark')">Dark</button>
<button class="btn" data-k="theme" data-set="light" onclick="setOpt('theme','light')">Light</button>
<button class="btn" data-k="theme" data-set="sepia" onclick="setOpt('theme','sepia')">Sepia</button>
<button class="btn" data-k="theme" data-set="dim" onclick="setOpt('theme','dim')">Dim</button>
<button class="btn" data-k="theme" data-set="contrast" onclick="setOpt('theme','contrast')">Contrast</button></div></div>
<div class="setrow"><h5>FONT</h5><div class="opts">
<button class="btn" data-k="font" data-set="sans" onclick="setOpt('font','sans')">Sans</button>
<button class="btn" data-k="font" data-set="serif" onclick="setOpt('font','serif')">Serif</button></div></div>
<div class="setrow"><h5>LINE HEIGHT</h5><div class="opts">
<button class="btn" data-k="lh" data-set="1.6" onclick="setOpt('lh',1.6)">Tight</button>
<button class="btn" data-k="lh" data-set="1.7" onclick="setOpt('lh',1.7)">Comfort</button>
<button class="btn" data-k="lh" data-set="1.9" onclick="setOpt('lh',1.9)">Roomy</button></div></div>
<div class="setrow"><h5>TEXT SIZE</h5><div class="opts">
<button class="btn" data-k="fs" data-set="16" onclick="setOpt('fs',16)">A−</button>
<button class="btn" data-k="fs" data-set="18" onclick="setOpt('fs',18)">A</button>
<button class="btn" data-k="fs" data-set="20" onclick="setOpt('fs',20)">A+</button>
<button class="btn" data-k="fs" data-set="22" onclick="setOpt('fs',22)">A++</button></div></div>
<div class="setrow"><h5>READING WIDTH</h5><div class="opts">
<button class="btn" data-k="width" data-set="680px" onclick="setOpt('width','680px')">Narrow</button>
<button class="btn" data-k="width" data-set="820px" onclick="setOpt('width','820px')">Comfortable</button>
<button class="btn" data-k="width" data-set="1020px" onclick="setOpt('width','1020px')">Wide</button></div></div>
<div class="setrow"><h5>SHORTCUTS</h5><p style="font-size:12px;color:var(--mut)">Ctrl+K search · T contents · ←/→ prev/next book · Esc close</p></div>
</div></div>
<script>{READER_JS}</script>
</body>
</html>"""
        open(os.path.join(READ, b["id"] + ".html"), "w", encoding="utf-8").write(page)
        stats.append((b, len(pages), len(toc)))

    cats = sorted(set(b["category"] for b in books))
    byid = {b["id"]: b for b in books}
    CAT_ORDER = ["CI/CD", "Delivery", "Build", "Testing", "Security", "Reliability", "Jenkins", "GitHub", "Platforms", "Labs", "Reference"]
    cats = [c for c in CAT_ORDER if c in byid or any(b["category"] == c for b in books)] + [c for c in cats if c not in CAT_ORDER]
    def card(b, i):
        initials = "".join(w[0] for w in re.sub(r"[^A-Za-z0-9 ]", "", b["title"]).split()[:2]).upper()
        tmin = b.get("time_minutes", 30)
        tags = " ".join(b.get("tags", []))
        return (
            f'<div class="card book" data-id="{b["id"]}" data-cat="{html.escape(b["category"])}" data-dif="{html.escape(b["difficulty"])}" data-time="{tmin}" data-tags="{html.escape(tags)}" data-title="{html.escape(b["title"])}" data-desc="{html.escape(b["description"])}">'
            f'<div class="coverart" aria-hidden="true"><b>{initials}</b></div>'
            f'<span class="num">PDF {i+1:02d} · {tmin} min · Updated {html.escape(b.get("updated", ""))}</span><h3><a href="book/{b["id"]}.html">{html.escape(b["title"])}</a></h3><p>{html.escape(b["description"])}</p>'
            f'<div class="dif"><i></i>{b["difficulty"]} · {html.escape(b.get("path", ""))}</div>'
            f'<div class="meta-line">{stats[i][1]} pages · {stats[i][2]} sections · v{b.get("version", "2.0")}</div>'
            f'<div class="prog"><b style="width:0%"></b></div>'
            f'<span><a class="read" href="{reader_url(b)}">Read</a> <a href="book/{b["id"]}.html" style="font-size:13px;color:var(--mut)">Overview</a></span></div>'
        )
    idx_of = {b["id"]: i for i, b in enumerate(books)}
    series_files = sorted(glob.glob(os.path.join(PDF, "series", "*.html")))
    def series_title(p):
        m = re.search(r"<title>(.*?)</title>", open(p, encoding="utf-8").read(), re.S)
        t = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else os.path.basename(p)
        return t.split(":", 1)[-1].strip()
    def series_card(p):
        h = open(p, encoding="utf-8").read()
        npages = h.count('class="page cover"') + h.count('class="page opener"') + h.count('class="page"')
        code = os.path.basename(p)[1:3]
        t = series_title(p)
        return (
            f'<div class="card book" data-title="{html.escape(t)}" data-cat="Series" data-desc="omnibus print edition series">'
            f'<span class="num">S{code}</span><h3>{html.escape(t)}</h3><p>Omnibus print edition — {npages} pages, chapters keep their numbers.</p>'
            f'<div class="dif"><i></i>Print</div>'
            f'<div class="meta-line">{npages} pages</div>'
            f'<a class="read" href="pdf/series/{os.path.basename(p)}">Open</a></div>'
        )
    CAT_COLORS = {"CI/CD": "#5B8DEF", "Build": "#F5A524", "Testing": "#2ECC71",
                  "Security": "#E5484D", "Reliability": "#9B7BF0", "Jenkins": "#22B8CF",
                  "Delivery": "#F472B6", "GitHub": "#94A3B8", "Platforms": "#F97316",
                  "Labs": "#EAB308", "Reference": "#64748B"}
    CORES = ["Build", "Testing", "Security", "Reliability"]

    def shelf(name, count, color, inner, grid=False, sid=""):
        arrows = ""
        if not grid:
            arrows = ('<span class="arrows"><button data-dir="-1" aria-label="Scroll left">←</button>'
                      '<button data-dir="1" aria-label="Scroll right">→</button></span>')
        wrap = f'<div class="cores-grid">{inner}</div>' if grid else f'<div class="rail">{inner}</div>'
        return (f'<section class="shelf" id="{sid}" style="--cat:{color}"><div class="shelf-head"><h2>{name}</h2>'
                f"<span>{count}</span>{arrows}</div>{wrap}</section>")

    def slug(name):
        return "shelf-" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

    bycat = {}
    for b in books:
        bycat.setdefault(b["category"], []).append(b)
    cores = [(c, [b for b in books if b["category"] == c]) for c in CORES]
    core_books = [b for _, bs in cores for b in bs]
    big = sorted(((c, bs) for c, bs in bycat.items() if c not in CORES and len(bs) >= 3),
                 key=lambda t: -len(t[1]))
    small = sorted(((c, bs) for c, bs in bycat.items() if c not in CORES and len(bs) < 3),
                   key=lambda t: -len(t[1]))
    small_books = [b for _, bs in small for b in bs]

    sections = []
    for c, bs in big:
        sections.append({"name": c, "n": len(bs), "grid": False, "color": CAT_COLORS.get(c, "#18E299"),
                         "inner": "".join(card(b, idx_of[b["id"]]) for b in bs)})
    sections.append({"name": "Series edition", "n": len(series_files), "grid": False, "color": "#18E299",
                     "inner": "".join(series_card(p) for p in series_files)})
    if core_books:
        sections.append({"name": "Core practices", "n": len(core_books), "grid": True, "color": "#18E299",
                         "inner": "".join(card(b, idx_of[b["id"]]) for b in core_books)})
    if small_books:
        sections.append({"name": "Quick topics", "n": len(small_books), "grid": True, "color": "#18E299",
                         "inner": "".join(card(b, idx_of[b["id"]]) for b in small_books)})
    sections.sort(key=lambda s: (-s["n"], 0 if not s["grid"] else 1))
    series_sec = [s for s in sections if s["name"] == "Series edition"]
    sections = [s for s in sections if s["name"] != "Series edition"] + series_sec
    ogdir = os.path.join(DIST, "og")
    os.makedirs(ogdir, exist_ok=True)
    for b in books:
        open(os.path.join(ogdir, b["id"] + ".svg"), "w", encoding="utf-8").write(og_svg(b["title"], b["category"], CAT_COLORS.get(b["category"], "#18E299")))
    open(os.path.join(ogdir, "library.svg"), "w", encoding="utf-8").write(og_svg("Technical Library", "CI/CD", "#18E299"))
    jump = ("<div class=\"jumpnav\">" + "".join(
        f"<a href=\"#{slug(s['name'])}\">{s['name']}</a>" for s in sections) + "</div>")
    rendered = "".join(
        shelf(s["name"], f"{s['n']} book" + ("s" if s["n"] != 1 else ""), s["color"], s["inner"],
              grid=s["grid"], sid=slug(s["name"])) for s in sections)
    SHOW_FIRST = 5
    if len(sections) > SHOW_FIRST:
        parts = rendered.split("</section>", SHOW_FIRST)
        shelves_html = ("</section>".join(parts[:SHOW_FIRST]) + "</section>"
                        f'<div class="morewrap"><button class="btn" id="morebtn">Browse all topics ↓</button></div>'
                        f'<div id="morecats" style="display:none">' + parts[SHOW_FIRST] + "</div>")
    else:
        shelves_html = rendered

    search_idx = [{"id": b["id"], "title": b["title"], "desc": b.get("description", ""), "cat": b["category"], "dif": b["difficulty"], "tags": b.get("tags", []), "time": b.get("time_minutes", 30), "sections": all_sections.get(b["id"], []), "body": all_body.get(b["id"], "")[:2000]} for b in books]
    # P2.1: single recommended cold-start path (Beginner, prereq-chain verified)
    RECOMMENDED = ["foundations", "git-branching", "pipelines", "ci", "lab-01"]
    rec_seq = [byid[i] for i in RECOMMENDED if i in byid]
    rec_total = sum(b.get("time_minutes", 30) for b in rec_seq)
    rec_steps = "".join(
        f'<li><span class="n">STEP {n}</span><b><a href="read/{b["id"]}.html">{html.escape(b["title"])}</a></b>'
        f'<span>{b.get("time_minutes", 30)} min · {b["difficulty"]}</span></li>'
        for n, b in enumerate(rec_seq, 1))
    first = rec_seq[0] if rec_seq else None
    rec_html = (
        f'<section class="recstrip" data-testid="recommended-path" aria-label="Recommended reading path for beginners">'
        f'<div class="rec-head"><span class="eyebrow">★ Start here — new to CI/CD</span>'
        f'<span class="rec-meta">{len(rec_seq)} books · ~{rec_total} min · Beginner</span></div>'
        f'<ol class="rec-steps">{rec_steps}</ol>'
        + (f'<a class="rec-cta" href="read/{first["id"]}.html">★ Start with {html.escape(first["title"])} — {first.get("time_minutes", 30)} min →</a>' if first else '')
        + f'</section>') if rec_seq else ""
    paths_html = ""
    for pid in (PATH_ORDER or sorted(bypath.keys())):
        seq = bypath.get(pid, [])
        if not seq:
            continue
        label = PATHS.get(pid, {}).get("label", pid)
        desc = PATHS.get(pid, {}).get("desc", "")
        tmin = sum(b.get("time_minutes", 30) for b in seq)
        lis = "".join(f'<li><a href="read/{b["id"]}.html"><b>{html.escape(b["title"])}</b></a> · {b.get("time_minutes", 30)} min · {b["difficulty"]}</li>' for b in seq)
        paths_html += f'<div class="pathcard"><h3>{html.escape(label)}</h3><p>{html.escape(desc)}</p><ol>{lis}</ol><div class="meta">{len(seq)} books · ~{tmin} min</div></div>'

    index = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CICD BY Nabawy</title>
{seo_tags("CICD BY Nabawy", SITE_DESC, f"{SITE_URL}/", image=f"{SITE_URL}/og/library.svg")}
<style>{BASE_CSS}</style>
<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":"CollectionPage","name":"CICD BY Nabawy","description":SITE_DESC,"url":SITE_URL,"hasPart":[{"@type":"TechArticle","name":b["title"],"url":SITE_URL + "/read/" + b["id"] + ".html"} for b in books]})}</script>
</head>
<body>
<header class="top"><div class="wrap">
<span class="logo"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="5" cy="12" r="2.6" stroke="#18E299" stroke-width="2"/><circle cx="19" cy="6" r="2.6" stroke="#18E299" stroke-width="2"/><circle cx="19" cy="18" r="2.6" stroke="#18E299" stroke-width="2"/><path d="M7.6 12h5.2m0 0-2.6-2.6m2.6 2.6-2.6 2.6M13.4 7.4l2.8-1M13.4 16.6l2.8 1" stroke="#18E299" stroke-width="2" stroke-linecap="round"/></svg>CICD<span> BY Nabawy</span></span>
<div class="search"><div class="searchwrap"><input id="q" type="search" placeholder="Search all {len(books)} books…" autocomplete="off"><div class="searchdrop" id="qdrop" role="listbox"></div></div><kbd>⌘K</kbd></div>
<a class="btn" href="roadmap/">Roadmap</a>
<a class="btn" href="glossary.html" style="text-decoration:none">Glossary</a>
<button class="btn" id="themebtn" aria-label="Toggle theme">☀</button>
</div></header>
<div class="wrap">
<div class="hero"><span class="eyebrow">CI/CD ENGINEERING MANUAL</span><h1>From commit to production, <span>explained end to end.</span></h1>
<p>{len(books)} concise technical books: fundamentals, pipelines, artifacts, delivery, Jenkins, GitHub Actions, security, reliability — plus hands-on labs.</p>
<div class="stats"><span><b>{len(books)}</b> books</span><span><b>{len(cats)}</b> topics</span><span><b>{sum(1 for b in books if b["category"]=="Labs")}</b> hands-on labs</span><span>BY Nabawy</span></div></div>
<div id="continue"></div>
<div id="marksrow"></div>
{rec_html}
<div class="collectlabel">LEARNING PATHS</div>
<p class="sub">Ordered end to end — follow a path, don't wander shelves.</p>
<div class="pathgrid">{paths_html}</div>
<div class="collectlabel">LEVELS</div>
<div class="rubric"><div><b>Beginner</b>No prior CI/CD. Start with Foundations → Git → Pipelines.</div><div><b>Intermediate</b>Built a pipeline. Tackle artifacts, delivery, Jenkins core, labs.</div><div><b>Advanced</b>Runs prod. Security, Jenkins advanced, GitOps, recovery drills.</div></div>
<div class="collectlabel">BROWSE EVERYTHING</div>
<div class="filterbar"><select id="fcat" aria-label="Filter by category"><option value="">All categories</option></select><select id="fdif" aria-label="Filter by level"><option value="">All levels</option><option>Beginner</option><option>Intermediate</option><option>Advanced</option></select><select id="fsort" aria-label="Sort books"><option value="">Path order</option><option value="az">A–Z</option><option value="time">Shortest</option><option value="level">Level</option></select><span class="count" id="fcount"></span></div>
<div class="filterbar"><a class="btn" href="read/foundations.html">★ Start here: Foundations</a><a class="btn" href="read/lab-01.html">Hands-on: Lab 01</a><a class="btn" href="read/cheatsheet.html">Cheatsheet</a></div>
<div class="popsearch" id="popsearch"></div>
{jump}
{shelves_html}
<div class="empty" id="empty" style="display:none">No books found. Try another search — or start with <a href="read/foundations.html">Foundations</a>.</div>
</div>
<a id="resume" href="#" style="display:none">Resume</a>
<footer><div class="wrap"><span>CICD BY Nabawy</span><span><a href="updates.html">Updates</a> · <a href="glossary.html">Glossary</a> · <a href="roadmap/">Roadmap</a> · v2.1 Sep 2026</span></div></footer>
<script>window.SEARCH_IDX={json.dumps(search_idx, ensure_ascii=False)};</script>
<script>{INDEX_JS}</script>
<script>
$$('.book').forEach(c=>{{const p=getP(PROG+c.dataset.id,null);if(p&&p.pct>0)c.querySelector('.prog b').style.width=p.pct+'%'}});
try{{const cats=[...new Set($$('.book[data-id]').map(c=>c.dataset.cat))].sort();const fc=$('#fcat');cats.forEach(c=>{{const o=document.createElement('option');o.textContent=c;fc.appendChild(o);}});const h=new URLSearchParams(location.hash.slice(1));if(h.get('cat'))fc.value=h.get('cat');filter();}}catch(e){{}}
</script>
</body>
</html>"""
    open(os.path.join(DIST, "index.html"), "w", encoding="utf-8").write(index)

    # glossary (dedupe by term, anchor links)
    rows = re.findall(r"^\| ([^|]+) \| ([^|]+) \| ([^|]+) \|", open(os.path.join(KB, "GLOSSARY.md"), encoding="utf-8").read(), re.M)
    seen = set()
    grows = ""
    for t, d, r in rows:
        t = t.strip()
        if "Term" in t or "---" in t or t.lower() in seen:
            continue
        seen.add(t.lower())
        slug = re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")
        grows += f'<tr id="g-{slug}"><td><b>{html.escape(t)}</b></td><td>{html.escape(d.strip())}</td><td>{html.escape(r.strip())}</td><td><a href="#g-{slug}">#</a></td></tr>'
    gloss = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Glossary — CICD BY Nabawy</title>{seo_tags("Glossary — CICD BY Nabawy", "CI/CD glossary: terms shared by all books, reader and search.", f"{SITE_URL}/glossary.html")}<style>{BASE_CSS}</style></head>
<body>
<header class="top"><div class="wrap"><a class="logo" href="index.html" style="text-decoration:none;color:inherit"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="5" cy="12" r="2.6" stroke="#18E299" stroke-width="2"/><circle cx="19" cy="6" r="2.6" stroke="#18E299" stroke-width="2"/><circle cx="19" cy="18" r="2.6" stroke="#18E299" stroke-width="2"/><path d="M7.6 12h5.2m0 0-2.6-2.6m2.6 2.6-2.6 2.6M13.4 7.4l2.8-1M13.4 16.6l2.8 1" stroke="#18E299" stroke-width="2" stroke-linecap="round"/></svg>CICD<span> BY Nabawy</span></a>
<div class="search"><input id="q" type="search" placeholder="Filter terms…"></div><a class="btn" href="roadmap/" style="text-decoration:none">Roadmap</a></div></header>
<div class="wrap"><h2 class="sec">Glossary</h2><p class="sub">{len(re.findall('<tr>', grows))} terms · shared by books, reader and search</p>
<table class="gloss"><tr><th>Term</th><th>Definition</th><th>Topic</th><th>Link</th></tr>{grows}</table></div>
<footer><div class="wrap">CICD BY Nabawy</div></footer>
<script>{BASE_JS}
$('#q').addEventListener('input',e=>{{const q=e.target.value.toLowerCase();
$$('table.gloss tr').forEach((r,i)=>{{if(!i)return;r.style.display=r.textContent.toLowerCase().includes(q)?'':'none'}})}});
</script></body></html>"""
    open(os.path.join(DIST, "glossary.html"), "w", encoding="utf-8").write(gloss)

    # --- P1: book landing pages ---
    bookdir = os.path.join(DIST, "book")
    os.makedirs(bookdir, exist_ok=True)
    for i, b in enumerate(books):
        rels = related_books(b)
        upnext = path_next(b)
        toc = [t for _, t, _ in toc_of(parse_book(os.path.join(PDF, b["file"]))[1])][:12]
        preq = "".join(f'<a href="{p}.html">{html.escape(byid[p]["title"])}</a>' if p in byid else f'<span>{html.escape(p)}</span>' for p in b.get("prereqs", [])) or "<span>None — start here</span>"
        outs = "".join(f"<li>{html.escape(o)}</li>" for o in b.get("outcomes", [])) or "<li>Read the full book</li>"
        initials = "".join(w[0] for w in re.sub(r"[^A-Za-z0-9 ]", "", b["title"]).split()[:2]).upper()
        bp = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>{html.escape(b['title'])} — Overview — CICD BY Nabawy</title>{seo_tags(b['title'] + " — Overview — CICD BY Nabawy", b.get("description", ""), f"{SITE_URL}/book/{b['id']}.html", image=f"{SITE_URL}/og/{b['id']}.svg")}<link rel="prefetch" href="../read/{b['id']}.html"><style>{BASE_CSS}</style>
{f'<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Library","item":SITE_URL + "/"},{"@type":"ListItem","position":2,"name":b["title"],"item":SITE_URL + "/book/" + b["id"] + ".html"}]})}</script>'}></head>
<body><header class="top"><div class="wrap"><a class="logo" href="../index.html" style="color:inherit">CICD<span> BY Nabawy</span></a><nav class="crumbs"><span class="sep">/</span><span class="here">{html.escape(b['title'])}</span></nav><div class="search"></div><a class="btn" href="../index.html">Library</a><button class="btn" id="themebtn">☀</button></div></header>
<div class="wrap"><div class="bookhero"><div class="coverart" data-cat="{html.escape(b['category'])}"><b>{initials}</b></div><div style="flex:1;min-width:260px"><span class="num">{html.escape(b['category'])} · {b['difficulty']} · {b.get('time_minutes', 30)} min · v{b.get('version', '2.0')} · Updated {html.escape(b.get('updated', ''))}</span><h1 style="font-size:34px;margin:6px 0">{html.escape(b['title'])}</h1><p class="sub">{html.escape(b.get('description', ''))}</p>
<div class="chiprow"><a id="startbtn" href="../read/{b['id']}.html">Start reading →</a><a href="../pdf/{b['file']}">Open print HTML</a><a href="../read/{b['id']}.html">Reader</a></div>
<div class="chiprow"><span>Prereqs:</span>{preq}</div></div></div>
<div class="outcomes"><b>What you'll learn</b><ul>{outs}</ul></div>
<h2 class="sec" style="margin-top:20px">Contents preview</h2><ul class="labcheck">{"".join(f"<li>{html.escape(t)}</li>" for t in toc)}</ul>
{f'<div class="upnext">Up next in {html.escape(PATHS.get(b.get("path", ""), {}).get("label", b.get("path", "")))} → <a href="{upnext["id"]}.html"><b>{html.escape(upnext["title"])}</b></a></div>' if upnext else ''}
<div class="relatedbox"><h4>Related books</h4><ul>{"".join(f'<li><a href="{r["id"]}.html">{html.escape(r["title"])}</a></li>' for r in rels)}</ul></div>
</div><footer><div class="wrap"><span>CICD BY Nabawy</span></div></footer>
<script>{BASE_JS}
const pref=getP('cicdlib:pref',{{theme:'dark'}});const THX=['dark','light','sepia','dim','contrast'];document.documentElement.dataset.theme=THX.includes(pref.theme)?pref.theme:'dark';
$('#themebtn').onclick=()=>{{pref.theme=THX[(THX.indexOf(pref.theme)+1)%THX.length];setP('cicdlib:pref',pref);document.documentElement.dataset.theme=pref.theme;}};
try{{const p=getP('cicdlib:prog:{b['id']}',null);if(p&&p.pct>0&&p.pct<100)$('#startbtn').textContent='Continue reading — '+p.pct+'% →';}}catch(e){{}}
</script></body></html>"""
        open(os.path.join(bookdir, b["id"] + ".html"), "w", encoding="utf-8").write(bp)

    # --- P1: updates page ---
    rows_u = "".join(f'<tr><td><a href="book/{b["id"]}.html">{html.escape(b["title"])}</a></td><td>{html.escape(b["category"])}</td><td>{b["difficulty"]}</td><td>v{html.escape(b.get("version", "2.0"))}</td><td>{html.escape(b.get("updated", ""))}</td><td>{b.get("time_minutes", 30)} min</td></tr>' for b in books)
    upd = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Updates — CICD BY Nabawy</title>{seo_tags("Updates — CICD BY Nabawy", "What changed across the library.", f"{SITE_URL}/updates.html")}<style>{BASE_CSS}</style></head><body><header class="top"><div class="wrap"><a class="logo" href="index.html" style="color:inherit">CICD<span> BY Nabawy</span></a><nav class="crumbs"><span class="sep">/</span><span class="here">Updates</span></nav></div></header><div class="wrap"><h2 class="sec">Updates</h2><p class="sub">{len(books)} books · P0+P1 shipped Sep 2026: metadata, filters, paths, bookmarks, related, lab checks</p><table class="gloss"><tr><th>Book</th><th>Category</th><th>Level</th><th>Ver</th><th>Updated</th><th>Time</th></tr>{rows_u}</table></div></body></html>"""
    open(os.path.join(DIST, "updates.html"), "w", encoding="utf-8").write(upd)

    # --- SEO: sitemap + robots ---
    from datetime import date as _d
    today = _d.today().isoformat()
    urls = [SITE_URL + "/", SITE_URL + "/glossary.html", SITE_URL + "/roadmap/", SITE_URL + "/updates.html"]
    for b in books:
        urls.append(f"{SITE_URL}/read/{b['id']}.html")
        urls.append(f"{SITE_URL}/book/{b['id']}.html")
    for q in sorted(pathlib.Path(os.path.join(DIST, "pdf")).rglob("*.html")):
        rel = q.relative_to(pathlib.Path(DIST)).as_posix()
        urls.append(f"{SITE_URL}/{rel}")
    sm = '<?xml version="1.0" encoding="UTF-8"?>' + chr(10) + '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + chr(10) + chr(10).join(f"  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>" for u in urls) + chr(10) + '</urlset>' + chr(10)
    pathlib.Path(os.path.join(DIST, "sitemap.xml")).write_text(sm, encoding="utf-8")
    pathlib.Path(os.path.join(DIST, "robots.txt")).write_text(f"User-agent: *{chr(10)}Allow: /{chr(10)}Sitemap: {SITE_URL}/sitemap.xml{chr(10)}", encoding="utf-8")

    # --- P0: 404 + search index ---
    notfound = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Not found — CICD BY Nabawy</title><meta name="theme-color" content="#0B0D10"><style>{BASE_CSS}</style></head><body><div class="wrap" style="text-align:center;padding:80px 20px"><h1>Page not found</h1><p class="sub">Try search or start with Foundations.</p><p><a class="btn" href="index.html">Library</a> <a class="btn" href="read/foundations.html">Foundations</a> <a class="btn" href="glossary.html">Glossary</a></p></div></body></html>"""
    pathlib.Path(os.path.join(DIST, "404.html")).write_text(notfound, encoding="utf-8")
    search_idx = [{"id": b["id"], "title": b["title"], "desc": b.get("description", ""), "cat": b["category"], "dif": b["difficulty"], "tags": b.get("tags", []), "time": b.get("time_minutes", 30), "sections": all_sections.get(b["id"], []), "body": all_body.get(b["id"], "")[:2000]} for b in books]
    pathlib.Path(os.path.join(DIST, "search.json")).write_text(json.dumps(search_idx, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"BUILT {len(books)} books + {len(books)} overviews + index + glossary + updates → {DIST}")


if __name__ == "__main__":
    build()
