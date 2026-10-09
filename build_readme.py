"""Refresh the "latest issues" block in README.md from the public feeds.

Standard library only. If a source cannot be read, its previous row is kept.
"""

import html
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

BASE = "https://rethinksci-gif.github.io"
README = Path(__file__).with_name("README.md")
ATOM = "{http://www.w3.org/2005/Atom}"
START, END = "<!-- latest starts -->", "<!-- latest ends -->"


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "rethinksci-readme"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8")


def md(text):
    """Make feed text safe for a Markdown table cell."""
    text = re.sub(r"\s+", " ", html.unescape(text)).strip()
    return text.replace("|", "\\|").replace("[", "\\[").replace("]", "\\]")


def latest_atom(path, label):
    entry = ET.fromstring(fetch(f"{BASE}/{path}")).find(f"{ATOM}entry")
    content = html.unescape(entry.findtext(f"{ATOM}content") or "")
    # Issues open with e.g. "From 23 items, 3 important content pieces were selected".
    counts = re.search(r"From (\d+) (\w+), (\d+)\b.*?selected", content)
    title = f"{label}: {counts[3]} picks from {counts[1]} {counts[2]}" if counts else entry.findtext(f"{ATOM}title")
    return {
        "title": md(title),
        "url": entry.find(f"{ATOM}link").get("href"),
        "date": entry.findtext(f"{ATOM}updated")[:10],
    }


def latest_rss(path):
    from email.utils import parsedate_to_datetime

    item = ET.fromstring(fetch(f"{BASE}/{path}")).find("channel/item")
    return {
        "title": md(item.findtext("title")),
        "url": item.findtext("link").strip(),
        "date": parsedate_to_datetime(item.findtext("pubDate")).date().isoformat(),
    }


def latest_electrification():
    site = f"{BASE}/electrification-intelligence-site"
    editions = re.findall(
        r"<loc>([^<]*/en/analyst-editions/(\d+)/)</loc>\s*<lastmod>(\d{4}-\d\d-\d\d)", fetch(f"{site}/sitemap.xml")
    )
    url, _, date = max(editions, key=lambda e: int(e[1]))
    title = re.search(r"<title>(.*?)</title>", fetch(url), re.S).group(1)
    return {"title": md(re.sub(r"\s*·\s*EI\s*$", "", html.unescape(title))), "url": url, "date": date}


SOURCES = [
    ("AIM4R", "Weekly · 中文 / EN", lambda: latest_atom("AIM4R/feed-en.xml", "Robotics & materials digest")),
    ("Plastic Signal Weekly", "Weekly · EN", lambda: latest_atom("plastic-signal-weekly/feed-en.xml", "Plastics brief")),
    ("Electrification Intelligence", "Editions · EN / 中文", latest_electrification),
    ("CCU Intelligence", "Biweekly · EN", lambda: latest_rss("ccu-intelligence/rss.xml")),
]


def main():
    readme = README.read_text(encoding="utf-8")
    head, rest = readme.split(START, 1)
    old_block, tail = rest.split(END, 1)
    rows = ["| Briefing | Latest issue | Date |", "| --- | --- | --- |"]
    for name, cadence, get in SOURCES:
        try:
            item = get()
            rows.append(f"| **{name}**<br><sub>{cadence}</sub> | [{item['title']}]({item['url']}) | {item['date']} |")
        except Exception as exc:  # keep the last good row rather than blanking it
            print(f"warning: {name}: {exc!r}", file=sys.stderr)
            previous = [r for r in old_block.splitlines() if r.startswith(f"| **{name}**")]
            rows.extend(previous[:1])
    block = "\n".join(rows)
    README.write_text(f"{head}{START}\n{block}\n{END}{tail}", encoding="utf-8")


if __name__ == "__main__":
    main()
