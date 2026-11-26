"""Builds the static social posts (weeks 1 to 13) as HTML, ready to render to PNG.

Every word on a post is real HTML text. Images are frames from the sample build films in films/,
and every one carries a "Sample" tag. Phone screens are drawn in HTML/CSS with made-up names.
Run: python3 social/build.py   then   node social/render.mjs
"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'src')
CAL = json.load(open(os.path.join(SRC, 'calendar-wk01-13.json')))
ROW = {int(float(r['Week'])): r for r in CAL}

FONTS = '../../assets/fonts/'
CSS = f"""
@font-face{{font-family:Barlow;font-weight:400;src:url({FONTS}barlow-400.woff2) format("woff2")}}
@font-face{{font-family:Barlow;font-weight:500;src:url({FONTS}barlow-500.woff2) format("woff2")}}
@font-face{{font-family:Barlow;font-weight:600;src:url({FONTS}barlow-600.woff2) format("woff2")}}
@font-face{{font-family:Barlow;font-weight:700;src:url({FONTS}barlow-700.woff2) format("woff2")}}
@font-face{{font-family:"Barlow Condensed";font-weight:600;src:url({FONTS}barlow-condensed-600.woff2) format("woff2")}}
@font-face{{font-family:"IBM Plex Mono";font-weight:500;src:url({FONTS}plex-mono-500.woff2) format("woff2")}}
:root{{--ink:#121417;--paper:#fafaf8;--paper2:#f1f0ea;--brand:#ff5a1f;--tone:#6c6a63;--grey:#57534e;--rule:#deddd7;--tone-d:#a39f96}}
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1080px;height:1350px;overflow:hidden}}
body{{font-family:Barlow,sans-serif;color:var(--ink);-webkit-font-smoothing:antialiased}}
.post{{position:relative;width:1080px;height:1350px;padding:96px;background:var(--paper);display:flex;flex-direction:column;overflow:hidden}}
.post.dark{{background:var(--ink);color:var(--paper)}}
.post.p2{{background:var(--paper2)}}
.label{{font:600 26px/1.2 "Barlow Condensed",sans-serif;letter-spacing:.14em;text-transform:uppercase;color:var(--grey)}}
.dark .label{{color:var(--tone-d)}}
h1{{font-weight:600;font-size:100px;line-height:1.02;letter-spacing:-.025em}}
h1 .t{{color:var(--tone)}}
.dark h1 .t{{color:var(--tone-d)}}
.big{{font-size:200px;line-height:.95}}
.sub{{font-size:36px;line-height:1.3;color:var(--grey);font-weight:400}}
.dark .sub{{color:var(--tone-d)}}
.mono{{font-family:"IBM Plex Mono",monospace;font-weight:500}}
.foot{{position:absolute;left:96px;right:96px;bottom:80px;display:flex;align-items:flex-end;justify-content:space-between;gap:24px}}
.src{{font-size:22px;line-height:1.35;color:var(--grey);max-width:640px}}
.dark .src{{color:var(--tone-d)}}
.brandmark{{display:flex;align-items:center;gap:14px;font-size:36px;letter-spacing:-.02em;white-space:nowrap}}
.brandmark svg{{width:56px;height:56px;display:block}}
.brandmark b{{font-weight:700}}
.brandmark span{{font-weight:400}}
.btn{{display:inline-flex;align-items:center;gap:16px;background:var(--brand);color:var(--ink);font:600 40px/1 Barlow,sans-serif;padding:30px 44px;border-radius:6px;box-shadow:0 3px 0 var(--ink)}}
.dark .btn{{box-shadow:none}}
.sample{{position:absolute;top:18px;left:18px;z-index:3;font:600 20px/1 "Barlow Condensed",sans-serif;letter-spacing:.14em;text-transform:uppercase;background:rgba(18,20,23,.78);color:var(--paper);padding:8px 12px;border-radius:4px}}
.progress{{position:absolute;top:44px;left:96px;right:96px;display:flex;gap:12px}}
.progress i{{flex:1;height:8px;border-radius:2px;background:var(--rule)}}
.dark .progress i{{background:#3a3d42}}
.progress i.on{{background:var(--brand)}}
/* phone */
.phone{{position:relative;width:420px;height:860px;border-radius:64px;background:#0b0c0e;padding:16px;box-shadow:0 30px 60px rgba(18,20,23,.22)}}
.dark .phone{{box-shadow:0 30px 60px rgba(0,0,0,.5);outline:2px solid #2a2d32}}
.screen{{position:relative;width:100%;height:100%;border-radius:50px;overflow:hidden;background:var(--paper);color:var(--ink)}}
.statusbar{{display:flex;justify-content:space-between;align-items:center;padding:20px 30px 6px;font:600 20px Barlow,sans-serif}}
.statusbar .batt{{width:34px;height:16px;border:2px solid currentColor;border-radius:4px;position:relative}}
.statusbar .batt:after{{content:"";position:absolute;inset:2px 8px 2px 2px;background:currentColor;border-radius:1px}}
.app-h{{padding:14px 26px 12px;border-bottom:1px solid var(--rule);display:flex;justify-content:space-between;align-items:baseline}}
.app-h b{{font-size:30px;letter-spacing:-.02em}}
.app-h span{{font:600 16px "Barlow Condensed";letter-spacing:.12em;text-transform:uppercase;color:var(--grey)}}
.row{{padding:18px 26px;border-bottom:1px solid var(--rule);display:grid;grid-template-columns:16px 1fr auto;gap:10px;align-items:start}}
.row .dot{{width:12px;height:12px;border-radius:50%;margin-top:9px;background:transparent}}
.row .dot.new{{background:var(--brand)}}
.row .n{{font-size:23px;font-weight:600}}
.row .m{{font-size:19px;color:var(--grey);margin-top:2px}}
.row .tm{{font:500 17px "IBM Plex Mono";color:var(--grey);margin-top:6px}}
.row.old .n{{font-weight:500;color:var(--grey)}}
.msg{{margin:16px 26px 0;padding:16px 18px;border-radius:14px;font-size:20px;line-height:1.35}}
.msg.in{{background:var(--paper2)}}
.msg.out{{background:#fff;border:1px solid var(--rule)}}
.msg .k{{display:block;font:600 15px "Barlow Condensed";letter-spacing:.12em;text-transform:uppercase;color:var(--grey);margin-bottom:6px}}
.msg .k .mono{{font-size:15px;letter-spacing:0;text-transform:none}}
.film{{position:absolute;inset:0}}
.film img{{width:100%;height:100%;object-fit:cover;display:block}}
.film .site-h{{position:absolute;left:0;right:0;top:0;padding:62px 28px 60px;background:linear-gradient(180deg,rgba(18,20,23,.7),rgba(18,20,23,0));color:var(--paper)}}
.film .site-h b{{font-size:34px;letter-spacing:-.02em;display:block}}
.film .site-h span{{font:600 15px "Barlow Condensed";letter-spacing:.2em;text-transform:uppercase;opacity:.85}}
.film .sample{{top:auto;bottom:22px;left:22px}}
.card{{background:#fff;border:1px solid var(--rule);border-radius:10px}}
"""


def mark(dark=False):
    bottom = '#fafaf8' if dark else '#121417'
    return (f'<svg viewBox="0 0 100 100" aria-hidden="true"><path fill="#ff5a1f" d="M0 0H100V32H76V24H24V38H58L42 62H0Z"/>'
            f'<path fill="{bottom}" d="M100 100H0V68H24V76H76V62H48L64 38H100Z"/></svg>')


def brandmark(dark=False):
    return f'<div class="brandmark">{mark(dark)}<div><span>scroll</span><b>built</b></div></div>'


def foot(dark=False, left='scrollbuilt.com'):
    return f'<div class="foot"><div class="src">{left}</div>{brandmark(dark)}</div>'


def progress(n, cur):
    return '<div class="progress">' + ''.join(f'<i class="{"on" if i == cur else ""}"></i>' for i in range(n)) + '</div>'


def page(body, cls='', title=''):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>{html.escape(title)}</title>'
            f'<style>{CSS}</style></head><body><div class="post {cls}">{body}</div></body></html>')


def statusbar(t='9:41'):
    return f'<div class="statusbar"><span>{t}</span><span class="batt"></span></div>'


def film_phone(img, name='Your Name Pools', trade='Pools · Your city', w=420, h=860):
    return (f'<div class="phone" style="width:{w}px;height:{h}px"><div class="screen"><div class="film">'
            f'<img src="img/{img}" alt=""><div class="site-h"><b>{name}</b><span>{trade}</span></div>'
            f'<span class="sample">Sample</span></div></div></div>')


def inbox_phone(time='9:02 PM', w=420, h=860):
    return f"""<div class="phone" style="width:{w}px;height:{h}px"><div class="screen">
  {statusbar(time.split()[0])}
  <div class="app-h"><b>Leads</b><span>1 new</span></div>
  <div class="row"><span class="dot new"></span><div><div class="n">A. Rivera</div><div class="m">Website form · Backyard pool</div></div><div class="tm">{time}</div></div>
  <div class="msg in"><span class="k">Their message</span>Hi, we're thinking about a pool this spring. Can someone come out to look at our yard?</div>
  <div class="msg out"><span class="k">Instant reply sent · <span class="mono">{time}</span></span>Thanks for reaching out. We got your request and will call you tomorrow morning to set a time.</div>
  <div class="row old" style="margin-top:18px;border-top:1px solid var(--rule)"><span class="dot"></span><div><div class="n">J. Moore</div><div class="m">Website form · Patio and lighting</div></div><div class="tm">Yesterday</div></div>
  <div class="row old"><span class="dot"></span><div><div class="n">K. Patel</div><div class="m">Website form · Pool remodel</div></div><div class="tm">Mon</div></div>
</div></div>"""


POSTS = []  # (week, slug, html, alt) ; slug like 'static' or 'slide1'


def add(week, slug, body, cls=''):
    POSTS.append((week, slug, page(body, cls, f'Week {week} {slug}')))


# ---- Week 2: the 10 seconds ------------------------------------------------------------------
r = ROW[2]
add(2, 'static', f"""
<div class="label">Before they read a word</div>
<h1 style="margin-top:36px">In the first 10 seconds, <span class="t">homeowners have already judged you.</span></h1>
<div class="mono" style="margin-top:auto;margin-bottom:220px;font-size:220px;line-height:1;color:var(--brand);letter-spacing:-.02em">00:10</div>
{foot(False, html.escape(r['Check before posting']))}
""")

# ---- Week 4: a reply in seconds --------------------------------------------------------------
add(4, 'static', f"""
<div style="display:grid;grid-template-columns:1fr 420px;gap:56px;align-items:center;height:100%">
  <div style="align-self:start">
    <div class="label">Website form leads</div>
    <h1 style="margin-top:36px;font-size:96px">A reply in seconds. <span class="t">Even at 9&nbsp;p.m.</span></h1>
    <p class="sub" style="margin-top:36px">The homeowner gets an answer right away. You get the lead in one inbox on your phone.</p>
  </div>
  <div style="align-self:center;margin-top:-60px">{inbox_phone('9:02 PM')}</div>
</div>
{foot(True)}
""", 'dark')

# ---- Week 6: carousel, 3 slides --------------------------------------------------------------
add(6, 'slide1', f"""{progress(3, 0)}
<div class="label" style="margin-top:40px">Homeowners compare before they call</div>
<h1 style="margin-top:36px;font-size:120px">The other guy's website <span class="t">looks better than yours.</span></h1>
<p class="sub" style="margin-top:auto;margin-bottom:170px">Swipe to see the difference.</p>
{foot()}
""")
OLD_SITE = """<div style="position:relative;width:420px;height:860px;border-radius:64px;background:#0b0c0e;padding:16px">
<div class="screen" style="background:#e9e9e9;font-family:Arial,Helvetica,sans-serif;color:#333">
  <div style="background:#2c3e66;color:#fff;padding:54px 16px 14px;font-size:17px;font-weight:700;letter-spacing:.02em">EXAMPLE CONTRACTOR LLC</div>
  <div style="background:#d7d7d7;padding:8px 10px;font-size:13px;color:#444;border-bottom:2px solid #999">Home | About Us | Services | Gallery | Contact Us</div>
  <div style="margin:14px;height:190px;background:linear-gradient(#b9c3cc,#97a3ad);display:grid;place-items:center;color:#fff;font-size:16px;font-weight:700;text-align:center;padding:10px">QUALITY WORK YOU CAN TRUST!!!</div>
  <div style="margin:0 14px;font-size:14px;line-height:1.5">Welcome to our website. We have been serving the area for many years. Call us today for a FREE ESTIMATE. We do pools, patios, decks, fences and much more. Licensed and insured.</div>
  <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px;margin:14px">
    <div style="background:#c7c7c7;height:70px"></div><div style="background:#bdbdbd;height:70px"></div><div style="background:#c7c7c7;height:70px"></div></div>
  <div style="margin:0 14px;background:#f5f5f5;border:1px solid #bbb;padding:10px;font-size:13px">Contact form: Name ____ Phone ____ Message ____ [SUBMIT]</div>
  <div style="position:absolute;bottom:20px;left:0;right:0;text-align:center;font-size:11px;color:#777">© 2014 Example Contractor LLC · Site by Template Co.</div>
</div></div>"""
add(6, 'slide2', f"""{progress(3, 1)}
<div class="label" style="margin-top:40px">Side by side</div>
<div style="display:grid;grid-template-columns:420px 420px;gap:48px;justify-content:center;margin-top:52px">
  <div>{OLD_SITE}<p class="src" style="margin-top:22px;text-align:center">A dated site (invented example)</p></div>
  <div>{film_phone('pool-mid.webp')}<p class="src" style="margin-top:22px;text-align:center">A ScrollBuilt draft, mid build film</p></div>
</div>
{foot()}
""")
add(6, 'slide3', f"""{progress(3, 2)}
<div class="label" style="margin-top:40px">Free · no card · no call</div>
<h1 style="margin-top:36px;font-size:132px">See yours <span class="t">in 30 seconds.</span></h1>
<p class="sub" style="margin-top:40px">Type your business name, trade and city. A draft of your own site appears.</p>
<div style="margin-top:64px"><span class="btn">Show me my site <span aria-hidden="true">→</span></span></div>
{foot(False, 'scrollbuilt.com')}
""")

# ---- Week 7: see your site first -------------------------------------------------------------
add(7, 'static', f"""
<div style="display:grid;grid-template-columns:1fr 400px;gap:56px;height:100%">
  <div>
    <div class="label">Free · no card · no call</div>
    <h1 style="margin-top:36px;font-size:112px">See your site first. <span class="t">Decide after.</span></h1>
    <p class="sub" style="margin-top:40px">Your draft is free. You only pay when your site goes live.</p>
  </div>
  <div style="margin-top:60px">{film_phone('pool-finished.webp', w=400, h=820)}</div>
</div>
{foot()}
""")

# ---- Week 8: carousel, 4 slides --------------------------------------------------------------
FOUND = """<div class="card" style="width:888px;padding:34px 38px;margin-top:64px">
  <div style="display:flex;justify-content:space-between;align-items:baseline"><b style="font-size:34px;letter-spacing:-.02em">Search &amp; AI</b><span class="label" style="font-size:18px">Your name pools</span></div>
  <div style="margin-top:26px;font:600 18px 'Barlow Condensed';letter-spacing:.12em;text-transform:uppercase;color:var(--grey)">Get found for</div>
  <div style="display:flex;flex-wrap:wrap;gap:12px;margin-top:12px">
    <span style="border:1px solid var(--rule);border-radius:6px;padding:10px 16px;font-size:24px">pool builder in your city</span>
    <span style="border:1px solid var(--rule);border-radius:6px;padding:10px 16px;font-size:24px">pool remodel</span>
    <span style="border:1px solid var(--rule);border-radius:6px;padding:10px 16px;font-size:24px">backyard spa</span></div>
  <div style="margin-top:26px;font:600 18px 'Barlow Condensed';letter-spacing:.12em;text-transform:uppercase;color:var(--grey)">Page title</div>
  <div style="margin-top:8px;font-size:26px;border:1px solid var(--rule);border-radius:6px;padding:14px 16px">Your Name Pools | Custom Pools in Your City</div>
  <div style="margin-top:22px;display:flex;align-items:center;gap:12px;font-size:24px"><span style="width:12px;height:12px;border-radius:50%;background:var(--brand)"></span>Set up for Google and AI assistants to read</div>
</div>"""
add(8, 'slide1', f"""{progress(4, 0)}
<div class="label" style="margin-top:40px">1 of 3</div>
<h1 class="big" style="margin-top:28px">Found.</h1>
<p class="sub" style="margin-top:28px">Set up so homeowners can find you.</p>
{FOUND}
{foot()}
""")
ANSWERED = """<div style="width:888px;margin-top:56px;background:#1c1f23;border:1px solid #33373d;border-radius:10px;padding:30px 36px;color:var(--paper)">
  <div style="display:flex;justify-content:space-between;align-items:baseline"><b style="font-size:34px;letter-spacing:-.02em">Leads</b><span class="label" style="font-size:18px">1 new</span></div>
  <div style="display:grid;grid-template-columns:18px 1fr auto;gap:14px;align-items:start;margin-top:22px;padding-top:22px;border-top:1px solid #33373d">
    <span style="width:14px;height:14px;border-radius:50%;background:var(--brand);margin-top:10px"></span>
    <div><div style="font-size:28px;font-weight:600">A. Rivera</div><div style="font-size:23px;color:var(--tone-d);margin-top:2px">Website form · Backyard pool</div></div>
    <span class="mono" style="font-size:21px;color:var(--tone-d);margin-top:6px">9:02 PM</span></div>
  <div style="margin:20px 0 0 32px;background:var(--paper);color:var(--ink);border-radius:10px;padding:18px 22px;font-size:23px;line-height:1.35">
    <span style="display:block;font:600 16px 'Barlow Condensed';letter-spacing:.12em;text-transform:uppercase;color:var(--grey);margin-bottom:6px">Instant reply sent · <span class="mono" style="font-size:16px;letter-spacing:0">9:02 PM</span></span>
    Thanks for reaching out. We got your request and will call you tomorrow morning to set a time.</div>
</div>"""
add(8, 'slide2', f"""{progress(4, 1)}
<div class="label" style="margin-top:40px">2 of 3</div>
<h1 class="big" style="margin-top:28px">Answered.</h1>
<p class="sub" style="margin-top:28px">Every form lead gets a reply in seconds.</p>
{ANSWERED}
{foot(True)}
""", 'dark')
WON = """<div class="card" style="width:888px;padding:34px 38px;margin-top:56px">
  <div style="display:flex;align-items:center;gap:14px;font-size:28px;font-weight:600"><span style="width:14px;height:14px;border-radius:50%;background:var(--brand)"></span>Your proposal was opened</div>
  <div style="margin-top:6px;font-size:23px;color:var(--grey)">A. Rivera · Backyard pool and spa · <span class="mono" style="font-size:21px">7:42 PM</span></div>
  <div style="border-top:1px solid var(--rule);margin-top:24px;padding-top:22px;display:flex;justify-content:space-between;font-size:24px"><span>Reminder: call A. Rivera</span><span class="mono" style="font-size:21px;color:var(--grey)">Tomorrow</span></div>
  <div style="border-top:1px solid var(--rule);margin-top:20px;padding-top:20px;display:flex;justify-content:space-between;font-size:24px"><span>Review request sent to J. Moore</span><span class="mono" style="font-size:21px;color:var(--grey)">Done</span></div>
</div>"""
add(8, 'slide3', f"""{progress(4, 2)}
<div class="label" style="margin-top:40px">3 of 3</div>
<h1 class="big" style="margin-top:28px">Won.</h1>
<p class="sub" style="margin-top:28px">Reminders, proposal pages and review requests keep the job moving.</p>
{WON}
{foot()}
""")
add(8, 'slide4', f"""{progress(4, 3)}
<div class="label" style="margin-top:40px">Found. Answered. Won.</div>
<h1 style="margin-top:36px;font-size:132px">See your site <span class="t">in 30 seconds.</span></h1>
<p class="sub" style="margin-top:40px">Free, no card, no call.</p>
<div style="margin-top:64px"><span class="btn">Show me my site <span aria-hidden="true">→</span></span></div>
{foot(True)}
""", 'dark')

# ---- Week 10: paid an agency -----------------------------------------------------------------
INVOICE = """<div style="background:var(--paper);color:var(--ink);border-radius:8px;width:460px;padding:34px 34px 30px;transform:rotate(-2deg);box-shadow:0 30px 60px rgba(0,0,0,.45)">
  <div style="display:flex;justify-content:space-between;align-items:baseline"><b style="font-size:34px;letter-spacing:-.02em">Invoice</b><span class="label" style="font-size:17px">Marketing agency</span></div>
  <div style="border-top:2px solid var(--ink);margin-top:18px"></div>
  <div style="display:flex;justify-content:space-between;gap:12px;padding:16px 0;border-bottom:1px solid var(--rule);font-size:23px;color:var(--tone);text-decoration:line-through"><span>Monthly retainer</span><span class="mono" style="font-size:20px">$3,500–$8,000</span></div>
  <div style="display:flex;justify-content:space-between;gap:12px;padding:16px 0;border-bottom:1px solid var(--rule);font-size:23px;color:var(--tone);text-decoration:line-through"><span>Website build</span><span class="mono" style="font-size:20px">$12,000+</span></div>
  <div style="display:flex;justify-content:space-between;gap:12px;padding:16px 0;border-bottom:1px solid var(--rule);font-size:23px;color:var(--tone);text-decoration:line-through"><span>Kickoff call</span><span class="mono" style="font-size:20px">1 hr</span></div>
  <div style="display:flex;justify-content:space-between;gap:12px;padding:16px 0;font-size:23px;color:var(--tone);text-decoration:line-through"><span>Strategy session</span><span class="mono" style="font-size:20px">TBD</span></div>
</div>"""
add(10, 'static', f"""
<div class="label">Agencies often charge thousands a month</div>
<h1 style="margin-top:36px;font-size:108px">Paid an agency. <span class="t">Got a kickoff call.</span></h1>
<div style="display:flex;align-items:flex-start;justify-content:space-between;margin-top:56px">
  <div style="margin-top:110px">{INVOICE}</div>
  <div style="text-align:center">{film_phone('landscape-finished.webp', 'Your Name Landscapes', 'Landscaping · Your city', w=330, h=660)}<p class="src" style="margin-top:16px">Your draft: free to see</p></div>
</div>
{foot(True, 'Typical agency fees. Prices vary.')}
""", 'dark')

# ---- Week 12: proposal opened ----------------------------------------------------------------
add(12, 'static', f"""
<div class="label">Proposal pages</div>
<h1 style="margin-top:36px;font-size:112px">Know when they open <span class="t">your proposal.</span></h1>
<div class="card" style="margin-top:96px;padding:40px 44px;box-shadow:0 24px 48px rgba(18,20,23,.10)">
  <div style="display:flex;justify-content:space-between;align-items:center"><div class="brandmark" style="font-size:26px;gap:10px">{mark()}<div><span>scroll</span><b>built</b></div></div><span class="mono" style="font-size:24px;color:var(--grey)">7:42 PM</span></div>
  <div style="display:flex;align-items:center;gap:18px;margin-top:30px"><span style="width:18px;height:18px;border-radius:50%;background:var(--brand);flex:none"></span><b style="font-size:44px;letter-spacing:-.02em">Your proposal was opened</b></div>
  <div style="margin-top:12px;margin-left:36px;font-size:30px;color:var(--grey)">A. Rivera · Backyard pool and spa</div>
</div>
<p class="sub" style="margin-top:48px">Call while it's fresh.</p>
{foot()}
""")


def main():
    os.makedirs(SRC, exist_ok=True)
    out = []
    for week, slug, doc in POSTS:
        name = f'wk{week:02d}-{slug}'
        if 'HOLD' in (ROW[week].get('Check before posting') or '').upper():
            name += '-HOLD'
        open(os.path.join(SRC, name + '.html'), 'w').write(doc)
        out.append({'week': week, 'file': name})
    json.dump(out, open(os.path.join(SRC, 'manifest.json'), 'w'), indent=1)
    print(len(out), 'pages')


if __name__ == '__main__':
    main()
