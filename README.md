# svg-minify

> SVG batch minifier that won't break your animations.

Most SVG optimizers strip out CSS keyframes, remove referenced IDs, and silently destroy animated SVGs. This one doesn't. Drop your files in, get clean optimized SVGs back — no config, no surprises.

---

## Why this one?

| Feature | svg-minify | SVGO | scour |
|---|---|---|---|
| Batch processing | ✅ | ❌ | ❌ |
| Animation-safe | ✅ | ⚠️ Breaks keyframes | ✅ |
| CSS keyframes preserved | ✅ | ⚠️ | ❌ |
| ARIA attributes preserved | ✅ | ⚠️ | ❌ |
| One-click Windows support | ✅ | ❌ | ❌ |
| Zero config needed | ✅ | ❌ | ❌ |

---

## Quick Start

**1. Clone the repo**

```bash
git clone https://github.com/bsod700/svg-minify.git
cd svg-minify
```

**2. Install dependencies**

```bash
pip install -r requirements.txt
```

**3. Drop your SVGs in the `svg` folder**

```
svg-minify/
  ├── svg/          ← drop your files here
  └── minify_svg.py
```

**4. Run it**

Windows — double-click `minify.bat`

Everyone else:
```bash
python minify_svg.py
```

**5. Pick up your files**

```
svg-minify/
  ├── svg/          ← originals untouched
  └── svg minified/ ← clean, optimized files
```

That's it.

---

## What it does

Removes what's safe to remove, keeps everything that matters:

**Removed**
- XML comments and editor metadata
- Unnecessary whitespace
- Redundant attributes and numeric precision

**Always preserved**
- CSS animations and keyframes
- ViewBox (responsive SVGs stay responsive)
- IDs referenced by styles or animations
- ARIA attributes
- Data attributes

---

## Example output

```
SVG Batch Minification Tool
────────────────────────────────────────

[1/3] logo.svg        45.23 KB → 38.15 KB   saved 15.65%
[2/3] icon.svg        12.50 KB → 10.20 KB   saved 18.40%
[3/3] hero.svg       935.50 KB → 840.15 KB  saved 10.19%

────────────────────────────────────────
3 files   993.23 KB → 888.50 KB   saved 104.73 KB (10.54%)
```

---

---

## Configuration

Change the folder names at the top of `minify_svg.py` if needed:

```python
INPUT_FOLDER  = 'svg'         # where your originals live
OUTPUT_FOLDER = 'svg minified' # where minified files are saved
```

---

## Files

| File | Purpose |
|---|---|
| `minify_svg.py` | Main script |
| `minify.bat` | One-click Windows runner |
| `requirements.txt` | Optional dependencies |

---

## Troubleshooting

**No files found** — check that files are in the `svg` folder and have a `.svg` extension.

**Python not found** — download from [python.org](https://python.org) and check "Add to PATH" during install.

**Minified SVG looks broken** — open the original in a browser first to confirm it works. If it does, try installing `scour`.

**Permission error** — run terminal as administrator, or check the output folder isn't open in another app.

---

MIT License