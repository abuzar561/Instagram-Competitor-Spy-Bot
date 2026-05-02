# Security Policy

## Supported Version

The `main` branch is the supported version of this project.

## Reporting a Vulnerability

Please report security issues through GitHub Security Advisories for this repository.

## Credential Safety

- Never commit `.env`, Instagram login credentials, n8n webhook URLs, Discord webhook URLs, Google Sheet IDs, or exported workflow credential bindings.
- Rotate any credential or webhook that was accidentally committed to a public repository.
- Use n8n credential storage for Google Sheets and Discord integrations.
- Treat monitored accounts and post history as potentially sensitive business intelligence.
