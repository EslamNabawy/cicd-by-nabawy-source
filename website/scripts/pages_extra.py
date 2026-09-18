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


THREAD_WHY = {
    'artifact-digest': ('Rebuilds waste hours and ship untested code — one digest ends that.', 'Exam: name the digest, the registry, and the promotion gate.'),
    'approval-gates': ('Every prod deploy is a decision — gates make the decision explicit.', 'Exam: who approves, on what signal, with what kill switch.'),
    'rollback-recovery': ('Deploys fail — recovery speed is the real SLO.', 'Exam: redeploy vs revert, then the postmortem pipeline change.'),
    'trunk-discipline': ('Long branches are merge hell — small daily merges keep main green.', 'Exam: PR gates, merge queue, red-main-first rule.'),
    'hermetic-builds': ('"Works here, fails there" is an input leak — seal the build.', 'Exam: lockfiles, clean containers, cache keys.'),
    'supply-chain': ('2025-26 attacks rode trusted deps into CI — verify everything.', 'Exam: pin, sign, attest, scan.'),
    'signals-slos': ('Without signals a deploy is a cliff — budgets turn noise into pages.', 'Exam: SLI vs SLO vs burn-rate alert.'),
    'gitops-pull': ('Push pipelines leak cluster creds — pull keeps them inside.', 'Exam: push vs pull blast radius, sync waves, git revert.'),
    'controller-agent': ('Every platform is scheduler plus executor — learn the shape once.', 'Exam: who schedules, who executes, where runners live.'),
}


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
    cards = []
    maxn = max(1, max(len(tindex[th['id']]) for th in threads))
    for th in threads:
        n = len(tindex[th['id']])
        nb = len({e['book'] for e in tindex[th['id']]})
        why = THREAD_WHY.get(th['id'], ('', ''))[0]
        cards.append('<a class="thread-card" href="#' + th['id'] + '" style="--cat:#0e7490" data-thread="' + th['id'] + '"><span class="thread-num">' + str(n) + ' sheets</span><b>' + htmllib.escape(th['label']) + '</b><span>' + htmllib.escape(th['desc']) + '</span>' + ('<span>' + htmllib.escape(why) + '</span>' if why else '') + '<span class="tbar" aria-hidden="true"><b style="width:' + str(round(100 * n / maxn)) + '%"></b></span><span class="thread-meta"><span class="tprog" data-tprog="' + th['id'] + '"></span>' + str(nb) + ' books · jump ↓</span></a>')
    PATH_RANK = {'start-here': 0, 'build': 1, 'deliver': 2, 'observability': 3, 'jenkins': 4, 'platforms': 5, 'labs': 6, 'reference': 7}
    bord = sorted(books, key=lambda b: (PATH_RANK.get(b.get('path', ''), 9), b['id']))
    secs = []
    for thi, th in enumerate(threads):
        groups = {}
        for e in tindex[th['id']]:
            groups.setdefault(e['book'], []).append(e)
        glist = []
        step = 0
        for b in bord:
            if b['id'] not in groups:
                continue
            step += 1
            es = groups[b['id']]
            vis = es[:6]
            hid = es[6:]
            chips = ''.join('<a class="chip" href="../read/' + e['book'] + '.html#' + e['sid'] + '" title="' + htmllib.escape(e['sheet']) + '">' + htmllib.escape(e['sheet'][:34]) + '</a>' for e in vis)
            if hid:
                chips += '<span class="morechips" hidden>' + ''.join('<a class="chip" href="../read/' + e['book'] + '.html#' + e['sid'] + '" title="' + htmllib.escape(e['sheet']) + '">' + htmllib.escape(e['sheet'][:34]) + '</a>' for e in hid) + '</span>'
                chips += ' <button class="btn morebtn" aria-expanded="false">+' + str(len(hid)) + ' more</button>'
            glist.append('<div class="tstop" data-n="' + str(step).zfill(2) + '" style="margin:8px 0"><b>' + htmllib.escape(b['title']) + '</b><div class="chiprow">' + chips + '</div></div>')
        why, exam = THREAD_WHY.get(th['id'], ('', ''))
        xlinks = '<p class="sub">Field links: <a href="../read/platforms-roadmaps.html#s29n">Tool vs Tool matrix</a> · <a href="../tools/">5-question picker</a></p>'
        secs.append('<section id="' + th['id'] + '" style="margin:26px 0;scroll-margin-top:70px"><h2 class="sec"><button class="sechead" aria-expanded="true">' + htmllib.escape(th['label']) + ' <span class="map-pill"><b>' + str(len(tindex[th['id']])) + '</b> sheets</span> <span class="chev">▾</span></button></h2><div class="secbody"><p class="sub">' + htmllib.escape(th['desc']) + ' Guided path: foundations first, depth later — ' + str(step) + ' stops. <span class="tprog" data-tprog="' + th['id'] + '"></span></p>' + ('<div class="mark m-key"><span class="tag">WHY IT MATTERS</span>' + htmllib.escape(why) + '</div>' if why else '') + ('<div class="m-exam"><span class="tag">🎓 EXAM</span>' + htmllib.escape(exam) + '</div>' if exam else '') + ''.join(glist) + xlinks + '<p><a href="#graph">↑ graph</a> · <a href="#thread-filter">↑ filter</a></p></div></section>')
    page = ('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            '<link rel="icon" type="image/svg+xml" href="../favicon.svg">'
            '<title>Concept threads - CICD BY Nabawy</title>'
            '<style>' + env['BASE_CSS'] + '.chiprow{margin:6px 0}.thread-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:10px;margin:16px 0 8px}.thread-card{display:flex;flex-direction:column;gap:6px;padding:14px 16px;border:1px solid var(--line-soft);border-radius:12px;background:var(--card);text-decoration:none;color:var(--ink)}.thread-card:hover{border-color:var(--cat);transform:translateY(-2px)}.thread-card b{font-size:15px}.thread-card span{font-size:12px;color:var(--mut)}.thread-num{font-family:var(--mono);font-size:10px;font-weight:800;letter-spacing:.12em;color:var(--cat)}.thread-meta{font-family:var(--mono);font-size:11px}.tfilter{position:sticky;top:57px;z-index:15;background:var(--bg);padding:10px 0 6px}.tfilter input{width:100%;background:var(--card);border:1px solid var(--line);color:var(--ink);border-radius:9999px;padding:9px 14px;font-size:14px}.tstop{display:flex;gap:10px}.tstop::before{content:attr(data-n);font-family:var(--mono);font-size:11px;font-weight:800;color:var(--brand);flex:none;padding-top:3px}.tbar{height:6px;border-radius:99px;background:var(--bg2);margin:6px 0;overflow:hidden}.tbar b{display:block;height:100%;border-radius:99px;background:var(--cat)}.sechead{background:none;border:none;color:inherit;font:inherit;cursor:pointer;display:flex;align-items:center;gap:8px;padding:0}.sechead .chev{transition:transform .15s;color:var(--mut)}.sechead[aria-expanded="false"] .chev{transform:rotate(-90deg)}@media(max-width:700px){#graphwrap{display:none}#graphwrap.open{display:block}.tfilter input{min-height:44px;font-size:16px}}</style>'
            + HEAD_THEME +
            '</head><body><header class="top"><div class="wrap">'
            '<a class="logo" href="../index.html" style="color:inherit">CICD<span> BY Nabawy</span></a>'
            '<nav class="crumbs"><span class="sep">/</span><span class="here">Threads</span></nav>'
            '<a class="btn" href="../index.html" style="text-decoration:none">Home</a>'
            '<a class="btn" href="../glossary.html" style="text-decoration:none">Study Deck</a>'
            '<a class="btn" href="../tools/" style="text-decoration:none">Tools</a>'
            '<button class="btn" id="themebtn" aria-label="Toggle theme">X</button>'
            '</div></header><div class="wrap">'
            '<div class="hero" style="padding:36px 24px 16px"><span class="eyebrow">THREADS</span>'
            '<h1>Follow an idea across books.</h1>'
            '<p>' + str(len(threads)) + ' concept threads stitched from every sheet. Pick a card or drag the graph to pan, scroll to zoom.</p></div>'
            '<div class="tfilter" id="thread-filter"><input id="tq" type="search" placeholder="Filter threads and sheets…" aria-label="Filter threads and sheets"></div>'
            '<div class="thread-grid">' + ''.join(cards) + '</div>'
            '<button class="btn" id="graphtoggle" aria-expanded="true">Graph: hide/show</button>'
            '<div id="graphwrap">' + svg +
            '<p class="sub">Scroll to zoom - drag to pan - double-click to reset.</p></div>'
            + ''.join(secs) +
            '</div><footer><div class="wrap"><span>CICD BY Nabawy</span><span><a href="../index.html">Home</a> · <a href="../glossary.html">Study Deck</a> · <a href="../tools/">Tools</a></span></div></footer>'
            '<script>'
            + THEME_JS +
            "const _tq=document.querySelector('#tq');if(_tq)_tq.addEventListener('input',e=>{const q=e.target.value.toLowerCase();document.querySelectorAll('.thread-grid .thread-card').forEach(c=>{c.style.display=c.textContent.toLowerCase().includes(q)?'':'none';});document.querySelectorAll('section[id]').forEach(s=>{const t=s.textContent.toLowerCase().includes(q);s.style.display=t?'':'none';});});" +
            "document.querySelectorAll('.sechead').forEach(b=>b.onclick=()=>{const sec=b.closest('section');const body=sec.querySelector('.secbody');const open=b.getAttribute('aria-expanded')==='true';b.setAttribute('aria-expanded',!open);body.hidden=open;});" +
            "try{const _prog=id=>{try{const v=JSON.parse(localStorage.getItem('cicdlib:prog:'+id));return(v&&v.pct)||0}catch(e){return 0}};document.querySelectorAll('section[id]').forEach(sec=>{const books=[...new Set([...sec.querySelectorAll('.chip')].map(a=>(a.getAttribute('href')||'').split('/').pop().split('.')[0]))].filter(Boolean);if(!books.length)return;const avg=Math.round(books.reduce((s,b)=>s+_prog(b),0)/books.length);document.querySelectorAll('[data-tprog=\"'+sec.id+'\"]').forEach(el=>{el.textContent=avg+'% read · ';});});}catch(e){};" +
            "const _gt=document.querySelector('#graphtoggle'),_gw=document.querySelector('#graphwrap');if(_gt&&_gw){if(matchMedia('(max-width:700px)').matches){_gw.classList.remove('open');_gw.style.display='none';_gt.setAttribute('aria-expanded','false');}_gt.onclick=()=>{const open=_gw.style.display!=='none';_gw.style.display=open?'none':'';_gw.classList.toggle('open',!open);_gt.setAttribute('aria-expanded',!open);};}" +
            "document.querySelectorAll('.morebtn').forEach(b=>b.onclick=()=>{const m=b.parentElement.querySelector('.morechips');const open=m.hidden;m.hidden=!open;b.setAttribute('aria-expanded',open);b.textContent=open?'show less':'+'+m.querySelectorAll('a').length+' more';});" +
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
    ('Where does your code live?', 'Source hosting decides half the answer — co-located CI wins on integration.', [('GitHub', {'actions': 2, 'jenkins': 1}, 'PR checks and runners built in'), ('GitLab', {'gitlab': 3, 'jenkins': 1}, 'Repo, pipeline and envs in one product'), ('Self-hosted git', {'jenkins': 2, 'argocd': 1}, 'No SaaS coupling — own the runners')]),
    ('Who runs infrastructure?', 'No ops team means SaaS; a platform team unlocks self-hosted power.', [('No ops team', {'actions': 2, 'gitlab': 1}, 'Zero maintenance beats control'), ('Small ops team', {'jenkins': 1, 'actions': 1, 'gitlab': 1}, 'Either road stays open'), ('Platform team', {'jenkins': 2, 'argocd': 2, 'gitlab': 1}, 'Run fleets, clusters, pull delivery')]),
    ('How much Kubernetes?', 'K8s estates pull toward GitOps; the rest stays push.', [('All in', {'argocd': 3, 'gitlab': 1}, 'Clusters want pull-model delivery'), ('Some', {'argocd': 1, 'actions': 1, 'jenkins': 1}, 'Mixed estate, mixed answer'), ('None', {'jenkins': 2, 'actions': 2, 'gitlab': 1}, 'Push pipelines cover it')]),
    ('Audit and compliance pressure?', 'Strict audit loves self-hosted evidence trails.', [('Strict', {'jenkins': 2, 'gitlab': 2, 'argocd': 1}, 'Own hardware, own audit trail'), ('Standard', {'actions': 1, 'gitlab': 1, 'jenkins': 1}, 'SaaS gates plus approvals suffice'), ('None', {'actions': 2}, 'Speed first, ceremony later')]),
    ('Team size?', 'Solo ships fastest on SaaS; fleets need control.', [('Solo', {'actions': 2}, 'Minutes to first green build'), ('2 to 20', {'actions': 1, 'gitlab': 2}, 'Review apps and trains help'), ('20 plus', {'jenkins': 2, 'gitlab': 1, 'argocd': 1}, 'Control and cost shape matter')]),
    ('Where do releases land?', 'The runtime picks the delivery model — K8s means pull.', [('VMs or bare metal', {'jenkins': 2}, 'Agents reach anywhere SSH does'), ('Cloud PaaS', {'actions': 2, 'gitlab': 1}, 'Push-to-deploy fits stateless apps'), ('Kubernetes clusters', {'argocd': 3, 'gitlab': 1}, 'Agents converge desired state'), ('Mixed', {'jenkins': 1, 'actions': 1, 'argocd': 1}, 'Gate in one place, execute anywhere')]),
]

