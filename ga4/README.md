# Local traffic data (not committed)

Put `ga4-data.js` here to turn on the Traffic page. Everything in this folder except this README is ignored by git.

Build it from your GA4 CSV exports:

```bash
python3 scripts/ga4-to-js.py ~/Downloads/ga4-exports/
```

Or skip this folder and drop the CSVs on the Traffic page instead; they're read in the browser only.

The file holds aggregated counts (views, users, sessions) and no personal data, but it is internal analytics: keep it out of the repository and shared copies.
