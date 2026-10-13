(function () {
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // nav state
  const build = $('.build');
  const onScroll = () => document.body.classList.toggle('scrolled', scrollY > (build ? build.offsetHeight - 90 : 30));
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  // reveal on scroll
  const io = new IntersectionObserver(es => es.forEach(x => { if (x.isIntersecting) { x.target.classList.add('v'); io.unobserve(x.target); } }), { threshold: .12, rootMargin: '0px 0px -40px 0px' });
  $$('.in').forEach(el => { const sib = [...el.parentElement.children].filter(c => c.classList.contains('in')); const i = sib.indexOf(el);
    if (sib.length > 2) el.style.transitionDelay = (i % 6) * 80 + 'ms'; io.observe(el); });

  // film grain
  (() => { const c = document.createElement('canvas'); c.width = c.height = 160; const g = c.getContext('2d'); const d = g.createImageData(160, 160);
    for (let i = 0; i < d.data.length; i += 4) { const v = Math.random() * 255; d.data[i] = d.data[i + 1] = d.data[i + 2] = v; d.data[i + 3] = 255; }
    g.putImageData(d, 0, 0); const el = document.createElement('div'); el.className = 'grain'; el.style.backgroundImage = `url(${c.toDataURL()})`; document.body.prepend(el); })();

  // ===== scroll-scrubbed AI build =====
  const cv = $('#scene');
  if (cv) {
    const ctx = cv.getContext('2d'), N = +cv.dataset.frames, SH = +cv.dataset.shots;
    const chapters = $$('.chapter'), num = $('#num'), ph = $('#phase'), bar = $('.bar'), hint = $('.hint');
    const phases = JSON.parse(cv.dataset.phases);
    let set = null, frames = [], W = 0, H = 0, dpr = 1, last = null;
    const pick = () => (innerHeight > innerWidth * 1.05 ? 'm' : 'd');
    function load() {
      const s = pick(); if (s === set) return; set = s; frames = new Array(N); last = null;
      const order = []; for (const step of [30, 10, 5, 2, 1]) for (let i = 0; i < N; i += step) if (!order.includes(i)) order.push(i);
      let q = 0; const next = () => { if (q >= order.length) return; const i = order[q++]; const im = new Image(); im.decoding = 'async';
        im.onload = () => { frames[i] = im; next(); }; im.onerror = next; im.src = `frames-${s}/f_${String(i + 1).padStart(4, '0')}.webp`; };
      for (let k = 0; k < 6; k++) next();
    }
    function size() { dpr = Math.min(devicePixelRatio || 1, 2); W = cv.clientWidth; H = cv.clientHeight; cv.width = W * dpr; cv.height = H * dpr; last = null; load(); }
    size(); addEventListener('resize', size);
    let target = 0, cur = 0;
    const read = () => { const r = build.getBoundingClientRect(); target = Math.min(1, Math.max(0, -r.top / (build.offsetHeight - innerHeight))); if (reduce) cur = target; };
    addEventListener('scroll', read, { passive: true }); read();
    function draw(p) {
      const i = Math.round(p * (N - 1)); let im = frames[i];
      for (let d = 1; !im && d < N; d++) im = frames[i - d] || frames[i + d];
      if (!im || im === last) return; last = im;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const s = Math.max(W / im.naturalWidth, H / im.naturalHeight), w = im.naturalWidth * s, h = im.naturalHeight * s;
      ctx.drawImage(im, (W - w) / 2, (H - h) / 2, w, h);
      const po = $('.stage .poster'); if (po) po.remove();
    }
    function ui(p) {
      const g = p * SH;
      chapters.forEach(c => { const a = +c.dataset.in, b = +c.dataset.out, f = .22;
        const o = Math.min(1, Math.max(0, (g - a) / f)) * Math.min(1, Math.max(0, (b - g) / f));
        c.style.opacity = o.toFixed(3); c.style.transform = `translateY(${((1 - o) * (g < a + f ? 26 : -26)).toFixed(1)}px)`; });
      let cp = phases[0]; phases.forEach(x => { if (g >= x[0]) cp = x; });
      num.textContent = cp[1]; ph.textContent = cp[2];
      bar.style.width = (p * 100).toFixed(2) + '%'; hint.style.opacity = p < .015 ? .85 : 0;
    }
    (function loop() { cur += (target - cur) * 0.1; if (Math.abs(target - cur) < 1e-4) cur = target;
      const r = build.getBoundingClientRect(); if (r.bottom > 0 && r.top < innerHeight) { draw(cur); ui(cur); } requestAnimationFrame(loop); })();
  }

  // ===== one-more-job calculator =====
  const job = $('#job'), extra = $('#extra');
  if (job) {
    const f = n => '$' + Math.round(n).toLocaleString();
    const upd = () => { const j = +job.value, e = +extra.value;
      $('#jobv').textContent = f(j); $('#extrav').textContent = e + (e === 1 ? ' job' : ' jobs');
      $('#rev').textContent = f(j * e); $('#rev5').textContent = f(j * e * 5); };
    job.oninput = extra.oninput = upd; upd();
  }

  // ===== contact form =====
  const form = $('#lead');
  if (form) {
    const qs = new URLSearchParams(location.search); if (qs.get('industry')) form.industry.value = qs.get('industry');
    form.addEventListener('submit', async e => {
      e.preventDefault(); const ok = $('.ok', form); ok.className = 'ok'; ok.textContent = 'Sending…';
      const data = Object.fromEntries(new FormData(form));
      try {
        const r = await fetch(form.action, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(data) });
        if (!r.ok) throw new Error(r.status);
        form.style.display = 'none'; $('.done').classList.add('show'); $('#done-market').textContent = data.market || 'your market';
        scrollTo({ top: 0, behavior: 'smooth' });
      } catch (err) { ok.className = 'ok bad'; ok.innerHTML = 'Something went wrong. Email us at <a href="mailto:hello@scrollbuilt.com" style="text-decoration:underline">hello@scrollbuilt.com</a>.'; }
    });
  }
})();
