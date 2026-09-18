'''Concept threads + tool picker pages. Called from build.py as
build_extra_pages(books, DIST, env) with env providing shared globals.'''
import os
import re
import json
import html as htmllib


def thread_hits(text, terms):
    n = 0
    for term in terms:
        if len(term) <= 5:
            pat = '\\b' + re.escape(term.lower()) + '\\b'
        else:
            pat = re.escape(term.lower())
        if re.search(pat, text):
            n += 1
    return n


def build_thread_index(books, env):
    threads = json.load(open(os.path.join(env['ROOT'], 'content', 'threads.json'), encoding='utf-8'))
    parse_book = env['parse_book']
    PDF = env['PDF']
    index = {}
    for th in threads:
        index[th['id']] = []
    for b in books:
        _css, pages = parse_book(os.path.join(PDF, b['file']))
        for pg in pages:
            m = re.search(r'id="([^"]+)"', pg[:200])
            sid = m.group(1) if m else ''
            h1 = re.search(r'<h1 class="t">(.*?)</h1>', pg, re.S)
            if h1:
                title = re.sub(r'<[^>]+>', '', h1.group(1)).strip()[:60]
            else:
                title = sid
            txt = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', pg)).strip().lower()
            for th in threads:
                if thread_hits(txt, th['terms']) >= 2:
                    index[th['id']].append({'book': b['id'], 'title': b['title'], 'sid': sid, 'sheet': title})
    return threads, index


THEME_JS = '''
const $=s=>document.querySelector(s);
function getP(k,d){try{const v=JSON.parse(localStorage.getItem(k));return v??d}catch(e){return d}}
function setP(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}
const pref=getP('cicdlib:pref',{theme:'sepia'});
const THS=['sepia','dark','light'],THI={dark:'\\u2600',light:'\\u263e',sepia:'\\u25d0'};
function syncTheme(){const th=THS.includes(pref.theme)?pref.theme:'sepia';document.documentElement.dataset.theme=th;const t=$('#themebtn');if(t)t.textContent=THI[th]||'\\u2600';}
syncTheme();
$('#themebtn').onclick=()=>{pref.theme=THS[(THS.indexOf(pref.theme)+1)%THS.length];setP('cicdlib:pref',pref);syncTheme();};
'''

HEAD_THEME = '''<script>try{var _p=JSON.parse(localStorage.getItem('cicdlib:pref')||'null');var _t=_p&&_p.theme;document.documentElement.dataset.theme='sepia';if(_t==='dark'||_t==='light')document.documentElement.dataset.theme=_t;}catch(e){document.documentElement.dataset.theme='sepia';}</script>'''


