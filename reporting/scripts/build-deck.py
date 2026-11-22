#!/usr/bin/env python3
"""Build a reveal.js deck from a brief source fragment, and optionally upload it to Postplan.

Usage:
  build-deck.py SOURCE.html --title "Title" --out DECK.html [--scroll] [--upload [--draft ID] [--description TEXT]]

SOURCE is an HTML body fragment: top-level <section id="..."> elements with an
<h2> each. A <section> that contains child <section>s becomes a vertical stack. A section with
class="scrollable" scrolls inside the slide. Code goes in <pre><code class="language-x">.
Keep SOURCE where the skill's deck reference says; it is the brief of record.
"""
import argparse, pathlib, shutil, subprocess, sys

HERE = pathlib.Path(__file__).resolve().parent
ASSETS = HERE.parent / "assets" / "deck"

CSS = """
:root { --r-main-font-size: 30px; --r-heading-font: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif; --r-main-font: -apple-system, BlinkMacSystemFont, "Segoe UI", system-ui, sans-serif; --r-code-font: ui-monospace, Menlo, Consolas, monospace; --r-link-color: #7ea2ff; --r-link-color-hover: #a5bdff; }
.reveal { background: #0a0a0a; }
.reveal h1, .reveal h2, .reveal h3 { text-transform: none; letter-spacing: -0.01em; font-weight: 600; }
.reveal h1 { font-size: 2em; } .reveal h2 { font-size: 1.4em; } .reveal h3 { font-size: 1em; color: #8a8a8a; }
.reveal .slides section { text-align: left; }
.reveal .slides section.scrollable { height: 100%; overflow-y: auto; padding-right: 0.5em; }
.reveal ul, .reveal ol { display: block; margin-left: 1em; }
.reveal li { margin: 0.25em 0; }
.reveal p { margin: 0.4em 0; }
.reveal table { font-size: 0.65em; width: 100%; }
.reveal table th { background: #111; font-weight: 500; color: #8a8a8a; }
.reveal table td, .reveal table th { border-bottom: 1px solid #1f1f1f; padding: 0.35em 0.6em; vertical-align: top; }
.reveal pre { width: 100%; font-size: 0.5em; line-height: 1.4; box-shadow: none; border: 1px solid #1f1f1f; border-radius: 8px; margin: 0.4em 0; }
.reveal pre code { max-height: 560px; padding: 12px 14px; background: #0d0d0d; }
.reveal :not(pre) > code { color: #7ea2ff; font-size: 0.9em; }
.reveal .muted { color: #8a8a8a; font-size: 0.8em; }
.reveal .tag { display: inline-block; padding: 2px 8px; border-radius: 6px; font-size: 0.6em; font-weight: 500; background: rgba(16,185,129,0.16); color: #34d399; vertical-align: middle; }
.reveal .tag.warn { background: rgba(245,158,11,0.16); color: #fbbf24; }
.reveal .tag.err { background: rgba(239,68,68,0.16); color: #f87171; }
.reveal .two { display: grid; grid-template-columns: 1fr 1fr; gap: 1.5em; align-items: start; }
.reveal .check { border: 1px dashed #3f3f46; border-radius: 8px; padding: 0.6em 0.9em; margin: 0.4em 0; font-size: 0.8em; }
.reveal .kicker { color: #8a8a8a; font-size: 0.7em; margin: 0; }
"""

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source")
    ap.add_argument("--title", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--scroll", action="store_true", help="open in reveal.js scroll view instead of paged slides")
    ap.add_argument("--upload", action="store_true")
    ap.add_argument("--draft", help="Postplan draft id to update in place")
    ap.add_argument("--description", default="")
    a = ap.parse_args()

    body = pathlib.Path(a.source).read_text()
    asset = lambda n: (ASSETS / n).read_text()
    view = ", view: 'scroll'" if a.scroll else ""
    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{a.title}</title>
<style>{asset('reveal.min.css')}</style>
<style>{asset('black.min.css')}</style>
<style>{asset('hljs-theme.min.css')}</style>
<style>{CSS}</style>
</head>
<body>
<div class="reveal"><div class="slides">
{body}
</div></div>
<script>{asset('reveal.min.js')}</script>
<script>{asset('hljs.min.js')}</script>
<script>
Reveal.initialize({{ hash: true, slideNumber: 'c/t', transition: 'fade', width: 1280, height: 720, margin: 0.05, center: false{view} }});
Reveal.on('ready', function () {{ document.querySelectorAll('pre code').forEach(function (el) {{ hljs.highlightElement(el); }}); }});
</script>
</body>
</html>
"""
    out = pathlib.Path(a.out)
    out.write_text(html)
    print(f"wrote {out} ({out.stat().st_size} bytes)")
    if a.upload:
        cmd = ["postplan"] if shutil.which("postplan") else ["npx", "-y", "postplan"]
        cmd.append("upload")
        cmd += ["--draft", a.draft] if a.draft else ["--new"]
        if a.description:
            cmd += ["--description", a.description]
        cmd.append(str(out))
        sys.exit(subprocess.call(cmd))

if __name__ == "__main__":
    main()
