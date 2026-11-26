"""Builds the static and carousel social posts for the 52-week calendar as HTML, ready to render to PNG.

Every word on a post is real HTML text. Images are frames from the sample build films in films/,
and every one carries a "Sample" tag. Phone screens are drawn in HTML/CSS with made-up names.
Run: python3 social/build.py   then   node social/render.mjs
"""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, 'src')
CAL = json.load(open(os.path.join(SRC, 'calendar.json')))
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


# ================================ Weeks 14 to 52 ================================================

def phone(inner, w=420, h=860, t='9:41'):
    return (f'<div class="phone" style="width:{w}px;height:{h}px"><div class="screen">{statusbar(t)}{inner}'
            f'</div></div>')


def photo(img, extra=''):
    return (f'<div style="position:absolute;inset:0;{extra}"><img src="img/{img}" alt="" style="width:100%;height:100%;'
            f'object-fit:cover;display:block"></div>')


def cta(title_a, title_b, sub='Free, no card, no call.', label='See it for yourself', dark=False, n=None, cur=None):
    bar = progress(n, cur) if n else ''
    return f"""{bar}
<div class="label" style="margin-top:40px">{label}</div>
<h1 style="margin-top:36px;font-size:132px">{title_a} <span class="t">{title_b}</span></h1>
<p class="sub" style="margin-top:40px">{sub}</p>
<div style="margin-top:64px"><span class="btn">Show me my site <span aria-hidden="true">→</span></span></div>
{foot(dark)}"""


def tag(text, kind):
    styles = {
        'new': 'background:var(--brand);color:var(--ink)',
        'ink': 'background:var(--ink);color:var(--paper)',
        'soft': 'background:var(--paper2);color:var(--grey);border:1px solid var(--rule)',
    }[kind]
    return (f'<span style="{styles};font:600 15px \'Barlow Condensed\';letter-spacing:.12em;text-transform:uppercase;'
            f'padding:5px 9px;border-radius:4px;white-space:nowrap">{text}</span>')


STAR = ('<svg viewBox="0 0 24 24" width="44" height="44" aria-hidden="true"><path d="M12 2.8l2.8 5.9 6.4.8-4.7 4.4 1.2 6.4L12 17.2'
        ' 6.3 20.3l1.2-6.4L2.8 9.5l6.4-.8z" fill="none" stroke="#ff5a1f" stroke-width="1.8" stroke-linejoin="round"/></svg>')

# ---- Week 14: asking AI, 4 slides ---------------------------------------------------------------
add(14, 'slide1', f"""{progress(4, 0)}
<div class="label" style="margin-top:40px">What homeowners type now</div>
<div style="margin-top:150px;display:flex;flex-direction:column;gap:28px">
  <div style="align-self:flex-end;max-width:760px;background:var(--ink);color:var(--paper);border-radius:28px 28px 6px 28px;padding:34px 40px;font-size:56px;line-height:1.15;font-weight:500;letter-spacing:-.01em">Who's the best landscaper near me?</div>
  <div style="align-self:flex-start;display:flex;gap:12px;background:#fff;border:1px solid var(--rule);border-radius:28px 28px 28px 6px;padding:30px 36px">
    <i style="width:16px;height:16px;border-radius:50%;background:var(--tone)"></i><i style="width:16px;height:16px;border-radius:50%;background:var(--tone);opacity:.6"></i><i style="width:16px;height:16px;border-radius:50%;background:var(--tone);opacity:.3"></i></div>
</div>
<p class="sub" style="margin-top:auto;margin-bottom:170px">Swipe.</p>
{foot()}
""")
add(14, 'slide2', f"""{progress(4, 1)}
<div class="label" style="margin-top:40px">It's already happening</div>
<h1 style="margin-top:36px;font-size:120px">Your customers are asking AI <span class="t">who to hire.</span></h1>
<p class="sub" style="margin-top:56px;color:var(--tone-d)">Nobody can promise an AI will recommend a business, and we won't.</p>
{foot(True)}
""", 'dark')
REPORT = """<div class="card" style="width:888px;padding:34px 38px;margin-top:56px">
  <div style="display:flex;justify-content:space-between;align-items:baseline"><b style="font-size:34px;letter-spacing:-.02em">Monthly visibility report</b><span class="label" style="font-size:17px">Sample</span></div>
  <div style="border-top:2px solid var(--ink);margin-top:18px"></div>
  <div style="display:flex;justify-content:space-between;gap:16px;padding:18px 0;border-bottom:1px solid var(--rule);font-size:25px"><span>Business name, services and towns are clear</span><span style="color:var(--grey)">Checked</span></div>
  <div style="display:flex;justify-content:space-between;gap:16px;padding:18px 0;border-bottom:1px solid var(--rule);font-size:25px"><span>Questions tested this month</span><span class="mono" style="font-size:22px;color:var(--grey)">12</span></div>
  <div style="display:flex;justify-content:space-between;gap:16px;padding:18px 0;border-bottom:1px solid var(--rule);font-size:25px"><span>How you showed up in the answers</span><span style="color:var(--grey)">Listed</span></div>
  <div style="padding:18px 0 0;font-size:25px;border-left:6px solid var(--brand);padding-left:18px;margin-top:18px"><b>Fix next:</b> add your license number to the About page.</div>
</div>"""
add(14, 'slide3', f"""{progress(4, 2)}
<div class="label" style="margin-top:40px">What you get</div>
<h1 style="margin-top:36px;font-size:84px">A site that's easy to understand, <span class="t">and a report each month.</span></h1>
{REPORT}
{foot()}
""")
add(14, 'slide4', cta('See your site', 'in 30 seconds.', dark=True, n=4, cur=3), 'dark')

