import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve('dist');
function outputFor(route) {
  const clean = route.replace(/^\/+|\/+$/g, '');
  if (!clean) return path.join(root, 'index.html');
  const candidates = [path.join(root, clean, 'index.html'), path.join(root, `${clean}.html`)];
  return candidates.find(fs.existsSync) ?? candidates[0];
}

const en = fs.readFileSync(outputFor('/'), 'utf8');
const ru = fs.readFileSync(outputFor('/ru'), 'utf8');
const sprite = path.join(root, 'screens', 'ru', 'somnori-0.30.4-sprite.avif');
if (!fs.existsSync(sprite)) throw new Error('v2.9 verified RU AVIF screenshot sprite missing from dist');

const bytes = fs.readFileSync(sprite);
if (bytes.length !== 55215) throw new Error(`v2.9 RU AVIF size mismatch: ${bytes.length}`);
if (bytes.subarray(4, 12).toString('ascii') !== 'ftypavif') throw new Error('v2.9 RU screenshot asset is not AVIF');
const ispe = bytes.indexOf(Buffer.from('ispe'));
if (ispe < 0) throw new Error('v2.9 RU AVIF ispe box missing');
const width = bytes.readUInt32BE(ispe + 8);
const height = bytes.readUInt32BE(ispe + 12);
if (width !== 340 || height !== 5292) throw new Error(`v2.9 RU AVIF dimensions mismatch: ${width}x${height}`);

const realScreens = ['home', 'assistant', 'routine', 'sounds', 'wake', 'morning', 'dreams'];
for (const screen of realScreens) {
  const marker = `data-screenshot-slot=\"ru-real-${screen}\"`;
  if (!ru.includes(marker)) throw new Error(`v2.9 RU real screen missing: ${screen}`);
  if (en.includes(marker)) throw new Error(`v2.9 RU real screen leaked into EN homepage: ${screen}`);
}

if (!ru.toLowerCase().includes('реальные экраны текущей сборки')) throw new Error('v2.9 RU real-build disclosure missing');
if (!ru.includes('ЕСТЬ В ТЕКУЩЕЙ СБОРКЕ')) throw new Error('v2.9 current wake capability label missing');
if (!ru.includes('Утром всё, что пришло ночью, снова перед вами')) throw new Error('v2.9 Morning showcase section missing');
if (!ru.includes('Собрать сценарий') && !ru.includes('собираются в один последовательный сценарий')) throw new Error('v2.9 current routine framing missing');

// English stays screenshot-neutral until a real English APK exists.
// Shared compiled CSS can contain RU component selectors; rendered RU phone markup cannot.
for (const forbidden of [
  'data-screenshot-slot=\"ru-real-',
  'Главный экран Somnori 0.30.4 на русском языке',
  'Ночной помощник Somnori: микрофон готов',
  'Экран Somnori «Как я хочу проснуться»',
]) {
  if (en.includes(forbidden)) throw new Error(`v2.9 rendered RU product UI leaked into EN homepage: ${forbidden}`);
}
const neutralSlots = (en.match(/data-screenshot-slot/g) || []).length;
if (neutralSlots < 4) throw new Error(`v2.9 EN neutral screenshot slots unexpectedly reduced: ${neutralSlots}`);

console.log('Somnori Web v2.9 RU real-screen validation OK');
console.log('RU real screens:', realScreens.length);
console.log('EN neutral slots:', neutralSlots);
console.log(`RU AVIF sprite: ${width}x${height}, ${bytes.length} bytes`);
