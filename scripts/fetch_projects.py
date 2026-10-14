#!/usr/bin/env python3
"""Haalt de projecten-feed van Bruinsma op en schrijft assets/data/projecten.json.

Gebruikt alleen de standaardbibliotheek. Lukt het ophalen of verwerken niet,
dan blijft het bestaande JSON-bestand staan zodat de site gewoon blijft werken.

Gebruik:
  python3 scripts/fetch_projects.py                 # haalt de live feed op
  python3 scripts/fetch_projects.py --file feed.xml # leest een lokaal bestand
"""
import argparse
import html
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

FEED_URL = "https://bruinsmakantoor.nl/ict/projecten/feed/"
OUTPUT = Path(__file__).resolve().parent.parent / "assets" / "data" / "projecten.json"
MAX_ITEMS = 6
EXCERPT_LENGTH = 180

NS = {"content": "http://purl.org/rss/1.0/modules/content/"}


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (portfolio feed sync)"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read()


def strip_html(value):
    text = re.sub(r"(?is)<(script|style).*?</\1>", " ", value or "")
    text = re.sub(r"<[^>]+>", " ", text)
    text = html.unescape(text)
    # WordPress sluit samenvattingen af met "[…]" of "The post ... appeared first on ..."
    text = re.sub(r"\[\s*(…|\.\.\.)\s*\]", "", text)
    text = re.sub(r"The post .* appeared first on .*$", "", text)
    return re.sub(r"\s+", " ", text).strip()


def excerpt(text):
    if len(text) <= EXCERPT_LENGTH:
        return text
    cut = text[:EXCERPT_LENGTH].rsplit(" ", 1)[0].rstrip(",.;:")
    return cut + "…"


def safe_url(value):
    value = (value or "").strip()
    return value if value.startswith(("https://", "http://")) else ""


def parse(xml_bytes):
    root = ET.fromstring(xml_bytes)
    projects = []
    for item in root.iter("item"):
        title = strip_html(item.findtext("title"))
        link = safe_url(item.findtext("link"))
        if not title or not link:
            continue
        date = ""
        if item.findtext("pubDate"):
            try:
                date = parsedate_to_datetime(item.findtext("pubDate")).astimezone(timezone.utc).date().isoformat()
            except (TypeError, ValueError):
                pass
        summary = strip_html(item.findtext("description"))
        if not summary:
            summary = strip_html(item.findtext("content:encoded", namespaces=NS))
        projects.append({
            "title": title,
            "link": link,
            "date": date,
            "excerpt": excerpt(summary),
            "categories": [strip_html(c.text) for c in item.findall("category") if c.text][:3],
        })
        if len(projects) >= MAX_ITEMS:
            break
    return projects


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="lees de feed uit een lokaal bestand")
    args = parser.parse_args()
    try:
        data = Path(args.file).read_bytes() if args.file else fetch(FEED_URL)
        projects = parse(data)
    except Exception as exc:  # netwerk- of parsefout: bestaande data behouden
        print(f"Feed niet bijgewerkt: {exc}", file=sys.stderr)
        return 0
    if not projects:
        print("Feed bevat geen projecten, bestaande data blijft staan.", file=sys.stderr)
        return 0
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(projects, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"{len(projects)} projecten geschreven naar {OUTPUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
