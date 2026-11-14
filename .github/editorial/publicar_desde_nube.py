# -*- coding: utf-8 -*-
"""
Autonomous Cloud Daily Publisher & Stock Inspector for PB Ideas Virtuales.

Publishing policy:
- Technical blogs (carpentry_blog, rv_camper_blog, electric_blog): 1 article per day EACH.
- Radio blogs (country_radio_blog, christmas_radio_blog, radios_mexico_blog):
  1 article total every 2 days rotating across the 3 radio blogs (= 1 every 6 days per radio blog).

Rebuilds HTML + sitemap via motor_nube.py once per run and tracks per-blog stock health.
"""

import argparse
import json
import os
import sys
from datetime import date, datetime
from pathlib import Path

EDITORIAL_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(EDITORIAL_DIR))

from motor_nube import (  # noqa: E402
    ARG_TZ,
    BLOG_CONFIGS,
    REPO_DIR,
    SITE_URL,
    auditar_politicas_estrictas,
    rebuild_blogs,
    today_arg_str,
)

PUBLISHED_PATH = EDITORIAL_DIR / "articulos_publicados.json"
VAULT_PATH = EDITORIAL_DIR / "boveda_editorial.json"

TECH_BLOGS = ("carpentry_blog", "rv_camper_blog", "electric_blog")
RADIO_BLOGS = ("country_radio_blog", "christmas_radio_blog", "radios_mexico_blog")
RADIO_INTERVAL_DAYS = 2  # 3 radio blogs rotating every 2 days => 1 post every 6 days each

DEFAULT_SAFETY_TOTAL = 15
DEFAULT_CRITICAL_TOTAL = 5
DEFAULT_TECH_SAFETY_DAYS = 5
DEFAULT_TECH_CRITICAL_DAYS = 3


def _load_json(path: Path, default):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def _save_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def _default_vault() -> dict:
    return {
        "safety_threshold": DEFAULT_SAFETY_TOTAL,
        "critical_alert_threshold": DEFAULT_CRITICAL_TOTAL,
        "tech_safety_threshold": DEFAULT_TECH_SAFETY_DAYS,
        "tech_critical_threshold": DEFAULT_TECH_CRITICAL_DAYS,
        "radio_interval_days": RADIO_INTERVAL_DAYS,
        "last_published": None,
        "last_blog": None,
        "last_published_per_blog": {},
        "last_radio_published": None,
        "last_radio_blog": None,
        "last_run_at": None,
        "remaining_count": 0,
        "queue": [],
        "history": [],
    }


def _write_github_outputs(metrics: dict) -> None:
    """Write key=value outputs to $GITHUB_OUTPUT when executing under GitHub Actions."""
    gh_out = os.environ.get("GITHUB_OUTPUT")
    if not gh_out:
        return
    with open(gh_out, "a", encoding="utf-8") as fh:
        for k, v in metrics.items():
            safe_val = str(v).replace("\n", " ").strip()
            fh.write(f"{k}={safe_val}\n")


def _compute_last_dates(published: list, vault: dict) -> dict:
    """Return most recent YYYY-MM-DD publish date per blog from published log and vault."""
    dates = dict(vault.get("last_published_per_blog") or {})
    for art in published:
        blog = art.get("blog")
        art_date = art.get("date") or ""
        if blog and art_date > dates.get(blog, ""):
            dates[blog] = art_date
    return dates


def _compute_last_radio_state(published: list, vault: dict) -> tuple:
    """Return (last_radio_date_str_or_None, last_radio_blog_or_None)."""
    best_date = vault.get("last_radio_published") or ""
    best_blog = vault.get("last_radio_blog")
    for art in published:
        if art.get("blog") in RADIO_BLOGS:
            art_date = art.get("date") or ""
            if art_date >= best_date and art_date:
                best_date = art_date
                best_blog = art.get("blog")
    return (best_date or None), best_blog


def _pop_next_for_blog(queue: list, target_blog: str, published_slugs: set):
    """Pop and return (article_dict, cleaned_queue) for the first eligible item of target_blog."""
    for idx, item in enumerate(queue):
        if item["slug"] in published_slugs:
            continue
        if item["blog"] == target_blog:
            art = queue.pop(idx)
            cleaned = [q for q in queue if q["slug"] != art["slug"] and q["slug"] not in published_slugs]
            return art, cleaned
    return None, queue