def build_threads_page(books, output_dir, env, threads, tindex):
    CAT_HEX = env['CAT_HEX']
    W = 1000
    RH = 64
    H = max(len(books), len(threads)) * RH + 60
    parts = []
    tids = [x['id'] for x in threads]
    for bi, b in enumerate(books):
        y = 30 + bi * RH
        for th in threads:
            n = 0
            for e in tindex[th['id']]:
                if e['book'] == b['id']:
                    n += 1
            if n:
                ti = tids.index(th['id'])
                parts.append('<line x1="250" y1="' + str(y + 20) + '" x2="750" y2="' + str(30 + ti * RH + 20) + '" stroke="var(--line)" stroke-width="1.5" opacity=".55"/>')
    for bi, b in enumerate(books):
        y = 30 + bi * RH
        col = CAT_HEX.get(b['category'], '#18E299')
        label = htmllib.escape(b['title'][:26])
        parts.append('<a href="../read/' + b['id'] + '.html"><rect x="20" y="' + str(y) + '" width="230" height="40" rx="10" fill="var(--card)" stroke="' + col + '" stroke-width="2"/><text x="32" y="' + str(y + 25) + '" font-size="13" font-weight="700" fill="var(--ink)">' + label + '</text></a>')
    for ti, th in enumerate(threads):
        y = 30 + ti * RH
        n = len(tindex[th['id']])
        parts.append('<a href="#' + th['id'] + '"><rect x="750" y="' + str(y) + '" width="230" height="40" rx="10" fill="var(--card)" stroke="#0e7490" stroke-width="2"/><text x="762" y="' + str(y + 25) + '" font-size="13" font-weight="700" fill="var(--ink)">' + htmllib.escape(th['label']) + ' (' + str(n) + ')</text></a>')
    svg = '<svg id="graph" width="100%" viewBox="0 0 ' + str(W) + ' ' + str(H) + '" style="max-height:70vh;border:1px solid var(--line);border-radius:14px;background:var(--card)">' + ''.join(parts) + '</svg>'
    secs = []
    for th in threads:
        groups = {}
        for e in tindex[th['id']]:
            groups.setdefault(e['book'], []).append(e)
        glist = []
        for b in books:
            if b['id'] not in groups:
                continue
            es = groups[b['id']][:6]
            chips = ''.join('<a class="chip" href="../read/' + e['book'] + '.html#' + e['sid'] + '">' + htmllib.escape(e['sheet'][:34]) + '</a>' for e in es)
            extra = ''
            if len(groups[b['id']]) > 6:
                extra = ' <span>+' + str(len(groups[b['id']]) - 6) + ' more</span>'
            glist.append('<div style="margin:8px 0"><b>' + htmllib.escape(b['title']) + '</b><div class="chiprow">' + chips + extra + '</div></div>')
        secs.append('<section id="' + th['id'] + '" style="margin:26px 0"><h2 class="sec">' + htmllib.escape(th['label']) + '</h2><p class="sub">' + htmllib.escape(th['desc']) + ' - ' + str(len(tindex[th['id']])) + ' sheets.</p>' + ''.join(glist) + '</section>')
    page = ('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            '<title>Concept threads - CICD BY Nabawy</title>'
            '<style>' + env['BASE_CSS'] + '.chiprow{margin:6px 0}</style>'
            + HEAD_THEME +
            '</head><body><header class="top"><div class="wrap">'
            '<a class="logo" href="../index.html" style="color:inherit">CICD<span> BY Nabawy</span></a>'
            '<nav class="crumbs"><span class="sep">/</span><span class="here">Threads</span></nav>'
            '<a class="btn" href="../index.html" style="text-decoration:none">Home</a>'
            '<a class="btn" href="../tools/" style="text-decoration:none">Tools</a>'
            '<button class="btn" id="themebtn" aria-label="Toggle theme">X</button>'
            '</div></header><div class="wrap">'
            '<div class="hero" style="padding:36px 24px 16px"><span class="eyebrow">THREADS</span>'
            '<h1>Follow an idea across books.</h1>'
            '<p>Nine concept threads stitched from every sheet. Drag to pan, scroll to zoom.</p></div>'
            + svg +
            '<p class="sub">Scroll to zoom - drag to pan - double-click to reset.</p>'
            + ''.join(secs) +
            '</div><footer><div class="wrap"><span>CICD BY Nabawy</span></div></footer>'
            '<script>'
            + THEME_JS +
            "const svg=document.querySelector('#graph');let vb=[0,0,1000," + str(H) + '];'
            "const apply=()=>svg.setAttribute('viewBox',vb.join(' '));"
            "svg.addEventListener('wheel',e=>{e.preventDefault();const f=e.deltaY>0?1.12:0.9;const r=svg.getBoundingClientRect();const mx=(e.clientX-r.left)/r.width*vb[2]+vb[0],my=(e.clientY-r.top)/r.height*vb[3]+vb[1];vb=[mx-(mx-vb[0])*f,my-(my-vb[1])*f,vb[2]*f,vb[3]*f];apply();},{passive:false});"
            "let drag=null;svg.addEventListener('pointerdown',e=>{drag=[e.clientX,e.clientY,vb[0],vb[1]];svg.setPointerCapture(e.pointerId);});"
            "svg.addEventListener('pointermove',e=>{if(!drag)return;const r=svg.getBoundingClientRect();vb[0]=drag[2]-(e.clientX-drag[0])/r.width*vb[2];vb[1]=drag[3]-(e.clientY-drag[1])/r.height*vb[3];apply();});"
            "svg.addEventListener('pointerup',()=>drag=null);"
            "svg.addEventListener('dblclick',()=>{vb=[0,0,1000," + str(H) + "];apply();});"
            '</script></body></html>')
    out = os.path.join(output_dir, 'threads')
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(page)
    print('BUILT threads: ' + str(len(threads)) + ' threads -> ' + out)


