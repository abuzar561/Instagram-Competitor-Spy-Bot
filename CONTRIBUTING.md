# Contributing

Thanks for improving Instagram Competitor Spy Bot.

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Checks

Run these checks before opening a pull request:

```bash
node scripts/validate-project.js
python -m py_compile spy.py src/instagram_spy_bot.py
```

## Guidelines

- Do not commit `.env`, Instagram credentials, n8n webhook URLs, Discord webhook URLs, Google Sheet IDs, or runtime history files.
- Keep scraping frequency conservative and respectful.
- Update docs when payload fields, environment variables, or workflow behavior changes.
- Test with `--dry-run` before sending data to a live workflow.
