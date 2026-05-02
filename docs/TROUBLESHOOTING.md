# Troubleshooting

## No Competitors Configured

Set `COMPETITORS` or pass `--competitors`:

```bash
python spy.py --competitors competitor_one,competitor_two --dry-run
```

## Instagram Blocks or Rate Limits Requests

- Reduce schedule frequency.
- Monitor fewer accounts per run.
- Use official APIs or first-party analytics when possible.
- Avoid repeated manual retries after a block.

## n8n Does Not Receive Data

- Use the production webhook URL after activating the workflow.
- Confirm `N8N_WEBHOOK_URL` is set.
- Test with `--dry-run` first, then run without `--dry-run`.
- Check n8n execution logs for credential or schema errors.

## Google Sheets Columns Do Not Match

Create the columns listed in [PAYLOAD.md](PAYLOAD.md), or update the Google Sheets node mapping in n8n.

## Duplicate Posts Appear

- Confirm `HISTORY_FILE` points to a persistent local path.
- Do not run multiple copies of the script at the same time with the same history file.
- Delete the history file only when you intentionally want to reprocess posts.