def _next_due_radio_blog(queue: list, last_radio_blog: str, published_slugs: set):
    """Pick next radio blog in round-robin order that has queued content."""
    if last_radio_blog in RADIO_BLOGS:
        start = (RADIO_BLOGS.index(last_radio_blog) + 1) % len(RADIO_BLOGS)
    else:
        start = 0
    order = [RADIO_BLOGS[(start + offset) % len(RADIO_BLOGS)] for offset in range(len(RADIO_BLOGS))]
    for candidate in order:
        if any(q["blog"] == candidate and q["slug"] not in published_slugs for q in queue):
            return candidate
    return None


def _pick_any_tech_fallback(queue: list, published_slugs: set):
    """Pick first queued technical article (used only when --force runs on an already-published day)."""
    for item in queue:
        if item["blog"] in TECH_BLOGS and item["slug"] not in published_slugs:
            return item["blog"]
    for item in queue:
        if item["slug"] not in published_slugs:
            return item["blog"]
    return None


def _summarize_stock(pending: list, vault: dict) -> dict:
    """Compute global, per-blog, technical minimum runway, and radio queue metrics."""
    per_blog = {b: 0 for b in (*TECH_BLOGS, *RADIO_BLOGS)}
    for item in pending:
        per_blog[item["blog"]] = per_blog.get(item["blog"], 0) + 1

    tech_counts = [per_blog[b] for b in TECH_BLOGS]
    tech_remaining = sum(tech_counts)
    min_tech_stock = min(tech_counts) if tech_counts else 0
    radio_remaining = sum(per_blog[b] for b in RADIO_BLOGS)

    safety_total = int(vault.get("safety_threshold", DEFAULT_SAFETY_TOTAL))
    critical_total = int(vault.get("critical_alert_threshold", DEFAULT_CRITICAL_TOTAL))
    tech_safety = int(vault.get("tech_safety_threshold", DEFAULT_TECH_SAFETY_DAYS))
    tech_critical = int(vault.get("tech_critical_threshold", DEFAULT_TECH_CRITICAL_DAYS))

    needs_refill = (len(pending) < safety_total) or (min_tech_stock < tech_safety)
    critical_alert = (len(pending) <= critical_total) or (min_tech_stock <= tech_critical)

    return {
        "remaining_count": len(pending),
        "tech_remaining": tech_remaining,
        "radio_remaining": radio_remaining,
        "min_tech_stock": min_tech_stock,
        "safety_threshold": safety_total,
        "critical_alert_threshold": critical_total,
        "tech_safety_threshold": tech_safety,
        "tech_critical_threshold": tech_critical,
        "needs_refill": needs_refill,
        "critical_alert": critical_alert,
        "pending_per_blog": per_blog,
    }


def check_stock() -> dict:
    """Inspect current editorial vault stock without mutating state."""
    vault = _load_json(VAULT_PATH, _default_vault())
    published = _load_json(PUBLISHED_PATH, [])
    published_slugs = {a["slug"] for a in published}
    pending = [a for a in vault.get("queue", []) if a["slug"] not in published_slugs]
    last_dates = _compute_last_dates(published, vault)
    last_radio_date, last_radio_blog = _compute_last_radio_state(published, vault)
    summary = _summarize_stock(pending, vault)

    return {
        "published_total": len(published),
        "last_published": vault.get("last_published"),
        "last_blog": vault.get("last_blog"),
        "last_published_per_blog": last_dates,
        "last_radio_published": last_radio_date,
        "last_radio_blog": last_radio_blog,
        **summary,
    }


