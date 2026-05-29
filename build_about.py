"""One-off: merge about 2.html into about.html with local assets."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
src = ROOT / "about 2.html"
dst = ROOT / "about.html"
lines = src.read_text(encoding="utf-8", errors="replace").splitlines()

out: list[str] = []
i = 0
while i < len(lines):
    line = lines[i]

    # Replace nav brand block (opening <a> through closing </a>)
    if '<a href="index.html" class="nav-brand"' in line:
        out.append('  <a href="index.html" class="nav-brand" aria-label="Faustina — Home">')
        out.append(
            '    <img class="nav-brand-img" src="assets/name + logo.png" '
            'width="237" height="108" alt="" decoding="async" />'
        )
        out.append("  </a>")
        i += 1
        while i < len(lines) and lines[i].strip() != "</a>":
            i += 1
        if i < len(lines):
            i += 1
        continue

    # Replace giant hero photo line inside about-hero-photo
    if '<div class="about-hero-photo">' in line:
        out.append(line)
        i += 1
        if i < len(lines) and len(lines[i]) > 10000 and "<img" in lines[i]:
            out.append(
                '    <img src="assets/about-photo.png" '
                'alt="Faustina in a garden by a fountain" width="471" height="321" '
                'loading="lazy" decoding="async" />'
            )
            i += 1
        continue

    if "playground.html" in line and "<li>" in line:
        i += 1
        continue

    out.append(line)
    i += 1

text = "\n".join(out) + "\n"
text = text.replace('href="resume.pdf"', 'href="assets/resume.pdf"')
text = text.replace("href='resume.pdf'", "href='assets/resume.pdf'")
text = text.replace("mailto:your@email.com", "mailto:hello@faustina.design")
text = text.replace("Copyright &copy; 2025", "Copyright &copy; 2026")
dst.write_text(text, encoding="utf-8")
print(f"Wrote {dst} ({dst.stat().st_size} bytes)")