# ---- Week 16: review request --------------------------------------------------------------------
REVIEW_SCREEN = f"""<div class="app-h"><b>Ask for a review</b><span>J. Moore</span></div>
  <div style="padding:22px 26px">
    <div style="font-size:21px;color:var(--grey)">Patio and lighting · finished this week</div>
    <div style="display:flex;gap:6px;margin-top:22px">{STAR*5}</div>
    <div class="msg out" style="margin:22px 0 0">Thanks for choosing us, J. Moore. Would you share a quick review of your new patio? It helps neighbors find us.</div>
    <div style="margin-top:24px;background:var(--brand);color:var(--ink);font:600 24px Barlow;text-align:center;padding:18px;border-radius:6px">Send review request</div>
  </div>"""
add(16, 'static', f"""
<div class="label">Review requests</div>
<h1 style="margin-top:36px;font-size:100px">Ask for the review <span class="t">while the job is fresh.</span></h1>
<div style="position:relative;margin-top:56px;height:640px;border-radius:8px;overflow:hidden">
  {photo('landscape-coastal.webp', 'object-position:center')}<span class="sample" style="top:auto;bottom:18px">Sample</span>
</div>
<div style="position:absolute;right:120px;bottom:150px">{phone(REVIEW_SCREEN, 380, 700)}</div>
{foot()}
""")

# ---- Week 18: 53% -------------------------------------------------------------------------------
add(18, 'static', f"""
<div class="mono" style="font-size:230px;line-height:1;color:var(--brand);letter-spacing:-.03em">53%</div>
<h1 style="margin-top:28px;font-size:84px">of mobile visits end <span class="t">if a page takes over 3 seconds.</span></h1>
<div style="margin-top:72px;display:grid;gap:30px">
  <div><div style="display:flex;justify-content:space-between;font-size:26px;color:var(--grey)"><span>A slow page</span><span class="mono" style="font-size:24px">3s+</span></div>
    <div style="height:28px;background:var(--rule);border-radius:4px;margin-top:10px;overflow:hidden"><div style="width:38%;height:100%;background:var(--tone)"></div></div></div>
  <div><div style="display:flex;justify-content:space-between;font-size:26px"><span><b>ScrollBuilt sites</b> · Lighthouse performance</span><span class="mono" style="font-size:24px">97–100</span></div>
    <div style="height:28px;background:var(--ink);border-radius:4px;margin-top:10px"></div></div>
</div>
{foot(False, 'Source: Google, 2016.')}
""")

# ---- Week 20: website chat ----------------------------------------------------------------------
CHAT = """<div class="app-h"><b>Your Name Pools</b><span>Chat</span></div>
  <div class="msg in" style="margin-left:90px;background:var(--ink);color:var(--paper)">Do you work in my area?</div>
  <div class="msg out" style="margin-right:60px"><span class="k">Answer from your site</span>Yes. We build in Your City and the towns around it, including Northside and Lakeview. Share your ZIP code and we'll confirm.</div>
  <div class="msg in" style="margin-left:90px;background:var(--ink);color:var(--paper)">Great, it's 00000.</div>
  <div style="position:absolute;left:0;right:0;bottom:0;padding:18px 22px;border-top:1px solid var(--rule);background:#fff;font-size:19px;color:var(--grey)">You get the conversation by email.</div>"""
add(20, 'static', f"""
<div style="display:grid;grid-template-columns:1fr 420px;gap:56px;height:100%">
  <div>
    <div class="label">Website chat</div>
    <h1 style="margin-top:36px;font-size:96px">Your website answers questions <span class="t">while you work.</span></h1>
    <p class="sub" style="margin-top:36px">From your own pages: where you work, what you build, how to start.</p>
  </div>
  <div style="margin-top:20px">{phone(CHAT)}</div>
</div>
{foot()}
""")

