
# Everyday Wants gift guide site builder. Reads guides.json, writes static HTML into out_dir.
import json, html, os
TAG = "everydaywa08c-20"
SITE = "https://computeragent7.github.io"
def amz(a): return f"https://www.amazon.com/dp/{a}?tag={TAG}"
CSS = """
:root{--cream:#F7F2EA;--paper:#FFFDF9;--ink:#212522;--green:#2E4A3A;--green2:#3D6350;--muted:#5F625A;--line:#E6DED1;--hl:#FBEFD9}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--cream);color:var(--ink);font:17px/1.6 'Work Sans',system-ui,sans-serif}
a{color:var(--green)}
.wrap{max-width:860px;margin:0 auto;padding:0 20px}
header.top{background:var(--paper);border-bottom:1px solid var(--line)}
header.top .wrap{display:flex;align-items:center;justify-content:space-between;height:64px}
.brand{font-family:'DM Serif Display',serif;font-size:26px;color:var(--ink);text-decoration:none}
.navlink{font-size:14px;font-weight:600;letter-spacing:.06em;text-transform:uppercase;text-decoration:none}
.disc{background:var(--green);color:#EEF2EC;font-size:13.5px;line-height:1.45;padding:10px 0;text-align:center}
.hero{position:relative;margin:28px 0 8px;border-radius:22px;overflow:hidden;background:#ddd}
.hero img{display:block;width:100%;height:300px;object-fit:cover}
.hero .shade{position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 30%,rgba(0,0,0,.55))}
.hero .txt{position:absolute;left:28px;right:28px;bottom:24px;color:#fff}
.eyebrow{font-size:13px;font-weight:600;letter-spacing:.14em;text-transform:uppercase;opacity:.9}
h1{font-family:'DM Serif Display',serif;font-weight:400;font-size:46px;line-height:1.05;margin:6px 0 0}
.intro{font-size:19px;color:var(--muted);margin:18px 0 6px}
.meta{font-size:14px;color:var(--muted);margin:0 0 22px}
ol.picks{list-style:none;padding:0;margin:0;counter-reset:n}
ol.picks li{counter-increment:n;background:var(--paper);border:1px solid var(--line);border-radius:18px;padding:22px 24px;margin:0 0 14px;display:grid;grid-template-columns:44px 1fr;gap:4px 16px;scroll-margin-top:20px}
ol.picks li::before{content:counter(n);grid-row:span 3;width:44px;height:44px;border-radius:50%;background:var(--cream);border:1px solid var(--line);display:flex;align-items:center;justify-content:center;font-family:'DM Serif Display',serif;font-size:22px;color:var(--green)}
ol.picks li:target{background:var(--hl);border-color:#E7C98F;box-shadow:0 0 0 3px #F3DDB0}
ol.picks h2{font-family:'DM Serif Display',serif;font-weight:400;font-size:26px;line-height:1.15;margin:4px 0 2px}
ol.picks p{margin:0 0 12px;color:#3c3f3a}
.btn{justify-self:start;display:inline-block;background:var(--green);color:#fff;text-decoration:none;font-weight:600;font-size:16px;padding:11px 22px;border-radius:999px}
.btn:hover{background:var(--green2)}
.more{margin:40px 0 10px}
.more h3{font-family:'DM Serif Display',serif;font-weight:400;font-size:28px;margin:0 0 14px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:14px}
.card{display:block;background:var(--paper);border:1px solid var(--line);border-radius:18px;overflow:hidden;text-decoration:none;color:var(--ink)}
.card img{display:block;width:100%;height:150px;object-fit:cover}
.card div{padding:14px 16px 16px}
.card b{font-family:'DM Serif Display',serif;font-weight:400;font-size:22px;display:block;line-height:1.15}
.card span{font-size:14px;color:var(--muted)}
footer{margin:46px 0 0;padding:26px 0 40px;border-top:1px solid var(--line);font-size:13.5px;color:var(--muted)}
@media (max-width:600px){h1{font-size:34px}.hero img{height:230px}ol.picks li{padding:18px 18px;grid-template-columns:36px 1fr;gap:2px 12px}ol.picks li::before{width:36px;height:36px;font-size:18px}ol.picks h2{font-size:22px}}
"""
DISC = "As an Amazon Associate I earn from qualifying purchases. Picks come from trusted gift guides and reviews. Prices change, so check Amazon for today's price."
def page(title, desc, body, path):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} | Everyday Wants</title><meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{SITE}{path}"><meta property="og:title" content="{html.escape(title)}"><meta property="og:description" content="{html.escape(desc)}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Work+Sans:wght@400;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css"></head><body>
<header class="top"><div class="wrap"><a class="brand" href="/">everyday wants</a><a class="navlink" href="/#guides">Gift guides</a></div></header>
<div class="disc"><div class="wrap">{DISC}</div></div>
<main class="wrap">{body}</main>
<footer><div class="wrap">Everyday Wants finds useful, cozy things worth giving. {DISC}</div></footer></body></html>"""
def card(g):
    return f'<a class="card" href="/{g["slug"]}/"><img src="/img/{g["slug"]}.jpg" alt="" loading="lazy"><div><b>{html.escape(g["title"])}</b><span>{len(g["items"])} picks</span></div></a>'
def build(data, out):
    I, G = data["items"], data["guides"]
    os.makedirs(out, exist_ok=True); open(os.path.join(out,"style.css"),"w").write(CSS)
    open(os.path.join(out,".nojekyll"),"w").write("")
    for g in G:
        lis = []
        for a in g["items"]:
            name, why = I[a]
            lis.append(f'<li id="{a}"><h2>{html.escape(name)}</h2><p>{html.escape(why)}</p><a class="btn" href="{amz(a)}" target="_blank" rel="sponsored nofollow noopener">See it on Amazon &rarr;</a></li>')
        others = "".join(card(o) for o in G if o["slug"]!=g["slug"])
        body = f"""<section class="hero"><img src="/img/{g['slug']}.jpg" alt=""><div class="shade"></div><div class="txt"><div class="eyebrow">Gift guide</div><h1>{html.escape(g['title'])}</h1></div></section>
<p class="intro">{html.escape(g['intro'])}</p><p class="meta">{len(g['items'])} picks · updated {data.get('updated','')}</p>
<ol class="picks">{''.join(lis)}</ol><section class="more"><h3>More gift guides</h3><div class="grid">{others}</div></section>"""
        d = os.path.join(out, g["slug"]); os.makedirs(d, exist_ok=True)
        open(os.path.join(d,"index.html"),"w").write(page(g["title"], g["intro"], body, f"/{g['slug']}/"))
    body = f"""<section class="hero"><img src="/img/{G[0]['slug']}.jpg" alt=""><div class="shade"></div><div class="txt"><div class="eyebrow">Holiday 2026</div><h1>Gift ideas people actually want</h1></div></section>
<p class="intro">Cozy, useful and affordable gift picks, sorted by who you're shopping for.</p><section class="more" id="guides"><div class="grid">{''.join(card(g) for g in G)}</div></section>"""
    open(os.path.join(out,"index.html"),"w").write(page("Gift Ideas People Actually Want","Cozy, useful, affordable gift guides for everyone on your list.",body,"/"))
    urls = [SITE+"/"]+[f"{SITE}/{g['slug']}/" for g in G]
    open(os.path.join(out,"sitemap.xml"),"w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{u}</loc></url>" for u in urls)+"</urlset>")
    open(os.path.join(out,"robots.txt"),"w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