def resolve_sheet(books, env, bid, needles):
    parse_book = env['parse_book']
    PDF = env['PDF']
    for b in books:
        if b['id'] != bid:
            continue
        _css, pages = parse_book(os.path.join(PDF, b['file']))
        for pg in pages:
            m = re.search(r'id="([^"]+)"', pg[:200])
            h1 = re.search(r'<h1 class="t">(.*?)</h1>', pg, re.S)
            title = re.sub(r'<[^>]+>', '', h1.group(1)).strip() if h1 else ''
            for nd in needles:
                if nd.lower() in title.lower():
                    return '../read/' + bid + '.html#' + (m.group(1) if m else '')
    return '../read/' + bid + '.html'


TOOLS_META = {
    'jenkins': ('Jenkins', 'Self-hosted control, deepest plugin ecosystem, proven at enterprise scale.'),
    'actions': ('GitHub Actions', 'Zero infrastructure if you live on GitHub - fastest path from push to green.'),
    'gitlab': ('GitLab CI', 'Repo, pipeline and registry in one product, with review apps built in.'),
    'argocd': ('ArgoCD', 'Pull-model GitOps for Kubernetes fleets - git as the audit trail.'),
}

QUESTIONS = [
    ('Where does your code live?', [('GitHub', {'actions': 2, 'jenkins': 1}), ('GitLab', {'gitlab': 3, 'jenkins': 1}), ('Self-hosted git', {'jenkins': 2, 'argocd': 1})]),
    ('Who runs infrastructure?', [('No ops team', {'actions': 2, 'gitlab': 1}), ('Small ops team', {'jenkins': 1, 'actions': 1, 'gitlab': 1}), ('Platform team', {'jenkins': 2, 'argocd': 2, 'gitlab': 1})]),
    ('How much Kubernetes?', [('All in', {'argocd': 3, 'gitlab': 1}), ('Some', {'argocd': 1, 'actions': 1, 'jenkins': 1}), ('None', {'jenkins': 2, 'actions': 2, 'gitlab': 1})]),
    ('Audit and compliance pressure?', [('Strict', {'jenkins': 2, 'gitlab': 2, 'argocd': 1}), ('Standard', {'actions': 1, 'gitlab': 1, 'jenkins': 1}), ('None', {'actions': 2})]),
    ('Team size?', [('Solo', {'actions': 2}), ('2 to 20', {'actions': 1, 'gitlab': 2}), ('20 plus', {'jenkins': 2, 'gitlab': 1, 'argocd': 1})]),
]


