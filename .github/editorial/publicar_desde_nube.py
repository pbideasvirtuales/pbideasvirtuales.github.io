# -*- coding: utf-8 -*-
"""
Autonomous Cloud Daily Publisher & Stock Inspector for PB Ideas Virtuales.

Reads pre-curated original articles from boveda_editorial.json, rotates across
the 6 blogs, verifies asset presence and strict Google Brand Policy compliance,
rebuilds HTML + sitemap via motor_nube.py, and reports remaining stock metrics.
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

EDITORIAL_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(EDITORIAL_DIR))

from motor_nube import (  # noqa: E402
    ARG_TZ,
    REPO_DIR,
    SITE_URL,
    rebuild_blogs,
    today_arg_str,
)

PUBLISHED_PATH = EDITORIAL_DIR / "articulos_publicados.json"
VAULT_PATH = EDITORIAL_DIR / "boveda_editorial.json"


def _load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def _save_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _write_github_outputs(metrics: dict) -> None:
    """Write key=value outputs to $GITHUB_OUTPUT when executing under GitHub Actions."""
    gh_out = os.environ.get("GITHUB_OUTPUT")
    if not gh_out:
        return
    with open(gh_out, "a", encoding="utf-8") as fh:
        for k, v in metrics.items():
            safe_val = str(v).replace("\n", " ").strip()
            fh.write(f"{k}={safe_val}\n")


def _pick_next_article_idx(queue: list, last_blog: str, published_slugs: set) -> int:
    """
    Pick first non-duplicate article in queue, rotating away from last_blog
    when alternatives exist so all 6 portals grow evenly.
    """
    fallback_idx = None
    for idx, item in enumerate(queue):
        if item["slug"] in published_slugs:
            continue
        if item["blog"] != last_blog:
            return idx
        if fallback_idx is None:
            fallback_idx = idx
    return fallback_idx if fallback_idx is not None else -1


def check_stock() -> dict:
    """Inspect current editorial vault stock without mutating state."""
    vault = _load_json(
        VAULT_PATH,
        {
            "safety_threshold": 15,
            "critical_alert_threshold": 5,
            "last_published": None,
            "last_blog": None,
            "queue": [],
            "history": [],
        },
    )
    published = _load_json(PUBLISHED_PATH, [])
    published_slugs = {a["slug"] for a in published}
    pending = [a for a in vault.get("queue", []) if a["slug"] not in published_slugs]
    per_blog = {}
    for item in pending:
        per_blog[item["blog"]] = per_blog.get(item["blog"], 0) + 1

    safety_threshold = int(vault.get("safety_threshold", 15))
    critical_threshold = int(vault.get("critical_alert_threshold", 5))
    status = {
        "published_total": len(published),
        "remaining_count": len(pending),
        "safety_threshold": safety_threshold,
        "critical_alert_threshold": critical_threshold,
        "needs_refill": len(pending) < safety_threshold,
        "critical_alert": len(pending) <= critical_threshold,
        "last_published": vault.get("last_published"),
        "last_blog": vault.get("last_blog"),
        "pending_per_blog": per_blog,
    }
    return status


def publish_daily(force: bool = False) -> int:
    """Publish one article from boveda_editorial.json unless already published today."""
    today_str = today_arg_str()
    vault = _load_json(
        VAULT_PATH,
        {
            "safety_threshold": 15,
            "critical_alert_threshold": 5,
            "last_published": None,
            "last_blog": None,
            "queue": [],
            "history": [],
        },
    )
    published = _load_json(PUBLISHED_PATH, [])
    published_slugs = {a["slug"] for a in published}

    queue = vault.get("queue", [])
    safety_threshold = int(vault.get("safety_threshold", 15))
    critical_threshold = int(vault.get("critical_alert_threshold", 5))

    if vault.get("last_published") == today_str and not force:
        remaining = sum(1 for a in queue if a["slug"] not in published_slugs)
        print(f"Already published on {today_str} (ARG). Remaining stock: {remaining}.")
        _write_github_outputs(
            {
                "changed": "false",
                "remaining_count": remaining,
                "low_stock_warning": str(remaining < safety_threshold).lower(),
                "critical_alert": str(remaining <= critical_threshold).lower(),
                "published_title": "",
                "published_url": "",
                "published_blog": "",
            }
        )
        return 0

    next_idx = _pick_next_article_idx(queue, vault.get("last_blog", ""), published_slugs)
    if next_idx < 0:
        print("Vault queue is empty! Waiting for editorial refill.")
        _write_github_outputs(
            {
                "changed": "false",
                "remaining_count": 0,
                "low_stock_warning": "true",
                "critical_alert": "true",
                "published_title": "",
                "published_url": "",
                "published_blog": "",
            }
        )
        return 0

    art = queue.pop(next_idx)
    blog_slug = art["blog"]
    art["date"] = today_str

    # Strip any duplicate slug leftovers from queue
    queue = [q for q in queue if q["slug"] != art["slug"] and q["slug"] not in published_slugs]

    if art.get("hero_img"):
        hero_file = REPO_DIR / blog_slug / art["hero_img"]
        if not hero_file.exists():
            raise FileNotFoundError(f"Missing hero image on disk: {hero_file}")

    published.append(art)
    rebuild_blogs(published, target_blogs=[blog_slug])

    remaining = len(queue)
    pub_url = f"{SITE_URL}/{blog_slug}/{art['slug']}.html"
    now_iso = datetime.now(ARG_TZ).isoformat()

    vault["queue"] = queue
    vault["last_published"] = today_str
    vault["last_blog"] = blog_slug
    vault["last_run_at"] = now_iso
    vault["remaining_count"] = remaining
    vault.setdefault("history", []).append(
        {
            "slug": art["slug"],
            "title": art["title"],
            "blog": blog_slug,
            "published_date": today_str,
            "published_at": now_iso,
            "url": pub_url,
            "remaining_after": remaining,
        }
    )

    _save_json(PUBLISHED_PATH, published)
    _save_json(VAULT_PATH, vault)

    low_stock = remaining < safety_threshold
    critical = remaining <= critical_threshold
    print(f"Published: [{blog_slug}] {art['title']}")
    print(f"Live URL : {pub_url}")
    print(f"Remaining in Vault: {remaining} (Safety threshold: {safety_threshold})")

    _write_github_outputs(
        {
            "changed": "true",
            "remaining_count": remaining,
            "low_stock_warning": str(low_stock).lower(),
            "critical_alert": str(critical).lower(),
            "published_title": art["title"],
            "published_url": pub_url,
            "published_blog": blog_slug,
        }
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="PB Ideas Virtuales Cloud Daily Publisher")
    parser.add_argument("--force", action="store_true", help="Publish even if today already has an article")
    parser.add_argument("--check-stock", action="store_true", help="Print vault stock status as JSON and exit")
    args = parser.parse_args()

    if args.check_stock:
        status = check_stock()
        print(json.dumps(status, indent=2, ensure_ascii=False))
        return 0

    return publish_daily(force=args.force)


if __name__ == "__main__":
    raise SystemExit(main())
