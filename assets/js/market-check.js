// Instant territory check against the ScrollBuilt platform API (GET /public/territories/check).
// Progressive enhancement: if the API can't be reached, nothing changes and the form still emails the team.
(() => {
  const form = document.getElementById('lead');
  const api = document.querySelector('meta[name="sb-api"]')?.content?.replace(/\/$/, '');
  if (!form || !api || !form.zip) return;

  const TRADE = {
    'Pools & spas': 'pools',
    'Custom homes': 'custom-homes',
    'Landscaping & outdoor living': 'landscaping',
    'Decks, patios & pergolas': 'outdoor-living',
    Remodeling: 'remodel',
    'Roofing & solar': 'roofing',
    'ADUs & casitas': 'adu',
  };
  const input = form.zip;
  const button = form.querySelector('button[type="submit"]');
  const buttonText = button.textContent;

  const out = document.createElement('div');
  out.className = 'mc';
  out.setAttribute('role', 'status');
  out.setAttribute('aria-live', 'polite');
  input.closest('label').after(out);

  const statusField = document.createElement('input');
  statusField.type = 'hidden';
  statusField.name = 'territory_status';
  form.append(statusField);

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

  let current = null; // { status, trade, zip }
  let seq = 0;

  const show = (status, message) => {
    out.className = status ? `mc show ${status}` : 'mc';
    out.textContent = message || '';
  };

  async function update() {
    const mine = ++seq;
    const trade = TRADE[form.industry.value];
    const zip = input.value.trim();
    current = null;
    statusField.value = '';
    button.textContent = buttonText;
    if (!trade || !/^\d{5}$/.test(zip)) return show('', '');
    const r = await get(`/public/territories/check?trade=${trade}&zip=${zip}`);
    if (mine !== seq || !r || !r.status) return show('', '');
    current = { status: r.status, trade, zip };
    statusField.value = r.status;
    // "unknown" means we will check it by hand: say so without colouring it as taken.
    show(r.status === 'unknown' ? '' : r.status, r.status === 'unknown' ? '' : r.message);
    if (r.status === 'taken') button.textContent = 'Join the waitlist ';
  }

  let timer = 0;
  const later = () => {
    clearTimeout(timer);
    timer = setTimeout(update, 300);
  };
  input.addEventListener('input', later);
  input.addEventListener('change', update);
  form.industry.addEventListener('change', update);
  if (form.industry.value && input.value) update();

  // Taken: also add them to the platform waitlist (the team still gets the email).
  form.addEventListener('submit', () => {
    if (!current || current.status !== 'taken' || !form.checkValidity()) return;
    fetch(`${api}/public/waitlist`, {
      method: 'POST',
      keepalive: true,
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ email: form.email.value, trade: current.trade, zip: current.zip }),
    }).catch(() => {});
  });
})();