# ---- Week 22: job site, phone on a tailgate (Gemini background) ---------------------------------
NOTIFY = """<div style="padding:16px 18px">
  <div style="background:rgba(255,255,255,.96);border-radius:22px;padding:20px 22px;box-shadow:0 10px 30px rgba(0,0,0,.18)">
    <div style="display:flex;justify-content:space-between;font:600 15px 'Barlow Condensed';letter-spacing:.12em;text-transform:uppercase;color:var(--grey)"><span>New lead · website form</span><span class="mono" style="letter-spacing:0">now</span></div>
    <div style="font-size:24px;font-weight:600;margin-top:8px">A. Rivera · Backyard patio</div>
    <div style="font-size:19px;color:var(--grey);margin-top:4px">Reply sent automatically.</div>
  </div></div>"""
add(22, 'static', f"""
{photo('wk22-tailgate.jpg')}
<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(18,20,23,.82) 0%,rgba(18,20,23,.35) 42%,rgba(18,20,23,0) 62%,rgba(18,20,23,.55) 100%)"></div>
<span class="sample" style="top:auto;bottom:170px;left:96px">Sample</span>
<div style="position:relative">
  <div class="label" style="color:#e6e3dc">Form leads, answered</div>
  <h1 style="margin-top:36px;font-size:116px;color:var(--paper)">On a job site. <span class="t" style="color:#d3d0c8">Not at a desk.</span></h1>
</div>
<div style="position:absolute;right:120px;bottom:190px;transform:rotate(4deg)">
  <div class="phone" style="width:340px;height:690px;background:#0b0c0e"><div class="screen" style="background:linear-gradient(160deg,#3a4250,#1b1f26)">
    <div class="statusbar" style="color:#fff"><span>4:52</span><span class="batt"></span></div>{NOTIFY}</div></div>
</div>
{foot(True)}
""", 'dark')

# ---- Week 24: the quote you forgot, 3 slides ----------------------------------------------------
add(24, 'slide1', f"""{progress(3, 0)}
<div style="margin:170px auto 0;width:780px;background:#fff8df;border:1px solid #ece3c2;border-radius:6px;padding:70px 64px;transform:rotate(-2.5deg);box-shadow:0 24px 50px rgba(18,20,23,.12)">
  <div class="label" style="color:#8a7a4a">Note to self</div>
  <h1 style="margin-top:26px;font-size:100px">The quote you forgot <span class="t">to follow up on.</span></h1>
</div>
{foot()}
""")
REMIND = f"""<div class="card" style="width:888px;padding:30px 36px;margin-top:56px">
  <div style="display:flex;justify-content:space-between;align-items:baseline"><b style="font-size:34px;letter-spacing:-.02em">Follow up today</b><span class="label" style="font-size:17px">3 people</span></div>
  <div style="display:grid;grid-template-columns:1fr auto;gap:6px 16px;padding:20px 0;border-top:1px solid var(--rule);margin-top:18px">
    <b style="font-size:27px">A. Rivera</b>{tag('Call', 'new')}<span style="font-size:22px;color:var(--grey)">Proposal sent 5 days ago</span></div>
  <div style="display:grid;grid-template-columns:1fr auto;gap:6px 16px;padding:20px 0;border-top:1px solid var(--rule)">
    <b style="font-size:27px">J. Moore</b>{tag('Text', 'ink')}<span style="font-size:22px;color:var(--grey)">Asked for a price last week</span></div>
  <div style="display:grid;grid-template-columns:1fr auto;gap:6px 16px;padding:20px 0 0;border-top:1px solid var(--rule)">
    <b style="font-size:27px">K. Patel</b>{tag('Send proposal', 'soft')}<span style="font-size:22px;color:var(--grey)">Site visit done Tuesday</span></div>
</div>"""
add(24, 'slide2', f"""{progress(3, 1)}
<div class="label" style="margin-top:40px">Reminders</div>
<h1 style="margin-top:36px;font-size:96px">Who to call back, <span class="t">and when.</span></h1>
{REMIND}
{foot()}
""")
add(24, 'slide3', cta('See your site', 'in 30 seconds.', dark=True, n=3, cur=2), 'dark')

# ---- Week 26: one more job ----------------------------------------------------------------------
add(26, 'static', f"""
<div class="label">Run your own numbers</div>
<h1 style="margin-top:36px;font-size:120px">One more job <span class="t">pays for it.</span></h1>
<div class="card" style="margin-top:72px;padding:44px 48px">
  <div style="display:flex;justify-content:space-between;align-items:baseline;gap:20px;padding-bottom:28px;border-bottom:1px solid var(--rule)">
    <span style="font-size:32px">Your average job</span><span class="mono" style="font-size:72px;color:var(--brand);letter-spacing:-.02em">$65,000</span></div>
  <div style="display:flex;justify-content:space-between;align-items:baseline;gap:20px;padding-top:28px">
    <span style="font-size:32px">ScrollBuilt for a year<br><span style="font-size:24px;color:var(--grey)">$249 a month, billed yearly</span></span><span class="mono" style="font-size:72px;letter-spacing:-.02em">$2,988</span></div>
</div>
{foot(False, 'Illustration only. Your results depend on your market, pricing and close rate.')}
""")

