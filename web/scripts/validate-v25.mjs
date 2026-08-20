import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve('dist');
const pairs = [
  {
    en: '/night-thought-recorder',
    ru: '/ru/zapis-mysley-golosom',
    ruH1: 'Запишите идею ночью — и снова спите.',
    marker: 'Запись ночной мысли',
  },
  {
    en: '/voice-alarm-at-night',
    ru: '/ru/golosovoy-budilnik',
    ruH1: 'Спросите время. Поставьте будильник. Не берите телефон в руки.',
    marker: 'Время и будильник',
  },
  {
    en: '/bedtime-routine-app',
    ru: '/ru/ritual-pered-snom',
    ruH1: 'Соберите свой ритуал перед сном в одном приложении.',
    marker: 'Ритуал перед сном',
  },
  {
    en: '/sleep-affirmations-app',
    ru: '/ru/affirmacii-pered-snom',
    ruH1: 'Аффирмации и самовнушение — как часть вашего вечернего ритуала.',
    marker: 'Самовнушение',
  },
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
  if (!fs.existsSync(ruFile)) throw new Error(`v2.5 missing RU route: ${pair.ru}`);
  if (!fs.existsSync(enFile)) throw new Error(`v2.5 missing EN pair: ${pair.en}`);

  const ruHtml = fs.readFileSync(ruFile, 'utf8');
  const enHtml = fs.readFileSync(enFile, 'utf8');

  if (!ruHtml.includes('<html lang="ru"')) throw new Error(`RU html lang missing: ${pair.ru}`);
  if (!ruHtml.includes(pair.ruH1)) throw new Error(`RU H1 drift: ${pair.ru}`);
  if (!ruHtml.includes(pair.marker)) throw new Error(`RU product marker missing: ${pair.ru}`);
  if (!ruHtml.includes(`https://somnori.com${pair.ru}`)) throw new Error(`RU canonical missing: ${pair.ru}`);
  if (!ruHtml.includes('hreflang="en"') || !ruHtml.includes('hreflang="ru"') || !ruHtml.includes('hreflang="x-default"')) {
    throw new Error(`RU hreflang set incomplete: ${pair.ru}`);
  }
  if (!ruHtml.includes(`href="${pair.en}"`)) throw new Error(`RU language switch does not reach EN equivalent: ${pair.ru}`);
  if (!enHtml.includes(`https://somnori.com${pair.ru}`)) throw new Error(`EN page missing RU hreflang target: ${pair.en}`);
  if (!enHtml.includes(`href="${pair.ru}"`)) throw new Error(`EN language switch does not reach RU equivalent: ${pair.en}`);
  if (!ruHtml.includes('Место для реального скриншота приложения')) throw new Error(`localized screenshot placeholder missing: ${pair.ru}`);
}

const ruHome = fs.readFileSync(outputFor('/ru'), 'utf8');
const enHome = fs.readFileSync(outputFor('/'), 'utf8');
for (const pair of pairs) {
  if (!ruHome.includes(`href="${pair.ru}"`)) throw new Error(`RU homepage missing internal link: ${pair.ru}`);
}
if (!ruHome.includes('id="system"') || !enHome.includes('id="system"')) throw new Error('homepage #system anchor missing');

const sitemap = fs.readdirSync(root)
  .filter((name) => name.startsWith('sitemap') && name.endsWith('.xml'))
  .map((name) => fs.readFileSync(path.join(root, name), 'utf8'))
  .join('\n');
for (const pair of pairs) {
  if (!sitemap.includes(`https://somnori.com${pair.ru}`)) throw new Error(`sitemap missing RU route: ${pair.ru}`);
}

if (fs.existsSync(outputFor('/ru/samovnushenie-pered-snom'))) {
  throw new Error('thin cannibalizing route /ru/samovnushenie-pered-snom must not be published');
}

console.log('Somnori Web v2.5 Russian product branch validation OK');
console.log('Validated RU/EN pairs:', pairs.length);