STUDY_THREAD = {'jenkins': 'controller-agent', 'actions': 'trunk-discipline', 'gitlab': 'approval-gates', 'argocd': 'gitops-pull'}
STUDY_LABEL = {'jenkins': 'Controllers & Agents', 'actions': 'Trunk Discipline', 'gitlab': 'Approval Gates', 'argocd': 'GitOps Pull Model'}

CATALOG = [
    ('Jenkins', 'Jenkins', 'Self-hosted automation server: controllers schedule, agents execute pipelines as code.', 'Regulated or air-gapped estates, complex heterogeneous builds, zero per-minute cost.', 'Total control over execution, deepest plugin ecosystem, proven at scale.', 'Jenkinsfile on controller, stages on labeled agents, credentials via bindings.', 4, 'jenkins-complete'),
    ('GitHub Actions', 'GitHub', 'CI/CD built into GitHub: workflows of jobs and steps on hosted or self-hosted runners.', 'Source already on GitHub, small teams wanting zero-infra CI.', 'Fastest path from push to green; PR checks and Marketplace built in.', 'YAML in .github/workflows, jobs with needs DAG, environments as gates.', 5, 'platforms-roadmaps'),
    ('GitLab CI', 'Platforms', 'Pipeline engine inside GitLab: single YAML driving stages, runners, review apps.', 'Single-platform shops wanting repo plus pipeline plus envs in one product.', 'Review apps per MR and merge trains come free with the platform.', '.gitlab-ci.yml stages with needs DAG, rules gating, runners by tags.', 3, 'platforms-roadmaps'),
    ('ArgoCD', 'Platforms', 'GitOps operator for Kubernetes: in-cluster agent pulls desired state from git.', 'Kubernetes fleets needing pull-model audit and env-per-branch scale.', 'Cluster creds never leave the cluster; git revert is the rollback.', 'Application objects with sync waves, ApplicationSets, manual prod sync.', 4, 'platforms-roadmaps'),
    ('Docker', 'Labs', 'Container runtime and image format: freeze the app plus its OS userland.', 'Every pipeline that must kill works-on-my-machine drift.', 'Identical bits from laptop to CI to prod; BuildKit caches keep it fast.', 'Multi-stage Dockerfiles, BuildKit secrets, push digests to a registry.', 5, 'labs-handbook'),
    ('Kubernetes', 'Platforms', 'Container orchestrator: desired-state scheduler for pods, services, jobs.', 'Fleets sharing clusters, elastic runners, pull delivery targets.', 'Bin-packing plus self-heal plus one API for runners and releases.', 'Manifests or Helm charts applied by hand, CI push, or ArgoCD pull.', 5, 'platforms-roadmaps'),
    ('Helm', 'Platforms', 'Package manager for Kubernetes: templated charts with per-env values.', 'K8s releases needing versioned, repeatable installs across envs.', 'One chart, many envs — diffs are value diffs, not manifest forks.', 'Chart plus values per env, helm upgrade with pinned image digests.', 4, 'platforms-roadmaps'),
    ('Terraform', 'Labs', 'Infrastructure as code: declare envs, plan the diff, apply gated.', 'Environments that must be reviewable, repeatable, and drift-checked.', 'Plan output is the review; state per env bounds the blast radius.', 'Modules pinned by version, remote state with locking, plan on PR.', 5, 'labs-handbook'),
    ('Prometheus', 'Observability', 'Metrics engine: scrapes numeric time series, alerts on burn rate.', 'Any service needing SLO alerts and capacity signals.', 'One query language over every target; alert on budgets, not blips.', 'Scrape targets, PromQL rules, Alertmanager with runbook links.', 4, 'observability'),
    ('Grafana', 'Observability', 'Unified dashboards over Loki, Prometheus, and traces.', 'Teams drowning in separate UIs for logs versus metrics.', 'One glass pane with version annotations on every deploy.', 'Data sources plus dashboards as code, alerts beside the graphs.', 5, 'observability'),
    ('Loki', 'Observability', 'Log aggregation indexed by labels, queried with LogQL.', 'Exact-error forensics without paying full-text index prices.', 'Labels keep it cheap; pairs with Prometheus metrics and Grafana.', 'Promtail DaemonSet ships lines, LogQL filters by labels and content.', 3, 'observability'),
    ('GHCR / Registries', 'Build', 'Artifact storage and distribution: images, SBOMs, attestations.', 'Every pipeline that promotes the same digest end to end.', 'Immutable digests make rollback a redeploy, not a rebuild.', 'Push by SHA tag, sign with Cosign, attest provenance, expire aggressively.', 3, 'build-artifacts'),
]


