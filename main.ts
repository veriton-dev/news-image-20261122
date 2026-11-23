// Copy the rendered poster to the directory the grader watches.
// Node 22+, standard library only.

import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const source = join(here, "entry.png");
const targetDir = resolve(process.env.MAKEFUN_OUTPUT_DIR ?? "/output");
const target = join(targetDir, "entry.png");

if (!existsSync(source)) {
  console.error(`missing ${source}; run python3 render.py first`);
  process.exit(1);
}

mkdirSync(targetDir, { recursive: true });
copyFileSync(source, target);

const bytes = statSync(target).size;
if (bytes === 0) {
  console.error(`wrote an empty file to ${target}`);
  process.exit(1);
}
console.log(`entry.png -> ${target} (${bytes} bytes)`);
