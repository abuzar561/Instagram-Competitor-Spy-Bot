# Setup Guide

## 1. Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 2. Configure Competitors

Create a local `.env` file or set environment variables in your scheduler:

```text
COMPETITORS=competitor_one,competitor_two
POSTS_TO_CHECK=5
VIRAL_THRESHOLD_PERCENT=2.0
N8N_WEBHOOK_URL=https://your-n8n-instance/webhook/instagram-spy
```

Do not commit `.env`.

## 3. Test Locally

Run a dry run first:

```bash
python spy.py --competitors competitor_one --dry-run
```

The script prints payloads and does not update the history file or send to n8n.

## 4. Connect n8n

Import `workflow/instagram-spy-google-sheets.json`, configure credentials, and activate the workflow. Copy the production webhook URL into `N8N_WEBHOOK_URL`.

## 5. Schedule

Use cron, Windows Task Scheduler, GitHub Actions, or another scheduler. Keep intervals conservative to avoid aggressive scraping.

Example cron schedule for every 4 hours:

```cron
0 */4 * * * cd /path/to/Instagram-Competitor-Spy-Bot && . .venv/bin/activate && python spy.py
```