# ---- Week 28: voice note in the truck (Gemini background) ---------------------------------------
WAVE = ''.join(f'<i style="width:6px;border-radius:3px;background:var(--brand);height:{h}px"></i>'
               for h in (14, 28, 44, 20, 60, 36, 72, 48, 26, 64, 40, 18, 52, 30, 68, 22, 46, 34, 58, 16, 38, 24))
VOICE = f"""<div class="app-h"><b>A. Rivera</b><span>Voice note</span></div>
  <div style="padding:20px 26px">
    <div style="display:flex;align-items:center;gap:5px;height:80px">{WAVE}</div>
    <div class="mono" style="font-size:18px;color:var(--grey);margin-top:6px">1:12 · recorded on the drive home</div>
    <div class="msg out" style="margin:20px 0 0"><span class="k">Written up</span><b>Wants:</b> a pool with a spa and a sun shelf.<br><b>Budget:</b> around $80,000.<br><b>Next:</b> send a proposal by Friday.</div>
  </div>"""
add(28, 'static', f"""
{photo('wk28-cupholder.jpg')}
<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(18,20,23,.85) 0%,rgba(18,20,23,.4) 40%,rgba(18,20,23,.15) 70%,rgba(18,20,23,.6) 100%)"></div>
<span class="sample" style="top:auto;bottom:170px;left:96px">Sample</span>
<div style="position:relative">
  <div class="label" style="color:#e6e3dc">Voice notes</div>
  <h1 style="margin-top:36px;font-size:108px;color:var(--paper)">Talk after the site visit. <span class="t" style="color:#d3d0c8">Get it in writing.</span></h1>
</div>
<div style="position:absolute;right:120px;bottom:170px">{phone(VOICE, 380, 700, '5:48')}</div>
{foot(True)}
""", 'dark')

# ---- Week 30: 46.1% -----------------------------------------------------------------------------
add(30, 'static', f"""
<div class="mono" style="font-size:230px;line-height:1;color:var(--brand);letter-spacing:-.03em">46.1%</div>
<h1 style="margin-top:36px;font-size:104px">Nearly half judge you <span class="t">by your website's design.</span></h1>
{foot(False, 'Source: Stanford Web Credibility Project, B.J. Fogg.')}
""")

# ---- Week 32: every lead in one place -----------------------------------------------------------
def lead(name, what, when, t, kind):
    return (f'<div class="row" style="grid-template-columns:1fr auto"><div><div class="n">{name}</div><div class="m">{what}</div>'
            f'<div class="tm">{when}</div></div><div style="margin-top:4px">{tag(t, kind)}</div></div>')


INBOX3 = ('<div class="app-h"><b>Leads</b><span>This week</span></div>'
          + lead('A. Rivera', 'Website form · Backyard pool', 'Today 9:02 PM', 'New', 'new')
          + lead('J. Moore', 'Chat · Patio and lighting', 'Wed', 'Proposal sent', 'ink')
          + lead('K. Patel', 'Website form · Pool remodel', 'Mon', 'Won', 'soft'))
add(32, 'static', f"""
<div style="display:grid;grid-template-columns:1fr 420px;gap:56px;height:100%">
  <div>
    <div class="label">One inbox</div>
    <h1 style="margin-top:36px;font-size:112px">Every lead <span class="t">in one place.</span></h1>
    <p class="sub" style="margin-top:36px">Form leads, chat and proposals, on your phone.</p>
  </div>
  <div style="margin-top:20px">{phone(INBOX3)}</div>
</div>
{foot()}
""")

# ---- Week 34: no time to mess with a website -----------------------------------------------------
EDITOR = """<div class="app-h"><b>Your site</b><span>Ask for a change</span></div>
  <div class="msg in" style="margin-left:70px;background:var(--ink);color:var(--paper)">Change our hours to 7 to 5 on weekdays.</div>
  <div class="msg out"><span class="k">Preview</span><b>Hours</b><br>Monday to Friday, 7 a.m. to 5 p.m.</div>
  <div style="margin:20px 26px 0;display:flex;gap:12px"><span style="flex:1;background:var(--brand);color:var(--ink);font:600 22px Barlow;text-align:center;padding:16px;border-radius:6px">Approve</span><span style="flex:1;border:1px solid var(--rule);font:600 22px Barlow;text-align:center;padding:16px;border-radius:6px">Change it</span></div>"""
