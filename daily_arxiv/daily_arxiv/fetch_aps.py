#!/usr/bin/env python3
import argparse
import html
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from collections import OrderedDict

import requests


RSS_NS = {
    "rss": "http://purl.org/rss/1.0/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "content": "http://purl.org/rss/1.0/modules/content/",
}


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, required=True, help="output jsonline file")
    return parser.parse_args()


def parse_feeds_config(config_value: str) -> list[tuple[str, str]]:
    if not config_value or not config_value.strip():
        raise ValueError("APS_FEEDS is required")

    parsed = []
    for raw_item in config_value.split(","):
        item = raw_item.strip()
        if not item:
            continue
        if "=" not in item:
            raise ValueError(f"Invalid APS_FEEDS item: {item}")

        category, url = item.split("=", 1)
        category = category.strip()
        url = url.strip()
        if not category or not url:
            raise ValueError(f"Invalid APS_FEEDS item: {item}")
        parsed.append((category, url))

    if not parsed:
        raise ValueError("APS_FEEDS did not contain any valid feed mappings")
    return parsed


def clean_html_text(raw_text: str) -> str:
    text = html.unescape(raw_text or "")
    text = re.sub(r"<math.*?</math>", " ", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_summary(item: ET.Element) -> str:
    description = item.findtext("rss:description", default="", namespaces=RSS_NS)
    encoded = item.findtext("content:encoded", default="", namespaces=RSS_NS)

    for source in (description, encoded):
        if not source:
            continue

        paragraphs = re.findall(r"<p>(.*?)</p>", source, flags=re.DOTALL | re.IGNORECASE)
        for paragraph in paragraphs:
            summary = clean_html_text(paragraph)
            if summary and not summary.startswith("Author(s):"):
                return summary

    cleaned = clean_html_text(description or encoded)
    cleaned = re.sub(r"^Author\(s\):.*?(?=\[Phys\. Rev\.|\Z)", "", cleaned).strip()
    cleaned = re.sub(r"\[Phys\. Rev\..*?$", "", cleaned).strip()
    return cleaned


def split_authors(raw_authors: str) -> list[str]:
    cleaned = clean_html_text(raw_authors)
    cleaned = re.sub(r"^Author\(s\):\s*", "", cleaned)
    if not cleaned:
        return []

    authors = re.split(r"\s*,\s*and\s+|\s+and\s+|\s*,\s*", cleaned)
    return [author.strip() for author in authors if author.strip()]


def parse_feed(session: requests.Session, category: str, feed_url: str) -> list[dict]:
    response = session.get(feed_url, timeout=30)
    response.raise_for_status()

    root = ET.fromstring(response.text)
    items = []

    for item in root.findall("rss:item", RSS_NS):
        doi = item.findtext("dc:identifier", default="", namespaces=RSS_NS)
        doi = doi.removeprefix("doi:").strip()
        if not doi:
            continue

        title = item.findtext("rss:title", default="", namespaces=RSS_NS).strip()
        link = item.findtext("rss:link", default="", namespaces=RSS_NS).strip()
        authors = split_authors(item.findtext("dc:creator", default="", namespaces=RSS_NS))
        summary = extract_summary(item)

        if not title or not link or not summary:
            continue

        items.append(
            {
                "id": doi,
                "categories": [category],
                "authors": authors,
                "title": title,
                "comment": None,
                "summary": summary,
                "abs": link.replace("http://", "https://"),
            }
        )

    return items


def merge_items(items: list[dict], paper_limit: int) -> list[dict]:
    merged: OrderedDict[str, dict] = OrderedDict()

    for item in items:
        existing = merged.get(item["id"])
        if existing is not None:
            for category in item["categories"]:
                if category not in existing["categories"]:
                    existing["categories"].append(category)
            continue

        if paper_limit and len(merged) >= paper_limit:
            continue

        merged[item["id"]] = item

    return list(merged.values())


def main():
    args = parse_args()
    paper_limit = int(os.environ.get("PAPER_LIMIT", "0") or "0")
    feeds = parse_feeds_config(os.environ.get("APS_FEEDS", ""))

    session = requests.Session()
    session.headers.update({"User-Agent": "aps-rss-ai/1.0"})

    all_items = []
    for category, feed_url in feeds:
        print(f"Fetching APS feed '{category}' from {feed_url}", file=sys.stderr)
        all_items.extend(parse_feed(session, category, feed_url))

    merged_items = merge_items(all_items, paper_limit)
    print(f"Collected {len(merged_items)} APS items", file=sys.stderr)

    with open(args.data, "w", encoding="utf-8") as file_obj:
        for item in merged_items:
            file_obj.write(json.dumps(item, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"APS fetch failed: {exc}", file=sys.stderr)
        sys.exit(1)
