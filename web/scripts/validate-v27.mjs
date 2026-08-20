import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve('dist');
const pairs = [
  { en: '/privacy', ru: '/ru/privacy', enH1: 'Privacy at Somnori', ruH1: 'Личные ночные записи требуют особенно аккуратного отношения.' },
  { en: '/terms', ru: '/ru/terms', enH1: 'Website Terms', ruH1: 'Условия использования сайта Somnori' },
  { en: '/faq', ru: '/ru/faq', enH1: 'What Somnori is — and what it is not yet.', ruH1: 'Что Somnori уже умеет — и что пока только в планах.' },
];

function outputFor(route) {
  const clean = route.replace(/^\/+|\/+$/g, '');
  if (!clean) return path.join(root, 'index.html');
  const candidates = [path.join(root, clean, 'index.html'), path.join(root, `${clean}.html`)];
  return candidates.find(fs.existsSync) ?? candidates[0];
}

for (const pair of pairs) {
  for (const [lang, route, h1] of [['en', pair.en, pair.enH1], ['ru', pair.ru, pair.ruH1]]) {
    const file = outputFor(route);
    if (!fs.existsSync(file)) throw new Error(`v2.7 missing ${lang} trust route: ${route}`);
    const html = fs.readFileSync(file, 'utf8');
    if (!html.includes(`<html lang="${lang}"`)) throw new Error(`lang missing: ${route}`);
    if (!html.includes(h1)) throw new Error(`H1 drift: ${route}`);
    if (!html.includes(`https://somnori.com${route}`)) throw new Error(`canonical missing: ${route}`);
    for (const hreflang of ['en', 'ru', 'x-default']) {
      if (!html.includes(`hreflang="${hreflang}"`)) throw new Error(`hreflang ${hreflang} missing: ${route}`);
    }
    const equivalent = lang === 'en' ? pair.ru : pair.en;
    if (!html.includes(`href="${equivalent}"`)) throw new Error(`language switch missing equivalent ${equivalent}: ${route}`);
  }
}

const enFaq = fs.readFileSync(outputFor('/faq'), 'utf8');
const ruFaq = fs.readFileSync(outputFor('/ru/faq'), 'utf8');
const enMarkers = [
  'Is Somnori only a dream journal?',
  'Can Somnori tell me the time?',
  'Can I set an alarm by voice?',
  'Does Somnori have a smart alarm?',
  'Can I record thoughts and ideas that are not dreams?',
  'Can Somnori run an autosuggestion after the alarm?',
  'Is Somnori available on iPhone?',
  'Can I download Somnori now?',
];
const ruMarkers = [
  'Somnori — это только дневник снов?',
  'Можно спросить у Somnori, сколько времени?',
  'Можно поставить будильник голосом?',
  'Есть ли в Somnori «умный будильник»?',
  'Можно записывать мысли и идеи, а не только сны?',
  'Может ли после будильника автоматически запуститься самовнушение?',
  'Есть версия для iPhone?',
  'Можно уже скачать приложение?',
];
for (const marker of enMarkers) if (!enFaq.includes(marker)) throw new Error(`EN FAQ marker missing: ${marker}`);
for (const marker of ruMarkers) if (!ruFaq.includes(marker)) throw new Error(`RU FAQ marker missing: ${marker}`);

// Product-state guardrails: wake protocol/iOS/public download must stay future/not-current.
for (const forbidden of [
  'Somnori is available on iPhone',
  'Download Somnori now from Google Play',
  'automatically runs your autosuggestion after every alarm',
  'guaranteed dream interpretation',
]) {
  if ((enFaq + ruFaq).toLowerCase().includes(forbidden.toLowerCase())) throw new Error(`false current-state FAQ claim: ${forbidden}`);
}

const ruHome = fs.readFileSync(outputFor('/ru'), 'utf8');
for (const route of ['/ru/privacy', '/ru/terms', '/ru/faq']) {
  if (!ruHome.includes(`href="${route}"`)) throw new Error(`RU footer missing localized trust link: ${route}`);
}
const enHome = fs.readFileSync(outputFor('/'), 'utf8');
for (const route of ['/privacy', '/terms', '/faq']) {
  if (!enHome.includes(`href="${route}"`)) throw new Error(`EN footer missing trust link: ${route}`);
}

const sitemap = fs.readdirSync(root)
  .filter((name) => name.startsWith('sitemap') && name.endsWith('.xml'))
  .map((name) => fs.readFileSync(path.join(root, name), 'utf8'))
  .join('\n');
for (const pair of pairs) {
  for (const route of [pair.en, pair.ru]) {
    if (!sitemap.includes(`https://somnori.com${route}`)) throw new Error(`sitemap missing trust route: ${route}`);
  }
}

console.log('Somnori Web v2.7 trust/FAQ validation OK');
console.log('Validated EN/RU trust pairs:', pairs.length);
