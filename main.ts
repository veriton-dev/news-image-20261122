// Build the front page and put it where the grader looks.
//
// The entrypoint does the whole build rather than copying a file that happens to
// be checked in: if entry.png is missing or older than render.py it is rendered
// again, then the PNG is verified before it is published. Node 22+, standard
// library only; the drawing itself is render.py (Python 3 + Pillow).

import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { spawnSync } from "node:child_process";

const here = dirname(fileURLToPath(import.meta.url));
const renderer = join(here, "render.py");
const image = join(here, "entry.png");
const outDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "/output");

function mtimeMs(path: string): number {
  try {
    return statSync(path).mtimeMs;
  } catch {
    return -1;
  }
}

// Render when there is nothing to publish, or when the renderer is newer than
// the image: a stale PNG next to a newer renderer is the classic silent defect.
if (!existsSync(image) || mtimeMs(image) < mtimeMs(renderer)) {
  const drawn = spawnSync("python3", [renderer], { cwd: here, encoding: "utf8" });
  if (drawn.stdout) process.stderr.write(drawn.stdout);
  if (drawn.stderr) process.stderr.write(drawn.stderr);
  if (drawn.error || drawn.status !== 0) {
    console.error(`render.py failed (status ${drawn.status})`);
    process.exit(1);
  }
}

const bytes = statSync(image).size;
if (bytes === 0) {
  console.error(`${image} is empty`);
  process.exit(1);
}

// The file must really be a PNG, not a renamed bitmap or an error page: check
// the eight-byte signature before anything reads the IHDR below.
const signature = readFileSync(image).subarray(0, 8);
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!signature.equals(PNG_MAGIC)) {
  console.error(`${image} is not a PNG (bad signature)`);
  process.exit(1);
}

// Read the PNG header back instead of trusting the writer: the competition
// requires one 1024x1024 PNG, and a wrong size is cheap to catch here.
const header = spawnSync(
  "python3",
  ["-c", "import struct,sys;d=open(sys.argv[1],'rb').read(33);print(struct.unpack('>II', d[16:24]))", image],
  { encoding: "utf8" },
);
const size = (header.stdout ?? "").trim();
if (size !== "(1024, 1024)") {
  console.error(`entry.png is ${size || "unreadable"}, expected (1024, 1024)`);
  process.exit(1);
}

mkdirSync(outDir, { recursive: true });
const target = join(outDir, "entry.png");
copyFileSync(image, target);
console.log(`entry.png -> ${target} (${bytes} bytes, ${size})`);
