// Publish the rendered front page to the directory the grader watches.
//
// Everything here is Node's standard library and nothing else: the grading
// sandbox is not this machine, so the build must not shell out to Python or
// assume Pillow is installed. The PNG is drawn ahead of time by render.py and
// committed; this step verifies the committed bytes and copies them.
//
// Node 22+, standard library only.

import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const image = join(here, "entry.png");
const outDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "/output");

function die(message: string): never {
  console.error(message);
  process.exit(1);
}

if (!existsSync(image)) {
  die(`missing ${image}: the committed front page is not in this checkout`);
}

const png = readFileSync(image);
if (png.length === 0) die(`${image} is empty`);

// A PNG starts with this eight-byte signature; a renamed bitmap or an error
// page saved over the render would otherwise publish without a complaint.
const MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (png.length < 33 || !png.subarray(0, 8).equals(MAGIC)) {
  die(`${image} is not a PNG (bad signature)`);
}

// IHDR is always the first chunk, so width and height sit at bytes 16 and 20.
const width = png.readUInt32BE(16);
const height = png.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  die(`${image} is ${width}x${height}; the competition asks for 1024x1024`);
}

mkdirSync(outDir, { recursive: true });
const target = join(outDir, "entry.png");

// Copying a file onto itself would empty it; the grader's output directory is
// never the repository, but refuse loudly rather than publish a zero-byte page.
if (target === image) die(`refusing to overwrite the source image at ${image}`);

copyFileSync(image, target);

// Read the published file back: a short or partial write is a failed build,
// not an entry, and it is far cheaper to learn that here than from a rejection.
const published = readFileSync(target);
if (!published.equals(png)) {
  die(`${target} differs from ${image} after the copy`);
}

console.log(`entry.png -> ${target} (${png.length} bytes, ${width}x${height})`);
