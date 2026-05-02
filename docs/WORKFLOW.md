# n8n Workflow Guide

The workflow template lives at `workflow/instagram-spy-google-sheets.json`.

## Nodes

| Node | Purpose |
| --- | --- |
| `Instagram Post Webhook` | Receives JSON payloads from the Python monitor. |
| `Log Post Snapshot` | Appends payload data into Google Sheets. |
| `Build Viral Alert` | Builds a Discord message only when a post is viral. |
| `Send Discord Alert` | Sends the viral alert to Discord. |

## Import Steps

1. Import `workflow/instagram-spy-google-sheets.json` into n8n.
2. Open `Log Post Snapshot` and connect Google Sheets credentials.
3. Replace `YOUR_GOOGLE_SHEET_ID` with your spreadsheet ID.
4. Create or select a sheet tab named `Instagram Spy`.
5. Add the columns listed in [PAYLOAD.md](PAYLOAD.md).
6. Open `Send Discord Alert` and connect your Discord webhook credential.
7. Activate the workflow.
8. Copy the production webhook URL into `N8N_WEBHOOK_URL`.

## Public Export Notes

The workflow is intentionally exported without:

- credential bindings
- webhook IDs
- private Google Sheet URLs
- Discord webhook URLs
- n8n instance metadata