def build_tools_page(books, output_dir, env):
    links = {
        'jenkins': resolve_sheet(books, env, 'jenkins-complete', ['Setup', 'Topology', 'Agents']),
        'actions': resolve_sheet(books, env, 'platforms-roadmaps', ['Actions']),
        'gitlab': resolve_sheet(books, env, 'platforms-roadmaps', ['GitLab CI', 'Pipeline Anatomy']),
        'argocd': resolve_sheet(books, env, 'platforms-roadmaps', ['ArgoCD & GitOps', 'Push vs Pull', 'Where It Fits']),
        'choice': resolve_sheet(books, env, 'platforms-roadmaps', ['The Choice', 'Decision Framework', 'Side-by-Side']),
    }
    qhtml = []
    for qi, (q, opts) in enumerate(QUESTIONS):
        btns = []
        for o, w in opts:
            btns.append('<button class="btn qopt" data-q="' + str(qi) + '" data-w="' + htmllib.escape(json.dumps(w), quote=True) + '">' + o + '</button>')
        vis = '' if qi == 0 else ' hidden'
        qhtml.append('<div class="qcard" id="q' + str(qi) + '"' + vis + '><h3>' + str(qi + 1) + '. ' + q + '</h3><div class="opts">' + ''.join(btns) + '</div></div>')
    names = {}
    whys = {}
    for k in TOOLS_META:
        names[k] = TOOLS_META[k][0]
        whys[k] = TOOLS_META[k][1]
    js_vars = ('const LINKS=' + json.dumps(links) + ';'
               'const WHY=' + json.dumps(whys) + ';'
               'const NAMES=' + json.dumps(names) + ';'
               'const NQ=' + str(len(QUESTIONS)) + ';')
    quiz_js = '''
let qi=0;const scores={jenkins:0,actions:0,gitlab:0,argocd:0};
document.querySelectorAll('.qopt').forEach(b=>b.onclick=()=>{
const w=JSON.parse(b.dataset.w);for(const k in w)scores[k]+=w[k];
document.querySelector('#q'+qi).hidden=true;qi++;
if(qi<NQ){document.querySelector('#q'+qi).hidden=false;}else{showResult();}});
function showResult(){const tot=Math.max(1,...Object.values(scores));
const rank=Object.keys(scores).sort((a,b)=>scores[b]-scores[a]);
let s='<div class="qcard"><h3>Your stack, ranked</h3>';
rank.forEach((k,i)=>{s+='<div class="tcard"><b>'+(i+1)+'. '+NAMES[k]+' - '+scores[k]+' pts</b><div class="tbar"><b style="width:'+Math.round(100*scores[k]/tot)+'%"></b></div><p>'+WHY[k]+'</p><a class="btn" href="'+LINKS[k]+'">Read why</a> ';if(i===0){s+='<a class="btn" href="'+LINKS.choice+'">Compare all</a>';}s+='</div>';});
s+='<p><button class="btn" onclick="location.reload()">Retake</button></p></div>';
document.querySelector('#result').innerHTML=s;
window.scrollTo({top:document.querySelector('#result').offsetTop-80});}
'''
    page = ('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            '<title>Tool picker - CICD BY Nabawy</title>'
            '<style>' + env['BASE_CSS'] + '.qcard{max-width:640px;margin:18px auto;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:22px}.qcard .opts{display:flex;gap:10px;flex-wrap:wrap;margin-top:12px}.qcard .btn{min-height:48px}.tcard{max-width:640px;margin:12px auto;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 22px}.tbar{height:8px;border-radius:99px;background:var(--bg2);margin:10px 0}.tbar b{display:block;height:100%;border-radius:99px;background:var(--brand)}</style>'
            + HEAD_THEME +
            '</head><body><header class="top"><div class="wrap">'
            '<a class="logo" href="../index.html" style="color:inherit">CICD<span> BY Nabawy</span></a>'
            '<nav class="crumbs"><span class="sep">/</span><span class="here">Tools</span></nav>'
            '<a class="btn" href="../index.html" style="text-decoration:none">Home</a>'
            '<a class="btn" href="../threads/" style="text-decoration:none">Threads</a>'
            '<button class="btn" id="themebtn" aria-label="Toggle theme">X</button>'
            '</div></header><div class="wrap">'
            '<div class="hero" style="padding:36px 24px 16px"><span class="eyebrow">TOOLS</span>'
            '<h1>Which tool fits?</h1><p>Five questions. Ranked answers with reasons and deep links.</p></div>'
            "<div id='quiz'>" + ''.join(qhtml) + "</div><div id='result'></div>"
            '</div><footer><div class="wrap"><span>CICD BY Nabawy</span></div></footer>'
            '<script>'
            + THEME_JS + js_vars + quiz_js +
            '</script></body></html>')
    out = os.path.join(output_dir, 'tools')
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, 'index.html'), 'w', encoding='utf-8').write(page)
    print('BUILT tools picker -> ' + out)


def build_extra_pages(books, output_dir, env):
    threads, tindex = build_thread_index(books, env)
    build_threads_page(books, output_dir, env, threads, tindex)
    build_tools_page(books, output_dir, env)