def build_tools_page(books, output_dir, env):
    CAT_HEX = env.get('CAT_HEX', {})
    ICON_FOR = {
        'Jenkins': '<img alt="" src="../assets/icons/jenkins/jenkins.svg" width="28" height="28">',
        'GitHub Actions': '<img alt="" src="../assets/icons/git/github.svg" width="28" height="28">',
        'GitLab CI': '<img alt="" src="../assets/icons/git/gitlab.svg" width="28" height="28">',
        'ArgoCD': '<img alt="" src="../assets/icons/deployment/argo.svg" width="28" height="28">',
        'Docker': '<img alt="" src="../assets/icons/docker/docker.svg" width="28" height="28">',
        'Kubernetes': '<img alt="" src="../assets/icons/deployment/argo.svg" width="28" height="28">',
        'Helm': '<img alt="" src="../assets/icons/general/puzzle.svg" width="28" height="28">',
        'Terraform': '<img alt="" src="../assets/icons/general/terraform.svg" width="28" height="28">',
        'Prometheus': '<img alt="" src="../assets/icons/monitoring/activity.svg" width="28" height="28">',
        'Grafana': '<img alt="" src="../assets/icons/monitoring/activity.svg" width="28" height="28">',
        'Loki': '<img alt="" src="../assets/icons/monitoring/activity.svg" width="28" height="28">',
        'GHCR / Registries': '<img alt="" src="../assets/icons/general/package.svg" width="28" height="28">',
    }
    cath = []
    for _t in CATALOG:
        _name, _cat, _what, _when, _why, _how, _pop, _bid = _t
        _col = CAT_HEX.get(_cat, '#18E299')
        _stars = '★' * _pop + '☆' * (5 - _pop)
        _icon = ICON_FOR.get(_name, '<span aria-hidden="true">' + htmllib.escape(_name[:1]) + '</span>')
        cath.append('<article class="toolcard" style="--cat:' + _col + '" aria-label="' + htmllib.escape(_name) + '">'
            '<div class="toolcard-head"><span class="map-icon" aria-hidden="true">' + _icon + '</span>'
            '<div><h3>' + htmllib.escape(_name) + '</h3>'
            '<span class="pop" title="Popularity: ' + str(_pop) + ' out of 5 in 2026 field adoption"><span class="poplbl">Popularity</span><span class="stars">' + _stars + '</span><b>' + str(_pop) + '/5</b></span></div></div>'
            '<dl class="tooldl"><dt>What</dt><dd>' + htmllib.escape(_what) + '</dd><dt>When</dt><dd>' + htmllib.escape(_when) + '</dd><dt>Why</dt><dd>' + htmllib.escape(_why) + '</dd><dt>How</dt><dd><code>' + htmllib.escape(_how) + '</code></dd></dl>'
            '<p><a class="btn" href="../read/' + _bid + '.html">Read in book →</a></p></article>')
    catalog_html = '<div class="hm-label" aria-hidden="true"><span>TOOL CATALOG</span><span>' + str(len(CATALOG)) + ' TOOLS</span></div><div class="toolgrid">' + ''.join(cath) + '</div><p class="sub">Popularity is a field estimate for 2026 hiring and community weight — fit beats fame; confirm with the matrix.</p>'
    links = {
        'jenkins': resolve_sheet(books, env, 'jenkins-complete', ['Setup', 'Topology', 'Agents']),
        'actions': resolve_sheet(books, env, 'platforms-roadmaps', ['Actions']),
        'gitlab': resolve_sheet(books, env, 'platforms-roadmaps', ['GitLab CI', 'Pipeline Anatomy']),
        'argocd': resolve_sheet(books, env, 'platforms-roadmaps', ['ArgoCD & GitOps', 'Push vs Pull', 'Where It Fits']),
        'choice': resolve_sheet(books, env, 'platforms-roadmaps', ['The Choice', 'Decision Framework', 'Side-by-Side']),
        'matrix': resolve_sheet(books, env, 'platforms-roadmaps', ['Tool vs Tool']),
    }
    qhtml = []
    for qi, (q, hint, opts) in enumerate(QUESTIONS):
        btns = []
        for o, w, x in opts:
            btns.append('<button class="btn qopt" data-q="' + str(qi) + '" data-w="' + htmllib.escape(json.dumps(w), quote=True) + '" title="' + htmllib.escape(x) + '">' + o + '</button>')
        vis = '' if qi == 0 else ' hidden'
        back = '' if qi == 0 else '<p><button class="btn qback">← Back</button></p>'
        qhtml.append('<div class="qcard" id="q' + str(qi) + '"' + vis + '><div class="qprog"><span style="width:' + str(round(100 * qi / len(QUESTIONS))) + '%"></span></div><p class="qstep">Question ' + str(qi + 1) + ' of ' + str(len(QUESTIONS)) + '</p><h3>' + q + '</h3><p class="qhint">' + hint + '</p><div class="opts">' + ''.join(btns) + '</div>' + back + '</div>')
    names = {}
    whys = {}
    for k in TOOLS_META:
        names[k] = TOOLS_META[k][0]
        whys[k] = TOOLS_META[k][1]
    js_vars = ('const LINKS=' + json.dumps(links) + ';'
               'const WHY=' + json.dumps(whys) + ';'
               'const NAMES=' + json.dumps(names) + ';'
               'const STUDY=' + json.dumps(STUDY_THREAD) + ';'
               'const STUDYLBL=' + json.dumps(STUDY_LABEL) + ';'
               'const NQ=' + str(len(QUESTIONS)) + ';')
    quiz_js = '''
let qi=0;const scores={jenkins:0,actions:0,gitlab:0,argocd:0};const hist=[];
document.querySelectorAll('.qopt').forEach(b=>b.onclick=()=>{
const w=JSON.parse(b.dataset.w);hist.push({qi:qi,w:w});for(const k in w)scores[k]+=w[k];
document.querySelector('#q'+qi).hidden=true;qi++;
if(qi<NQ){document.querySelector('#q'+qi).hidden=false;}else{showResult();}});
document.querySelectorAll('.qback').forEach(b=>b.onclick=()=>{const last=hist.pop();if(!last)return;for(const k in last.w)scores[k]-=last.w[k];document.querySelector('#q'+qi).hidden=true;qi=last.qi;document.querySelector('#q'+qi).hidden=false;});
function showResult(){const tot=Math.max(1,...Object.values(scores));
const rank=Object.keys(scores).sort((a,b)=>scores[b]-scores[a]);
const tie=rank.length>1&&scores[rank[0]]===scores[rank[1]];
let s='<div class="qcard"><div class="qprog"><span style="width:100%"></span></div><h3>Your stack, ranked</h3>';
if(tie)s+='<p class="qhint">Tie at the top — either winner fits; read both WHEN TO USE boxes before you commit.</p>';
const MEDAL=['\U0001F947','\U0001F948','\U0001F949','4.'];
rank.forEach((k,i)=>{s+='<div class="tcard'+(i===0?' winner':'')+'"><b>'+MEDAL[i]+' '+NAMES[k]+' - '+scores[k]+' pts</b><div class="tbar"><b style="width:'+Math.round(100*scores[k]/tot)+'%"></b></div><p>'+WHY[k]+'</p><a class="btn" href="'+LINKS[k]+'">Read why</a> ';if(i===0){s+='<a class="btn" href="'+LINKS.choice+'">Compare all</a> <a class="btn" href="'+LINKS.matrix+'">Full field matrix</a><a class="btn" href="../threads/#'+STUDY[k]+'">Study: '+STUDYLBL[k]+'</a>';}s+='</div>';});
const h='#r='+rank.map(k=>k+':'+scores[k]).join(',');
s+='<p><button class="btn" onclick="location.reload()">Retake</button> <button class="btn" id="sharebtn">Copy result link</button></p></div>';
document.querySelector('#result').innerHTML=s;
try{history.replaceState(null,'',h);}catch(e){}
const _sb=document.querySelector('#sharebtn');if(_sb)_sb.onclick=()=>{try{navigator.clipboard.writeText(location.href);_sb.textContent='Copied!';}catch(e){_sb.textContent=location.href;}};
window.scrollTo({top:document.querySelector('#result').offsetTop-80});}
try{const _m=location.hash.match(/^#r=([a-z,0-9:]+)$/);if(_m){_m[1].split(',').forEach(p=>{const kv=p.split(':');if(scores[kv[0]]!==undefined)scores[kv[0]]=+kv[1]||0;});document.querySelectorAll('.qcard[id^=q]').forEach(e=>e.hidden=true);showResult();}}catch(e){}
'''
    page = ('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">'
            '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            '<link rel="icon" type="image/svg+xml" href="../favicon.svg">'
            '<title>Tool picker - CICD BY Nabawy</title>'
            '<style>' + env['BASE_CSS'] + '.qcard{max-width:640px;margin:18px auto;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:22px}.qcard .opts{display:flex;gap:10px;flex-wrap:wrap;margin-top:12px}.qcard .btn{min-height:48px}.qcard .opts .btn{flex:1 1 140px}.qprog{height:6px;border-radius:99px;background:var(--bg2);margin-bottom:12px;overflow:hidden}.qprog span{display:block;height:100%;background:var(--brand);border-radius:99px;transition:width .2s}.qstep{font-family:var(--mono);font-size:11px;color:var(--mut);letter-spacing:.1em;margin-bottom:6px}.qhint{font-size:13px;color:var(--mut);margin:4px 0 6px}.qback{margin-top:4px}.toolgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px;margin:14px 0}.toolcard{background:var(--card);border:1px solid var(--line-soft);border-radius:14px;padding:18px}.toolcard:hover{border-color:var(--cat)}.toolcard-head{display:flex;gap:12px;align-items:center;margin-bottom:8px}.toolcard{position:relative;overflow:hidden}.toolcard::before{content:'';position:absolute;top:0;left:0;right:0;height:3px;background:var(--cat)}.toolcard-head .map-icon{font-size:20px;font-weight:800;width:44px;height:44px;overflow:hidden}.toolcard-head .map-icon img{width:28px;height:28px;display:block;object-fit:contain}.toolcard h3{font-size:16px;margin:0}.toolcard .pop{display:inline-flex;align-items:center;gap:6px;color:var(--mut);font-size:12px}.toolcard .pop .poplbl{font-family:var(--mono);font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--mut)}.toolcard .pop .stars{color:var(--cat);letter-spacing:1px}.toolcard .tooldl{margin:10px 0 6px}.toolcard .tooldl dt{font-family:var(--mono);font-size:10px;letter-spacing:.12em;text-transform:uppercase;color:var(--cat);margin-top:8px}.toolcard .tooldl dd{font-size:13px;color:var(--mut);margin:2px 0 0}.toolcard .tooldl dd code{font-family:var(--mono);font-size:12px;background:color-mix(in srgb,var(--cat) 8%,var(--bg2));border:1px solid color-mix(in srgb,var(--cat) 14%,var(--line));border-radius:6px;padding:2px 6px;color:var(--ink)}.tcard{max-width:640px;margin:12px auto;background:var(--card);border:1px solid var(--line);border-radius:14px;padding:18px 22px}.tcard.winner{border-color:var(--brand);box-shadow:var(--shadow-lift)}.tbar{height:8px;border-radius:99px;background:var(--bg2);margin:10px 0}.tbar b{display:block;height:100%;border-radius:99px;background:var(--brand)}</style>'
            + HEAD_THEME +
            '</head><body><header class="top"><div class="wrap">'
            '<a class="logo" href="../index.html" style="color:inherit">CICD<span> BY Nabawy</span></a>'
            '<nav class="crumbs"><span class="sep">/</span><span class="here">Tools</span></nav>'
            '<a class="btn" href="../index.html" style="text-decoration:none">Home</a>'
            '<a class="btn" href="../glossary.html" style="text-decoration:none">Study Deck</a>'
            '<a class="btn" href="../threads/" style="text-decoration:none">Threads</a>'
            '<button class="btn" id="themebtn" aria-label="Toggle theme">X</button>'
            '</div></header><div class="wrap">'
            '<div class="hero" style="padding:36px 24px 16px"><span class="eyebrow">TOOLS</span>'
            '<h1>Which tool fits?</h1><p>' + str(len(QUESTIONS)) + ' questions. Ranked answers with reasons, study threads, and deep links.</p></div>'
            "<div id='quiz'>" + ''.join(qhtml) + "</div><div id='result'></div>" + catalog_html +
            '</div><footer><div class="wrap"><span>CICD BY Nabawy</span><span><a href="../index.html">Home</a> · <a href="../glossary.html">Study Deck</a> · <a href="../threads/">Threads</a></span></div></footer>'
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
