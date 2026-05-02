import argparse
import json
import os
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import instaloader
import requests


DEFAULT_POSTS_TO_CHECK = 5
DEFAULT_VIRAL_THRESHOLD_PERCENT = 2.0
DEFAULT_HISTORY_FILE = "sent_posts_history.json"


@dataclass
class PostSnapshot:
    competitor: str
    post_shortcode: str
    post_url: str
    image_url: str
    caption: str
    likes: int
    comments: int
    followers: int
    engagement_rate: float
    is_viral: bool
    viral_threshold_percent: float
    taken_at: str
    scraped_at: str


def parse_competitors(raw_value: str | None) -> list[str]:
    if not raw_value:
        return []

    return [
        username.strip().lstrip("@")
        for username in raw_value.split(",")
        if username.strip()
    ]


def load_history(path: Path) -> set[str]:
    if not path.exists():
        return set()

    try:
        return set(json.loads(path.read_text(encoding="utf-8")))
    except json.JSONDecodeError:
        backup_path = path.with_suffix(".invalid.json")
        path.replace(backup_path)
        print(f"History file was invalid JSON. Moved it to {backup_path.name}.")
        return set()


def save_history(path: Path, history: Iterable[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(sorted(set(history)), indent=2), encoding="utf-8")


def create_loader() -> instaloader.Instaloader:
    loader = instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False,
        quiet=True,
    )

    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")

    if username and password:
        loader.login(username, password)

    return loader


def build_snapshot(
    competitor: str,
    followers: int,
    post,
    viral_threshold_percent: float,
) -> PostSnapshot:
    likes = int(post.likes or 0)
    comments = int(post.comments or 0)
    engagement_rate = ((likes + comments) / followers) * 100 if followers else 0.0
    caption = (post.caption or "").replace("\r", " ").replace("\n", " ").strip()

    return PostSnapshot(
        competitor=competitor,
        post_shortcode=post.shortcode,
        post_url=f"https://www.instagram.com/p/{post.shortcode}/",
        image_url=str(post.url),
        caption=caption[:500],
        likes=likes,
        comments=comments,
        followers=followers,
        engagement_rate=round(engagement_rate, 2),
        is_viral=engagement_rate >= viral_threshold_percent,
        viral_threshold_percent=viral_threshold_percent,
        taken_at=post.date_utc.replace(tzinfo=timezone.utc).isoformat(),
        scraped_at=datetime.now(timezone.utc).isoformat(),
    )


def send_to_webhook(webhook_url: str, payload: dict) -> None:
    response = requests.post(webhook_url, json=payload, timeout=30)
    response.raise_for_status()


def monitor_competitors(
    competitors: list[str],
    posts_to_check: int,
    viral_threshold_percent: float,
    history_file: Path,
    webhook_url: str | None,
    dry_run: bool,
) -> list[PostSnapshot]:
    loader = create_loader()
    sent_posts = load_history(history_file)
    next_history = sent_posts.copy()
    snapshots: list[PostSnapshot] = []

    for competitor in competitors:
        print(f"Analyzing @{competitor}...")

        try:
            profile = instaloader.Profile.from_username(loader.context, competitor)
            followers = int(profile.followers or 0)
        except Exception as error:
            print(f"Failed to load @{competitor}: {error}")
            continue

        for index, post in enumerate(profile.get_posts()):
            if index >= posts_to_check:
                break

            if post.shortcode in sent_posts:
                print(f"Skipping already processed post {post.shortcode}.")
                continue

            snapshot = build_snapshot(
                competitor=competitor,
                followers=followers,
                post=post,
                viral_threshold_percent=viral_threshold_percent,
            )
            payload = asdict(snapshot)
            snapshots.append(snapshot)

            print(json.dumps(payload, indent=2))

            if dry_run:
                continue

            if not webhook_url:
                raise RuntimeError("N8N_WEBHOOK_URL is required unless --dry-run is used.")

            send_to_webhook(webhook_url, payload)
            next_history.add(post.shortcode)
            print(f"Sent {post.shortcode} to n8n.")

    if not dry_run:
        save_history(history_file, next_history)

    return snapshots


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Monitor competitor Instagram posts and send snapshots to n8n.")
    parser.add_argument(
        "--competitors",
        default=os.getenv("COMPETITORS"),
        help="Comma-separated Instagram usernames without @.",
    )
    parser.add_argument(
        "--posts-to-check",
        type=int,
        default=int(os.getenv("POSTS_TO_CHECK", str(DEFAULT_POSTS_TO_CHECK))),
        help="Number of recent posts to inspect per competitor.",
    )
    parser.add_argument(
        "--viral-threshold-percent",
        type=float,
        default=float(os.getenv("VIRAL_THRESHOLD_PERCENT", str(DEFAULT_VIRAL_THRESHOLD_PERCENT))),
        help="Engagement rate threshold used to mark a post as viral.",
    )
    parser.add_argument(
        "--history-file",
        default=os.getenv("HISTORY_FILE", DEFAULT_HISTORY_FILE),
        help="JSON file used to remember sent post shortcodes.",
    )
    parser.add_argument(
        "--webhook-url",
        default=os.getenv("N8N_WEBHOOK_URL"),
        help="Production n8n webhook URL.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print payloads without sending them or updating history.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    competitors = parse_competitors(args.competitors)

    if not competitors:
        raise SystemExit("No competitors configured. Set COMPETITORS or pass --competitors.")

    if args.posts_to_check < 1:
        raise SystemExit("--posts-to-check must be at least 1.")

    monitor_competitors(
        competitors=competitors,
        posts_to_check=args.posts_to_check,
        viral_threshold_percent=args.viral_threshold_percent,
        history_file=Path(args.history_file),
        webhook_url=args.webhook_url,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
