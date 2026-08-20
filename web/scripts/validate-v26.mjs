import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve('dist');
const pairs = [
  { en: '/dream-journal', ru: '/ru/dnevnik-snov', h1: 'Дневник снов, который начинается ещё ночью.', marker: 'Дневник снов' },
  { en: '/voice-dream-journal', ru: '/ru/zapis-snov-golosom', h1: 'Расскажите сон голосом, пока он ещё не исчез.', marker: 'Запись сна голосом' },
  { en: '/hands-free-dream-journal', ru: '/ru/beskontaktnaya-zapis-snov', h1: 'Запишите сон, не разблокируя телефон.', marker: 'Бесконтактная запись сна' },
  { en: '/remember-dreams', ru: '/ru/kak-zapominat-sny', h1: 'Как запоминать сны до того, как они исчезнут.', marker: 'Запоминание снов' },
];

function outputFor(route) {
  const clean = route.replace(/^\/+|\/+$/g, '');
  if (!clean) return path.join(root, 'index.html');
  const candidates = [path.join(root, clean, 'index.html'), path.join(root, `${clean}.html`)];
  return candidates.find(fs.existsSync) ?? candidates[0];
}

for (const pair of pairs) {
  const ruFile = outputFor(pair.ru);
  const enFile = outputFor(pair.en);
  if (!fs.existsSync(ruFile)) throw new Error(`v2.6 missing RU dream route: ${pair.ru}`);
  if (!fs.existsSync(enFile)) throw new Error(`v2.6 missing EN dream pair: ${pair.en}`);
  const ruHtml = fs.readFileSync(ruFile, 'utf8');
  const enHtml = fs.readFileSync(enFile, 'utf8');
  if (!ruHtml.includes('<html lang="ru"')) throw new Error(`RU lang missing: ${pair.ru}`);
  if (!ruHtml.includes(pair.h1)) throw new Error(`RU H1 drift: ${pair.ru}`);
  if (!ruHtml.includes(pair.marker)) throw new Error(`RU dream marker missing: ${pair.ru}`);
  if (!ruHtml.includes(`https://somnori.com${pair.ru}`)) throw new Error(`RU canonical missing: ${pair.ru}`);
  for (const lang of ['en', 'ru', 'x-default']) {
    if (!ruHtml.includes(`hreflang="${lang}"`)) throw new Error(`RU hreflang ${lang} missing: ${pair.ru}`);
  }
  if (!ruHtml.includes(`href="${pair.en}"`)) throw new Error(`RU switch missing EN pair: ${pair.ru}`);
  if (!enHtml.includes(`https://somnori.com${pair.ru}`)) throw new Error(`EN dream page missing RU hreflang: ${pair.en}`);
  if (!enHtml.includes(`href="${pair.ru}"`)) throw new Error(`EN switch missing RU pair: ${pair.en}`);
  if (!ruHtml.includes('Место для реального скриншота приложения')) throw new Error(`RU screenshot placeholder missing: ${pair.ru}`);
}

const ruHome = fs.readFileSync(outputFor('/ru'), 'utf8');
for (const route of ['/ru/dnevnik-snov', '/ru/kak-zapominat-sny']) {
  if (!ruHome.includes(`href="${route}"`)) throw new Error(`RU homepage missing dream link: ${route}`);
}

const sitemap = fs.readdirSync(root)
  .filter((name) => name.startsWith('sitemap') && name.endsWith('.xml'))
  .map((name) => fs.readFileSync(path.join(root, name), 'utf8'))
  .join('\n');
for (const pair of pairs) {
  if (!sitemap.includes(`https://somnori.com${pair.ru}`)) throw new Error(`sitemap missing RU dream route: ${pair.ru}`);
}

for (const forbidden of ['/ru/sonnik', '/ru/tolkovanie-snov', '/ru/sonnik-po-simvolam']) {
  if (fs.existsSync(outputFor(forbidden))) throw new Error(`premature thin dream-interpretation route published: ${forbidden}`);
}

console.log('Somnori Web v2.6 Russian dream branch validation OK');
console.log('Validated RU/EN dream pairs:', pairs.length);