add(34, 'static', f"""
<div style="display:grid;grid-template-columns:1fr 400px;gap:56px;height:100%">
  <div>
    <div class="label">Made for you</div>
    <h1 style="margin-top:36px;font-size:104px">No time to mess with a website? <span class="t">Good.</span></h1>
    <p class="sub" style="margin-top:36px">Ask in plain words. One change a month is made by a person.</p>
  </div>
  <div style="margin-top:60px">{phone(EDITOR, 400, 820)}</div>
</div>
{foot(True)}
""", 'dark')

# ---- Week 35: price -----------------------------------------------------------------------------
add(35, 'static', f"""
<div class="label">One plan · no setup fee</div>
<h1 style="margin-top:36px;font-size:120px">From $249 <span class="t">a month.</span></h1>
<div class="card" style="margin-top:80px;padding:52px 56px">
  <div style="display:flex;align-items:baseline;gap:22px;flex-wrap:nowrap"><span class="mono" style="font-size:150px;line-height:1;color:var(--brand);letter-spacing:-.03em">$249</span><span style="font-size:40px;font-weight:600;white-space:nowrap">a month, billed yearly</span></div>
  <div style="margin-top:30px;padding-top:28px;border-top:1px solid var(--rule);font-size:32px;color:var(--grey)">Or $299 month to month. You only pay when your site goes live.</div>
</div>
{foot()}
""")

# ---- Week 36: your content is yours -------------------------------------------------------------
DL = ('<div style="position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);z-index:4;width:128px;height:128px;border-radius:50%;'
      'background:var(--brand);display:grid;place-items:center;box-shadow:0 16px 36px rgba(18,20,23,.35)">'
      '<svg viewBox="0 0 24 24" width="64" height="64" aria-hidden="true"><path d="M12 4v11M7 10.5l5 5 5-5M5 19.5h14" fill="none" stroke="#121417" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg></div>')
add(36, 'static', f"""
<div style="display:grid;grid-template-columns:1fr 400px;gap:56px;height:100%">
  <div>
    <div class="label">No lock-in</div>
    <h1 style="margin-top:36px;font-size:112px">Your content is yours. <span class="t">Always.</span></h1>
    <p class="sub" style="margin-top:36px">Text, photos and leads download any time. The full site goes with you from day one on the annual plan, or after three paid months.</p>
  </div>
  <div style="margin-top:60px;position:relative">{film_phone('pool-finished.webp', w=400, h=820)}{DL}</div>
</div>
{foot()}
""")

# ---- Week 38: get found for, 3 slides -----------------------------------------------------------
add(38, 'slide1', f"""{progress(3, 0)}
<div class="label" style="margin-top:40px">Get found for</div>
<h1 style="margin-top:36px;font-size:132px">Get found for <span class="t">the jobs you want.</span></h1>
<p class="sub" style="margin-top:auto;margin-bottom:170px">Swipe to see a plan.</p>
{foot()}
""")
PLAN = f"""<div class="card" style="width:888px;padding:30px 36px;margin-top:48px">
  <div style="font:600 18px 'Barlow Condensed';letter-spacing:.12em;text-transform:uppercase;color:var(--grey)">Work you want more of</div>
  <div style="font-size:30px;font-weight:600;margin-top:8px">Pool remodels and spas</div>
  <div style="font:600 18px 'Barlow Condensed';letter-spacing:.12em;text-transform:uppercase;color:var(--grey);margin-top:28px">Your plan</div>
  <div style="display:grid;grid-template-columns:1fr auto;gap:16px;padding:18px 0;border-bottom:1px solid var(--rule);font-size:25px"><span>New page: Pool remodeling in Your City</span>{tag('New', 'new')}</div>
  <div style="display:grid;grid-template-columns:1fr auto;gap:16px;padding:18px 0;border-bottom:1px solid var(--rule);font-size:25px"><span>Home page title mentions spas</span>{tag('Update', 'soft')}</div>
  <div style="display:grid;grid-template-columns:1fr auto;gap:16px;padding:18px 0;font-size:25px"><span>FAQ: How long does a remodel take?</span>{tag('Add', 'soft')}</div>
  <div style="margin-top:14px;display:inline-block;background:var(--brand);color:var(--ink);font:600 24px Barlow;padding:16px 26px;border-radius:6px">Apply the plan</div>
</div>"""
add(38, 'slide2', f"""{progress(3, 1)}
<div class="label" style="margin-top:40px">Your "Get found for" plan</div>
<h1 style="margin-top:36px;font-size:84px">Tell us the work you want. <span class="t">We make the changes.</span></h1>
{PLAN}
{foot(False, "Nobody can promise rankings, and we won't.")}
""")
add(38, 'slide3', cta('See your site', 'in 30 seconds.', dark=True, n=3, cur=2), 'dark')

