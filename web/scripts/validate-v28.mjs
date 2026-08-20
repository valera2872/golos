import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve('dist');
if (!fs.existsSync(root)) throw new Error('dist missing');

function routeForFile(file) {
  let rel = path.relative(root, file).replaceAll('\\', '/');
  if (rel === 'index.html') return '/';
  if (rel.endsWith('/index.html')) return '/' + rel.slice(0, -'/index.html'.length);
  if (rel.endsWith('.html')) return '/' + rel.slice(0, -'.html'.length);
  return null;
}
function outputFor(route) {
  const clean = route.replace(/^\/+|\/+$/g, '');
  if (!clean) return path.join(root, 'index.html');
  const candidates = [path.join(root, clean, 'index.html'), path.join(root, `${clean}.html`)];
  return candidates.find(fs.existsSync) ?? candidates[0];
}
function firstMatch(html, re) {
  const m = html.match(re);
  return m?.[1]?.trim() ?? '';
}
function stripTags(value) {
  return value.replace(/<[^>]*>/g, ' ').replace(/\s+/g, ' ').trim();
}

const files = [];
function walk(dir) {
  for (const name of fs.readdirSync(dir)) {
    const full = path.join(dir, name);
    const stat = fs.statSync(full);
    if (stat.isDirectory()) walk(full);
    else if (name.endsWith('.html')) files.push(full);
  }
}
walk(root);

const pages = new Map();
for (const file of files) {
  const route = routeForFile(file);
  if (!route) continue;
  const html = fs.readFileSync(file, 'utf8');
  const title = stripTags(firstMatch(html, /<title>([\s\S]*?)<\/title>/i));
  const description = firstMatch(html, /<meta\s+name="description"\s+content="([^"]*)"/i) || firstMatch(html, /<meta\s+content="([^"]*)"\s+name="description"/i);
  const canonical = firstMatch(html, /<link\s+rel="canonical"\s+href="([^"]+)"/i) || firstMatch(html, /<link\s+href="([^"]+)"\s+rel="canonical"/i);
  const robots = firstMatch(html, /<meta\s+name="robots"\s+content="([^"]+)"/i) || firstMatch(html, /<meta\s+content="([^"]+)"\s+name="robots"/i);
  const h1Count = (html.match(/<h1(?:\s|>)/gi) || []).length;
  const lang = firstMatch(html, /<html\s+lang="([^"]+)"/i);
  const hrefs = [...html.matchAll(/<a\b[^>]*href="([^"]+)"/gi)].map((m) => m[1]);
  pages.set(route, { file, html, title, description, canonical, robots, h1Count, lang, hrefs });
}

const errors = [];
const titleOwners = new Map();
const descOwners = new Map();
const canonicalOwners = new Map();

for (const [route, page] of pages) {
  if (!page.title) errors.push(`missing title: ${route}`);
  if (!page.description) errors.push(`missing meta description: ${route}`);
  if (!page.canonical) errors.push(`missing canonical: ${route}`);
  if (page.h1Count !== 1) errors.push(`expected exactly one H1 (${page.h1Count}): ${route}`);
  if (!page.robots) errors.push(`missing explicit robots meta: ${route}`);
  if (!page.html.includes('rel="icon" href="/favicon.svg"')) errors.push(`favicon link missing: ${route}`);
  if (!page.html.includes('rel="manifest" href="/site.webmanifest"')) errors.push(`manifest link missing: ${route}`);
  if (!page.html.includes('name="twitter:card" content="summary"')) errors.push(`twitter summary metadata missing: ${route}`);
  if (!page.html.includes('property="og:locale"')) errors.push(`og locale missing: ${route}`);

  if (route === '/404') {
    if (!page.robots.includes('noindex')) errors.push('404 must be noindex');
    continue;
  }
  if (!page.robots.includes('index')) errors.push(`indexable page missing index robots: ${route}`);

  for (const [value, owners, label] of [
    [page.title, titleOwners, 'title'],
    [page.description, descOwners, 'description'],
    [page.canonical, canonicalOwners, 'canonical'],
  ]) {
    if (!value) continue;
    if (!owners.has(value)) owners.set(value, []);
    owners.get(value).push(route);
  }
}

