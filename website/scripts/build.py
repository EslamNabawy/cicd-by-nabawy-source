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
SITE_DESC = "14 merged handbooks: CI/CD fundamentals, pipelines, artifacts, delivery, Jenkins, GitHub Actions, security, reliability \u2014 plus hands-on labs. By Nabawy."

def seo_tags(title, desc, canonical, og_type="website", image=None):
    d = html.escape(desc, quote=True)
    t = html.escape(title, quote=True)
    c = html.escape(canonical, quote=True)
    parts = [
        f'<link rel="icon" type="image/svg+xml" href="{SITE_URL}/favicon.svg">',
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


FAVICON_SVG = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="14" fill="#0B0D10"/><g fill="none" stroke="#18E299" stroke-width="5" stroke-linecap="round"><circle cx="17" cy="32" r="7"/><circle cx="47" cy="17" r="7"/><circle cx="47" cy="47" r="7"/><path d="M24 32h11m0 0-6-6m6 6-6 6M36 20l6-2M36 44l6 2"/></g></svg>'

def og_svg(title, category, color):
    t = html.escape(title[:28])
    c = html.escape(category)
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630"><rect width="1200" height="630" fill="#0B0D10"/><rect width="1200" height="14" fill="{color}"/><circle cx="120" cy="120" r="34" fill="none" stroke="#18E299" stroke-width="8"/><text x="80" y="330" font-family="monospace" font-size="44" fill="#18E299">{c}</text><text x="80" y="430" font-family="sans-serif" font-weight="bold" font-size="84" fill="#ededed">{t}</text><text x="80" y="500" font-family="sans-serif" font-size="36" fill="#a0a0a0">CICD BY Nabawy</text></svg>'


try:
    from PIL import Image as _PILImage, ImageDraw as _PILDraw, ImageFont as _PILFont
    _PIL = True
except Exception:
    _PIL = False
OG_EXT = "png" if _PIL else "svg"


def og_png(title, category, color):
    """1200x630 social card mirroring og_svg. PNG bytes, or None without Pillow."""
    if not _PIL:
        return None
    import io as _io
    W, H = 1200, 630
    img = _PILImage.new("RGB", (W, H), "#0B0D10")
    dr = _PILDraw.Draw(img)
    dr.rectangle([0, 0, W, 14], fill=color)
    dr.ellipse([86, 86, 154, 154], outline="#18E299", width=8)
    def _font(name, size):
        try:
            return _PILFont.truetype(name, size)
        except Exception:
            return _PILFont.load_default()
    fcat = _font("arial.ttf", 44)
    ftitle = _font("arialbd.ttf", 84)
    ffoot = _font("arial.ttf", 36)
    dr.text((80, 270), str(category)[:28], font=fcat, fill="#18E299")
    words, lines, cur = str(title).split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if dr.textlength(t, font=ftitle) > 1040 and cur:
            lines.append(cur)
            cur = w
        else:
            cur = t
    lines.append(cur)
    lines = lines[:2]
    y = 340
    for ln in lines:
        dr.text((80, y), ln, font=ftitle, fill="#ededed")
        y += 100
    dr.text((80, 500), "CICD BY Nabawy", font=ffoot, fill="#a0a0a0")
    buf = _io.BytesIO()
    img.save(buf, "PNG")
    return buf.getvalue()
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
header.top{position:sticky;top:0;background:color-mix(in srgb,var(--bg) 92%,transparent);backdrop-filter:blur(16px);-webkit-backdrop-filter:blur(16px);border-bottom:1px solid var(--line);box-shadow:0 1px 0 rgba(255,255,255,.04);z-index:20}
header.top .wrap{display:flex;align-items:center;gap:10px;max-width:1320px;padding:10px 28px;min-height:58px}
.logo{display:flex;align-items:center;gap:8px;font-weight:700;letter-spacing:.01em;font-size:16px;white-space:nowrap;margin-right:8px}
.logo svg{flex:none}
.logo span{color:var(--ink)}
.search{flex:1;display:flex;max-width:440px;margin:0 auto}
.search input{flex:1;background:var(--card);border:1px solid var(--line);color:var(--ink);border-radius:10px;padding:9px 16px;font-size:14px;outline:none;box-shadow:inset 0 1px 2px rgba(0,0,0,.04)}
[data-theme=light] .search input{border-color:rgba(0,0,0,.08)}
.search input:focus{border-color:var(--brand);box-shadow:0 0 0 1px var(--brand)}
.search input::placeholder{color:var(--mut)}
.search kbd{font-family:var(--mono);font-size:11px;color:var(--mut);border:1px solid var(--line);border-radius:6px;padding:1px 7px;margin-left:-44px;align-self:center;pointer-events:none}
.btn{background:var(--card);border:1px solid var(--line);color:var(--ink);border-radius:9px;padding:8px 13px;font-size:13px;font-weight:600;cursor:pointer;white-space:nowrap;transition:background .15s ease,border-color .15s ease,transform .15s ease}
[data-theme=light] .btn{border-color:rgba(0,0,0,.08)}
.btn:hover{opacity:1;background:var(--bg2);border-color:var(--brand);transform:translateY(-1px)}
header.top .wrap>.btn[aria-current="page"]{background:var(--acc-soft);border-color:var(--brand);color:var(--brand)}
header.top #themebtn{min-width:38px;padding-left:9px;padding-right:9px}
header.top .reader-nav{display:flex;align-items:center;gap:8px}
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
.card a.read{margin-top:8px;align-self:flex-start;background:var(--cat,var(--brand));border:2px solid var(--cat,var(--brand));color:#08251b;font-weight:700;font-size:16px;border-radius:9999px;padding:12px 30px;min-height:48px;display:inline-flex;align-items:center;box-shadow:0 3px 10px color-mix(in srgb,var(--cat,var(--brand)) 22%,transparent)}
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
.empty p{margin:0 0 14px;font-size:14px}
.empty-cats{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;margin:0 0 16px}
.empty .chip{font-family:var(--mono);font-size:12px;display:inline-flex;align-items:center;gap:6px;padding:6px 12px;border-radius:9999px;border:1px solid var(--line);background:var(--base);color:var(--mut);text-decoration:none}
.empty .chip:hover{border-color:var(--brand);color:var(--brand)}
.empty a{color:var(--brand);font-weight:600}
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
.rlayout{display:flex;max-width:1320px;margin:0 auto;min-height:100vh;min-height:100dvh}
aside.toc{width:300px;flex:none;border-right:1px solid var(--line-soft);padding:24px 16px;position:sticky;top:57px;height:calc(100vh - 57px);height:calc(100dvh - 57px);overflow:auto}
aside.toc h4{font-family:var(--mono);font-size:11px;font-weight:600;letter-spacing:.6px;text-transform:uppercase;color:var(--mut)}
aside.toc a{display:block;font-size:14px;font-weight:500;color:var(--mut);text-decoration:none;padding:7px 12px;border-radius:8px;border-left:2px solid transparent;line-height:1.45}
aside.toc a:hover{color:var(--ink);background:var(--bg2)}
aside.toc a.cur{background:var(--acc-soft);color:var(--brand);font-weight:600;border-left-color:var(--brand)}
[data-theme=light] aside.toc a.cur{color:#0fa76e}
main.read{flex:1;min-width:0;padding:32px 32px 90px}
.readbody{margin:0 auto;max-width:820px}
.readbody .page{width:auto !important;min-height:0 !important;margin:0 auto 22px !important;padding:26px !important;border-radius:14px;scroll-margin-top:80px}
.readbody .page.cover{align-items:flex-start !important}
.readbody .cover{display:grid;grid-template-columns:1fr !important;max-width:100%}
.readbody .cover-left{padding:28px 22px !important}
.readbody .cover-right{padding:28px 22px !important;border-left:none !important;border-top:1px solid #2a2f2d}
.readbody .cover-title{font-size:34px !important;letter-spacing:-.5px}
@media(max-width:700px){.readbody .pipeline,.readbody .map-row,.readbody .arch-row,.readbody .dec-branches,.readbody .lab-step,.readbody .v-stage{flex-wrap:wrap}.readbody .pipeline .stage,.readbody .map-box,.readbody .arch-node{flex:1 1 140px;min-width:0}.readbody .pipeline .connector,.readbody .map-arr{flex-shrink:0}.readbody .lab-step .lab-content,.readbody .lab-step .step-body{min-width:0}.readbody .cmdres{grid-template-columns:1fr !important}.readbody .cmdres .col,.readbody .cmdres .res-block,.readbody .cmdres .term-box,.readbody .cmdres .cmd-block{min-width:0}}
.readbody .cover-sub{font-size:16px !important;margin-bottom:24px !important}
.readbody .cover h1{font-size:32px !important}
.readbody .cover .sig{white-space:normal !important}
.readbody .page,.readbody .cover,.readbody .cover-left,.readbody .cover-right{max-width:100%}
.readbody pre,.readbody .terminal{position:relative;overflow-x:auto;max-width:100%;scrollbar-width:thin;white-space:pre}
.readbody code,.readbody .mono{overflow-wrap:anywhere}.readbody .step .mono{overflow-wrap:break-word}
.readbody .md-fallback{font-size:18px;line-height:var(--lh,1.75)}
.readbody .md-fallback .body{font-size:18px;line-height:inherit;margin:14px 0}
.readbody .md-fallback .sec{font-size:27px;line-height:1.25;margin:30px 0 12px}
.readbody .md-fallback .tight{font-size:17px;line-height:1.7;margin:14px 0 14px 24px}
.readbody .md-fallback .terminal{font-size:15px;line-height:1.6;padding:16px}
.readbody .md-fallback.cover h1{font-size:32px;line-height:1.1}
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
.tocbtn{display:inline-flex;align-items:center}
.pdflink{display:inline-block;margin-top:12px;background:var(--ink);color:var(--bg);border-radius:9999px;padding:8px 24px;text-decoration:none;font-size:14px;font-weight:500;box-shadow:var(--shadow-btn)}
.pdflink:hover{opacity:.85;color:var(--bg)}
.crumbs{display:flex;align-items:center;gap:8px;font-size:13.5px;min-width:0}
.crumbs .here{font-weight:700;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:280px}
.crumbs .sep{color:var(--mut)}
@media(max-width:900px){aside.toc{position:fixed;left:0;top:0;bottom:0;background:var(--card);z-index:60;transform:translateX(-105%);transition:transform .2s;height:100vh;height:100dvh}
aside.toc.open{transform:none}.tocscrim{display:none}@media(max-width:900px){body.toc-open .tocscrim{display:block;position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:55}}
aside.toc a{padding:11px 12px;font-size:15px}
.tocbtn{display:inline-block}
main.read{padding:20px 14px 90px}
.crumbs .here{max-width:140px}
.hero{padding:36px 0 6px}
.chapnav{flex-direction:column}
.readbody table,.readbody .terminal,table.gloss{display:block;overflow-x:auto;-webkit-overflow-scrolling:touch}
.drawer .panel{width:min(320px,88vw)}}
aside.toc a{scroll-margin-top:0}
body.lock{overflow:hidden}
@media(min-width:901px){body.toc-hide aside.toc{display:none}}
#fsbar{display:none;position:fixed;left:50%;transform:translateX(-50%);bottom:max(14px,env(safe-area-inset-bottom));z-index:80;background:var(--card);border:1px solid var(--line);border-radius:20px;padding:8px 10px;gap:5px;box-shadow:var(--shadow-lift);align-items:center;max-width:96vw}
body.fs #fsbar{display:flex}
body.fs header.top,body.fs .readcontext{display:none !important}
body.fs main.read{padding-top:24px}
#fsbar .btn{min-height:44px;padding:7px 14px}
#fs-prog{font-family:var(--mono);font-size:12px;color:var(--mut);padding:0 8px;white-space:nowrap}
body.fs .topbtn,body.lock .topbtn{display:none !important}
.toc-head{display:flex;align-items:center;gap:8px;margin-bottom:12px}.toc-head h4{flex:1;min-width:0;margin:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.drawerx{position:static;flex:0 0 auto;width:40px;height:40px;display:inline-flex;align-items:center;justify-content:center;background:transparent;border:1px solid var(--line);border-radius:10px;color:var(--mut);font-size:20px;cursor:pointer}
.drawerx:hover{color:var(--ink);border-color:var(--brand)}
.readbody .step{list-style:none;display:flex;gap:10px;align-items:flex-start;margin:8px 0}
.readbody .step input[type=checkbox]{width:22px;height:22px;flex:none;margin-top:2px;accent-color:var(--brand);cursor:pointer;flex:none}.readbody .stephit{display:inline-flex;padding:11px;margin:-11px;cursor:pointer;flex:none}
.readbody pre,.readbody .terminal{background-image:linear-gradient(to left,rgba(127,127,127,.28),transparent 16px);background-position:right center;background-size:16px 100%;background-repeat:no-repeat;background-attachment:scroll}
@media(max-width:600px){
.wrap{padding:16px 14px}
.search input,#mobileq{font-size:16px}
.grid{grid-template-columns:1fr}
.hero .stats{gap:6px}
main.read{padding:16px 10px 90px}
.readbody .page{padding:18px !important}
.btn{min-height:40px}
.readbody pre,.readbody .terminal{font-size:11px}}
@media(max-width:480px){
header.top .wrap{height:56px;min-height:56px;padding:8px 10px;gap:7px;flex-wrap:nowrap}
header.top .crumbs{flex:1;min-width:0;gap:5px;font-size:12px}
header.top .crumbs .logo{font-size:13px;gap:4px}
header.top .crumbs .logo svg{width:17px;height:17px}
header.top .crumbs .sep,header.top .crumbs .here{display:none}
header.top .search,header.top #qcount,header.top #markbtn,header.top nav.reader-nav{display:none}
header.top .mobilemenu{display:inline-flex;align-items:center;justify-content:center;width:44px;height:44px;padding:0;font-size:19px}
header.top #tocbtn{display:inline-flex;order:2;width:78px;height:44px;padding:0;overflow:hidden;font-size:0;align-items:center;justify-content:center;color:transparent}
header.top #tocbtn::before{content:'Contents';font-size:11px;font-family:var(--mono);color:var(--ink)}
header.top #backbtn{display:inline-flex;order:3;font-size:12px;padding:5px 9px;min-height:44px;align-items:center}
.readcontext{padding:6px 12px}
.readcontext .wrap{gap:5px}
.readcontext .readback{display:none}
.readcontext .wrap>a:not(.readback),.readcontext .wrap>span:not(.here):not(.pathpos):not(.prereq){display:none}
.readcontext .here{display:block;flex-basis:100%;font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.readcontext .pathpos,.readcontext .prereq{font-size:11px;padding:2px 7px}
.readcontext .prereq a{padding:1px 6px}
.topbtn{right:12px;bottom:14px}
.mobile-controls,.mobile-search{display:flex;gap:8px;flex-wrap:wrap}
.mobile-controls .btn{min-height:38px}
.mobile-search{display:block}.mobile-search label{display:block;font-family:var(--mono);font-size:11px;text-transform:uppercase;color:var(--mut);margin-bottom:7px}.mobile-search input{width:100%;background:var(--bg);border:1px solid var(--line);color:var(--ink);border-radius:9999px;padding:9px 12px}
}
/* shared non-reader chrome: keep the landing, shelf, roadmap and glossary
   inside the viewport instead of letting the nav establish a wide canvas */
@media(max-width:600px){
header.top .wrap{min-width:0;max-width:100%;padding:8px 10px;gap:4px;overflow:hidden}
header.top .logo{font-size:14px;gap:5px;flex:none}
header.top .logo{margin-right:0}
header.top .logo span{display:none}
header.top .search{display:none}
header.top .btn{padding:5px 7px;font-size:11px;min-height:44px}
header.top .wrap>.btn{flex:none}
header.top #themebtn{width:28px;min-width:28px;min-height:44px;padding:0}
}
@media(min-width:601px) and (max-width:900px){
header.top .wrap{min-width:0;max-width:100%;padding:10px 18px;gap:8px;overflow:hidden}
header.top .search{display:none}
header.top .btn{padding:6px 11px;font-size:13px;flex:none}
}


/* icon: dark glyphs (github #181717 + currentColor line icons) invert ONLY on dark surfaces; light/sepia keep native dark svg */
:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .readbody .page.cover img[src*="github"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .coverart img[src*="github"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .readbody .page.cover img[src*="workflow"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .readbody .page.cover img[src*="hammer"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .readbody .page.cover img[src*="package"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .readbody .page.cover img[src*="database"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .readbody .page.cover img[src*="puzzle"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .readbody .page.cover img[src*="server"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .readbody .page.cover img[src*="terminal"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .readbody .page.cover img[src*="shield"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .readbody .page.cover img[src*="activity"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .readbody .page.cover img[src*="webhook"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .readbody .page.cover img[src*="wrench"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .readbody .page.cover img[src*="flask"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .readbody .page.cover img[src*="rocket"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .coverart img[src*="workflow"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .coverart img[src*="hammer"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .coverart img[src*="package"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .coverart img[src*="database"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .coverart img[src*="puzzle"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .coverart img[src*="server"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .coverart img[src*="terminal"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .coverart img[src*="shield"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .coverart img[src*="activity"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .coverart img[src*="webhook"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .coverart img[src*="wrench"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .coverart img[src*="flask"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .coverart img[src*="rocket"]{filter:invert(1) brightness(1.05);}
/* icon: currentColor line glyphs resolve via OS CanvasText (unreliable) — force black strokes on light surfaces */
:is([data-theme="light"],[data-theme="sepia"]) .readbody .page.cover img[src*="github"],:is([data-theme="light"],[data-theme="sepia"]) .coverart img[src*="github"],:is([data-theme="light"],[data-theme="sepia"]) .readbody .page.cover img[src*="workflow"],:is([data-theme="light"],[data-theme="sepia"]) .readbody .page.cover img[src*="hammer"],:is([data-theme="light"],[data-theme="sepia"]) .readbody .page.cover img[src*="package"],:is([data-theme="light"],[data-theme="sepia"]) .readbody .page.cover img[src*="database"],:is([data-theme="light"],[data-theme="sepia"]) .readbody .page.cover img[src*="puzzle"],:is([data-theme="light"],[data-theme="sepia"]) .readbody .page.cover img[src*="server"],:is([data-theme="light"],[data-theme="sepia"]) .readbody .page.cover img[src*="terminal"],:is([data-theme="light"],[data-theme="sepia"]) .readbody .page.cover img[src*="shield"],:is([data-theme="light"],[data-theme="sepia"]) .readbody .page.cover img[src*="activity"],:is([data-theme="light"],[data-theme="sepia"]) .readbody .page.cover img[src*="webhook"],:is([data-theme="light"],[data-theme="sepia"]) .readbody .page.cover img[src*="wrench"],:is([data-theme="light"],[data-theme="sepia"]) .readbody .page.cover img[src*="flask"],:is([data-theme="light"],[data-theme="sepia"]) .readbody .page.cover img[src*="rocket"],:is([data-theme="light"],[data-theme="sepia"]) .coverart img[src*="workflow"],:is([data-theme="light"],[data-theme="sepia"]) .coverart img[src*="hammer"],:is([data-theme="light"],[data-theme="sepia"]) .coverart img[src*="package"],:is([data-theme="light"],[data-theme="sepia"]) .coverart img[src*="database"],:is([data-theme="light"],[data-theme="sepia"]) .coverart img[src*="puzzle"],:is([data-theme="light"],[data-theme="sepia"]) .coverart img[src*="server"],:is([data-theme="light"],[data-theme="sepia"]) .coverart img[src*="terminal"],:is([data-theme="light"],[data-theme="sepia"]) .coverart img[src*="shield"],:is([data-theme="light"],[data-theme="sepia"]) .coverart img[src*="activity"],:is([data-theme="light"],[data-theme="sepia"]) .coverart img[src*="webhook"],:is([data-theme="light"],[data-theme="sepia"]) .coverart img[src*="wrench"],:is([data-theme="light"],[data-theme="sepia"]) .coverart img[src*="flask"],:is([data-theme="light"],[data-theme="sepia"]) .coverart img[src*="rocket"]{filter:brightness(0);}


@media print{body{background:#fff !important;color:#000 !important}header.top,aside.toc,.drawer,.chapnav,.copybtn,.settingsbar,.copybar,.codehead,.topbtn,#resume,#fsbar,.drawerx{display:none !important}
main.read{padding:0}.readbody{max-width:none}}
table.gloss{width:100%;border-collapse:collapse;font-size:14px;margin:16px 0}
table.gloss td,table.gloss th{border:1px solid var(--line);padding:9px 11px;text-align:left}
table.gloss th{background:var(--bg2)}
table.gloss .upd{color:var(--brand);font-weight:700;font-size:11px;white-space:nowrap}
.gtbar{position:sticky;top:57px;z-index:15;background:var(--bg);padding:10px 0 6px}
.gtbar input{width:100%;background:var(--card);border:1px solid var(--line);color:var(--ink);border-radius:9999px;padding:9px 14px;font-size:14px}
.az{display:flex;gap:4px;overflow-x:auto;padding:8px 2px 2px;-webkit-overflow-scrolling:touch}
.az a,.az span.dim{flex:none;min-width:34px;height:34px;display:inline-flex;align-items:center;justify-content:center;border:1px solid var(--line);border-radius:8px;font-family:var(--mono);font-size:13px;color:var(--ink)}
.az a{background:var(--card)}
.az span.dim{opacity:.3}
table.gloss tr{scroll-margin-top:150px}
@media(max-width:600px){table.gloss,table.gloss tbody{display:block;width:100%;overflow:visible}table.gloss tr:first-child{display:none}table.gloss tr{display:block;background:var(--card);border:1px solid var(--line-soft);border-radius:12px;margin:0 0 10px;padding:12px 14px}table.gloss td{display:block;border:none;padding:3px 0}table.gloss td:first-child{font-size:16px}table.gloss td:last-child a{display:inline-block;padding:10px 16px;border:1px solid var(--line);border-radius:9999px}.gtbar input{min-height:44px;font-size:16px}.az a,.az span.dim{min-width:44px;height:44px}}
/* P0: sepia theme + light leak guards + covers + filters + a11y */
[data-theme=sepia]{--bg:#F6F1E7;--bg2:#EDE3CC;--card:#FFFBF0;--ink:#3B2F1E;--mut:#6F665A;--line:rgba(59,47,30,.16);--line-soft:rgba(59,47,30,.09);--acc:#0B9B68;--acc-soft:rgba(11,155,104,.11);--brand:#0B9B68;--shadow:rgba(59,47,30,.08) 0px 2px 8px;--shadow-btn:rgba(59,47,30,.10) 0px 1px 3px;--shadow-lift:rgba(59,47,30,.16) 0px 16px 32px -10px}
[data-theme=sepia] .readbody{--paper:#FFFBF0;--white:#FFFBF0;--ink:#3B2F1E;--muted:#6F665A;--line:rgba(59,47,30,.14);--panel:#EDE3CC;--text-light:#3B2F1E}
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
@media(max-width:600px){header.top .wrap{gap:4px}}
@media(max-width:380px){header.top .wrap>a[href$="glossary.html"]{display:none}}


/* icon: dark glyphs (github #181717 + currentColor line icons) invert ONLY on dark surfaces; light/sepia keep native dark svg */
:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .readbody .page.cover img[src*="github"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .coverart img[src*="github"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .readbody .page.cover img[src*="workflow"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .readbody .page.cover img[src*="hammer"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .readbody .page.cover img[src*="package"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .readbody .page.cover img[src*="database"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .readbody .page.cover img[src*="puzzle"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .readbody .page.cover img[src*="server"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .readbody .page.cover img[src*="terminal"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .readbody .page.cover img[src*="shield"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .readbody .page.cover img[src*="activity"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .readbody .page.cover img[src*="webhook"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .readbody .page.cover img[src*="wrench"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .readbody .page.cover img[src*="flask"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .readbody .page.cover img[src*="rocket"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .coverart img[src*="workflow"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .coverart img[src*="hammer"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .coverart img[src*="package"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .coverart img[src*="database"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .coverart img[src*="puzzle"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .coverart img[src*="server"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .coverart img[src*="terminal"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .coverart img[src*="shield"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .coverart img[src*="activity"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .coverart img[src*="webhook"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .coverart img[src*="wrench"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .coverart img[src*="flask"],:is([data-theme="dark"],[data-theme="dim"],[data-theme="contrast"]) .coverart img[src*="rocket"]{filter:invert(1) brightness(1.05);}
/* icon: currentColor line glyphs resolve via OS CanvasText (unreliable) — force black strokes on light surfaces */
:is([data-theme="light"],[data-theme="sepia"]) .readbody .page.cover img[src*="github"],:is([data-theme="light"],[data-theme="sepia"]) .coverart img[src*="github"],:is([data-theme="light"],[data-theme="sepia"]) .readbody .page.cover img[src*="workflow"],:is([data-theme="light"],[data-theme="sepia"]) .readbody .page.cover img[src*="hammer"],:is([data-theme="light"],[data-theme="sepia"]) .readbody .page.cover img[src*="package"],:is([data-theme="light"],[data-theme="sepia"]) .readbody .page.cover img[src*="database"],:is([data-theme="light"],[data-theme="sepia"]) .readbody .page.cover img[src*="puzzle"],:is([data-theme="light"],[data-theme="sepia"]) .readbody .page.cover img[src*="server"],:is([data-theme="light"],[data-theme="sepia"]) .readbody .page.cover img[src*="terminal"],:is([data-theme="light"],[data-theme="sepia"]) .readbody .page.cover img[src*="shield"],:is([data-theme="light"],[data-theme="sepia"]) .readbody .page.cover img[src*="activity"],:is([data-theme="light"],[data-theme="sepia"]) .readbody .page.cover img[src*="webhook"],:is([data-theme="light"],[data-theme="sepia"]) .readbody .page.cover img[src*="wrench"],:is([data-theme="light"],[data-theme="sepia"]) .readbody .page.cover img[src*="flask"],:is([data-theme="light"],[data-theme="sepia"]) .readbody .page.cover img[src*="rocket"],:is([data-theme="light"],[data-theme="sepia"]) .coverart img[src*="workflow"],:is([data-theme="light"],[data-theme="sepia"]) .coverart img[src*="hammer"],:is([data-theme="light"],[data-theme="sepia"]) .coverart img[src*="package"],:is([data-theme="light"],[data-theme="sepia"]) .coverart img[src*="database"],:is([data-theme="light"],[data-theme="sepia"]) .coverart img[src*="puzzle"],:is([data-theme="light"],[data-theme="sepia"]) .coverart img[src*="server"],:is([data-theme="light"],[data-theme="sepia"]) .coverart img[src*="terminal"],:is([data-theme="light"],[data-theme="sepia"]) .coverart img[src*="shield"],:is([data-theme="light"],[data-theme="sepia"]) .coverart img[src*="activity"],:is([data-theme="light"],[data-theme="sepia"]) .coverart img[src*="webhook"],:is([data-theme="light"],[data-theme="sepia"]) .coverart img[src*="wrench"],:is([data-theme="light"],[data-theme="sepia"]) .coverart img[src*="flask"],:is([data-theme="light"],[data-theme="sepia"]) .coverart img[src*="rocket"]{filter:brightness(0);}


@media print{header.top,aside.toc,.drawer,.chapnav,.copybtn,.copybar,.codehead,.filterbar,#resume,.jumpnav,.shelf-head .arrows{display:none !important} body{background:#fff !important;color:#000 !important} .card,.readbody .page{break-inside:avoid;border:1px solid #ccc !important;background:#fff !important;color:#000 !important} main.read{padding:0}.readbody{max-width:none;font-size:12pt}}
@media(prefers-reduced-motion:reduce){*{animation:none !important;transition:none !important;scroll-behavior:auto !important}.rail{scroll-snap-type:none}}
/* P1: paths + rubric + search dropdown + bookmarks + related + labs + lightbox */
/* Learning Paths — journey cards reusing the map card system (same gradient/border/shadow tokens, --cat accent, currentColor icons) */
.pathgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px;margin:16px 0 8px}
.pathcard{position:relative;background:linear-gradient(135deg,color-mix(in srgb,var(--cat) 7%,var(--card)) 0%,var(--card) 55%);border:1.5px solid color-mix(in srgb,var(--cat) 28%,var(--line-soft));border-radius:16px;padding:0;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.06),0 8px 24px -8px color-mix(in srgb,var(--cat) 18%,transparent),0 2px 10px rgba(0,0,0,.06);display:flex;flex-direction:column}
.pathcard::before{content:"";position:absolute;top:0;left:0;right:0;height:5px;background:var(--cat,var(--brand));z-index:2}
.pathcard-head{display:flex;gap:12px;align-items:flex-start;padding:22px 20px 0}
.pathcard-head .map-icon{width:42px;height:42px;border-radius:11px;flex:none}
.pathcard-head .map-icon svg{width:22px;height:22px}
.pathcard-titles h3{font-size:16px;font-weight:700;letter-spacing:-.2px;line-height:1.25}
.pathcount{font-family:var(--mono);font-size:11px;color:var(--mut);font-weight:500}
.pathdesc{font-size:13px;color:var(--mut);line-height:1.55;padding:8px 20px 0}
.pathsteps{list-style:none;margin:12px 0 0;padding:2px 20px 0;position:relative;display:flex;flex-direction:column}
.pathstep{position:relative;padding:2px 0 16px 36px;min-height:44px}
.pathstep::before{content:attr(data-n);position:absolute;left:0;top:0;width:26px;height:26px;border-radius:50%;background:var(--card);border:1.5px solid var(--cat,var(--brand));color:var(--ink);font-family:var(--mono);font-size:10px;font-weight:700;display:flex;align-items:center;justify-content:center;z-index:1}
.pathstep::after{content:"";position:absolute;left:12px;top:28px;bottom:0;width:2px;background:color-mix(in srgb,var(--cat) 32%,var(--line-soft));border-radius:2px}
.pathstep:last-child::after{display:none}
.pathstep.finish::before{background:var(--cat,var(--brand));border-color:var(--cat,var(--brand));color:#0B0D10}
[data-theme=light] .pathstep.finish::before{color:#fff}
.pathsteps.long .pathstep{padding-bottom:9px;min-height:38px}
.steptitle{display:block;font-size:14.5px;font-weight:600;line-height:1.35;color:var(--ink)}
.steptitle:hover{color:var(--cat,var(--brand))}
.stepmeta{display:block;font-family:var(--mono);font-size:11px;color:var(--mut);margin-top:3px}
.finpill{display:inline-block;font-family:var(--mono);font-size:10px;font-weight:700;letter-spacing:.4px;background:color-mix(in srgb,var(--cat) 12%,transparent);border:1px solid color-mix(in srgb,var(--cat) 35%,transparent);color:var(--cat);border-radius:9999px;padding:1px 8px;margin-left:6px;white-space:nowrap}
.difbadge{font-family:var(--mono);font-size:10px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;padding:3px 9px;border-radius:9999px;border:1px solid;color:var(--cat);background:color-mix(in srgb,var(--cat) 10%,var(--bg2));border-color:color-mix(in srgb,var(--cat) 22%,var(--line-soft));white-space:nowrap}
.difbadge.beg{--cat:#2ECC71}
.difbadge.int{--cat:#F5A524}
.difbadge.adv{--cat:#E5484D}
.pathfoot{display:flex;gap:6px;flex-wrap:wrap;padding:14px 20px 18px;margin-top:auto}
@media(max-width:600px){.pathgrid{grid-template-columns:1fr}.pathstep{padding-bottom:14px}.pathsteps.long .pathstep{padding-bottom:8px}}
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
.relatedbox h4{font-family:var(--mono);font-size:11px;letter-spacing:.6px;text-transform:uppercase;color:var(--mut);margin-bottom:12px}
.relgrid{list-style:none;display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:10px;margin:0;padding:0}
.relcard{position:relative;display:flex;gap:10px;align-items:flex-start;background:var(--bg2);border:1px solid var(--line-soft);border-left:3px solid var(--cat,var(--brand));border-radius:10px;padding:10px 12px}
.rel-icon{width:30px;height:30px;border-radius:8px;flex:none;display:flex;align-items:center;justify-content:center;background:color-mix(in srgb,var(--cat) 12%,var(--bg2));border:1px solid color-mix(in srgb,var(--cat) 18%,var(--line-soft));color:var(--cat)}
.rel-icon svg{width:16px;height:16px;display:block}
.rel-main{display:flex;flex-direction:column;gap:4px;min-width:0;flex:1}
.rel-main>a{font-size:13.5px;font-weight:600;line-height:1.35;color:var(--ink)}
.rel-main>a:hover{color:var(--cat,var(--brand))}
.rel-meta{font-family:var(--mono);font-size:11px;color:var(--mut);display:flex;align-items:center;gap:6px;flex-wrap:wrap}
.rel-why{font-family:var(--mono);font-size:10px;font-weight:600;color:var(--cat)}
@media(max-width:600px){.relgrid{grid-template-columns:1fr}}
.upnext{display:flex;justify-content:space-between;gap:10px;background:var(--acc-soft);border:1px solid var(--brand);border-radius:14px;padding:14px 20px;margin-top:20px;font-size:14px}
.labcheck{list-style:none;margin:12px 0}
.labcheck li{display:flex;gap:10px;align-items:flex-start;background:var(--card);border:1px solid var(--line-soft);border-radius:10px;padding:10px 14px;margin-bottom:8px;font-size:14px}
.labcheck li.done{opacity:.6;text-decoration:line-through}
.labcheck input{margin-top:4px;accent-color:var(--brand)}
.labbanner{background:var(--acc-soft);border:1px solid var(--brand);border-radius:12px;padding:12px 18px;margin:0 auto 20px;max-width:820px;font-size:14px}
#lightbox{display:none;position:fixed;inset:0;z-index:100;background:rgba(0,0,0,.85);align-items:center;justify-content:center;padding:24px}
#lightbox.open{display:flex}
#lightbox img{max-width:94vw;max-height:90vh;max-height:90dvh;border-radius:10px}
.readbody table{border-collapse:collapse}
.readbody thead th{position:sticky;top:0;background:var(--bg2);z-index:1}
.readbody tbody tr:nth-child(even){background:rgba(127,127,127,.07)}
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
@media(max-width:700px){.readcontext{padding:8px 14px;font-size:12px}.readcontext .wrap{gap:7px}.readback{order:-1}.readcontext .here{flex-basis:100%;overflow-wrap:anywhere}.readcontext .pathpos,.readcontext .prereq{max-width:100%;white-space:normal;overflow-wrap:anywhere}.readcontext .prereq a{white-space:normal;overflow-wrap:anywhere}.upnext{align-items:flex-start;flex-wrap:wrap;padding:12px 14px}.upnext a{overflow-wrap:anywhere}}
.readcontext{background:var(--bg);border-bottom:1px solid var(--line-soft);padding:8px 32px}
.readcontext .pathpos{background:transparent;border:0;border-left:2px solid var(--brand);border-radius:0;padding:2px 0 2px 10px}
.readcontext .prereq a{border:0;border-bottom:1px solid var(--line);border-radius:0;padding:1px 0}
.upnext{background:var(--card);border:0;border-left:3px solid var(--brand);border-radius:0;padding:14px 18px;margin-top:22px;box-shadow:0 1px 0 var(--line-soft)}
.labbanner{display:flex;align-items:center;gap:10px;flex-wrap:wrap;background:var(--card);border:0;border-left:3px solid var(--brand);border-radius:0;padding:12px 16px;margin:0 auto 24px;max-width:820px;font-size:14px;box-shadow:0 1px 0 var(--line-soft)}
.labbanner a{color:var(--brand);font-weight:600;text-decoration:underline;text-underline-offset:3px}
.labbanner .markbtn{margin-left:auto !important;background:transparent;border:1px solid var(--line);color:var(--ink);border-radius:7px;padding:6px 10px}
/* P2.4: mobile icon-chain reflow (≤480px only, desktop untouched) */
@media(max-width:480px){
.readbody .life{flex-direction:column;gap:0}
.readbody .life .lconn{transform:rotate(90deg);padding:3px 0;align-self:center}
.readbody .life .lnode{display:flex;align-items:center;gap:10px;text-align:left;padding:8px 12px}
.readbody .life .lnode img{margin:0;flex:none}
.readbody .life .lnode b{font-size:11px}
.readbody .two{grid-template-columns:1fr}.readbody .timeline{flex-wrap:wrap;row-gap:6px}
.readbody .fnode{font-size:13px}
.readbody .vflow{margin:8px 0}
}
/* P2: typography, reading preferences, and ratings */
body[data-font=serif] .readbody{font-family:Georgia,'Times New Roman',serif}
body[data-font=serif] .readbody code,body[data-font=serif] .readbody pre,body[data-font=serif] .readbody .terminal{font-family:var(--mono)}
.readbody{line-height:var(--lh,1.7)}
.readback{display:inline-flex;align-items:center;gap:6px;color:var(--mut);text-decoration:none;font-size:13px;font-weight:600;border:1px solid var(--line-soft);border-radius:9999px;padding:5px 12px;white-space:nowrap}
.readback:hover{color:var(--ink);border-color:var(--line);background:var(--bg2)}
.topbtn{position:fixed;right:20px;bottom:20px;z-index:40;width:42px;height:42px;border:1px solid var(--line);border-radius:50%;background:var(--card);color:var(--ink);box-shadow:var(--shadow-lift);font-size:19px;cursor:pointer;opacity:0;visibility:hidden;transform:translateY(8px);transition:opacity .2s ease,transform .2s ease,visibility .2s ease}
.topbtn.on{opacity:1;visibility:visible;transform:none}
.mobilemenu{display:none}
.reader-nav{display:flex;align-items:center;gap:8px}
.mobile-controls,.mobile-search{display:none}
@media(prefers-reduced-motion:reduce){.topbtn{transition:none}}
.popsearch{font-size:12px;color:var(--mut);margin-top:6px}
.popsearch a{color:var(--mut);text-decoration:underline;cursor:pointer}
/* Home blocks — pseudo-3D isometric (B1.2/B2/B3) */
.map-hero{padding:52px 24px 16px;text-align:center;position:relative}
.map-hero .eyebrow{display:inline-block;font-family:var(--mono);font-size:12px;font-weight:600;letter-spacing:.6px;text-transform:uppercase;color:var(--brand);background:var(--acc-soft);border-radius:9999px;padding:5px 14px;margin-bottom:16px}
.map-hero h1{font-size:clamp(28px,4.4vw,46px);font-weight:700;letter-spacing:-.9px;line-height:1.08}
.map-hero p{color:var(--mut);font-size:16px;max-width:640px;margin:12px auto 0;line-height:1.55}
/* — Home hero: pipeline motif, CTAs, stat pills — */
.herocta{display:flex;gap:12px;justify-content:center;flex-wrap:wrap;margin-top:24px}
.btn.prim{background:var(--brand);color:#08251b;border-color:transparent;box-shadow:0 8px 24px -8px color-mix(in srgb,var(--brand) 50%,transparent)}
.btn.prim:hover{background:color-mix(in srgb,var(--brand) 86%,#fff);border-color:transparent;transform:translateY(-1px)}
.stat-row{display:flex;gap:10px;justify-content:center;flex-wrap:wrap;margin-top:20px}
.stat-pill{display:inline-flex;align-items:baseline;gap:6px;font-family:var(--mono);font-size:12.5px;color:var(--mut);background:var(--card);border:1px solid var(--line-soft);border-radius:9999px;padding:6px 14px}
.stat-pill b{font-size:14px;color:var(--ink)}
.stat-level b{color:var(--brand)}
.map-hero{overflow:hidden}
.pipeline{max-width:1060px;margin:6px auto 0;height:150px;pointer-events:none;opacity:.32}
.map-hero-inner{position:relative;z-index:2}
.pipeline svg{width:100%;height:100%;display:block}
.pnode{fill:var(--card);stroke:var(--brand);stroke-width:2}
.pnode.mut{stroke:color-mix(in srgb,var(--mut) 70%,transparent)}
.pcore{fill:var(--brand)}
.pcore.mut{fill:var(--mut)}
.pedge{stroke:var(--line);stroke-width:2;fill:none;stroke-dasharray:7 9;stroke-linecap:round;animation:dashflow 3.4s linear infinite}
.pedge.live{stroke:var(--brand);opacity:.85}
.plabel{font-family:var(--mono);font-size:11px;letter-spacing:.6px;text-transform:uppercase;fill:var(--mut)}
@keyframes dashflow{to{stroke-dashoffset:-128}}
@media(prefers-reduced-motion:reduce){.pedge{animation:none}}
@media(max-width:600px){.pipeline{opacity:.14;height:110px}.herocta{flex-direction:column;align-items:stretch;max-width:320px;margin-left:auto;margin-right:auto}.herocta .btn{justify-content:center}}
/* — MAP GRID: exterior blocks as distinct objects — */
.map-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:20px;margin:32px 0 28px;perspective:1200px}
.map-block{position:relative;background:linear-gradient(135deg,color-mix(in srgb,var(--cat) 7%,var(--card)) 0%,var(--card) 55%);border:1.5px solid color-mix(in srgb,var(--cat) 28%,var(--line-soft));border-radius:16px;padding:0;display:flex;flex-direction:column;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.06),0 8px 24px -8px color-mix(in srgb,var(--cat) 18%,transparent),0 2px 10px rgba(0,0,0,.06);transition:transform .24s cubic-bezier(.2,.8,.2,1),box-shadow .24s ease,border-color .24s ease;text-align:left;cursor:pointer;color:var(--ink);text-decoration:none;transform-style:preserve-3d}
.map-block::before{content:"";position:absolute;top:0;left:0;right:0;height:5px;background:var(--cat,var(--brand));z-index:2}
.map-block::after{content:"";position:absolute;top:5px;left:0;right:0;height:1px;background:linear-gradient(90deg,rgba(255,255,255,.55),transparent 60%);pointer-events:none;z-index:2}
[data-theme=dark] .map-block::after,[data-theme=dim] .map-block::after{background:linear-gradient(90deg,rgba(255,255,255,.12),transparent 60%)}
.map-block:hover{transform:perspective(700px) rotateX(3deg) rotateY(-5deg) translateY(-6px) scale(1.015);box-shadow:0 4px 12px rgba(0,0,0,.1),0 20px 40px -12px color-mix(in srgb,var(--cat) 22%,transparent),0 8px 20px rgba(0,0,0,.08);border-color:color-mix(in srgb,var(--cat) 42%,var(--line))}
.map-block:focus-visible{outline:2px solid var(--cat,var(--brand));outline-offset:3px}
.map-block:active{transform:perspective(700px) rotateX(2deg) rotateY(-3deg) translateY(-2px) scale(.995)}
/* block interior layout */
.map-block-inner{padding:22px 20px 18px;display:flex;flex-direction:column;gap:10px;flex:1}
.map-block-top{display:flex;align-items:flex-start;gap:14px}
.map-icon{width:52px;height:52px;border-radius:14px;display:flex;align-items:center;justify-content:center;background:color-mix(in srgb,var(--cat) 12%,var(--bg2));border:1px solid color-mix(in srgb,var(--cat) 18%,var(--line-soft));color:var(--cat);flex:none;box-shadow:inset 0 1px 0 rgba(255,255,255,.6)}
[data-theme=dark] .map-icon,[data-theme=dim] .map-icon{box-shadow:inset 0 1px 0 rgba(255,255,255,.08)}
.map-icon svg{width:28px;height:28px;display:block}
.map-cat{font-size:18px;font-weight:800;letter-spacing:-.3px;line-height:1.2;flex:1;min-width:0}
.map-count{font-family:var(--mono);font-size:12.5px;color:var(--mut);font-weight:600;display:flex;align-items:center;gap:6px}
.map-count::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--cat);flex:none;opacity:.9}
.map-difficulty{display:flex;align-items:center;gap:8px;margin-top:2px}
.map-diff-label{font-family:var(--mono);font-size:10px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;color:var(--mut)}
.map-diff-bar{display:flex;gap:3px;align-items:center;flex:1}
.map-diff-seg{height:6px;border-radius:9999px;min-width:8px;transition:width .2s}
.map-diff-seg.beg{background:#2ECC71}
.map-diff-seg.int{background:#F5A524}
.map-diff-seg.adv{background:#E5484D}
.map-diff-dots{display:flex;gap:4px;align-items:center}
.map-diff-dots i{width:8px;height:8px;border-radius:50%;display:inline-block}
.map-diff-dots i.beg{background:#2ECC71}
.map-diff-dots i.int{background:#F5A524}
.map-diff-dots i.adv{background:#E5484D}
.map-diff-count{font-family:var(--mono);font-size:11px;color:var(--mut);font-weight:600}
.map-pills{display:flex;gap:6px;flex-wrap:wrap;margin-top:2px}
.map-pill{font-family:var(--mono);font-size:11px;font-weight:600;padding:3px 9px;border-radius:9999px;background:color-mix(in srgb,var(--cat) 8%,var(--bg2));border:1px solid color-mix(in srgb,var(--cat) 14%,var(--line-soft));color:var(--mut)}
.map-pill b{color:var(--ink)}
/* hover/focus preview popover — 2-3 titles */
.map-preview{position:absolute;left:12px;right:12px;bottom:12px;background:var(--card);border:1px solid var(--line);border-radius:12px;padding:12px 14px;box-shadow:var(--shadow-lift);opacity:0;transform:translateY(8px);pointer-events:none;transition:opacity .2s ease,transform .2s ease;z-index:5;max-height:120px;overflow:hidden}
.map-block:hover .map-preview,.map-block:focus-within .map-preview,.map-block.preview-open .map-preview{opacity:1;transform:translateY(0);pointer-events:auto}
.map-preview-title{font-family:var(--mono);font-size:10px;font-weight:700;letter-spacing:.6px;text-transform:uppercase;color:var(--cat);margin-bottom:6px}
.map-preview ul{list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:4px}
.map-preview li{font-size:12.5px;font-weight:500;color:var(--ink);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;line-height:1.35}
.map-preview li::before{content:"→ ";color:var(--cat);font-weight:600}
.map-preview-more{font-family:var(--mono);font-size:11px;color:var(--mut);margin-top:6px}
/* touch affordance — preview button on mobile */
.map-preview-btn{display:none;position:absolute;top:10px;right:10px;z-index:3;width:32px;height:32px;border-radius:50%;background:var(--card);border:1px solid var(--line);color:var(--mut);font-size:16px;cursor:pointer;align-items:center;justify-content:center;box-shadow:var(--shadow)}
.map-preview-btn:hover{border-color:var(--cat);color:var(--cat)}
/* — MAP DETAIL: interior as distinct themed space — */
.map-detail{display:none}
.map-detail.active{display:block;animation:mapZoomIn .32s cubic-bezier(.2,.8,.2,1)}
.map-detail.exiting{animation:mapZoomOut .24s ease forwards}
@keyframes mapZoomIn{from{opacity:0;transform:scale(.96) translateY(12px)}to{opacity:1;transform:scale(1) translateY(0)}}
@keyframes mapZoomOut{from{opacity:1;transform:scale(1) translateY(0)}to{opacity:0;transform:scale(.98) translateY(8px)}}
.map-detail-hero{position:relative;background:linear-gradient(135deg,color-mix(in srgb,var(--cat) 7%,var(--card)) 0%,var(--card) 55%);border:1.5px solid color-mix(in srgb,var(--cat) 28%,var(--line-soft));border-radius:16px;padding:22px 22px 18px;margin:16px 0 20px;overflow:hidden;box-shadow:0 1px 3px rgba(0,0,0,.06),0 8px 24px -8px color-mix(in srgb,var(--cat) 18%,transparent),0 2px 10px rgba(0,0,0,.06)}
.map-detail-hero::before{content:"";position:absolute;top:0;left:0;right:0;height:5px;background:var(--cat);z-index:2}
.map-detail-hero::after{content:"";position:absolute;top:5px;left:0;right:0;height:1px;background:linear-gradient(90deg,rgba(255,255,255,.55),transparent 60%);pointer-events:none;z-index:2}
[data-theme=dark] .map-detail-hero::after,[data-theme=dim] .map-detail-hero::after{background:linear-gradient(90deg,rgba(255,255,255,.12),transparent 60%)}
.map-detail-hero-top{display:flex;align-items:flex-start;gap:14px;flex-wrap:wrap}
.map-detail-hero .map-icon{width:52px;height:52px;border-radius:14px;flex:none;background:color-mix(in srgb,var(--cat) 12%,var(--bg2));border:1px solid color-mix(in srgb,var(--cat) 18%,var(--line-soft));color:var(--cat);box-shadow:inset 0 1px 0 rgba(255,255,255,.6);display:flex;align-items:center;justify-content:center}
[data-theme=dark] .map-detail-hero .map-icon,[data-theme=dim] .map-detail-hero .map-icon{box-shadow:inset 0 1px 0 rgba(255,255,255,.08)}
.map-detail-hero .map-icon svg{width:28px;height:28px;display:block}
.map-detail-hero h2{font-size:22px;font-weight:800;letter-spacing:-.3px;line-height:1.2;flex:1;min-width:160px}
.map-detail-hero .count{font-family:var(--mono);font-size:12.5px;color:var(--mut);font-weight:600;display:flex;align-items:center;gap:6px}
.map-detail-hero .count::before{content:"";width:6px;height:6px;border-radius:50%;background:var(--cat);flex:none;opacity:.9}
.map-detail-hero .desc{color:var(--mut);font-size:13.5px;line-height:1.55;max-width:680px;margin-top:10px}
.map-detail-hero .map-pills{margin-top:10px}
.map-detail-hero .map-difficulty{margin-top:8px}
.map-back{display:inline-flex;align-items:center;gap:8px;font-size:14px;font-weight:600;background:var(--card);border:1.5px solid var(--line);border-radius:9999px;padding:10px 18px;margin:0 0 4px;cursor:pointer;color:var(--ink);transition:border-color .15s,background .15s,transform .15s;box-shadow:var(--shadow)}
.map-back:hover{border-color:var(--cat);color:var(--cat);transform:translateX(-2px)}
.map-back:active{transform:translateX(-1px) scale(.98)}
/* interior cards — reuse map card chrome: slim top bar + chip, same tokens as .map-block */
.map-cards{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:18px}
.map-cards .card{position:relative;background:linear-gradient(135deg,color-mix(in srgb,var(--cat) 7%,var(--card)) 0%,var(--card) 55%);border:1.5px solid color-mix(in srgb,var(--cat) 28%,var(--line-soft));border-radius:16px;padding:0;overflow:hidden;display:flex;flex-direction:column;gap:0;box-shadow:0 1px 3px rgba(0,0,0,.06),0 8px 24px -8px color-mix(in srgb,var(--cat) 18%,transparent),0 2px 10px rgba(0,0,0,.06);transition:transform .18s ease,box-shadow .18s ease,border-color .18s ease}
.map-cards .card::before{content:"";position:absolute;top:0;left:0;right:0;height:3px;background:var(--cat,var(--brand));z-index:2}
.map-cards .card::after{content:"";position:absolute;top:3px;left:0;right:0;height:1px;background:linear-gradient(90deg,rgba(255,255,255,.55),transparent 60%);pointer-events:none;z-index:2}
[data-theme=dark] .map-cards .card::after,[data-theme=dim] .map-cards .card::after{background:linear-gradient(90deg,rgba(255,255,255,.12),transparent 60%)}
.map-cards .card:hover{transform:translateY(-3px);box-shadow:0 4px 12px rgba(0,0,0,.1),0 20px 40px -12px color-mix(in srgb,var(--cat) 22%,transparent),0 8px 20px rgba(0,0,0,.08);border-color:color-mix(in srgb,var(--cat) 42%,var(--line))}
.map-card-top{padding:22px 22px 14px;display:flex;flex-direction:column;gap:10px;flex:1}
.map-card-head{display:flex;align-items:flex-start;gap:12px}
.map-cards .card .map-icon{width:42px;height:42px;border-radius:11px;display:flex;align-items:center;justify-content:center;background:color-mix(in srgb,var(--cat) 12%,var(--bg2));border:1px solid color-mix(in srgb,var(--cat) 18%,var(--line-soft));color:var(--cat);flex:none;box-shadow:inset 0 1px 0 rgba(255,255,255,.6)}
[data-theme=dark] .map-cards .card .map-icon,[data-theme=dim] .map-cards .card .map-icon{box-shadow:inset 0 1px 0 rgba(255,255,255,.08)}
.map-cards .card .map-icon svg{width:22px;height:22px;display:block}
.map-card-meta{display:flex;align-items:center;gap:8px;flex-wrap:wrap}
.map-card-badge{font-family:var(--mono);font-size:10px;font-weight:700;letter-spacing:.5px;text-transform:uppercase;padding:4px 10px;border-radius:9999px;border:1px solid;color:var(--cat);background:color-mix(in srgb,var(--cat) 10%,var(--bg2));border-color:color-mix(in srgb,var(--cat) 22%,var(--line-soft))}
.map-card-badge.beg{--cat:#2ECC71}
.map-card-badge.int{--cat:#F5A524}
.map-card-badge.adv{--cat:#E5484D}
.map-card-time{font-family:var(--mono);font-size:11px;color:var(--mut);font-weight:500}
.map-cards .card h3{font-size:17px;font-weight:700;letter-spacing:-.2px;line-height:1.3;margin:0}
.map-cards .card h3 a{color:var(--ink)}
.map-cards .card h3 a:hover{color:var(--cat,var(--brand))}
.map-cards .card .desc{font-size:13.5px;color:var(--mut);line-height:1.55;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden;flex:1}
.map-card-footer{padding:14px 22px 18px;border-top:0;display:flex;align-items:center;gap:10px;background:transparent}
.map-card-footer .meta-line{font-size:12px;color:var(--mut);flex:1}
.map-card-footer a.read{margin:0;min-width:116px;justify-content:center}
@media(max-width:600px){
  .map-grid{grid-template-columns:1fr;gap:16px;perspective:none}
  .map-block{transform:none !important}
  .map-block:hover{transform:translateY(-2px) !important;box-shadow:var(--shadow-lift)}
  .map-preview{position:static;opacity:1;transform:none;pointer-events:auto;margin:0 12px 12px;max-height:none;box-shadow:none;border:1px dashed color-mix(in srgb,var(--cat) 22%,var(--line-soft));background:color-mix(in srgb,var(--cat) 4%,var(--card))}
  .map-preview-btn{display:flex}
  .map-block:not(.preview-open) .map-preview{display:none}
  .map-block.preview-open .map-preview{display:block}
  .map-cards{grid-template-columns:1fr}
  .map-hero{padding:28px 16px 8px}
  .map-detail-hero{padding:20px 18px 18px;border-radius:16px}
  .map-detail-hero h2{font-size:22px}
}
@media(prefers-reduced-motion:reduce){
  .map-block,.map-detail,.map-grid{transition:none !important;animation:none !important;transform:none !important}
  .map-detail.active{animation:none}
  .map-detail.exiting{animation:none;display:none}
  .map-preview{transition:none !important}
}
"""

BASE_JS = """
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
function getP(k,d){try{const v=JSON.parse(localStorage.getItem(k));return v??d}catch(e){return d}}
function setP(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}
"""

INDEX_JS = BASE_JS + """
const PREF='cicdlib:pref',PROG='cicdlib:prog:';
const pref=getP(PREF,{theme:'sepia'});
const THEMES=['sepia','dark','light'],THICON={dark:'☀',light:'☾',sepia:'◐'};
function syncTheme(){const th=THEMES.includes(pref.theme)?pref.theme:'sepia';document.documentElement.dataset.theme=th;const t=$('#themebtn');if(t)t.textContent=THICON[th]||'☀'}
syncTheme();
function cycleTheme(){pref.theme=THEMES[(THEMES.indexOf(pref.theme)+1)%THEMES.length]||'sepia';setP(PREF,pref);syncTheme();}
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
  const filtering=!!(q||cat||dif);
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
  $$('.railmore').forEach(m=>{m.style.display=(filtering||m.dataset.exp)?'':'none';});
  $$('.railbtn').forEach(b=>b.style.display=filtering?'none':'');
  $('#empty').style.display=n?'none':'';
  const cc=$('#fcount');if(cc)cc.textContent=n+' shown';
  try{const h=new URLSearchParams();if($('#q').value)h.set('q',$('#q').value);if(cat)h.set('cat',cat);if(dif)h.set('dif',dif);history.replaceState(null,'','#'+h.toString());}catch(e){}
}
['q','fcat','fdif','fsort'].forEach(id=>{const el=document.getElementById(id);if(el)el.addEventListener('input',()=>{filter();drop();});});
$$('.railbtn').forEach(b=>b.onclick=()=>{const m=b.parentElement.previousElementSibling;const open=m.style.display!=='none';m.style.display=open?'none':'';m.dataset.exp=open?'':'1';b.textContent=open?('View all '+b.dataset.n+' \u2193'):'Show less \u2191';});
try{if(location.protocol.indexOf('http')===0)fetch('search.json').then(r=>r.ok?r.json():null).then(j=>{if(j&&j.length)window.SEARCH_IDX=j;}).catch(()=>{});}catch(e){}
function norm(s){return (s||'').toLowerCase().replace(/[-_/]/g,' ');}
function drop(){const raw=($('#q').value||''),q=raw.toLowerCase(),box=$('#qdrop');if(!box)return;if(q.length<2){box.classList.remove('open');box.innerHTML='';return;}
const STOP=new Set(['how','does','did','can','what','when','where','which','that','this','with','from','have','has','are','was','were','been','will','would','there','their','about','into','your','you','our','the','and','for','are','but','not','all','any','can','had','her','him','his','one','our','out','day','get','has','him','how','its','may','new','now','old','see','two','way','who','boy','did','she','use','her','now','do','i','an','a','to','in','of','or','is','it','my','me','on','as','at','by','we','if','up','so']);
const qn=norm(raw);let toks=qn.split(/\\s+/).filter(t=>t.length>=3&&!STOP.has(t));if(!toks.length)toks=[qn].filter(t=>t.length>=2);if(!toks.length){box.classList.remove('open');return;}
const idx=window.SEARCH_IDX||[];const res=idx.map(b=>{const secs=(b.sections||[]).join(' ');const body=(b.body||'');const hay=norm(b.title+' '+b.desc+' '+(b.tags||[]).join(' ')+' '+secs+' '+body);if(!toks.every(t=>hay.includes(t)))return null;let s=1,hit='';const secHit=(b.sections||[]).find(t=>{const tn=norm(t);return toks.every(tk=>tn.includes(tk))||tn.includes(toks[0]);});const titleHit=toks.every(t=>norm(b.title).includes(t));if(titleHit)s=3;else if(secHit){s=2;hit=secHit;}else{const bi=norm(body).indexOf(toks[0]);if(bi>=0){hit='…'+body.slice(Math.max(0,bi-30),bi+50).replace(/\\s+/g,' ')+'…';}else if(b.desc){hit=b.desc.slice(0,70);}}if((b.tags||[]).some(t=>toks.some(k=>norm(t).includes(k))))s+=0.5;return {b,s,hit};}).filter(Boolean).sort((a,b2)=>b2.s-a.s).slice(0,8);
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
const pref=Object.assign({theme:'sepia',fs:18,width:'820px',font:'sans',lh:1.7},getP(PREF,{}));
const RTHEMES=['sepia','dark','light'];
function applyPref(){document.documentElement.dataset.theme=RTHEMES.includes(pref.theme)?pref.theme:'sepia';
  document.body.dataset.font=pref.font==='serif'?'serif':'sans';
  const rb=document.querySelector('.readbody');if(rb){rb.style.fontSize=pref.fs+'px';rb.style.setProperty('max-width',pref.width);rb.style.setProperty('--lh',pref.lh);}
  $$('.setrow .opts .btn').forEach(b=>b.classList.toggle('on',b.dataset.set===undefined?'':String(pref[b.dataset.k])===b.dataset.set));
  setP(PREF,pref);}
function setOpt(k,v){pref[k]=v;applyPref()}
$$('.terminal').forEach(t=>{const bar=document.createElement('div');bar.className='copybar';const b=document.createElement('button');b.className='copybtn';b.textContent='Copy';b.onclick=()=>{let txt=t.innerText.split('\\n').filter(l=>!l.match(/^\\s*(NAME|nginx-|CONTAINER|NAME\\s+READY)/)).join('\\n');navigator.clipboard.writeText(txt||t.innerText).then(()=>{b.textContent='Copied!';setTimeout(()=>b.textContent='Copy',1200)})};bar.appendChild(b);t.before(bar)});
$$('.readbody pre').forEach(p=>{if(p.closest('.terminal')||p.previousElementSibling?.classList?.contains('codehead'))return;const h=document.createElement('div');h.className='codehead';h.innerHTML='<span class=dot></span><span>'+(p.dataset.lang||"code")+'</span>';const b=document.createElement('button');b.textContent='Copy';b.onclick=()=>{navigator.clipboard.writeText(p.innerText).then(()=>{b.textContent='Copied!';setTimeout(()=>b.textContent='Copy',1200)})};const w=document.createElement('button');w.textContent='Wrap';w.style.marginLeft='6px';w.onclick=()=>{p.style.whiteSpace=p.style.whiteSpace==='pre-wrap'?'pre':'pre-wrap'};h.appendChild(b);h.appendChild(w);p.before(h)});
$$('.readbody img').forEach(im=>{im.setAttribute('loading','lazy');if(!im.getAttribute('alt'))im.setAttribute('alt','Diagram from '+BID);im.style.cursor='zoom-in';im.addEventListener('click',()=>{const lb=$('#lightbox');if(lb){lb.querySelector('img').src=im.src;lb.classList.add('open');}});im.addEventListener('error',()=>{im.dataset.broken='1';const f=document.createElement('div');f.className='imgfallback';f.style.display='block';f.textContent='Image unavailable: '+(im.getAttribute('alt')||im.src);im.after(f);});});
const _lb=$('#lightbox');if(_lb)_lb.addEventListener('click',()=>_lb.classList.remove('open'));
const MARKS='cicdlib:marks';
const _mb=$('#markbtn');function syncMark(){const m=getP(MARKS,{});const on=!!m[BID];if(_mb){_mb.textContent=on?'★ Saved':'☆ Save';_mb.classList.toggle('on',on);}}
if(_mb)_mb.onclick=()=>{const m=getP(MARKS,{});if(m[BID])delete m[BID];else m[BID]=Date.now();setP(MARKS,m);syncMark();};syncMark();
const LABKEY='cicdlib:lab:'+BID;
function labChecks(){const done=getP(LABKEY,{});$$('.readbody .step').forEach((st,i)=>{if(st.querySelector('input[type=checkbox]'))return;const lab=document.createElement('input');lab.type='checkbox';lab.checked=!!done[i];lab.setAttribute('aria-label','Mark step done');lab.onchange=()=>{const d=getP(LABKEY,{});if(lab.checked)d[i]=1;else delete d[i];setP(LABKEY,d);st.classList.toggle('done',lab.checked);};st.classList.toggle('done',!!done[i]);const lb=document.createElement('label');lb.className='stephit';lb.setAttribute('aria-label','Mark step done');lb.appendChild(lab);st.prepend(lb);});const rst=$('#labreset');if(rst)rst.onclick=()=>{setP(LABKEY,{});$$('.readbody .step').forEach(st=>{st.classList.remove('done');const c=st.querySelector('input[type=checkbox]');if(c)c.checked=false;});};}
labChecks();
function tocUpdate(){const links=$$('aside.toc a');let cur=null;
  links.forEach(a=>{const h=a.getAttribute('href');if(!h||h[0]!=='#')return;
    const el=document.getElementById(h.slice(1));
    if(el&&el.getBoundingClientRect().top<160)cur=h;});
  window._cur=cur?cur.slice(1):null;
  links.forEach(a=>a.classList.toggle('cur',a.getAttribute('href')===cur));}
window.addEventListener('scroll',()=>{tocUpdate();
  const h=document.documentElement,p=Math.min(100,Math.round(100*(h.scrollTop)/(h.scrollHeight-h.clientHeight||1)));
  setP(PKEY,{pct:p,ts:Date.now()});const bar=$('#pbar');if(bar)bar.style.width=p+'%';const fp=$('#fs-prog');if(fp)fp.textContent=p+'%';},{passive:true});
function findBook(q){$$('.readbody mark').forEach(m=>{m.replaceWith(document.createTextNode(m.textContent))});if(!q)return 0;
  let n=0;const walker=document.createTreeWalker(document.querySelector('.readbody'),NodeFilter.SHOW_TEXT);
  const nodes=[];while(walker.nextNode())nodes.push(walker.currentNode);
  nodes.forEach(nd=>{const i=nd.textContent.toLowerCase().indexOf(q.toLowerCase());if(i<0)return;
    if(nd.parentElement.closest('.terminal,script,style'))return;
    const r=document.createRange();r.setStart(nd,i);r.setEnd(nd,i+q.length);
    const m=document.createElement('mark');r.surroundContents(m);n++;});
  const f=document.querySelector('.readbody mark');if(f)f.scrollIntoView({block:'center'});
  window._marks=[...document.querySelectorAll('.readbody mark')];window._mi=0;window._lastQ=q;return n;}
$('#q').addEventListener('keydown',e=>{if(e.key==='Enter'){const v=e.target.value;
  if(v&&v===window._lastQ&&(window._marks||[]).length){window._mi=(window._mi+1)%window._marks.length;window._marks[window._mi].scrollIntoView({block:'center'});$('#qcount').textContent='match '+(window._mi+1)+' of '+window._marks.length;return;}
  const n=findBook(v);$('#qcount').textContent=n?n+' match'+(n>1?'es':'')+' in this book — Enter for next':'no matches in this book'}});
$('#q').addEventListener('input',e=>{if(!e.target.value)findBook('')});
document.addEventListener('keydown',e=>{
  if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='k'){e.preventDefault();$('#q').focus()}
  if(e.key==='Escape'){if(document.activeElement===$('#q')||document.activeElement===$('#mobileq')){document.activeElement.value='';findBook('');const qc=$('#qcount');if(qc)qc.textContent='';}const _do=$('#drawer').classList.contains('open'),_to=$('aside.toc').classList.contains('open');$('#drawer').classList.remove('open');if($('aside.toc').classList.contains('open')){const tb=$('#tocbtn');if(tb)setTimeout(()=>tb.focus(),0);}$('aside.toc').classList.remove('open');if(!_do&&!_to&&document.body.classList.contains('fs'))setFS(false);lockScroll();}
  if(e.key.toLowerCase()==='t'&&document.activeElement.tagName!=='INPUT'){$('aside.toc').classList.toggle('open')}
  if(e.key==='ArrowRight'&&document.activeElement.tagName!=='INPUT'){const n=$('#nextbook');if(n)location.href=n.href}
  if(e.key==='ArrowLeft'&&document.activeElement.tagName!=='INPUT'){const p=$('#prevbook');if(p)location.href=p.href}
  if(e.key.toLowerCase()==='c'&&document.activeElement.tagName!=='INPUT'&&window._cur){try{navigator.clipboard.writeText(location.href.split('#')[0]+'#'+window._cur);const qc=$('#qcount');if(qc)qc.textContent='section link copied';}catch(err){}}});
$('#setbtn').onclick=()=>$('#drawer').classList.add('open');
const _pr=$('#prefreset');if(_pr)_pr.onclick=()=>{setP(PREF,{theme:'sepia',fs:18,width:'820px',font:'sans',lh:1.7});location.reload();};
$('#drawer .scrim').onclick=()=>$('#drawer').classList.remove('open');
$('#tocbtn').onclick=()=>tocToggle();
$$('aside.toc a').forEach(a=>a.onclick=()=>{if(innerWidth<=900)$('aside.toc').classList.remove('open')});
const back=$('#backbtn');
if(back)back.addEventListener('click',e=>{
  let sameOrigin=false;
  try{sameOrigin=!!document.referrer&&new URL(document.referrer,location.href).origin===location.origin;}catch(err){}
  if(sameOrigin&&history.length>1){e.preventDefault();history.back();}
});
const menuBtn=$('#mobilemenubtn');
if(menuBtn)menuBtn.onclick=()=>{const d=$('#drawer'),open=!d.classList.contains('open');d.classList.toggle('open',open);menuBtn.setAttribute('aria-expanded',String(open));};
const mobileMark=$('#mobilemarkbtn');
if(mobileMark)mobileMark.onclick=()=>{if(_mb)_mb.click();mobileMark.textContent=_mb?.textContent||'☆ Save';};
const mobileQ=$('#mobileq'),bookQ=$('#q');
if(mobileQ&&bookQ){mobileQ.addEventListener('input',()=>{bookQ.value=mobileQ.value;});mobileQ.addEventListener('keydown',e=>{if(e.key==='Enter'){bookQ.value=mobileQ.value;bookQ.dispatchEvent(new KeyboardEvent('keydown',{key:'Enter'}));}});}
const topBtn=$('#topbtn');let topTimer;
function syncTop(){if(!topBtn)return;const eligible=scrollY>innerHeight*.9;topBtn.classList.toggle('on',eligible);clearTimeout(topTimer);if(eligible)topTimer=setTimeout(()=>topBtn.classList.remove('on'),2800);}
window.addEventListener('scroll',syncTop,{passive:true});
if(topBtn)topBtn.onclick=()=>window.scrollTo({top:0,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
window.addEventListener('hashchange',tocUpdate);
window.addEventListener('pageshow',tocUpdate);
function lockScroll(){const any=$('#drawer').classList.contains('open')||document.querySelector('aside.toc').classList.contains('open');document.body.classList.toggle('toc-open',document.querySelector('aside.toc').classList.contains('open')&&matchMedia('(max-width:900px)').matches);document.body.classList.toggle('lock',any);document.querySelector('aside.toc').setAttribute('aria-modal',document.querySelector('aside.toc').classList.contains('open')?'true':'false');document.querySelector('#drawer .panel').setAttribute('aria-modal',$('#drawer').classList.contains('open')?'true':'false');}
new MutationObserver(lockScroll).observe(document.querySelector('aside.toc'),{attributes:true,attributeFilter:['class']});
new MutationObserver(lockScroll).observe($('#drawer'),{attributes:true,attributeFilter:['class']});
function tocToggle(){const mob=matchMedia('(max-width:900px)').matches;const toc=document.querySelector('aside.toc');if(mob){toc.classList.toggle('open');}else{document.body.classList.toggle('toc-hide');}lockScroll();const tb=$('#tocbtn');if(tb)tb.setAttribute('aria-expanded',String(!document.body.classList.contains('toc-hide')));}
const _tocx=$('#tocx');if(_tocx)_tocx.onclick=()=>{document.querySelector('aside.toc').classList.remove('open');document.body.classList.add('toc-hide');lockScroll();const tb=$('#tocbtn');if(tb)tb.focus();};const _ts=$('#tocscrim');if(_ts)_ts.onclick=()=>{document.querySelector('aside.toc').classList.remove('open');lockScroll();const tb=$('#tocbtn');if(tb)tb.focus();};(function(){const toc=document.querySelector('aside.toc');let sx=0;toc.addEventListener('touchstart',e=>{sx=e.touches[0].clientX},{passive:true});toc.addEventListener('touchend',e=>{if(sx-e.changedTouches[0].clientX>60&&matchMedia('(max-width:900px)').matches&&toc.classList.contains('open')){toc.classList.remove('open');lockScroll();const tb=$('#tocbtn');if(tb)tb.focus();}sx=0;},{passive:true});})();
const _setx=$('#setx');if(_setx)_setx.onclick=()=>{$('#drawer').classList.remove('open');lockScroll();};
document.addEventListener('keydown',e=>{if(e.key!=='Tab')return;const open=document.querySelector('aside.toc.open')||document.querySelector('#drawer.open');if(!open)return;const f=[...open.querySelectorAll('button,a[href],input,[tabindex]')].filter(el=>el.offsetParent);if(!f.length)return;if(e.shiftKey&&document.activeElement===f[0]){e.preventDefault();f[f.length-1].focus();}else if(!e.shiftKey&&document.activeElement===f[f.length-1]){e.preventDefault();f[0].focus();}});
// Fullscreen: Fullscreen API where available, CSS-immersive fallback otherwise. Per-session toggle (never auto-restored).
function syncFS(){const on=document.body.classList.contains('fs');const bar=$('#fsbar');if(bar)bar.hidden=!on;const fb=$('#fsbtn');if(fb)fb.setAttribute('aria-pressed',on?'true':'false');}
function setFS(on){if(on){document.body.classList.add('fs');try{const el=document.documentElement;const pr=el.requestFullscreen&&el.requestFullscreen();if(pr&&pr.catch)pr.catch(()=>{});}catch(err){}}else{document.body.classList.remove('fs');try{if(document.fullscreenElement&&document.exitFullscreen)document.exitFullscreen().catch(()=>{});}catch(err){}}syncFS();}
document.addEventListener('fullscreenchange',()=>{if(!document.fullscreenElement)document.body.classList.remove('fs');syncFS();});
const _fsb=$('#fsbtn'),_fsm=$('#fsbtnm');if(_fsb)_fsb.onclick=()=>setFS(!document.body.classList.contains('fs'));if(_fsm)_fsm.onclick=()=>{$('#drawer').classList.remove('open');setFS(!document.body.classList.contains('fs'));};
const _ft=$('#fs-toc');if(_ft)_ft.onclick=()=>tocToggle();
const _fx=$('#fs-exit');if(_fx)_fx.onclick=()=>setFS(false);
const _fth=$('#fs-theme');if(_fth)_fth.onclick=()=>{setOpt('theme',RTHEMES[(RTHEMES.indexOf(pref.theme)+1)%RTHEMES.length]);};
function _fsStep(dd){const S=[16,18,20,22];let i=S.indexOf(pref.fs);if(i<0)i=1;setOpt('fs',S[Math.min(S.length-1,Math.max(0,i+dd))]);}
const _fd=$('#fs-dec'),_fi=$('#fs-inc');if(_fd)_fd.onclick=()=>_fsStep(-1);if(_fi)_fi.onclick=()=>_fsStep(1);
applyPref();tocUpdate();syncFS();
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


def md_inline(text):
    """Render the small Markdown inline subset used by the knowledge base."""
    text = html.escape(text, quote=False)
    text = re.sub(r"`([^`]+)`", r'<code>\1</code>', text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<b>\1</b>", text)
    text = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", text)
    return text


def markdown_pages(path, title):
    """Build readable print/reader pages when a legacy PDF shell is empty."""
    raw = open(path, encoding="utf-8").read()
    raw = re.sub(r"^---.*?---\s*", "", raw, flags=re.S)
    raw = re.sub(r"<!--.*?-->\s*", "", raw, flags=re.S)
    lines = raw.replace("\r\n", "\n").split("\n")
    pages = []
    current = []
    in_code = False
    code = []
    lang = "code"

    def flush():
        nonlocal current
        if current:
            pages.append("".join(current))
            current = []

    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("```"):
            if in_code:
                current.append('<pre class="codeblock" data-lang="' + html.escape(lang, quote=True) + '"><code>' + html.escape("\n".join(code)) + '</code></pre>')
                code = []
                in_code = False
            else:
                in_code = True
                lang = line[3:].strip() or "code"
            i += 1
            continue
        if in_code:
            code.append(line)
            i += 1
            continue
        if not line.strip():
            i += 1
            continue
        m = re.match(r"^(#{1,4})\s+(.+)$", line)
        if m:
            if len(m.group(1)) == 1:
                i += 1
                continue
            if len(current) and len(current) > 18:
                flush()
            current.append(f'<h3 class="sec">{md_inline(m.group(2))}</h3>')
            i += 1
            continue
        if line.startswith("> "):
            current.append(f'<p class="body"><em>{md_inline(line[2:])}</em></p>')
            i += 1
            continue
        if re.match(r"^[-*]\s+", line):
            items = []
            while i < len(lines) and re.match(r"^[-*]\s+", lines[i]):
                _item = re.sub(r"^[-*]\s+", "", lines[i])
                if re.match(r"^\[ \]\s*", _item):
                    items.append('<li class="step">' + md_inline(re.sub(r"^\[ \]\s*", "", _item)) + "</li>")
                else:
                    items.append("<li>" + md_inline(_item) + "</li>")
                i += 1
            current.append('<ul class="tight">' + "".join(items) + "</ul>")
            continue
        if re.match(r"^\d+[.)]\s+", line):
            items = []
            while i < len(lines) and re.match(r"^\d+[.)]\s+", lines[i]):
                items.append("<li>" + md_inline(re.sub(r"^\d+[.)]\s+", "", lines[i])) + "</li>")
                i += 1
            current.append('<ol class="tight">' + "".join(items) + "</ol>")
            continue
        paragraph = [line.strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#{1,4})\s+|^>\s|^[-*]\s+|^\d+[.)]\s+|^```", lines[i]):
            paragraph.append(lines[i].strip())
            i += 1
        current.append('<p class="body">' + md_inline(" ".join(paragraph)) + '</p>')
    if in_code and code:
        current.append('<pre class="codeblock" data-lang="' + html.escape(lang, quote=True) + '"><code>' + html.escape("\n".join(code)) + '</code></pre>')
    flush()
    cover = (f'<div class="page cover"><div class="brand">CI/CD ENGINEERING · KNOWLEDGE BASE</div>'
             f'<h1>{html.escape(title)}</h1><p class="sub">CICD BY Nabawy</p>'
             f'<div class="cover foot" style="gap:18px"><span>Reader edition</span><span class="sig">Nabawy</span></div></div>')
    return [cover.replace('class="page cover"', 'class="page cover md-fallback"')] + [f'<div class="page md-fallback">{p}<div class="pfoot"><span>CICD BY Nabawy</span><span>{i + 2}</span></div></div>' for i, p in enumerate(pages)]


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
        heads = re.findall(r"<(h2|h3|h4)([^>]*)>(.*?)</\1>", p, re.S)
        if not heads:
            m = re.search(r"<h1[^>]*>(.*?)</h1>", p, re.S)
            label = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else f"Page {i+1}"
            items.append((f"p{i+1}", "Cover — " + label[:40], 1))
            continue
        for heading_index, (tag, attrs, htxt) in enumerate(heads, 1):
            clean = re.sub(r"<[^>]+>", "", htxt).strip()
            if not clean:
                continue
            m = re.search(r'id="([^"]+)"', attrs)
            anchor = m.group(1) if m else f"p{i+1}-h{heading_index}"
            if tag == "h2":
                n1 += 1; n2 = n3 = 0; num = f"{n1}"
                lvl = 1
            elif tag == "h3":
                n2 += 1; n3 = 0; num = f"{n1}.{n2}" if n1 else f"{n2}"
                lvl = 2
            else:
                n3 += 1
                if n1:
                    num = f"{n1}.{n2}.{n3}"
                elif n2:
                    num = f"{n2}.{n3}"
                else:
                    num = f"{n3}"
                lvl = 3
            items.append((anchor, f"{num} {clean[:60]}", lvl))
    return items


DIFF_RANK = {"Beginner": 0, "Intermediate": 1, "Advanced": 2}
CAT_HEX = {"CI/CD":"#5B8DEF","Build":"#F5A524","Testing":"#2ECC71","Security":"#E5484D","Reliability":"#9B7BF0","Jenkins":"#22B8CF","Delivery":"#F472B6","GitHub":"#94A3B8","Platforms":"#F97316","Labs":"#EAB308","Reference":"#64748B","Roadmap":"#18E299"}
DIF_SHORT = {"Beginner":"Beg","Intermediate":"Int","Advanced":"Adv"}
DIF_CLS = {"Beginner":"beg","Intermediate":"int","Advanced":"adv"}


def reader_url(b):
    """Single URL-building rule for reader pages; library cards and roadmap share it."""
    return f"read/{b['id']}.html"


CATEGORY_ICONS = {
    "CI/CD": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="5" cy="12" r="1.9"/><circle cx="19" cy="6" r="1.9"/><circle cx="19" cy="18" r="1.9"/><path d="M7.2 12h5M13.4 7.4l3-1M13.4 16.6l3 1"/><path d="M9 8l-2 4 2 4M15 8l2 4-2 4" opacity=".7"/></svg>',
    "Jenkins": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M7 8h10M7 12h10M7 16h10"/><circle cx="12" cy="12" r="9" opacity=".35"/></svg>',
    "Labs": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 3h6v6l3 5a3 3 0 01-3 4H9a3 3 0 01-3-4l3-5V3z"/><path d="M8 14h8" opacity=".6"/></svg>',
    "Platforms": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l8 4-8 4-8-4z"/><path d="M4 10l8 4 8-4"/><path d="M4 14l8 4 8-4"/><path d="M4 18l8 4 8-4" opacity=".4"/></svg>',
    "Roadmap": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 3L4 5v14l5-2 6 2 5-2V3l-5 2z"/><path d="M9 5v14M15 7v14"/></svg>',
    "Build": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14.5 6l3.5 3.5-8 8H6v-4l8.5-8z"/><path d="M11 9l3 3"/><path d="M13 6l3-3 3 3-3 3-3-3z" opacity=".5"/></svg>',
    "Testing": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 3h6"/><path d="M10 7a5 5 0 1010 0 5 5 0 00-10 0z"/><path d="M12 12v3l2 2"/><path d="M8 14h8" opacity=".6"/></svg>',
    "Delivery": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l4 6-4 12-4-12z"/><path d="M8 9h8"/><path d="M10 3v4M14 3v4" opacity=".6"/><circle cx="12" cy="9" r="1.2" fill="currentColor" stroke="none"/></svg>',
    "Security": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3l7 4v5c0 4.2-2.8 7.3-7 9-4.2-1.7-7-4.8-7-9V7z"/><path d="M9 12l2 2 4-4" opacity=".9"/></svg>',
    "Reliability": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 12h4l2-4 3 7 2-4h7"/><circle cx="12" cy="12" r="9" opacity=".2"/></svg>',
    "Reference": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 4h8a2 2 0 012 2v12a2 2 0 01-2 2H6z"/><path d="M6 8h6"/><path d="M6 12h6"/><path d="M6 16h4" opacity=".6"/></svg>',
    "GitHub": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 3a9 9 0 00-3 17.5"/><path d="M9 18c-2.2 1-3-1-3-1"/><path d="M12 16c-1 .3-2 .1-2.5-.8"/><path d="M14.5 18V15a2.5 2.5 0 00-.7-1.8c1.6-.2 3.2-.8 3.2-3.5a2.7 2.7 0 00-.7-1.9s-.6-.2-2 .7a7.8 7.8 0 00-3.6 0c-1.4-.9-2-.7-2-.7a2.7 2.7 0 00-.7 1.9c0 2.7 1.6 3.3 3.2 3.5A2.5 2.5 0 0011.5 15v3"/><circle cx="12" cy="3" r=".3" fill="currentColor"/></svg>',
}

def _slug_cat(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-").replace("--","-")

def build_map_page(books, output_dir, paths_html=""):
    """Home — 12 pseudo-3D blocks derived from books.json categories at build time.
    No second manifest: grouping, counts, difficulty spread computed here.
    Reuses card() markup for detail views, BASE_CSS vars for theming.
    """
    from collections import Counter
    bycat = {}
    for b in books:
        bycat.setdefault(b["category"], []).append(b)
    # deterministic order: CAT_ORDER first, then rest alpha; no hardcoded count
    CAT_ORDER = ["CI/CD","Jenkins","Labs","Platforms","Roadmap","Build","Testing","Delivery","Security","Reliability","Reference","GitHub"]
    cats_sorted = [c for c in CAT_ORDER if c in bycat] + sorted([c for c in bycat if c not in CAT_ORDER])
    CAT_COLORS_MAP = CAT_HEX
    # Build blocks html
    blocks_html = ""
    detail_html = ""
    cat_chips = []
    for cat in cats_sorted:
        bs = sorted(bycat[cat], key=lambda x: (DIFF_RANK.get(x["difficulty"],9), x["title"].lower()))
        cnt = len(bs)
        slug = _slug_cat(cat)
        cat_chips.append((slug, cat))
        color = CAT_COLORS_MAP.get(cat, "#18E299")
        icon = CATEGORY_ICONS.get(cat, CATEGORY_ICONS["Reference"])
        diff_cnt = Counter(b["difficulty"] for b in bs)
        pills = ""
        for lvl in ["Beginner","Intermediate","Advanced"]:
            n = diff_cnt.get(lvl,0)
            if n:
                pills += f'<span class="map-pill"><b>{n}</b> {lvl[:3]}</span>'
        # Difficulty bar: proportional segments (beg/int/adv)
        total_d = sum(diff_cnt.values()) or 1
        bar_segs = ""
        for lvl, cls in [("Beginner","beg"),("Intermediate","int"),("Advanced","adv")]:
            n = diff_cnt.get(lvl,0)
            if n:
                pct = max(12, round(n/total_d*100))
                bar_segs += f'<span class="map-diff-seg {cls}" style="width:{pct}%" title="{lvl}: {n}"></span>'
        # Dots variant for small counts
        dots = ""
        for lvl, cls in [("Beginner","beg"),("Intermediate","int"),("Advanced","adv")]:
            n = diff_cnt.get(lvl,0)
            for _ in range(n):
                dots += f'<i class="{cls}" title="{lvl}"></i>'
        # Preview titles: 2-3 books in this category
        preview_titles = bs[:3]
        preview_items = "".join(f'<li>{html.escape(b["title"])}</li>' for b in preview_titles)
        more_n = cnt - len(preview_titles)
        more_txt = f'<div class="map-preview-more">+{more_n} more</div>' if more_n>0 else ""
        preview_html = f'<div class="map-preview" aria-hidden="true"><div class="map-preview-title">Inside — {cnt} books</div><ul>{preview_items}</ul>{more_txt}</div>' if cnt else ""
        # aria-label
        aria_parts = [f"{diff_cnt.get(l,0)} {l}" for l in ["Beginner","Intermediate","Advanced"] if diff_cnt.get(l,0)]
        aria = html.escape(f"{cat} — {cnt} {'book' if cnt==1 else 'books'}" + (", " + ", ".join(aria_parts) if aria_parts else ""))
        count_label = f"{cnt} {'book' if cnt==1 else 'books'}"
        blocks_html += (
            f'<a href="#{slug}" class="map-block" data-cat="{html.escape(cat)}" id="block-{slug}" '
            f'style="--cat:{color}" data-slug="{slug}" aria-label="{aria}" tabindex="0">'
            f'<button class="map-preview-btn" aria-label="Preview {html.escape(cat)} contents" data-preview-btn="{slug}">…</button>'
            f'<div class="map-block-inner">'
            f'<div class="map-block-top"><span class="map-icon" aria-hidden="true">{icon}</span>'
            f'<span class="map-cat">{html.escape(cat)}</span></div>'
            f'<span class="map-count">{count_label}</span>'
            f'<div class="map-difficulty"><span class="map-diff-label">Level mix</span><span class="map-diff-bar">{bar_segs}</span><span class="map-diff-dots">{dots}</span><span class="map-diff-count">{cnt}</span></div>'
            f'<span class="map-pills">{pills}</span>'
            f'</div>'
            f'{preview_html}'
            f'</a>'
        )
        # detail view — themed interior with improved card hierarchy
        cat_desc = {"CI/CD":"Fundamentals: lifecycle, branching, pipelines & artifacts","Jenkins":"Controllers, agents, pipelines, Groovy & plugins","Labs":"Hands-on labs — build, deploy & recover","Platforms":"Jenkins, GitHub Actions, GitLab & ArgoCD","Roadmap":"Planned paths through the library","Build":"Hermetic builds, BuildKit & Kaniko","Testing":"Strategy, pyramids & flaky tests","Delivery":"Releasable always, deployed by decision","Security":"Signing, SBOM & supply chain","Reliability":"Rollback, recovery & resilience","Reference":"Cheatsheets & quick lookup","GitHub":"Actions, workflows & automation"}.get(cat, f"{cnt} books in {cat}")
        cards = ""
        for b in bs:
            idx = next((i for i, x in enumerate(books) if x["id"]==b["id"]), 0)
            tmin = b.get("time_minutes", 30)
            tags = " ".join(b.get("tags", []))
            diff_cls = {"Beginner":"beg","Intermediate":"int","Advanced":"adv"}.get(b["difficulty"],"int")
            desc_short = b.get("description","")[:140]
            book_icon = CATEGORY_ICONS.get(b["category"], CATEGORY_ICONS["Reference"])
            cards += (
                f'<div class="card book" data-id="{__import__("html").escape(b["id"])}" data-cat="{__import__("html").escape(b["category"])}" data-dif="{__import__("html").escape(b["difficulty"])}" data-time="{tmin}" data-tags="{__import__("html").escape(tags)}" data-title="{__import__("html").escape(b["title"])}" data-desc="{__import__("html").escape(b.get("description",""))}" style="--cat:{color}">'
                f'<div class="map-card-top">'
                f'<div class="map-card-head"><span class="map-icon" aria-hidden="true">{book_icon}</span><div class="map-card-meta"><span class="map-card-badge {diff_cls}">{html.escape(b["difficulty"])}</span><span class="map-card-time">{tmin} min · {html.escape(b.get("path",""))}</span></div></div>'
                f'<h3><a href="read/{__import__("html").escape(b["id"])}.html">{__import__("html").escape(b["title"])}</a></h3>'
                f'<p class="desc">{html.escape(desc_short)}</p>'
                f'</div>'
                f'<div class="map-card-footer"><a class="read" href="read/{__import__("html").escape(b["id"])}.html">Read</a></div>'
                f'</div>'
            )
        detail_html += (
            f'<section class="map-detail" id="detail-{slug}" data-cat="{html.escape(cat)}" aria-label="{html.escape(cat)} books" style="--cat:{color}">'
            f'<button class="map-back" data-back aria-label="Back to map">← Back to map</button>'
            f'<div class="map-detail-hero" style="--cat:{color}"><div class="map-detail-hero-top">'
            f'<span class="map-icon" aria-hidden="true">{CATEGORY_ICONS.get(cat, CATEGORY_ICONS["Reference"])}</span>'
            f'<h2>{html.escape(cat)}</h2><span class="count">{cnt} {"book" if cnt==1 else "books"}</span></div>'
            f'<p class="desc">{html.escape(cat_desc)}</p>'
            f'<div class="map-difficulty"><span class="map-diff-label">Level mix</span><span class="map-diff-bar">{bar_segs}</span><span class="map-diff-dots">{dots}</span><span class="map-diff-count">{cnt}</span></div>'
            f'<span class="map-pills">{pills}</span></div>'
            f'<div class="map-cards">{cards}</div>'
            f'</section>'
        )
    empty_chips = "".join(f'<a class="chip" href="#{s}">{html.escape(c)}</a>' for s, c in cat_chips)
    n_paths = len({b.get("path", "") for b in books if b.get("path")})
    n_hours = sum(b.get("time_minutes", 30) for b in books) // 60
    ranked = [b for b in books if b.get("difficulty") in DIFF_RANK]
    inv = {v: k for k, v in DIFF_RANK.items()}
    lo_s = DIF_SHORT.get(inv[min((DIFF_RANK[b["difficulty"]] for b in ranked), default=1)], "") if ranked else ""
    hi_s = DIF_SHORT.get(inv[max((DIFF_RANK[b["difficulty"]] for b in ranked), default=1)], "") if ranked else ""
    lvl = lo_s if lo_s == hi_s else f"{lo_s}→{hi_s}"
    stats_pills = (
        f'<span class="stat-pill"><b>{len(books)}</b> books</span>'
        f'<span class="stat-pill"><b>{n_paths}</b> learning paths</span>'
        f'<span class="stat-pill"><b>~{n_hours}h</b> end to end</span>'
        f'<span class="stat-pill stat-level"><b>{lvl}</b> levels</span>'
    )
    # Site header chrome: reuse same header as index, with Home active
    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<title>CICD BY Nabawy</title>
{seo_tags("CICD BY Nabawy", "Home of the CI/CD library — 14 merged handbooks plus ordered learning paths.", f"{SITE_URL}/")}
<style>{BASE_CSS}</style><script>try{{var _p=JSON.parse(localStorage.getItem('cicdlib:pref')||'null');var _t=_p&&_p.theme;var _ok=['sepia','dark','light','dim','contrast'].indexOf(_t)>=0;document.documentElement.dataset.theme=_ok?_t:'sepia'}}catch(e){{document.documentElement.dataset.theme='sepia'}}</script>
</head>
<body>
<header class="top"><div class="wrap">
<a class="logo" href="index.html" style="color:inherit"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="5" cy="12" r="2.6" stroke="#18E299" stroke-width="2"/><circle cx="19" cy="6" r="2.6" stroke="#18E299" stroke-width="2"/><circle cx="19" cy="18" r="2.6" stroke="#18E299" stroke-width="2"/><path d="M7.6 12h5.2m0 0-2.6-2.6m2.6 2.6-2.6 2.6M13.4 7.4l2.8-1M13.4 16.6l2.8 1" stroke="#18E299" stroke-width="2" stroke-linecap="round"/></svg>CICD<span> BY Nabawy</span></a>
<div class="search"><div class="searchwrap"><input id="q" type="search" placeholder="Search all {len(books)} books…" autocomplete="off"><div class="searchdrop" id="qdrop" role="listbox"></div></div><kbd>⌘K</kbd></div>
<a class="btn" href="index.html" aria-current="page" style="text-decoration:none;border-color:var(--brand);color:var(--brand)">Home</a>
<a class="btn" href="roadmap/" style="text-decoration:none">Roadmap</a>
<a class="btn" href="glossary.html" style="text-decoration:none">Glossary</a>
<button class="btn" id="themebtn" aria-label="Toggle theme">☀</button>
</div></header>
<div class="wrap">
<div class="map-hero">
<div class="map-hero-inner"><span class="eyebrow">HOME</span>
<h1>The whole building, <span style="color:var(--mut)">one glance.</span></h1>
<div class="herocta"><a class="btn prim" href="read/start-here.html">Start here <span aria-hidden="true">→</span></a><a class="btn" href="roadmap/">Follow the roadmap</a></div>
<div class="stat-row">{stats_pills}</div></div>
<div class="pipeline" aria-hidden="true"><svg width="1000" height="170" viewBox="0 0 1000 170" fill="none">
<defs><g id="nd"><circle class="pnode" cx="0" cy="0" r="26"/><circle class="pcore" cx="0" cy="0" r="7"/></g>
<g id="ndm"><circle class="pnode mut" cx="0" cy="0" r="26"/><circle class="pcore mut" cx="0" cy="0" r="7"/></g></defs>
<path class="pedge live" d="M106 70 C 200 70, 228 60, 264 60"/>
<path class="pedge" d="M316 60 C 390 60, 412 76, 464 76"/>
<path class="pedge" d="M516 76 C 570 76, 592 62, 654 62"/>
<path class="pedge live" d="M706 62 C 775 62, 805 68, 854 68"/>
<g><use href="#nd" x="80" y="70"/><text class="plabel" x="80" y="116" text-anchor="middle">Source</text></g>
<g><use href="#nd" x="290" y="60"/><text class="plabel" x="290" y="28" text-anchor="middle">Build</text></g>
<g><use href="#nd" x="490" y="76"/><text class="plabel" x="490" y="122" text-anchor="middle">Test</text></g>
<g><use href="#ndm" x="680" y="62"/><text class="plabel" x="680" y="30" text-anchor="middle">Artifact</text></g>
<g><use href="#nd" x="880" y="68"/><text class="plabel" x="880" y="114" text-anchor="middle">Deploy</text></g>
</svg></div>
</div>
<div class="map-grid" id="mapGrid" role="list" aria-label="Knowledge structure map">{blocks_html}</div>
{paths_html}
<div id="mapDetails">{detail_html}</div>
<div class="empty" id="mapEmpty" style="display:none"><p>That link doesn't match a category. Jump straight to one:</p><div class="empty-cats">{empty_chips}</div><a href="index.html">Back to overview</a></div>
</div>
<footer><div class="wrap"><span>CICD BY Nabawy</span><span><a href="index.html">Home</a> · <a href="roadmap/">Roadmap</a> · <a href="glossary.html">Glossary</a> · v2.1 Sep 2026</span></div></footer>
<script>
(function(){{
const $=s=>document.querySelector(s),$$=s=>[...document.querySelectorAll(s)];
function getP(k,d){{try{{const v=JSON.parse(localStorage.getItem(k));return v??d}}catch(e){{return d}}}}
function setP(k,v){{try{{localStorage.setItem(k,JSON.stringify(v))}}catch(e){{}}}}
const pref=getP('cicdlib:pref',{{theme:'sepia'}});
const THS=['sepia','dark','light'],THI={{dark:'☀',light:'☾',sepia:'◐'}};
function syncTheme(){{const th=THS.includes(pref.theme)?pref.theme:'sepia';document.documentElement.dataset.theme=th;const t=$('#themebtn');if(t)t.textContent=THI[th]||'☀'}}
syncTheme();
$('#themebtn').onclick=()=>{{pref.theme=THS[(THS.indexOf(pref.theme)+1)%THS.length];setP('cicdlib:pref',pref);syncTheme()}};
const grid=$('#mapGrid'),details=$$('.map-detail'),empty=$('#mapEmpty'),paths=$('#mapPaths');
function slugFromHash(){{return location.hash.replace(/^#/,'').trim().toLowerCase();}}
function showDetail(slug, push){{
  const target=document.getElementById('detail-'+slug);
  if(!slug){{ grid.style.display='';if(paths)paths.style.display=''; grid.classList.remove('hidden'); details.forEach(d=>d.classList.remove('active')); empty.style.display='none'; document.title='Home — CICD BY Nabawy'; return; }}
  if(!target){{ grid.style.display='none';if(paths)paths.style.display='none'; details.forEach(d=>d.classList.remove('active')); empty.style.display=''; return; }}
  grid.style.display='none';if(paths)paths.style.display='none'; grid.classList.add('hidden');
  details.forEach(d=>d.classList.toggle('active', d===target));
  empty.style.display='none';
  const cat=target.dataset.cat||slug;
  document.title=cat+' — CICD BY Nabawy';
  target.scrollIntoView({{block:'start'}});
}}
function navigate(slug){{ if(!slug){{ history.pushState(null,'',location.pathname); showDetail('',false); }} else {{ if(location.hash.slice(1)!==slug){{ location.hash='#'+slug; }} else {{ showDetail(slug,false); }} }} }}
$$('.map-block').forEach(a=>{{
  a.addEventListener('keydown',e=>{{
    if(e.key===' '||e.key==='Spacebar'){{ e.preventDefault(); a.click(); }}
    if(e.key==='Enter'){{ /* anchor handles natively */ }}
  }});
}});
/* touch preview toggle (mobile where hover doesn't exist) */
$$('[data-preview-btn]').forEach(btn=>{{
  btn.addEventListener('click', e=>{{
    e.preventDefault(); e.stopPropagation();
    const card = btn.closest('.map-block');
    const wasOpen = card.classList.contains('preview-open');
    $$('.map-block.preview-open').forEach(c=>c.classList.remove('preview-open'));
    if(!wasOpen) card.classList.add('preview-open');
  }});
}});
document.addEventListener('click', e=>{{
  if(!e.target.closest('.map-block')) $$('.map-block.preview-open').forEach(c=>c.classList.remove('preview-open'));
}});
$$('[data-back]').forEach(b=>b.addEventListener('click',()=>{{
  const active = document.querySelector('.map-detail.active');
  const prefersReduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  function backHome(){{
    if(location.hash){{ history.pushState(null,'',location.pathname+location.search); }}
    if(active)active.classList.remove('exiting');
    showDetail('',false);
    window.scrollTo({{top:0,behavior: prefersReduced ? 'auto':'smooth'}});
  }}
  if(active && !prefersReduced){{
    active.classList.add('exiting');
    active.addEventListener('animationend', backHome, {{once:true}});
    setTimeout(()=>{{ if(document.querySelector('.map-detail.exiting')) backHome(); }}, 500);
  }} else {{
    backHome();
  }}
}}));;
window.addEventListener('hashchange',()=>showDetail(slugFromHash(),false));
window.addEventListener('popstate',()=>showDetail(slugFromHash(),false));
const initial=slugFromHash();
if(initial) showDetail(initial,false);
}})();
</script>
</body>
</html>"""
    pathlib.Path(output_dir, "index.html").write_text(page, encoding="utf-8")
    redir = ("<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"UTF-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\">"
        "<title>Home — CICD BY Nabawy</title>"
        "<link rel=\"canonical\" href=\"https://eslamnabawy.github.io/cicd-by-nabawy/\">"
        "<meta http-equiv=\"refresh\" content=\"0; url=./\">"
        "<script>location.replace('./'+location.hash)</script>"
        "</head><body><p>Map moved home — <a href=\"./\">continue home</a>.</p></body></html>")
    pathlib.Path(output_dir, "map.html").write_text(redir, encoding="utf-8")
    print(f"BUILT home: {len(books)} books in {len(cats_sorted)} categories -> {output_dir}/index.html (+ map.html redirect)")

def build_roadmap_page(books, output_dir):
    """Ordered learning roadmap: every manifest book as a milestone stop,

    grouped by the ordered paths in content/paths.json (single taxonomy,
    shared with home/reader). Same tokens, same card language.
    """
    try:
        _pd = json.load(open(os.path.join(ROOT, "content", "paths.json"), encoding="utf-8"))
        _order, _pathmeta = _pd.get("order", []), _pd.get("paths", {})
    except Exception:
        _order, _pathmeta = [], {}
    def slug(name):
        return "rm-" + re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")

    _bypath = {}
    for b in books:
        _bypath.setdefault(b.get("path", ""), []).append(b)
    if _order:
        sections = [(_pathmeta.get(p, {}).get("label", p), _pathmeta.get(p, {}).get("desc", ""),
                      [x for x in books if x.get("path") == p]) for p in _order]
        sections = [(l, dd, bs) for l, dd, bs in sections if bs]
    else:
        groups = {}
        for b in books:
            groups.setdefault(b["category"], []).append(b)
        sections = [(c, "", sorted(bs, key=lambda b: (DIFF_RANK.get(b["difficulty"], 9), b["title"].lower())))
                    for c, bs in sorted(groups.items())]

    mile = [0]

    def rcard(b):
        mile[0] += 1
        return (
            f'<li class="stop" data-mile="{mile[0]:02d}" data-cat="{b["category"]}" data-book="{b["id"]}">'
            f'<div class="card book" data-cat="{b["category"]}" data-title="{html.escape(b["title"])}">'
            f'<span class="num">{html.escape(b["category"])} \u00b7 {b.get("time_minutes", 30)} min</span><h3>{html.escape(b["title"])}</h3>'
            f'<p>{html.escape(b.get("description", ""))}</p>'
            f'<div class="dif"><i></i>{b["difficulty"]}</div>'
            f'<a class="read" href="../{reader_url(b)}">Read</a></div></li>'
        )

    jump = ("<div class=\"jumpnav\">" + "".join(
        f"<a href=\"#{slug(n)}\">{n} · {len(bs)}</a>" for n, dd, bs in sections) + "</div>")
    body = '<div class="trip"><span>START · 01</span></div>' + "".join(
        f'<section class="shelf" id="{slug(n)}"><div class="shelf-head"><h2>{n}</h2>'
        f"<span>{len(bs)} book" + ("s" if len(bs) != 1 else "") + f" \u00b7 ~{sum(b.get('time_minutes', 30) for b in bs)} min</span>"
        f"<p>{html.escape(dd)}</p></div>"
        f"<ol class=\"route\">" + "".join(rcard(b) for b in bs) + "</ol></section>"
        for n, dd, bs in sections) + '<div class="trip"><span>FINISH · SHIP IT</span></div>'

    page = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<title>Roadmap — CICD BY Nabawy</title>
{seo_tags("Roadmap — CICD BY Nabawy", "Visual roadmap of all " + str(len(books)) + " books in path order — the same source as the library.", f"{SITE_URL}/roadmap/")}
<style>{BASE_CSS}</style><script>try{{var _p=JSON.parse(localStorage.getItem('cicdlib:pref')||'null');var _t=_p&&_p.theme;var _ok=['sepia','dark','light','dim','contrast'].indexOf(_t)>=0;document.documentElement.dataset.theme=_ok?_t:'sepia'}}catch(e){{document.documentElement.dataset.theme='sepia'}}</script>
</head>
<body>
<header class="top"><div class="wrap">
<a class="logo" href="../index.html" style="color:inherit"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="5" cy="12" r="2.6" stroke="#18E299" stroke-width="2"/><circle cx="19" cy="6" r="2.6" stroke="#18E299" stroke-width="2"/><circle cx="19" cy="18" r="2.6" stroke="#18E299" stroke-width="2"/><path d="M7.6 12h5.2m0 0-2.6-2.6m2.6 2.6-2.6 2.6M13.4 7.4l2.8-1M13.4 16.6l2.8 1" stroke="#18E299" stroke-width="2" stroke-linecap="round"/></svg>CICD<span> BY Nabawy</span></a>
<nav class="crumbs"><span class="sep">/</span><span class="here">Roadmap</span></nav>
<div class="search"></div>
<a class="btn" href="../index.html" style="text-decoration:none">Home</a>
<a class="btn" href="../glossary.html" style="text-decoration:none">Glossary</a>
<button class="btn" id="themebtn" aria-label="Toggle theme">☀</button>
</div></header>
<div class="wrap">
<div class="hero" style="padding:36px 24px 16px"><span class="eyebrow">ROADMAP</span><h1>Follow the path, <span>ship with confidence.</span></h1>
<p>{len(books)} stops in path order · ~{sum(b.get("time_minutes", 30) for b in books) // 60} hours end to end — same source as the library, impossible to drift.</p></div>
{jump}
{body}
</div>
<footer><div class="wrap"><span>CICD BY Nabawy</span></div></footer>
<script>
const $=s=>document.querySelector(s);
function getP(k,d){{try{{const v=JSON.parse(localStorage.getItem(k));return v??d}}catch(e){{return d}}}}
function setP(k,v){{try{{localStorage.setItem(k,JSON.stringify(v))}}catch(e){{}}}}
const pref=getP('cicdlib:pref',{{theme:'sepia'}});
const THS=['sepia','dark','light'],THI={{dark:'☀',light:'☾',sepia:'◐'}};
function syncTheme(){{const th=THS.includes(pref.theme)?pref.theme:'sepia';document.documentElement.dataset.theme=th;const t=$('#themebtn');if(t)t.textContent=THI[th]||'☀'}}
syncTheme();
$('#themebtn').onclick=()=>{{pref.theme=THS[(THS.indexOf(pref.theme)+1)%THS.length];setP('cicdlib:pref',pref);syncTheme()}};
try{{document.querySelectorAll('.stop[data-book]').forEach(s=>{{const p=getP('cicdlib:prog:'+s.dataset.book,null);if(p&&p.pct>=100){{const h=s.querySelector('h3');if(h&&!h.querySelector('.tick'))h.innerHTML+=' <span class="tick" style="color:var(--brand);font-weight:700">\u2713</span>';}}}});}}catch(e){{}}
</script>
</body>
</html>"""
    out = os.path.join(output_dir, "roadmap")
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, "index.html"), "w", encoding="utf-8").write(page)
    print(f"BUILT roadmap: {len(books)} books in {len(sections)} sections -> {out}")


def build():
    from collections import Counter
    books = json.load(open(os.path.join(ROOT, "content", "books.json"), encoding="utf-8"))
    os.makedirs(READ, exist_ok=True)
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

    def related_books(b, n=4):
        """Build-time static, context-aware: adjacent path steps first, then
        explicit prereq links, then same path / same category / shared tags."""
        seq = bypath.get(b.get("path", ""), [])
        ids = [x["id"] for x in seq]
        pos = ids.index(b["id"]) if b["id"] in ids else -1
        btags = set(b.get("tags", []))
        scored = []
        for o in books:
            if o["id"] == b["id"]:
                continue
            opos = ids.index(o["id"]) if o["id"] in ids else -1
            sig = []
            if pos >= 0 and opos >= 0:
                d = opos - pos
                if d == 1:
                    sig.append((12, "Next in path"))
                elif d == -1:
                    sig.append((10, "Previous in path"))
                else:
                    sig.append((4, "Same path"))
            if o["id"] in b.get("prereqs", []):
                sig.append((8, "Prerequisite"))
            elif b["id"] in o.get("prereqs", []):
                sig.append((8, "Follow-up"))
            if o["category"] == b["category"]:
                sig.append((3, "Same topic"))
            shared = len(btags & set(o.get("tags", [])))
            if shared:
                sig.append((2 * shared, "Shared tags"))
            score = sum(w for w, _ in sig)
            why = max(sig)[1] if sig else "More to explore"
            scored.append((score, o, why))
        scored.sort(key=lambda t: (-t[0], t[1]["title"]))
        return [(o, w) for _, o, w in scored[:n]]

    def path_next(b):
        seq = bypath.get(b.get("path", ""), [])
        ids = [x["id"] for x in seq]
        if b["id"] in ids and ids.index(b["id"]) + 1 < len(ids):
            return byid[ids[ids.index(b["id"]) + 1]]
        return None

    def related_box_html(rels):
        items = ""
        for o, why in rels:
            color = CAT_HEX.get(o.get("category", ""), "#18E299")
            icon = CATEGORY_ICONS.get(o.get("category", ""), CATEGORY_ICONS["Reference"])
            dc = DIF_CLS.get(o.get("difficulty", ""), "int")
            ds = DIF_SHORT.get(o.get("difficulty", ""), o.get("difficulty", ""))
            items += (
                f'<li class="relcard" data-cat="{html.escape(o.get("category", ""))}" style="--cat:{color}">'
                f'<span class="rel-icon" aria-hidden="true">{icon}</span>'
                f'<span class="rel-main"><a href="{o["id"]}.html">{html.escape(o["title"])}</a>'
                f'<span class="rel-meta">{o.get("time_minutes", 30)} min · <span class="difbadge {dc}">{ds}</span></span>'
                f'<span class="rel-why">→ {html.escape(why)}</span></span></li>')
        return f'<div class="relatedbox"><h4>Related books</h4><ul class="relgrid">{items}</ul></div>'

    def paths_section_html(wrap_id=""):
        """Journey cards: dominant-category accent+icon, connected numbered
        steps with difficulty badges + finish marker, pill footer stats."""
        cards = ""
        for pid in (PATH_ORDER or sorted(bypath.keys())):
            seq = bypath.get(pid, [])
            if not seq:
                continue
            label = PATHS.get(pid, {}).get("label", pid)
            desc = PATHS.get(pid, {}).get("desc", "")
            tmin = sum(x.get("time_minutes", 30) for x in seq)
            dom = Counter(x.get("category", "") for x in seq).most_common(1)[0][0]
            color = CAT_HEX.get(dom, "#18E299")
            icon = CATEGORY_ICONS.get(dom, CATEGORY_ICONS["Reference"])
            ranks = sorted(DIFF_RANK.get(x.get("difficulty", ""), 9) for x in seq)
            inv = {v: k for k, v in DIFF_RANK.items()}
            lo, hi = DIF_SHORT.get(inv.get(ranks[0], ""), ""), DIF_SHORT.get(inv.get(ranks[-1], ""), "")
            span = lo if lo == hi else f"{lo}→{hi}"
            steps = ""
            for n, x in enumerate(seq, 1):
                last = n == len(seq)
                dc = DIF_CLS.get(x.get("difficulty", ""), "int")
                ds = DIF_SHORT.get(x.get("difficulty", ""), x.get("difficulty", ""))
                fin = ' <span class="finpill">🏁 Finish</span>' if last else ""
                steps += (
                    f'<li class="pathstep{" finish" if last else ""}" data-n="{n:02d}">'
                    f'<a class="steptitle" href="read/{x["id"]}.html">{html.escape(x["title"])}</a>'
                    f'<span class="stepmeta">{x.get("time_minutes", 30)} min · <span class="difbadge {dc}">{ds}</span>{fin}</span></li>')
            long = " long" if len(seq) >= 6 else ""
            unit = "book" if len(seq) == 1 else "books"
            cards += (
                f'<article class="pathcard" id="path-{pid}" data-cat="{html.escape(dom)}" style="--cat:{color}" aria-label="{html.escape(label)} learning path">'
                f'<div class="pathcard-head"><span class="map-icon" aria-hidden="true">{icon}</span>'
                f'<div class="pathcard-titles"><h3>{html.escape(label)}</h3>'
                f'<span class="pathcount">{len(seq)} {unit} · ~{tmin} min</span></div></div>'
                f'<p class="pathdesc">{html.escape(desc)}</p>'
                f'<ol class="pathsteps{long}">{steps}</ol>'
                f'<div class="pathfoot"><span class="map-pill"><b>{len(seq)}</b> {unit}</span>'
                f'<span class="map-pill">~<b>{tmin}</b> min</span>'
                f'<span class="map-pill">Level <b>{span}</b></span></div></article>')
        inner = ('<div class="collectlabel">LEARNING PATHS</div>'
                 '<p class="sub">Ordered end to end — follow a path, don\u2019t wander shelves.</p>'
                 f'<div class="pathgrid" data-testid="learning-paths">{cards}</div>')
        return f'<div id="{wrap_id}">{inner}</div>' if wrap_id else inner

    build_map_page(books, DIST, paths_html=paths_section_html(wrap_id="mapPaths"))
    build_roadmap_page(books, DIST)
    # shared icon library: single source (KB assets) copied into dist
    shutil.rmtree(os.path.join(DIST, "assets"), ignore_errors=True)
    shutil.copytree(os.path.join(KB, "assets"), os.path.join(DIST, "assets"))
    # print editions ship with the site so reader "Open print HTML" works live
    shutil.rmtree(os.path.join(DIST, "pdf"), ignore_errors=True)
    shutil.copytree(PDF, os.path.join(DIST, "pdf"))
    stats = []

    # (path context + related/path helpers are defined at the top of build())

    all_sections = {}
    # P2.3: book id -> markdown source (from AUDIT_STRUCTURE mapping; 3 roadmaps are pdf-only)
    MD_MAP = {"start-here": "00-foundations/start-here-merged.md", "pipelines-build-test": "06-ci-cd-pipelines/pipelines-build-test.md", "artifacts": "05-artifacts-and-packaging/artifact-management.md", "delivery-envs": "07-continuous-delivery/delivery-envs-iac.md", "strategies": "10-deployment-strategies/deployment-strategies.md", "observe-recover-secure": "13-observability-and-feedback/observe-recover-secure.md", "jenkins-core": "15-platforms-and-tools/jenkins/jenkins-core-merged.md", "jenkins-advanced-ops": "15-platforms-and-tools/jenkins/jenkins-advanced-ops.md", "github-actions": "15-platforms-and-tools/github-actions.md", "gitlab-argocd": "15-platforms-and-tools/gitlab-argocd.md", "core-labs": "16-labs/core-labs-handbook.md", "jenkins-labs-handbook": "16-labs/jenkins-labs-handbook.md", "cheatsheet": "17-reference/command-cheatsheet.md"}
    all_body = {}
    for idx, b in enumerate(books):
        css, pages = parse_book(os.path.join(PDF, b["file"]))
        # Some older print files are shells with a cover but no article body.
        # The canonical Markdown source is the authoritative fallback so those
        # books and labs remain readable instead of silently rendering empty.
        source_path = MD_MAP.get(b["id"])
        page_text = re.sub(r"<[^>]+>", " ", "".join(pages))
        if source_path and os.path.exists(os.path.join(KB, source_path)) and len(page_text.strip()) < 500:
            pages = markdown_pages(os.path.join(KB, source_path), b["title"])
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
            f'<a href="../index.html">Home</a><span>›</span>'
            f'<a href="../index.html#path-{html.escape(b.get("path", ""))}">{html.escape(plabel)}</a><span>›</span>'
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
            hnum = 0
            def mark_heading(match):
                nonlocal hnum
                if 'id=' in match.group(2):
                    return match.group(0)
                hnum += 1
                return f'<{match.group(1)} id="p{i+1}-h{hnum}"{match.group(2)}>'
            # Same heading set as toc_of() (bare + attributed h2/h3/h4) so
            # per-heading anchors p{i}-h{n} stay aligned with TOC numbering.
            p = re.sub(r'<(h[234])([^>]*)>', mark_heading, p)
            body_pages.append(re.sub(r'class="page', f'id="p{i+1}" class="page', p, count=1))
        # Reader TOC is rebuilt from the post-strip, id-injected pages so
        # every entry points at a heading that exists in the output.
        # (The loop-top toc stays pre-strip for the search index.)
        toc = toc_of(body_pages)
        toc_html = "".join(f'<a href="#{page_id}" class="toc-l{lvl}" aria-label="{html.escape(t)}">{html.escape(t)}</a>' for page_id, t, lvl in toc)
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
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<title>{html.escape(b['title'])} — CICD BY Nabawy</title>
{seo_tags(f"{b['title']} — CICD BY Nabawy", b.get("description",""), f"{SITE_URL}/read/{b['id']}.html", og_type="article", image=f"{SITE_URL}/og/{b['id']}.{OG_EXT}")}
{(f'<link rel="prefetch" href="{upnext["id"]}.html">' if upnext else '') + (f'<link rel="prefetch" href="{nextb["id"]}.html">' if nextb and (not upnext or nextb["id"] != upnext["id"]) else '')}
<style>{BASE_CSS}</style><script>try{{var _p=JSON.parse(localStorage.getItem('cicdlib:pref')||'null');var _t=_p&&_p.theme;var _ok=['sepia','dark','light','dim','contrast'].indexOf(_t)>=0;document.documentElement.dataset.theme=_ok?_t:'sepia'}}catch(e){{document.documentElement.dataset.theme='sepia'}}</script>
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
<button class="btn tocbtn" id="tocbtn" aria-label="Open table of contents">{tocbtn_label}</button>
<nav class="crumbs"><a class="logo" href="../index.html" style="color:inherit"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="5" cy="12" r="2.6" stroke="#18E299" stroke-width="2"/><circle cx="19" cy="6" r="2.6" stroke="#18E299" stroke-width="2"/><circle cx="19" cy="18" r="2.6" stroke="#18E299" stroke-width="2"/><path d="M7.6 12h5.2m0 0-2.6-2.6m2.6 2.6-2.6 2.6M13.4 7.4l2.8-1M13.4 16.6l2.8 1" stroke="#18E299" stroke-width="2" stroke-linecap="round"/></svg>CICD<span> BY Nabawy</span></a>
<span class="sep">/</span>
<span class="here">{html.escape(b['title'])}</span></nav>
<div class="search"><input id="q" type="search" placeholder="Find in this book…" aria-label="Find in this book"><kbd>⌘K</kbd></div>
<span id="qcount" style="font-size:12px;color:var(--mut)"></span>
<button class="markbtn" id="markbtn" aria-label="Bookmark this book">☆ Save</button>
<a class="readback btn reader-nav" id="backbtn" href="../book/{b["id"]}.html">← Back</a>
<nav class="reader-nav" aria-label="Reader navigation"><a class="btn" href="../index.html" style="text-decoration:none">Home</a>
<a class="btn" href="../book/{b['id']}.html" style="text-decoration:none">Overview</a></nav>
<button class="btn" id="fsbtn" aria-label="Toggle fullscreen">⛶</button>
<button class="btn" id="setbtn" aria-label="Reading settings">⚙ A⁺</button>
<button class="btn mobilemenu" id="mobilemenubtn" aria-label="Open reader menu" aria-expanded="false">☰</button>
</div>
<div class="prog" style="height:3px;background:var(--line)"><b id="pbar" style="display:block;height:100%;width:0;background:var(--acc)"></b></div>
</header>
{contextbar}
<div class="rlayout">
<aside class="toc" role="dialog" aria-modal="false" aria-label="Table of contents"><div class="toc-head"><h4>CONTENTS · {len(pages)} PAGES · {len(toc)} SECTIONS</h4><button class="drawerx" id="tocx" aria-label="Close contents">×</button></div>{toc_html}
</aside><div class="tocscrim" id="tocscrim" aria-hidden="true"></div>
<main class="read"><div class="readbody">
{top_upnext}
{f'<div class="labbanner">🧪 Hands-on lab · {b.get("time_minutes", 45)} min · Env: {html.escape(b.get("lab_env", "See book overview"))} · <a href="../book/' + b["id"] + '.html">Overview &amp; prereqs</a> · <a href="../downloads/labs/' + b["id"] + '.pdf" download>Download PDF</a> · <button class="markbtn" id="labreset" style="margin-left:8px">Reset checks</button></div>' if is_lab else ''}
{''.join(body_pages)}
{f'<div class="upnext">Up next in {html.escape(PATHS.get(b.get("path", ""), {}).get("label", b.get("path", "")))} → <a href="{upnext["id"]}.html"><b>{html.escape(upnext["title"])}</b></a></div>' if upnext else ''}
{related_box_html(rels)}
<div class="chapnav">{prev_link}{next_link}</div>
</div></main>
<div id="lightbox" role="dialog" aria-label="Diagram viewer"><img alt="Enlarged diagram"></div>
</div>
<button class="topbtn" id="topbtn" aria-label="Back to top" title="Back to top">↑</button>
<div class="drawer" id="drawer"><div class="scrim"></div><div class="panel" role="dialog" aria-modal="false" aria-label="Reading settings"><button class="drawerx" id="setx" aria-label="Close settings">×</button>
<h3>Reading settings</h3>
<div class="setrow mobile-controls"><a class="readback btn" href="../book/{b["id"]}.html">← Back</a> <button class="btn" id="mobilemarkbtn">☆ Save</button><button class="btn" id="fsbtnm" aria-label="Toggle fullscreen">⛶</button><a class="btn" href="../index.html">Home</a><a class="btn" href="../book/{b['id']}.html">Overview</a></div>
<div class="setrow mobile-search"><label for="mobileq">Find in this book</label><input id="mobileq" type="search" placeholder="Search this book…"></div>
<div class="setrow"><h5>THEME</h5><div class="opts">
<button class="btn" data-k="theme" data-set="dark" onclick="setOpt('theme','dark')">Dark</button>
<button class="btn" data-k="theme" data-set="light" onclick="setOpt('theme','light')">Light</button>
<button class="btn" data-k="theme" data-set="sepia" onclick="setOpt('theme','sepia')">Sepia</button>
</div></div>
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
<div class="setrow"><button class="btn" id="prefreset">Reset reading settings</button></div>
</div></div>
<div id="fsbar" hidden><button class="btn" id="fs-toc" aria-label="Open contents">☰</button><button class="btn" id="fs-theme" aria-label="Cycle theme">◐</button><button class="btn" id="fs-dec" aria-label="Smaller text">A−</button><button class="btn" id="fs-inc" aria-label="Larger text">A+</button><span id="fs-prog">0%</span><button class="btn" id="fs-exit">⛶ Exit</button></div>
<script>{READER_JS}</script>
</body>
</html>"""
        open(os.path.join(READ, b["id"] + ".html"), "w", encoding="utf-8").write(page)
        stats.append((b, len(pages), len(toc)))

    # Dedicated lab manuals: same reader theme, direct lab-to-lab navigation,
    # checklists, and downloadable PDFs without mixing labs into the library UI.
    lab_dir = os.path.join(DIST, "labs")
    os.makedirs(lab_dir, exist_ok=True)
    lab_books = [b for b in books if b.get("category") == "Labs"]
    for b in lab_books:
        source = os.path.join(READ, b["id"] + ".html")
        target = os.path.join(lab_dir, b["id"] + ".html")
        shutil.copyfile(source, target)
    lab_links = "".join(
        f'<li><a href="{b["id"]}.html">{html.escape(b["title"])}</a>'
        f'<span>{b.get("time_minutes", 45)} min · {html.escape(b.get("lab_env", "Hands-on environment"))}</span></li>'
        for b in lab_books
    )
    lab_index = f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><title>Hands-on Labs — CICD BY Nabawy</title>{seo_tags("Hands-on Labs — CICD BY Nabawy", "Direct HTML manuals for every CI/CD lab.", f"{SITE_URL}/labs/")}<style>{BASE_CSS}.lab-index{{max-width:920px;margin:0 auto;padding:54px 24px 90px}}.lab-index h1{{font-size:42px;margin:12px 0}}.lab-index p{{color:var(--mut);font-size:17px;max-width:680px;line-height:1.6}}.lab-index ul{{list-style:none;padding:0;margin:34px 0;display:grid;gap:10px}}.lab-index li{{display:flex;justify-content:space-between;align-items:center;gap:18px;padding:18px 20px;background:var(--card);border:1px solid var(--line-soft);border-radius:12px}}.lab-index li span{{color:var(--mut);font-size:13px}}@media(max-width:600px){{.lab-index{{padding:34px 14px}}.lab-index h1{{font-size:32px}}.lab-index li{{display:block}}.lab-index li span{{display:block;margin-top:6px}}}}</style></head><body><header class="top"><div class="wrap"><a class="logo" href="../index.html" style="color:inherit">CICD<span> BY Nabawy</span></a><a class="btn" href="../index.html">Home</a></div></header><main class="lab-index"><span class="eyebrow">HANDS-ON LABS</span><h1>Practice the pipeline.</h1><p>Eight guided exercises from the first green check through Jenkins recovery. Each manual includes setup, execution, verification, failure scenarios, cleanup, and a downloadable PDF edition.</p><ul>{lab_links}</ul></main></body></html>'''
    open(os.path.join(lab_dir, "index.html"), "w", encoding="utf-8").write(lab_index)

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
            f'<h3><a href="book/{b["id"]}.html">{html.escape(b["title"])}</a></h3><p>{html.escape(b["description"])}</p>'
            f'<div class="dif"><i></i>{b["difficulty"]} · {html.escape(b.get("path", ""))}</div>'
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

    RAIL_SHOW = 6
    def rail_inner(cards):
        """First RAIL_SHOW cards inline; rest behind a View-all toggle (outside .rail)."""
        if len(cards) <= RAIL_SHOW:
            return "".join(cards), ""
        extra = ('<div class="railmore" style="display:none">' + "".join(cards[RAIL_SHOW:]) + '</div>'
                   f'<div class="morewrap"><button class="btn railbtn" data-n="{len(cards)}">View all {len(cards)} \u2193</button></div>')
        return "".join(cards[:RAIL_SHOW]), extra
    def shelf(name, count, color, inner, grid=False, sid="", extra=""):
        arrows = ""
        if not grid:
            arrows = ('<span class="arrows"><button data-dir="-1" aria-label="Scroll left">←</button>'
                      '<button data-dir="1" aria-label="Scroll right">→</button></span>')
        wrap = f'<div class="cores-grid">{inner}</div>' if grid else f'<div class="rail">{inner}</div>'
        return (f'<section class="shelf" id="{sid}" style="--cat:{color}"><div class="shelf-head"><h2>{name}</h2>'
                f"<span>{count}</span>{arrows}</div>{wrap}{extra}</section>")

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
        _vis, _xtra = rail_inner([card(b, idx_of[b["id"]]) for b in bs])
        sections.append({"name": c, "n": len(bs), "grid": False, "color": CAT_COLORS.get(c, "#18E299"),
                         "inner": _vis, "extra": _xtra})
    _svis, _sxtra = rail_inner([series_card(p) for p in series_files])
    sections.append({"name": "Series edition", "n": len(series_files), "grid": False, "color": "#18E299",
                     "inner": _svis, "extra": _sxtra})
    if core_books:
        _cvis, _cxtra = rail_inner([card(b, idx_of[b["id"]]) for b in core_books])
        sections.append({"name": "Core practices", "n": len(core_books), "grid": True, "color": "#18E299",
                         "inner": _cvis, "extra": _cxtra})
    if small_books:
        _qvis, _qxtra = rail_inner([card(b, idx_of[b["id"]]) for b in small_books])
        sections.append({"name": "Quick topics", "n": len(small_books), "grid": True, "color": "#18E299",
                         "inner": _qvis, "extra": _qxtra})
    sections.sort(key=lambda s: (-s["n"], 0 if not s["grid"] else 1))
    series_sec = [s for s in sections if s["name"] == "Series edition"]
    sections = [s for s in sections if s["name"] != "Series edition"] + series_sec
    ogdir = os.path.join(DIST, "og")
    os.makedirs(ogdir, exist_ok=True)
    for b in books:
        open(os.path.join(ogdir, b["id"] + ".svg"), "w", encoding="utf-8").write(og_svg(b["title"], b["category"], CAT_COLORS.get(b["category"], "#18E299")))
        _png = og_png(b["title"], b["category"], CAT_COLORS.get(b["category"], "#18E299"))
        if _png:
            open(os.path.join(ogdir, b["id"] + ".png"), "wb").write(_png)
    open(os.path.join(ogdir, "library.svg"), "w", encoding="utf-8").write(og_svg("Technical Library", "CI/CD", "#18E299"))
    _libpng = og_png("Technical Library", "CI/CD", "#18E299")
    if _libpng:
        open(os.path.join(ogdir, "library.png"), "wb").write(_libpng)
    # (Browse shelf page removed 2026-09-18: Home index is the single library surface.
    # Search/OG data below is still built for search.json and social cards.)


    # glossary (dedupe by term, anchor links)
    rows = re.findall(r"^\| ([^|]+) \| ([^|]+) \| ([^|]+) \|", open(os.path.join(KB, "GLOSSARY.md"), encoding="utf-8").read(), re.M)
    seen = set()
    MD_INV = {v: k for k, v in MD_MAP.items()}
    grows = ""
    first_by_letter = {}
    for t, d, r in rows:
        t = t.strip()
        if "Term" in t or "---" in t or t.lower() in seen:
            continue
        seen.add(t.lower())
        slug = re.sub(r"[^a-z0-9]+", "-", t.lower()).strip("-")
        _L = re.sub(r"^[^A-Za-z0-9]*", "", t).strip()[:1].upper() or "#"
        if _L not in first_by_letter:
            first_by_letter[_L] = slug
        rm = re.match(r"\[([^]]+)\]\(([^)]+)\)", r.strip())
        if rm:
            rlabel, rpath = rm.group(1), rm.group(2)
            rid = MD_INV.get(rpath)
            topic = f'<a href="read/{rid}.html">{html.escape(rlabel)}</a>' if rid else html.escape(rlabel)
        else:
            topic = md_inline(r.strip())
        grows += f'<tr id="g-{slug}"><td><b>{html.escape(t)}</b></td><td>{html.escape(d.strip())}</td><td>{topic}</td><td><a href="#g-{slug}" title="Permalink">¶</a></td></tr>'
    _az = "".join(f'<a href="#g-{first_by_letter[L]}">{L}</a>' if L in first_by_letter else f'<span class="dim">{L}</span>' for L in [chr(c) for c in range(65, 91)])
    gloss = f"""<!DOCTYPE html>
<html lang="en">
<head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<title>Glossary — CICD BY Nabawy</title>{seo_tags("Glossary — CICD BY Nabawy", "CI/CD glossary: terms shared by all books, reader and search.", f"{SITE_URL}/glossary.html")}<style>{BASE_CSS}</style><script>try{{var _p=JSON.parse(localStorage.getItem('cicdlib:pref')||'null');var _t=_p&&_p.theme;var _ok=['sepia','dark','light','dim','contrast'].indexOf(_t)>=0;document.documentElement.dataset.theme=_ok?_t:'sepia'}}catch(e){{document.documentElement.dataset.theme='sepia'}}</script></head>
<body>
<header class="top"><div class="wrap"><a class="logo" href="index.html" style="text-decoration:none;color:inherit"><svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true"><circle cx="5" cy="12" r="2.6" stroke="#18E299" stroke-width="2"/><circle cx="19" cy="6" r="2.6" stroke="#18E299" stroke-width="2"/><circle cx="19" cy="18" r="2.6" stroke="#18E299" stroke-width="2"/><path d="M7.6 12h5.2m0 0-2.6-2.6m2.6 2.6-2.6 2.6M13.4 7.4l2.8-1M13.4 16.6l2.8 1" stroke="#18E299" stroke-width="2" stroke-linecap="round"/></svg>CICD<span> BY Nabawy</span></a>
<div class="search"><input id="q" type="search" placeholder="Filter terms…"></div><a class="btn" href="index.html" style="text-decoration:none">Home</a><a class="btn" href="roadmap/" style="text-decoration:none">Roadmap</a><button class="btn" id="themebtn">☀</button></div></header>
<div class="wrap"><h2 class="sec">Glossary</h2><p class="sub">{len(re.findall('<tr ', grows))} terms · shared by books, reader and search</p>
<div class="gtbar"><input id="q2" type="search" placeholder="Filter terms…" aria-label="Filter glossary terms"><nav class="az" aria-label="Jump to letter">{_az}</nav></div>
<table class="gloss"><tr><th>Term</th><th>Definition</th><th>Topic</th><th>Link</th></tr>{grows}</table></div>
<footer><div class="wrap">CICD BY Nabawy</div></footer>
<script>{BASE_JS}
function gfilter(el){{const q=(el.value||'').toLowerCase();
$$('table.gloss tr').forEach((r,i)=>{{if(!i)return;r.style.display=r.textContent.toLowerCase().includes(q)?'':'none'}});}};
$('#q').addEventListener('input',e=>gfilter(e.target));const _q2=$('#q2');if(_q2)_q2.addEventListener('input',e=>gfilter(e.target));
const THS=['sepia','dark','light'],THI={{dark:'☀',light:'☾',sepia:'◐'}};
function syncTheme(){{const p=getP('cicdlib:pref',{{theme:'sepia'}});const th=THS.includes(p.theme)?p.theme:'sepia';document.documentElement.dataset.theme=th;const t=$('#themebtn');if(t)t.textContent=THI[th]||'☀'}}
syncTheme();
$('#themebtn').onclick=()=>{{const p=getP('cicdlib:pref',{{theme:'sepia'}});p.theme=THS[(THS.indexOf(p.theme)+1)%THS.length];setP('cicdlib:pref',p);syncTheme()}};
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
        bp = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><title>{html.escape(b['title'])} — Overview — CICD BY Nabawy</title>{seo_tags(b['title'] + " — Overview — CICD BY Nabawy", b.get("description", ""), f"{SITE_URL}/book/{b['id']}.html", image=f"{SITE_URL}/og/{b['id']}.{OG_EXT}")}<link rel="prefetch" href="../read/{b['id']}.html"><style>{BASE_CSS}</style><script>try{{var _p=JSON.parse(localStorage.getItem('cicdlib:pref')||'null');var _t=_p&&_p.theme;var _ok=['sepia','dark','light','dim','contrast'].indexOf(_t)>=0;document.documentElement.dataset.theme=_ok?_t:'sepia'}}catch(e){{document.documentElement.dataset.theme='sepia'}}</script>
{f'<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Library","item":SITE_URL + "/"},{"@type":"ListItem","position":2,"name":b["title"],"item":SITE_URL + "/book/" + b["id"] + ".html"}]})}</script>'}></head>
<body><header class="top"><div class="wrap"><a class="logo" href="../index.html" style="color:inherit">CICD<span> BY Nabawy</span></a><nav class="crumbs"><span class="sep">/</span><span class="here">{html.escape(b['title'])}</span></nav><div class="search"></div><a class="btn" href="../index.html">Home</a><button class="btn" id="themebtn">☀</button></div></header>
<div class="wrap"><div class="bookhero"><div class="coverart" data-cat="{html.escape(b['category'])}"><b>{initials}</b></div><div style="flex:1;min-width:260px"><span class="num">{html.escape(b['category'])} · {b['difficulty']} · {b.get('time_minutes', 30)} min · v{b.get('version', '2.0')} · Updated {html.escape(b.get('updated', ''))}</span><h1 style="font-size:34px;margin:6px 0">{html.escape(b['title'])}</h1><p class="sub">{html.escape(b.get('description', ''))}</p>
<div class="chiprow"><a id="startbtn" href="../read/{b['id']}.html">Start reading →</a><a href="../read/{b['id']}.html">Reader</a></div>
<div class="chiprow"><span>Prereqs:</span>{preq}</div></div></div>
<div class="outcomes"><b>What you'll learn</b><ul>{outs}</ul></div>
<h2 class="sec" style="margin-top:20px">Contents preview</h2><ul class="labcheck">{"".join(f"<li>{html.escape(t)}</li>" for t in toc)}</ul>
{f'<div class="upnext">Up next in {html.escape(PATHS.get(b.get("path", ""), {}).get("label", b.get("path", "")))} → <a href="{upnext["id"]}.html"><b>{html.escape(upnext["title"])}</b></a></div>' if upnext else ''}
{related_box_html(rels)}
</div><footer><div class="wrap"><span>CICD BY Nabawy</span></div></footer>
<script>{BASE_JS}
const pref=getP('cicdlib:pref',{{theme:'sepia'}});const THX=['sepia','dark','light','dim','contrast'];document.documentElement.dataset.theme=THX.includes(pref.theme)?pref.theme:'sepia';
$('#themebtn').onclick=()=>{{pref.theme=THX[(THX.indexOf(pref.theme)+1)%THX.length]||'sepia';setP('cicdlib:pref',pref);document.documentElement.dataset.theme=pref.theme;}};
try{{const p=getP('cicdlib:prog:{b['id']}',null);if(p&&p.pct>0&&p.pct<100)$('#startbtn').textContent='Continue reading — '+p.pct+'% →';}}catch(e){{}}
</script></body></html>"""
        open(os.path.join(bookdir, b["id"] + ".html"), "w", encoding="utf-8").write(bp)

    # --- P1: updates page (per-book date from git, manifest fallback) ---
    import subprocess as _sp
    from datetime import date as _du
    _today = _du.today()
    def _book_date(b):
        cands = [os.path.join(PDF, b["file"])]
        _src = MD_MAP.get(b["id"])
        if _src:
            cands.append(os.path.join(KB, _src))
        for _cp in cands:
            try:
                _out = _sp.check_output(["git", "log", "-1", "--format=%ad", "--date=short", "--", os.path.relpath(_cp, KB)], cwd=KB, stderr=_sp.DEVNULL, text=True).strip()
                if _out:
                    return _out
            except Exception:
                pass
        return b.get("updated", "")
    def _fresh(ds):
        try:
            return (_today - _du.fromisoformat(ds)).days <= 60
        except Exception:
            return False
    def _urow(b):
        _ds = _book_date(b)
        _rib = ' <span class="upd">\u25cf Updated</span>' if _fresh(_ds) else ""
        return (f'<tr><td><a href="book/{b["id"]}.html">{html.escape(b["title"])}</a></td><td>{html.escape(b["category"])}</td><td>{b["difficulty"]}</td><td>v{html.escape(b.get("version", "2.0"))}</td><td>{html.escape(_ds)}{_rib}</td><td>{b.get("time_minutes", 30)} min</td></tr>')
    rows_u = "".join(_urow(b) for b in books)
    upd = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><title>Updates — CICD BY Nabawy</title>{seo_tags("Updates — CICD BY Nabawy", "What changed across the library.", f"{SITE_URL}/updates.html")}<style>{BASE_CSS}</style><script>try{{var _p=JSON.parse(localStorage.getItem('cicdlib:pref')||'null');var _t=_p&&_p.theme;var _ok=['sepia','dark','light','dim','contrast'].indexOf(_t)>=0;document.documentElement.dataset.theme=_ok?_t:'sepia'}}catch(e){{document.documentElement.dataset.theme='sepia'}}</script></head><body><header class="top"><div class="wrap"><a class="logo" href="index.html" style="color:inherit">CICD<span> BY Nabawy</span></a><nav class="crumbs"><span class="sep">/</span><span class="here">Updates</span></nav></div></header><div class="wrap"><h2 class="sec">Updates</h2><p class="sub">{len(books)} books · P0+P1 shipped Sep 2026: metadata, filters, paths, bookmarks, related, lab checks</p><table class="gloss"><tr><th>Book</th><th>Category</th><th>Level</th><th>Ver</th><th>Updated</th><th>Time</th></tr>{rows_u}</table></div></body></html>"""
    open(os.path.join(DIST, "updates.html"), "w", encoding="utf-8").write(upd)

    # --- SEO: sitemap + robots ---
    from datetime import date as _d
    today = _d.today().isoformat()
    urls = [SITE_URL + "/", SITE_URL + "/glossary.html", SITE_URL + "/roadmap/", SITE_URL + "/map.html", SITE_URL + "/updates.html"]
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
    notfound = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><title>Not found — CICD BY Nabawy</title><link rel="icon" type="image/svg+xml" href="https://eslamnabawy.github.io/cicd-by-nabawy/favicon.svg"><meta name="theme-color" content="#0B0D10"><style>{BASE_CSS}</style><script>try{{var _p=JSON.parse(localStorage.getItem('cicdlib:pref')||'null');var _t=_p&&_p.theme;var _ok=['sepia','dark','light','dim','contrast'].indexOf(_t)>=0;document.documentElement.dataset.theme=_ok?_t:'sepia'}}catch(e){{document.documentElement.dataset.theme='sepia'}}</script></head><body><div class="wrap" style="text-align:center;padding:80px 20px"><h1>Page not found</h1><p class="sub">Try search or start with Foundations.</p><p><a class="btn" href="index.html">Home</a> <a class="btn" href="read/start-here.html">Start here</a> <a class="btn" href="glossary.html">Glossary</a></p></div></body></html>"""
    pathlib.Path(os.path.join(DIST, "404.html")).write_text(notfound, encoding="utf-8")
    pathlib.Path(os.path.join(DIST, "favicon.svg")).write_text(FAVICON_SVG, encoding="utf-8")
    search_idx = [{"id": b["id"], "title": b["title"], "desc": b.get("description", ""), "cat": b["category"], "dif": b["difficulty"], "tags": b.get("tags", []), "time": b.get("time_minutes", 30), "sections": all_sections.get(b["id"], []), "body": all_body.get(b["id"], "")[:2000]} for b in books]
    pathlib.Path(os.path.join(DIST, "search.json")).write_text(json.dumps(search_idx, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"BUILT {len(books)} books + {len(books)} overviews + index + glossary + updates -> {DIST}")


if __name__ == "__main__":
    build()