# ---- Week 39: three steps, 4 slides --------------------------------------------------------------
STEPS = [
    ('01', 'Type your business name,', 'trade and city.'),
    ('02', 'Watch your', 'draft load.'),
    ('03', 'Like it? Go live.', "Don't? Walk away."),
]
for i, (n, a, b) in enumerate(STEPS):
    add(39, f'slide{i + 1}', f"""{progress(4, i)}
<div class="label" style="margin-top:40px">Three steps. About 30 seconds.</div>
<div class="mono" style="margin-top:110px;font-size:280px;line-height:.9;color:var(--brand);letter-spacing:-.04em">{n}</div>
<h1 style="margin-top:56px;font-size:112px">{a} <span class="t">{b}</span></h1>
{foot()}
""")
add(39, 'slide4', cta('Three steps.', 'About 30 seconds.', label='Free · no card · no call', sub='See yours now.', dark=True, n=4, cur=3), 'dark')

# ---- Week 40: know how you show up -------------------------------------------------------------
REP = """<div class="app-h"><b>Your report</b><span>This month</span></div>
  <div class="row" style="grid-template-columns:1fr auto"><div class="n" style="font-weight:500">Business details are clear</div><div class="tm" style="margin-top:2px">Checked</div></div>
  <div class="row" style="grid-template-columns:1fr auto"><div class="n" style="font-weight:500">Questions tested</div><div class="tm" style="margin-top:2px">12</div></div>
  <div class="row" style="grid-template-columns:1fr auto;border-left:6px solid var(--brand);background:var(--paper2)"><div class="n">Named for “pool builder near me”</div><div class="tm" style="margin-top:2px">Listed</div></div>
  <div class="row" style="grid-template-columns:1fr auto"><div class="n" style="font-weight:500">Service towns found</div><div class="tm" style="margin-top:2px">6</div></div>
  <div class="msg out"><span class="k">Fix next</span>Add your license number to the About page.</div>"""
add(40, 'static', f"""
<div style="display:grid;grid-template-columns:1fr 420px;gap:56px;height:100%">
  <div>
    <div class="label">Monthly report</div>
    <h1 style="margin-top:36px;font-size:112px">Know how <span class="t">you show up.</span></h1>
    <p class="sub" style="margin-top:36px">A short report each month, in plain words. Sample shown.</p>
  </div>
  <div style="margin-top:20px">{phone(REP)}</div>
</div>
{foot()}
""")

# ---- Week 42: busy season ends ------------------------------------------------------------------
add(42, 'static', f"""
{photo('pool-night.webp', 'object-position:center 60%')}
<div style="position:absolute;inset:0;background:linear-gradient(180deg,rgba(18,20,23,.88) 0%,rgba(18,20,23,.45) 38%,rgba(18,20,23,0) 60%,rgba(18,20,23,.55) 100%)"></div>
<span class="sample" style="top:auto;bottom:170px;left:96px">Sample</span>
<div style="position:relative">
  <div class="label" style="color:#e6e3dc">After the rush</div>
  <h1 style="margin-top:36px;font-size:112px;color:var(--paper)">Busy season ends. <span class="t" style="color:#d3d0c8">Your website keeps working.</span></h1>
</div>
{foot(True)}
""", 'dark')

# ---- Week 43: your ZIP codes, protected ---------------------------------------------------------
ZIPS = [('M60 70 L250 40 L300 190 L120 230 Z', 'ZIP 1', 170, 140), ('M300 190 L250 40 L460 60 L470 210 Z', 'ZIP 2', 370, 135),
        ('M120 230 L300 190 L330 360 L90 380 Z', 'ZIP 3', 210, 300), ('M300 190 L470 210 L500 370 L330 360 Z', 'ZIP 4', 405, 290),
        ('M470 210 L460 60 L640 90 L660 260 L500 370 Z', 'ZIP 5', 560, 200)]
ROADS = ''.join(f'<path d="{d}" stroke="#deddd7" stroke-width="{w}" fill="none"/>' for d, w in (
    ('M0 120 C200 100 500 160 888 130', 10), ('M0 300 C250 330 600 280 888 320', 8), ('M200 0 C230 200 180 300 220 470', 8),
    ('M620 0 C600 160 680 300 640 470', 10), ('M0 420 L888 380', 5), ('M420 0 L400 470', 5), ('M760 0 L790 470', 5)))
MAP = (f'<svg viewBox="-110 0 888 470" width="888" height="470" aria-hidden="true"><rect x="-110" width="888" height="470" fill="#fff"/><g transform="translate(-110 0)">{ROADS}</g>'
       + ''.join(f'<path d="{d}" fill="rgba(255,90,31,.07)" stroke="#ff5a1f" stroke-width="4" stroke-linejoin="round"/>'
                 f'<text x="{x}" y="{y}" text-anchor="middle" font-family="IBM Plex Mono" font-weight="500" font-size="24" fill="#121417">{t}</text>'
                 for d, t, x, y in ZIPS) + '</svg>')