def audit_vault() -> dict:
    """Validate every queued vault article for schema, duplicates, assets, and policy compliance."""
    vault = _load_json(VAULT_PATH, {})
    queue = vault.get("queue", [])
    published = _load_json(PUBLISHED_PATH, [])
    published_slugs = {a["slug"] for a in published}

    required_fields = (
        "blog",
        "slug",
        "title",
        "hero_img",
        "hero_caption",
        "summary",
        "keywords",
        "faq_q",
        "faq_a",
        "body_html",
    )
    seen_queue_slugs = set()
    errors = []
    per_blog = {}

    for idx, art in enumerate(queue):
        label = art.get("slug") or f"index_{idx}"
        missing = [f for f in required_fields if not str(art.get(f, "")).strip()]
        if missing:
            errors.append(f"[{label}] Missing required fields: {', '.join(missing)}")
            continue

        blog_slug = art["blog"]
        if blog_slug not in BLOG_CONFIGS:
            errors.append(f"[{label}] Unknown blog slug: '{blog_slug}'")
            continue

        slug = art["slug"]
        if slug in published_slugs:
            errors.append(f"[{label}] Duplicate slug already present in articulos_publicados.json")
        if slug in seen_queue_slugs:
            errors.append(f"[{label}] Duplicate slug inside boveda_editorial.json queue")
        seen_queue_slugs.add(slug)

        hero_file = REPO_DIR / blog_slug / art["hero_img"]
        if not hero_file.exists():
            errors.append(f"[{label}] Missing hero_img file on disk: {hero_file}")

        combined_text = " ".join(
            str(art.get(k, "")) for k in ("title", "hero_caption", "summary", "keywords", "faq_q", "faq_a", "body_html")
        )
        try:
            auditar_politicas_estrictas(combined_text, f"vault:{label}")
        except SystemExit as exc:
            errors.append(str(exc).strip())

        per_blog[blog_slug] = per_blog.get(blog_slug, 0) + 1

    if errors:
        for err in errors:
            print(err, file=sys.stderr)
        raise SystemExit(f"Vault audit failed with {len(errors)} error(s).")

    return {
        "audit_passed": True,
        "queued_count": len(queue),
        "declared_remaining_count": vault.get("remaining_count"),
        "matches_remaining_count": vault.get("remaining_count") == len(queue),
        "per_blog": per_blog,
    }


def _collect_due_articles(queue: list, published: list, vault: dict, today_str: str, force: bool):
    """Select all due technical articles (1/day/blog) plus due radio article (1 every 2 days)."""
    published_slugs = {a["slug"] for a in published}
    last_dates = _compute_last_dates(published, vault)
    last_radio_date, last_radio_blog = _compute_last_radio_state(published, vault)
    today_dt = date.fromisoformat(today_str)
    interval_days = int(vault.get("radio_interval_days", RADIO_INTERVAL_DAYS))

    chosen = []

    for blog_slug in TECH_BLOGS:
        if last_dates.get(blog_slug) == today_str:
            continue
        art, queue = _pop_next_for_blog(queue, blog_slug, published_slugs)
        if art:
            chosen.append(art)
            published_slugs.add(art["slug"])
            last_dates[blog_slug] = today_str

    radio_due = (last_radio_date is None) or ((today_dt - date.fromisoformat(last_radio_date)).days >= interval_days)
    if radio_due:
        next_radio = _next_due_radio_blog(queue, last_radio_blog, published_slugs)
        if next_radio:
            art, queue = _pop_next_for_blog(queue, next_radio, published_slugs)
            if art:
                chosen.append(art)
                published_slugs.add(art["slug"])
                last_dates[next_radio] = today_str
                last_radio_date = today_str
                last_radio_blog = next_radio

    if not chosen and force:
        fallback_blog = _pick_any_tech_fallback(queue, published_slugs)
        if fallback_blog:
            art, queue = _pop_next_for_blog(queue, fallback_blog, published_slugs)
            if art:
                chosen.append(art)
                published_slugs.add(art["slug"])
                last_dates[fallback_blog] = today_str
                if fallback_blog in RADIO_BLOGS:
                    last_radio_date = today_str
                    last_radio_blog = fallback_blog

    return chosen, queue, last_dates, last_radio_date, last_radio_blog


