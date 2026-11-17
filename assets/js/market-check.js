// Instant market check against the ScrollBuilt platform API (GET /public/metros, /public/markets/check).
// Progressive enhancement: if the API can't be reached, nothing changes and the form still emails the team.
(() => {
  const form = document.getElementById('lead');
  const api = document.querySelector('meta[name="sb-api"]')?.content?.replace(/\/$/, '');
  if (!form || !api) return;

  const TRADE = {
    'Pools & spas': 'pools',
    'Custom homes': 'custom-homes',
    'Landscaping & outdoor living': 'outdoor-living',
    'Decks, patios & pergolas': 'outdoor-living',
    Remodeling: 'remodel',
    'Roofing & solar': 'roofing',
    'ADUs & casitas': 'adu',
  };
  const input = form.market;
  const button = form.querySelector('button[type="submit"]');
  const buttonText = button.textContent;

  const list = document.createElement('datalist');
  list.id = 'sb-metros';
  form.append(list);
  input.setAttribute('list', 'sb-metros');

  const out = document.createElement('div');
  out.className = 'mc';
  out.setAttribute('role', 'status');
  out.setAttribute('aria-live', 'polite');
  input.closest('label').after(out);

  const hidden = (name) => {
    const el = document.createElement('input');
    el.type = 'hidden';
    el.name = name;
    form.append(el);
    return el;
  };
  const statusField = hidden('market_status');
  const metroField = hidden('metro');

  const get = async (path) => {
    const ctl = new AbortController();
    const t = setTimeout(() => ctl.abort(), 4000);
    try {
      const r = await fetch(api + path, { signal: ctl.signal });
      return r.ok ? await r.json() : null;
    } catch {
      return null;
    } finally {
      clearTimeout(t);
    }
  };

  let metros = [];
  let current = null; // { status, trade, metro }
  let seq = 0;

  const show = (status, message) => {
    out.className = status ? `mc show ${status}` : 'mc';
    out.textContent = message || '';
  };

  const pickMetro = () => {
    const v = input.value.trim().toLowerCase();
    if (!v) return null;
    return (
      metros.find((m) => m.name.toLowerCase() === v) ||
      (metros.length === 1 ? metros[0] : null) ||
      metros.find((m) => m.name.toLowerCase().includes(v)) ||
      null
    );
  };

  async function update() {
    const mine = ++seq;
    const q = input.value.split(',')[0].trim();
    if (q.length >= 2) {
      const r = await get(`/public/metros?q=${encodeURIComponent(q)}`);
      if (mine !== seq) return;
      if (r) {
        metros = r.metros;
        list.replaceChildren(
          ...metros.map((m) => {
            const o = document.createElement('option');
            o.value = m.name;
            return o;
          }),
        );
      }
    }
    const trade = TRADE[form.industry.value];
    const metro = pickMetro();
    current = null;
    statusField.value = '';
    metroField.value = '';
    button.textContent = buttonText;
    if (!trade || !metro) return show('', '');
    const r = await get(`/public/markets/check?trade=${trade}&metro=${metro.cbsaCode}`);
    if (mine !== seq || !r || r.status === 'unknown') return show('', '');
    current = { status: r.status, trade, metro };
    statusField.value = r.status;
    metroField.value = `${metro.name} (${metro.cbsaCode})`;
    show(r.status, r.message);
    if (r.status !== 'open') button.textContent = 'Join the waitlist ';
  }

  let timer = 0;
  const later = () => {
    clearTimeout(timer);
    timer = setTimeout(update, 300);
  };
  input.addEventListener('input', later);
  input.addEventListener('change', update);
  form.industry.addEventListener('change', update);
  if (form.industry.value) update();

  // Taken or held: also add them to the platform waitlist (the team still gets the email).
  form.addEventListener('submit', () => {
    if (!current || current.status === 'open' || !form.checkValidity()) return;
    fetch(`${api}/public/waitlist`, {
      method: 'POST',
      keepalive: true,
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ email: form.email.value, trade: current.trade, metro: current.metro.cbsaCode }),
    }).catch(() => {});
  });
})();