add(43, 'static', f"""
<div class="label">Annual plan</div>
<h1 style="margin-top:36px;font-size:120px">Your ZIP codes, <span class="t">protected.</span></h1>
<div class="card" style="margin-top:56px;overflow:hidden;padding:0;line-height:0">{MAP}</div>
{foot(False, "On the annual plan your territory is protected: we won't build a site for another company in your trade located in your ZIP codes (up to five) for that year.")}
""")

# ---- Week 48: first click to signed job, 5 slides, one timeline ---------------------------------
def timeline(cur, n=5):
    # The same line on every slide, at the same height, so it reads as one line when swiped.
    dots = ''.join(f'<span style="position:absolute;top:-9px;left:{(i + .5) / n * 100:.1f}%;width:22px;height:22px;margin-left:-11px;'
                   f'border-radius:50%;background:{"var(--brand)" if i <= cur else "var(--paper)"};border:3px solid var(--brand)"></span>'
                   for i in range(n))
    return f'<div style="position:absolute;left:0;right:0;top:640px;height:4px;background:var(--brand)">{dots}</div>'


FLOW = [
    ('A form comes in.', 'A reply goes out in seconds.', inbox_phone),
    ('A reminder', 'tells you to call.', None),
    ('The proposal', 'gets opened.', None),
    ('The review request goes out', "when you're done.", None),
]
add(48, 'slide1', f"""{progress(5, 0)}{timeline(0)}
<div class="label" style="margin-top:40px">How a job moves</div>
<h1 style="margin-top:56px;font-size:132px">From first click <span class="t">to signed job.</span></h1>
{foot()}
""")
add(48, 'slide2', f"""{progress(5, 1)}{timeline(1)}
<div class="label" style="margin-top:40px">Step 1</div>
<h1 style="margin-top:56px;font-size:84px">A form comes in. <span class="t">A reply goes out in seconds.</span></h1>
<div style="position:absolute;left:96px;top:720px">{ANSWERED.replace('background:#1c1f23;border:1px solid #33373d', 'background:#fff;border:1px solid var(--rule)').replace('color:var(--paper)">', 'color:var(--ink)">').replace('border-top:1px solid #33373d', 'border-top:1px solid var(--rule)').replace('color:var(--tone-d)', 'color:var(--grey)').replace('background:var(--paper);color:var(--ink)', 'background:var(--paper2);color:var(--ink)')}</div>
{foot()}
""")
add(48, 'slide3', f"""{progress(5, 2)}{timeline(2)}
<div class="label" style="margin-top:40px">Step 2</div>
<h1 style="margin-top:56px;font-size:96px">A reminder <span class="t">tells you to call.</span></h1>
<div class="card" style="position:absolute;left:96px;right:96px;top:720px;padding:34px 38px;display:grid;grid-template-columns:1fr auto;gap:8px 16px;align-items:center">
  <b style="font-size:30px">Call A. Rivera</b>{tag('Today', 'new')}<span style="font-size:24px;color:var(--grey)">Asked about a backyard pool on Tuesday</span></div>
{foot()}
""")
add(48, 'slide4', f"""{progress(5, 3)}{timeline(3)}
<div class="label" style="margin-top:40px">Step 3</div>
<h1 style="margin-top:56px;font-size:96px">The proposal <span class="t">gets opened.</span></h1>
<div class="card" style="position:absolute;left:96px;right:96px;top:720px;padding:34px 38px">
  <div style="display:flex;align-items:center;gap:16px;font-size:32px;font-weight:600"><span style="width:16px;height:16px;border-radius:50%;background:var(--brand)"></span>Your proposal was opened</div>
  <div style="margin-top:8px;margin-left:32px;font-size:24px;color:var(--grey)">A. Rivera · Backyard pool and spa · <span class="mono" style="font-size:22px">7:42 PM</span></div></div>
{foot()}
""")
add(48, 'slide5', f"""{progress(5, 4)}{timeline(4)}
<div class="label" style="margin-top:40px">Step 4</div>
<h1 style="margin-top:56px;font-size:84px">The review request goes out <span class="t">when you're done.</span></h1>
<div style="position:absolute;left:96px;top:740px"><span class="btn">See your site in 30 seconds <span aria-hidden="true">→</span></span></div>
<p class="sub" style="position:absolute;left:96px;top:860px">Free, no card, no call.</p>
{foot()}
""")

