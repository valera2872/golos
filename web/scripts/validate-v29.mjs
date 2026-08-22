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
const sprite = path.join(root, 'screens', 'ru', 'somnori-0.30.4-sprite.webp');
if (!fs.existsSync(sprite)) throw new Error('v2.9 real RU screenshot sprite missing from dist');

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
if (en.includes('/screens/ru/') || en.includes('ru-real-')) throw new Error('v2.9 Russian screenshots leaked into English output');
const neutralSlots = (en.match(/data-screenshot-slot/g) || []).length;
if (neutralSlots < 4) throw new Error(`v2.9 EN neutral screenshot slots unexpectedly reduced: ${neutralSlots}`);

const spriteSize = fs.statSync(sprite).size;
if (spriteSize > 260_000) throw new Error(`v2.9 screenshot sprite too large: ${spriteSize} bytes`);

console.log('Somnori Web v2.9 RU real-screen validation OK');
console.log('RU real screens:', realScreens.length);
console.log('EN neutral slots:', neutralSlots);
console.log('RU screenshot sprite bytes:', spriteSize);
