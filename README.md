# Resume & Cover Letter API

A Flask (`flask-restx`) microservice that **generates tailored cover letters
and styled resume PDFs** from structured input. It combines a job-title
reconciler, skills extraction (RAKE keyword extraction + curated skill
lookups), a sentence-template engine, and WeasyPrint-based PDF rendering.

The generation engine lives in [`modules/`](modules/) and can be imported and
used **without** the Flask layer; `app.py` is just the HTTP interface over it.

## Architecture

```
app.py                      Flask REST API (the HTTP interface)
position_reconciler.py      Maps free-text job titles to canonical positions
modules/
  cover_letter_v2/          Cover-letter generation engine
    cover_letter_generator.py   Main orchestrator
    skill_lookups.py            Skill extraction from text
    cover_letter_html.py        HTML assembly
    templates/                  Sentence-template JSON
    generic_sentences/          Fallback sentence banks
  stylize_resume/           Resume -> styled PDF (WeasyPrint)
  external_apply/           External application helpers
weasyprint_css/             PDF stylesheets
```

## Key endpoints

| Method | Path | Purpose |
|--------|------|---------|
| POST | `/api/v1/create-job-application` | Generate a cover letter for one job |
| POST | `/api/v1/mass-create-job-applications` | Batch cover-letter generation |
| POST | `/api/v1/coverletter_as_html` | Return a cover letter as HTML |
| POST | `/api/v1/job-match` | Reconcile a job title to a known position |
| POST | `/api/v1/stylize_resume` | Render a resume to a styled PDF |
| GET  | `/api/v1/hello-world` | Health check |

## Setup

WeasyPrint and `cld2-cffi` need system libraries. On Debian/Ubuntu:

```bash
sudo apt-get install -y build-essential python3-dev python3-cffi \
  libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 \
  libffi-dev shared-mime-info

CFLAGS="-Wno-narrowing" pip install cld2-cffi
pip install -r requirements.txt
```

Run locally:

```bash
cp .env.example .env   # fill in values
python app.py          # dev server
# or: gunicorn --workers 3 --bind 0.0.0.0:5000 wsgi:app
```

## Configuration

Copy `.env.example` to `.env`. Anything S3-related is optional and only needed
if you enable persistence of generated documents; the core generation runs
fully locally. Never commit real credentials.

## Deployment

See [`deployment/`](deployment/) for sample `nginx`, `gunicorn` (systemd), and
`supervisord` configs. Replace the placeholder hosts/IPs with your own.

## License

MIT — see [LICENSE](LICENSE).