for (const [value, owners] of titleOwners) if (owners.length > 1) errors.push(`duplicate title ${JSON.stringify(value)}: ${owners.join(', ')}`);
for (const [value, owners] of descOwners) if (owners.length > 1) errors.push(`duplicate description ${JSON.stringify(value)}: ${owners.join(', ')}`);
for (const [value, owners] of canonicalOwners) if (owners.length > 1) errors.push(`duplicate canonical ${JSON.stringify(value)}: ${owners.join(', ')}`);

// Build internal-link graph and enforce that every indexable page is discoverable from EN or RU home.
const graph = new Map();
for (const [route, page] of pages) {
  const targets = [];
  for (const href of page.hrefs) {
    if (!href.startsWith('/') || href.startsWith('//')) continue;
    const pathname = href.split('#')[0].split('?')[0] || route;
    if (pathname.startsWith('/_astro/')) continue;
    if (pages.has(pathname)) targets.push(pathname);
  }
  graph.set(route, [...new Set(targets)]);
}
function bfs(start) {
  const depth = new Map([[start, 0]]);
  const queue = [start];
  while (queue.length) {
    const current = queue.shift();
    const d = depth.get(current);
    for (const next of graph.get(current) || []) {
      if (!depth.has(next)) { depth.set(next, d + 1); queue.push(next); }
    }
  }
  return depth;
}
const enDepth = bfs('/');
const ruDepth = bfs('/ru');
for (const [route, page] of pages) {
  if (route === '/404' || page.robots.includes('noindex')) continue;
  const localizedRoot = route === '/ru' || route.startsWith('/ru/') ? ruDepth : enDepth;
  if (!localizedRoot.has(route)) errors.push(`orphan/unreachable from localized home: ${route}`);
  else if (localizedRoot.get(route) > 4) errors.push(`page deeper than 4 internal clicks (${localizedRoot.get(route)}): ${route}`);
}

// Language sanity.
for (const [route, page] of pages) {
  if (route === '/404') continue;
  const expected = route === '/ru' || route.startsWith('/ru/') ? 'ru' : 'en';
  if (page.lang !== expected) errors.push(`html lang mismatch ${page.lang} != ${expected}: ${route}`);
}

// Static brand/manifest files.
for (const rel of ['favicon.svg', 'site.webmanifest', 'robots.txt', 'sitemap-index.xml']) {
  if (!fs.existsSync(path.join(root, rel))) errors.push(`missing built launch asset: ${rel}`);
}

const sitemap = fs.readdirSync(root)
  .filter((name) => name.startsWith('sitemap') && name.endsWith('.xml'))
  .map((name) => fs.readFileSync(path.join(root, name), 'utf8'))
  .join('\n');
if (sitemap.includes('https://somnori.com/404')) errors.push('404 leaked into sitemap');

// FAQ structured data must exist in both languages.
for (const route of ['/faq', '/ru/faq']) {
  const html = pages.get(route)?.html ?? '';
  if (!html.includes('"@type":"FAQPage"')) errors.push(`FAQPage JSON-LD missing: ${route}`);
  if (!html.includes('"@type":"Question"')) errors.push(`FAQ questions JSON-LD missing: ${route}`);
}

if (errors.length) {
  console.error('Somnori Web v2.8 launch audit FAILED');
  for (const error of errors) console.error('-', error);
  process.exit(1);
}

console.log('Somnori Web v2.8 technical launch audit OK');
console.log('HTML pages:', pages.size);
console.log('Unique titles:', titleOwners.size);
console.log('Unique canonicals:', canonicalOwners.size);
console.log('Max EN depth:', Math.max(...enDepth.values()));
console.log('Max RU depth:', Math.max(...ruDepth.values()));
