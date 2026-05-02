# Instagram Competitor Spy Bot

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?logo=python&logoColor=white)
![n8n](https://img.shields.io/badge/n8n-workflow%20automation-EA4B71?logo=n8n&logoColor=white)
![Google Sheets](https://img.shields.io/badge/Google%20Sheets-reporting-34A853?logo=googlesheets&logoColor=white)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)

A social media intelligence automation that monitors public Instagram competitor accounts, calculates engagement rates for recent posts, sends new post snapshots to n8n, logs them in Google Sheets, and triggers Discord alerts for posts that cross a viral threshold.

## What This Project Does

- Scrapes recent public posts from one or more configured Instagram accounts.
- Calculates engagement rate with `(likes + comments) / followers * 100`.
- Uses a local history file to avoid sending the same post repeatedly.
- Sends structured JSON payloads to an n8n webhook.
- Includes a sanitized n8n workflow template for Google Sheets logging and Discord alerts.
- Ships with setup docs, payload docs, examples, validation checks, and GitHub Actions CI.

## Architecture

```mermaid
flowchart LR
    A["Scheduled Python monitor"] --> B["Instaloader public profile fetch"]
    B --> C["Engagement scoring"]
    C --> D["n8n webhook"]
    D --> E["Google Sheets log"]
    E --> F["Viral alert filter"]
    F --> G["Discord notification"]
```

## Project Structure

```text
.
+-- spy.py
+-- src/
|   +-- instagram_spy_bot.py
+-- workflow/
|   +-- instagram-spy-google-sheets.json
|   +-- README.md
+-- docs/
|   +-- PAYLOAD.md
|   +-- SETUP.md
|   +-- TROUBLESHOOTING.md
|   +-- WORKFLOW.md
+-- examples/
|   +-- payload.example.json
+-- scripts/
|   +-- validate-project.js
+-- requirements.txt
+-- .env.example
```

## Quick Start

```bash
git clone https://github.com/abuzar561/Instagram-Competitor-Spy-Bot.git
cd Instagram-Competitor-Spy-Bot
python -m venv .venv
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:COMPETITORS = "competitor_one,competitor_two"
$env:N8N_WEBHOOK_URL = "https://your-n8n-instance/webhook/instagram-spy"
python spy.py --dry-run
```

macOS or Linux:

```bash
source .venv/bin/activate
pip install -r requirements.txt
COMPETITORS="competitor_one,competitor_two" \
N8N_WEBHOOK_URL="https://your-n8n-instance/webhook/instagram-spy" \
python spy.py --dry-run
```

Remove `--dry-run` after confirming the payload is correct and your n8n workflow is active.

## Configuration

| Variable | Required | Description |
| --- | --- | --- |
| `COMPETITORS` | Yes | Comma-separated Instagram usernames without `@`. |
| `N8N_WEBHOOK_URL` | Required outside dry-run | Production n8n webhook URL. |
| `POSTS_TO_CHECK` | No | Number of recent posts per account. Defaults to `5`. |
| `VIRAL_THRESHOLD_PERCENT` | No | Engagement threshold for viral alerts. Defaults to `2.0`. |
| `HISTORY_FILE` | No | Local JSON file for deduplication. Defaults to `sent_posts_history.json`. |
| `INSTAGRAM_USERNAME` | No | Optional Instagram login username. Use only when permitted. |
| `INSTAGRAM_PASSWORD` | No | Optional Instagram login password. Never commit it. |

See [.env.example](.env.example) for a complete template.

## n8n Workflow

Import [workflow/instagram-spy-google-sheets.json](workflow/instagram-spy-google-sheets.json) into n8n, connect your Google Sheets and Discord credentials, replace placeholder values, and activate the workflow.

Detailed workflow instructions are in [docs/WORKFLOW.md](docs/WORKFLOW.md).

## Validation

```bash
node scripts/validate-project.js
python -m py_compile spy.py src/instagram_spy_bot.py
```

GitHub Actions runs these checks on every push and pull request.

## Responsible Use

Use this project only with accounts and data you are allowed to access. Respect Instagram's terms, rate limits, privacy rules, and local laws. Prefer official APIs or first-party analytics where possible, and keep request frequency conservative.

## License

This project is licensed under the [MIT License](LICENSE).
