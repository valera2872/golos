import fs from 'node:fs';
import path from 'node:path';

const root = path.resolve('dist');
const routes = {
  '/night-thought-recorder': ['Record the Idea Without Waking Yourself Up', 'Night thought capture'],
  '/voice-alarm-at-night': ['Ask the Time. Set an Alarm. Keep Your Eyes Closed.', 'Time &amp; voice alarm'],
  '/bedtime-routine-app': ['Build a Bedtime Routine That Belongs to the Whole Night', 'Bedtime routine'],
  '/sleep-affirmations-app': ['Make Autosuggestion Part of the Night You Planned', 'Autosuggestion'],
};

function outputFor(route) {
  const clean = route.replace(/^\/+|\/+$/g, '');
  const candidates = [path.join(root, clean, 'index.html'), path.join(root, `${clean}.html`)];
  return candidates.find(fs.existsSync) ?? candidates[0];
}

for (const [route, markers] of Object.entries(routes)) {
  const file = outputFor(route);
  if (!fs.existsSync(file)) throw new Error(`v2.4 missing route: ${route}`);
  const html = fs.readFileSync(file, 'utf8');
  const canonical = `https://somnori.com${route}`;
  if (!html.includes(canonical)) throw new Error(`v2.4 canonical missing: ${route}`);
  if (!html.toLowerCase().includes('<h1')) throw new Error(`v2.4 H1 missing: ${route}`);
  if (!html.includes('One night system') && !html.includes('Capture layer') && !html.includes('Night layer') && !html.includes('Routine layer')) {
    throw new Error(`v2.4 product bridge missing: ${route}`);
  }
  for (const marker of markers) {
    if (!html.includes(marker)) throw new Error(`v2.4 marker missing in ${route}: ${marker}`);
  }
}

const home = fs.readFileSync(outputFor('/'), 'utf8');
for (const route of Object.keys(routes)) {
  if (!home.includes(`href=\"${route}\"`)) throw new Error(`homepage missing internal link: ${route}`);
}

const sitemap = fs.readdirSync(root)
  .filter((name) => name.startsWith('sitemap') && name.endsWith('.xml'))
  .map((name) => fs.readFileSync(path.join(root, name), 'utf8'))
  .join('\n');
for (const route of Object.keys(routes)) {
  if (!sitemap.includes(`https://somnori.com${route}`)) throw new Error(`sitemap missing: ${route}`);
}

const affirmations = fs.readFileSync(outputFor('/sleep-affirmations-app'), 'utf8');
for (const forbidden of ['guaranteed subconscious reprogramming', 'treat insomnia', 'cure anxiety']) {
  if (affirmations.toLowerCase().includes(forbidden)) throw new Error(`unsafe affirmation claim leaked: ${forbidden}`);
}

console.log('Somnori Web v2.4 product branch validation OK');
console.log('Validated routes:', Object.keys(routes).length);