# ---- Week 49: pick your film, 5 slides -----------------------------------------------------------
BTN = '<div style="margin-top:56px"><span class="btn" style="white-space:nowrap;font-size:34px;padding:26px 34px">Show me my site <span aria-hidden="true">→</span></span></div>'
FILMS = [('pool-finished.webp', 'Pool'), ('landscape-finished.webp', 'Patio'), ('landscape-coastal.webp', 'Front yard'), ('pool-night.webp', 'Night pool')]


def thumb(img, name, w, h):
    return (f'<div style="position:relative;width:{w}px;height:{h}px;border-radius:8px;overflow:hidden">'
            f'<img src="img/{img}" alt="" style="width:100%;height:100%;object-fit:cover;display:block">'
            f'<span class="sample">Sample</span><span style="position:absolute;left:16px;bottom:14px;color:var(--paper);'
            f'font:600 26px Barlow;text-shadow:0 2px 12px rgba(0,0,0,.6)">{name}</span></div>')


add(49, 'slide1', f"""{progress(5, 0)}
<div class="label" style="margin-top:40px">Build films</div>
<h1 style="margin-top:28px;font-size:92px">Pick your film. <span class="t">Switch any time.</span></h1>
<div style="display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:44px">{''.join(thumb(i, n, 434, 380) for i, n in FILMS)}</div>
{foot()}
""")
for k, (img, name) in enumerate(FILMS):
    last = k == len(FILMS) - 1
    add(49, f'slide{k + 2}', f"""{progress(5, k + 1)}
<div class="label" style="margin-top:40px">{name}</div>
<div style="display:grid;grid-template-columns:1fr 400px;gap:56px;margin-top:36px">
  <div><h1 style="font-size:{96 if last else 104}px">{'Matched to your trade' if not last else 'See yours'} <span class="t">{'and region.' if not last else 'in 30 seconds.'}</span></h1>
  {BTN if last else ''}</div>
  <div>{film_phone(img, 'Your Name ' + ('Pools' if 'pool' in img else 'Landscapes'), ('Pools' if 'pool' in img else 'Landscaping') + ' · Your city', w=400, h=820)}</div>
</div>
{foot()}
""")

# ---- Week 50: slow season -----------------------------------------------------------------------
BUILDING = """<div style="padding:40px 28px">
  <div class="label" style="font-size:16px;color:var(--brand)">Building</div>
  <div style="font-size:30px;font-weight:600;margin-top:6px;letter-spacing:-.02em">Your Name Landscapes</div>
  <div style="margin-top:34px;display:grid;gap:22px;font-size:22px">
    <div style="display:flex;gap:14px;align-items:center"><span style="width:30px;height:30px;border-radius:50%;background:#1f7a4d;color:#fff;display:grid;place-items:center;font-size:17px">✓</span>Choosing your design</div>
    <div style="display:flex;gap:14px;align-items:center"><span style="width:30px;height:30px;border-radius:50%;background:#1f7a4d;color:#fff;display:grid;place-items:center;font-size:17px">✓</span>Adding your name, city and phone</div>
    <div style="display:flex;gap:14px;align-items:center"><span style="width:30px;height:30px;border-radius:50%;border:3px solid var(--brand)"></span><b>Laying out your pages</b></div>
  </div></div>"""
add(50, 'static', f"""
<div style="display:grid;grid-template-columns:1fr 400px;gap:56px;height:100%">
  <div>
    <div class="label">Free · no card · no call</div>
    <h1 style="margin-top:36px;font-size:104px">Slow season is when <span class="t">you fix the website.</span></h1>
    <p class="sub" style="margin-top:36px">Spend 30 seconds of it seeing what yours could look like.</p>
  </div>
  <div style="margin-top:60px">{phone(BUILDING, 400, 820)}</div>
</div>
{foot(True)}
""", 'dark')

# ---- Week 51: missed call (HOLD) ----------------------------------------------------------------
MISSED = """<div class="app-h"><b>Your Name Pools</b><span>Calls</span></div>
  <div class="row" style="grid-template-columns:1fr auto"><div><div class="n" style="color:#b42318">Missed call</div><div class="m mono" style="font-size:18px">(555) 010-0142</div></div><div class="tm">2:14 PM</div></div>
  <div class="msg out" style="margin-left:70px"><span class="k">Text sent automatically · <span class="mono">2:14 PM</span></span>Sorry we missed your call. This is Your Name Pools. What can we help you with?</div>
  <div class="msg in" style="margin-right:70px">Hi, looking for a quote on a backyard pool.</div>"""
add(51, 'static', f"""
<div style="display:grid;grid-template-columns:1fr 420px;gap:56px;height:100%">
  <div>
    <div class="label">Missed-call text-back</div>
    <h1 style="margin-top:36px;font-size:104px">Missed the call? <span class="t">They get a text.</span></h1>
    <p class="sub" style="margin-top:36px">From your business number, right away.</p>
  </div>
  <div style="margin-top:20px">{phone(MISSED)}</div>
</div>
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