def publish_daily(force: bool = False) -> int:
    """Publish 1 article per technical blog daily + 1 radio article every 2 days."""
    today_str = today_arg_str()
    vault = _load_json(VAULT_PATH, _default_vault())
    published = _load_json(PUBLISHED_PATH, [])
    queue = vault.get("queue", [])

    chosen, queue, last_dates, last_radio_date, last_radio_blog = _collect_due_articles(
        queue, published, vault, today_str, force
    )

    published_slugs = {a["slug"] for a in published}
    pending_after = [a for a in queue if a["slug"] not in published_slugs]
    stock = _summarize_stock(pending_after, vault)

    if not chosen:
        print(
            f"All due blogs already published for {today_str} (ARG) or queue empty. "
            f"Remaining: {stock['remaining_count']} (min tech blog: {stock['min_tech_stock']})."
        )
        _write_github_outputs(
            {
                "changed": "false",
                "remaining_count": stock["remaining_count"],
                "min_tech_stock": stock["min_tech_stock"],
                "low_stock_warning": str(stock["needs_refill"]).lower(),
                "critical_alert": str(stock["critical_alert"]).lower(),
                "published_count": 0,
                "published_title": "",
                "published_url": "",
                "published_blog": "",
            }
        )
        return 0

    now_iso = datetime.now(ARG_TZ).isoformat()
    changed_blogs = []
    pub_urls = []

    for art in chosen:
        blog_slug = art["blog"]
        if art.get("hero_img"):
            hero_file = REPO_DIR / blog_slug / art["hero_img"]
            if not hero_file.exists():
                raise FileNotFoundError(f"Missing hero image on disk: {hero_file}")

        art["date"] = today_str
        published.append(art)
        if blog_slug not in changed_blogs:
            changed_blogs.append(blog_slug)

        pub_url = f"{SITE_URL}/{blog_slug}/{art['slug']}.html"
        pub_urls.append(pub_url)
        print(f"Published: [{blog_slug}] {art['title']}")
        print(f"Live URL : {pub_url}")

    rebuild_blogs(published, target_blogs=changed_blogs)

    # Refresh remaining metrics after appending chosen articles cleanly
    remaining = len(queue)
    stock = _summarize_stock(queue, vault)
    for idx, art in enumerate(chosen):
        vault.setdefault("history", []).append(
            {
                "slug": art["slug"],
                "title": art["title"],
                "blog": art["blog"],
                "published_date": today_str,
                "published_at": now_iso,
                "url": pub_urls[idx],
                "remaining_after": remaining,
            }
        )

    vault["queue"] = queue
    vault["tech_safety_threshold"] = int(vault.get("tech_safety_threshold", DEFAULT_TECH_SAFETY_DAYS))
    vault["tech_critical_threshold"] = int(vault.get("tech_critical_threshold", DEFAULT_TECH_CRITICAL_DAYS))
    vault["radio_interval_days"] = int(vault.get("radio_interval_days", RADIO_INTERVAL_DAYS))
    vault["last_published"] = today_str
    vault["last_blog"] = chosen[-1]["blog"]
    vault["last_published_per_blog"] = last_dates
    vault["last_radio_published"] = last_radio_date
    vault["last_radio_blog"] = last_radio_blog
    vault["last_run_at"] = now_iso
    vault["remaining_count"] = remaining

    _save_json(PUBLISHED_PATH, published)
    _save_json(VAULT_PATH, vault)

    summary_title = (
        chosen[0]["title"]
        if len(chosen) == 1
        else f"{len(chosen)} articles ({', '.join(changed_blogs)})"
    )
    print(
        f"Summary: Published {len(chosen)} article(s). "
        f"Remaining: {remaining} (tech={stock['tech_remaining']}, radios={stock['radio_remaining']}, "
        f"min_tech_blog={stock['min_tech_stock']})."
    )

    _write_github_outputs(
        {
            "changed": "true",
            "remaining_count": remaining,
            "min_tech_stock": stock["min_tech_stock"],
            "low_stock_warning": str(stock["needs_refill"]).lower(),
            "critical_alert": str(stock["critical_alert"]).lower(),
            "published_count": len(chosen),
            "published_title": summary_title,
            "published_url": pub_urls[0],
            "published_blog": ", ".join(changed_blogs),
        }
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="PB Ideas Virtuales Cloud Daily Publisher")
    parser.add_argument("--force", action="store_true", help="Publish even if due blogs already ran today")
    parser.add_argument("--check-stock", action="store_true", help="Print vault stock status as JSON and exit")
    parser.add_argument("--audit-vault", action="store_true", help="Validate schema, duplicates, assets & policy rules")
    args = parser.parse_args()

    if args.audit_vault:
        result = audit_vault()
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    if args.check_stock:
        status = check_stock()
        print(json.dumps(status, indent=2, ensure_ascii=False))
        return 0

    return publish_daily(force=args.force)


if __name__ == "__main__":
    raise SystemExit(main())
