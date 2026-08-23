import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const chunks = [0, 1, 2, 3, 4].map((i) =>
  path.join(root, 'src', 'screens', `ru-sprite-0${i}.txt`)
);

for (const file of chunks) {
  if (!fs.existsSync(file)) throw new Error(`RU screenshot chunk missing: ${file}`);
}

const b64 = chunks.map((file) => fs.readFileSync(file, 'utf8').trim()).join('');
const bytes = Buffer.from(b64, 'base64');

if (bytes.length !== 55215) {
  throw new Error(`RU AVIF sprite size mismatch: ${bytes.length} != 55215`);
}
if (bytes.subarray(4, 12).toString('ascii') !== 'ftypavif') {
  throw new Error('RU screenshot sprite is not AVIF (ftypavif missing)');
}

const ispe = bytes.indexOf(Buffer.from('ispe'));
if (ispe < 0) throw new Error('RU AVIF sprite ispe box missing');
const width = bytes.readUInt32BE(ispe + 8);
const height = bytes.readUInt32BE(ispe + 12);
if (width !== 340 || height !== 5292) {
  throw new Error(`RU AVIF sprite dimensions mismatch: ${width}x${height}`);
}

const outDir = path.join(root, 'public', 'screens', 'ru');
fs.mkdirSync(outDir, { recursive: true });
const out = path.join(outDir, 'somnori-0.30.4-sprite.avif');
fs.writeFileSync(out, bytes);
console.log(`Built verified RU screenshot sprite: ${width}x${height}, ${bytes.length} bytes`);
