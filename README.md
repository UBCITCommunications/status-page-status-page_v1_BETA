# Status Page Status Page

A review of how a public [Atlassian Statuspage](https://www.atlassian.com/software/statuspage) status page communicates, built around the 12 November 2026 Microsoft 365 outage as seen on [status.it.ubc.ca](https://status.it.ubc.ca).

It doesn't judge whether services worked. It looks at what readers were told, and when: open incidents, update timing and promises, maintenance windows, the page's clock, and how the Statuspage editor shapes all of that. Findings are framed as process, not people.

## Open it

Open `index.html` in any browser. No server, no install, no build step, no network calls. It's one self-contained file, so it can also be attached or shared as is.

Pages: **Overview**, **Issues**, **Incidents**, **Maintenance**, **Traffic** (optional, see below), **Services**, **Method**. Each has its own link (`index.html#issues`).

## Data

| File | What it is |
|---|---|
| `data/snapshots/summary-2026-11-12.json` | Status page snapshot, 12 Nov 2026 22:36 PST. **Reconstructed** from a pasted copy; some text shortened. See `data/snapshots/NOTES.md`. |
| `data/snapshots/summary-2026-11-14.json` | Status page snapshot, 14 Nov 2026 22:09 PST. Statuses, times and texts as published; unused fields omitted. See `NOTES.md`. |
| `data/history-titles.json` | Titles of recently resolved incidents, from the page's public history feed (`/history.atom`), so traffic to older incident pages can be named. |

All of it is public: it comes from `https://status.it.ubc.ca/api/v2/summary.json` and `/history.atom`.

`index.html` carries an embedded copy of these files, because a page opened from disk can't read other local files. The JSON files are the source of truth. After adding or changing a snapshot:

```bash
python3 scripts/embed-snapshots.py           # re-embed data/ into index.html
python3 scripts/embed-snapshots.py --check   # confirm index.html matches data/
```

The page also accepts a fresh `summary.json` through **Load a snapshot** and compares it with the one shown.

## How findings are worked out

The **Method** page in the review is the full description. In short:

- **Affected now:** the services an incident's own latest update lists as not operational, checked against each service's current status.
- **Promises:** read from update text ("Next update is scheduled for 16:30 PCT", "tomorrow at 08:00", "Monday 10:00") and compared with when the next update was posted.
- **Edited updates:** an update whose last-changed time is more than a minute after it was created.
- **Changes:** two snapshots compared item by item.
- Each issue is shown as *what the data shows / likely cause / suggested fix*, tagged **Confirmed** (in the data, or tested on a Statuspage account) or **Likely** (best reading, still to check).

## Traffic layer (GA4): local only

The Traffic page lines up Google Analytics (GA4) counts with the incident timeline. **Traffic data is never committed.** The repository contains only public status page data.

Two ways to load it:

1. **Local file.** Export CSVs from GA4, then:
   ```bash
   python3 scripts/ga4-to-js.py ~/Downloads/ga4-exports/
   ```
   This writes `ga4/ga4-data.js`, which `index.html` loads if it's present. `.gitignore` excludes it.
2. **In the browser.** Drop GA4 CSV exports on the Traffic page. They're read in memory and gone when the page closes.

Without traffic data, the Traffic page shows a short note and everything else is unchanged.

Exports the page recognises (by column names):

| Export | Where in GA4 |
|---|---|
| Views by day | Reports → Engagement → Pages and screens, dimension **Date** (up to 13 months) |
| Views by hour | Same report, dimension **Date + hour (YYYYMMDDHH)**, with Page path and screen class |
| Views by minute | GA4 Query Explorer: dimensions `dateHourMinute` (+ `pagePath`), metrics `screenPageViews`, `activeUsers` |
| Sources | Reports → Acquisition → Traffic acquisition, **Session source / medium** + Page path and screen class |
| Top pages | Pages and screens, Page path and screen class, no date dimension |

Notes:

- GA4 reports this property's hours in **PST (UTC−8)**. The page converts them to absolute times and shows PST with PCT (UTC−7) alongside.
- Missing days or minutes are shown as gaps, never filled in. Days cut off by the export's end are marked as partial.
- Hourly data can't show whether people arrived before the first post within the same hour. Minute data can.

## Caveats

- One snapshot shows only what's open at that moment. Resolved incidents drop out, and posted updates can be edited without a visible record, so history needs regular snapshots.
- "Last edited" on a service changes with any edit, not only status changes.
- "Likely" causes still need checking with the team that runs the page.
- See `data/snapshots/NOTES.md` for exactly how each snapshot was captured.

## Repository layout

```
index.html                 the review (self-contained)
data/snapshots/            status page snapshots + NOTES.md (provenance)
data/history-titles.json   resolved incident titles from the public history feed
ga4/                       local traffic data goes here (not committed)
scripts/embed-snapshots.py re-embed and check snapshot data
scripts/ga4-to-js.py       GA4 CSV exports → ga4/ga4-data.js
```

Scripts need Python 3 and nothing else.

## Licence

MIT. See `LICENSE`.
