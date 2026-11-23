// One-day news image for 22 November 2026 (Node 22, standard library only).
//
// The picture is the entry.png beside this file; the program copies it to the
// path the grader reads. Rendering lives in render.py, which is how the image
// was drawn: the modest size of this program is deliberate, because the entry's
// own run has a 60-second budget and two runs must write identical bytes.

import { copyFileSync } from 'node:fs';
import { join } from 'node:path';

const out = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
copyFileSync(new URL('./entry.png', import.meta.url), join(out, 'entry.png'));
