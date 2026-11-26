"""Writes social/posts/index.html: every built post with its week, date, caption and alt text,
laid out for reviewing on a phone. Run after build.py and render.mjs."""
import html
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
CAL = {int(float(r['Week'])): r for r in json.load(open(os.path.join(HERE, 'src/calendar.json')))}
MAN = json.load(open(os.path.join(HERE, 'src/manifest.json')))
e = html.escape

built = {}
for m in MAN:
    built.setdefault(m['week'], []).append(m['file'])


def para(text):
    return ''.join(f'<p>{e(line)}</p>' for line in text.split('\n') if line.strip())


cards = []
for week, files in built.items():
    r = CAL[week]
    date = r['Post date'][:10]
    imgs = ''.join(
        f'<figure><a href="{f}@2x.png"><img src="{f}.png" alt="{e(r["Alt text"])}" loading="lazy" width="1080" height="1350"></a>'
        f'<figcaption>{f}.png · <a href="{f}@2x.png">@2x</a></figcaption></figure>'
        for f in files
    )
    check = r['Check before posting'] if r['Check before posting'] not in ('', 'None') else 'Nothing extra.'
    cards.append(f"""<article id="wk{week:02d}">
  <header><span class="wk">Week {week}</span><span class="meta">{e(date)} · {e(r['Pillar'])} · {e(r['Format'])}</span></header>
  <div class="imgs{' many' if len(files) > 1 else ''}">{imgs}</div>
  <dl>
    <dt>Caption, line 1</dt><dd>{e(r['Caption opener (post as line 1)'])}</dd>
    <dt>Caption</dt><dd>{para(r['Caption'])}</dd>
    <dt>Alt text</dt><dd>{e(r['Alt text'])}</dd>
    <dt>Link</dt><dd><a href="{e(r['Link'])}">{e(r['Link'])}</a></dd>
    <dt>Supporting page</dt><dd><a href="..{e(r['Supporting page'])}">{e(r['Supporting page'])}</a></dd>
    <dt>Check before posting</dt><dd>{e(check)}</dd>
  </dl>
</article>""")

skipped = [w for w in sorted(CAL) if w not in built]
skip_rows = ''.join(f'<li><b>Week {w}</b> · {e(CAL[w]["Post date"][:10])} · {e(CAL[w]["Format"])}: {e(CAL[w]["On-image headline"])}</li>' for w in skipped)

doc = f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex, nofollow"><title>Social posts — ScrollBuilt</title>
<style>
@font-face{{font-family:Barlow;font-weight:400;src:url(../../assets/fonts/barlow-400.woff2) format("woff2")}}
@font-face{{font-family:Barlow;font-weight:600;src:url(../../assets/fonts/barlow-600.woff2) format("woff2")}}
@font-face{{font-family:"Barlow Condensed";font-weight:600;src:url(../../assets/fonts/barlow-condensed-600.woff2) format("woff2")}}
:root{{--ink:#121417;--paper:#fafaf8;--paper2:#f1f0ea;--brand:#ff5a1f;--tone:#6c6a63;--grey:#57534e;--rule:#deddd7}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font:400 16px/1.5 Barlow,system-ui,sans-serif}}
.wrap{{max-width:760px;margin:0 auto;padding:28px 16px 64px}}
h1{{font-weight:600;font-size:32px;line-height:1.08;letter-spacing:-.025em;margin:6px 0 8px}}h1 span{{color:var(--tone)}}
.label{{font:600 13px "Barlow Condensed";letter-spacing:.14em;text-transform:uppercase;color:var(--grey)}}
.intro{{color:var(--grey);margin:0 0 8px}}
nav{{display:flex;flex-wrap:wrap;gap:8px;margin:18px 0 8px}}nav a{{font:600 15px Barlow;border:1px solid var(--rule);border-radius:6px;padding:6px 10px;color:var(--ink);text-decoration:none;background:#fff}}
article{{background:#fff;border:1px solid var(--rule);border-radius:8px;margin-top:22px;overflow:hidden}}
article header{{display:flex;flex-wrap:wrap;gap:4px 12px;align-items:baseline;padding:14px 16px;border-bottom:1px solid var(--rule)}}
.wk{{font-weight:600;font-size:20px}}.meta{{color:var(--grey);font-size:14px}}
.imgs{{padding:14px 16px 4px}}.imgs.many{{display:flex;gap:12px;overflow-x:auto;scroll-snap-type:x mandatory}}
.imgs.many figure{{flex:0 0 82%;scroll-snap-align:start}}
figure{{margin:0 0 10px}}figure img{{width:100%;height:auto;display:block;border:1px solid var(--rule);border-radius:4px}}
figcaption{{font-size:13px;color:var(--grey);margin-top:4px}}figcaption a{{color:var(--grey)}}
dl{{margin:0;padding:4px 16px 16px}}dt{{font:600 12px "Barlow Condensed";letter-spacing:.14em;text-transform:uppercase;color:var(--grey);margin-top:12px}}
dd{{margin:2px 0 0}}dd p{{margin:0 0 6px}}dd a{{color:var(--ink);overflow-wrap:anywhere}}
.skipped{{margin-top:28px;background:var(--paper2);border-radius:8px;padding:16px}}.skipped ul{{margin:8px 0 0;padding-left:18px}}.skipped li{{margin:4px 0}}
</style></head><body><div class="wrap">
<div class="label">ScrollBuilt · social calendar</div>
<h1>52-week calendar. <span>Static and carousel posts.</span></h1>
<p class="intro">{len(MAN)} images across {len(built)} posts, 1080 × 1350. Tap an image for the @2x file. Swipe sideways through carousels.</p>
<nav>{''.join(f'<a href="#wk{w:02d}">Wk {w}</a>' for w in built)}</nav>
{''.join(cards)}
<section class="skipped"><div class="label">Not built: you're recording these</div><ul>{skip_rows}</ul></section>
</div></body></html>"""
open(os.path.join(HERE, 'posts/index.html'), 'w').write(doc)
print('contact sheet:', len(built), 'posts,', len(skipped), 'skipped')
