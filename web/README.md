# Somnori Web

Static SEO-first website for `https://somnori.com`.

## Stack

- Astro 7
- Static output
- Official `@astrojs/sitemap` integration
- No client framework and no analytics in the initial build

## Local development

```bash
cd web
npm install
npm run dev
```

## Production build

```bash
cd web
npm install
npm run build
```

Upload the contents of `web/dist/` to the document root for `somnori.com`.

## Canonical host

The generated canonical URLs use `https://somnori.com`. Production hosting should permanently redirect:

- `http://somnori.com/*` → `https://somnori.com/*`
- `https://www.somnori.com/*` → `https://somnori.com/*`

## Launch routes

- `/`
- `/voice-dream-journal`
- `/hands-free-dream-journal`
- `/remember-dreams`
- `/dream-journal`
- `/privacy`
- `/terms`

The future `/tools/dream-interpreter` route must **not** be published or indexed until a real interactive tool exists.

## SEO invariants

- English is served from the root.
- Future Russian pages live under `/ru/` and use reciprocal `hreflang` only when real localized equivalents exist.
- One canonical URL per search intent.
- No mass-generated thin dream-symbol pages.
- Product claims must match the physically verified Android build.
- Comparisons must disclose Somnori ownership and use the same criteria for competitors.

## After deployment

1. Verify the domain in Google Search Console.
2. Submit `https://somnori.com/sitemap-index.xml`.
3. Verify Bing Webmaster Tools and submit the same sitemap.
4. Test the public site on a physical Android device at 360–430 px widths.
5. Add analytics only after deciding the privacy/consent implementation and updating `/privacy`.
