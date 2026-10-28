import { readdir, readFile, writeFile } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
const dist = fileURLToPath(new URL('../dist/', import.meta.url));
const configured = process.env.SITE_URL || (process.env.VERCEL_PROJECT_PRODUCTION_URL ? 'https://' + process.env.VERCEL_PROJECT_PRODUCTION_URL : process.env.VERCEL_URL ? 'https://' + process.env.VERCEL_URL : '');
if (!configured) throw new Error('Set SITE_URL=https://your-domain.com before building locally.');
const url = new URL(configured);
if (url.protocol !== 'https:' || url.pathname !== '/' || url.search || url.hash || url.username || url.password || url.hostname.endsWith('.example')) throw new Error('SITE_URL must be a real HTTPS origin without a path.');
const origin = url.origin;
const home = await readFile(dist + '/index.html', 'utf8');
const previous = home.match(/<link rel="canonical" href="(https:\/\/[^/"]+)\/"/)?.[1];
if (!previous) throw new Error('Missing canonical origin in dist/index.html');
let count = 0;
async function walk(dir) {
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const file = dir + '/' + entry.name;
    if (entry.isDirectory()) await walk(file);
    else if (/\.(html|xml|txt)$/.test(entry.name)) {
      const text = await readFile(file, 'utf8');
      await writeFile(file, text.replaceAll(previous, origin));
      count++;
    }
  }
}
await walk(dist);
console.log('Prepared ' + count + ' static files for ' + origin);
