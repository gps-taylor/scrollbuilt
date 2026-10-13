# scrollbuilt.com

Static site — no build step. Hosted free on Cloudflare Pages from this repo.

| Path | What it is |
| --- | --- |
| `index.html` | Homepage with the AI scroll-build hero |
| `contact.html` | "Check your market" lead form |
| `assets/` | CSS, JS, images |
| `frames-d/`, `frames-m/` | Scroll animation frames (desktop 16:9, phone 9:16) |
| `video/` | Build reels for social (16:9 and 9:16) |
| `_headers` | Cloudflare caching rules |

## One-time setup
1. **Cloudflare Pages:** Workers & Pages → Create → Pages → Connect to Git → pick this repo. Framework preset: *None*. Build command: *(blank)*. Output directory: `/`. Deploy.
2. **Domain:** in the Pages project → Custom domains → add `scrollbuilt.com` and `www.scrollbuilt.com`.
3. **Email:** Cloudflare → scrollbuilt.com → Email → Email Routing → forward `hello@scrollbuilt.com` to your inbox.
4. **Form:** submit the contact form once yourself. FormSubmit emails `hello@scrollbuilt.com` an activation link — click it. After that every lead arrives by email.

## Adding an industry page later
Create a folder (e.g. `pools/`) with its own `index.html`, `frames-d/` and `frames-m/`, and link it from the Trades cards on the homepage.
