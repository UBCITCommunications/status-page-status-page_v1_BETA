# Snapshot provenance

Both files are copies of `https://status.it.ubc.ca/api/v2/summary.json`, the public Statuspage summary. Times inside the files are as published, with the page's own offset (`-08:00`, the page is set to America/Los_Angeles).

## summary-2026-11-12.json: reconstructed

- Captured: page `updated_at` 2026-11-12 22:36:17 PST.
- Source: a copy pasted into a chat session, rebuilt into a file afterwards. It is not the raw download.
- Kept as published: every component's id, name, status, group and created/updated times; every open incident's and maintenance window's id, name, status, impact, created/started/updated/resolved times, scheduled window and shortlink; for each update its status, time and affected components with old and new status.
- Changed: long update texts were shortened. The M365 incident's updates keep their "next update" sentences verbatim. Other updates keep their first sentence or two.
- Left out: component descriptions and `showcase`, update ids and their `updated_at` times, and the full component copies inside each incident. So checks that need these (edited updates, uptime display) only run on the 14 Nov snapshot.

## summary-2026-11-14.json: transcribed, content complete

- Captured: page `updated_at` 2026-11-14 22:09:14 PST.
- Source: a copy pasted into a chat session, transcribed into this file.
- Kept as published: every status, time, impact, update text (verbatim), update id, created/updated/display time, and affected-component list.
- Left out: fields the review doesn't use (`page_id`, `start_date`, `only_show_if_degraded`, the full component copies inside each incident, and some component descriptions).
- To make this byte-exact, replace it with the raw file saved on that date and run `python3 scripts/embed-snapshots.py`.

## Going forward

Save raw files unchanged, named by capture time:

```bash
curl -s https://status.it.ubc.ca/api/v2/summary.json -o data/snapshots/summary-$(date +%Y-%m-%d-%H%M).json
```

Then run `python3 scripts/embed-snapshots.py`. The page shows the newest snapshot and compares it with the one before.
