# GreenGold Bioscience — Website

Marketing website for GreenGold Bioscience — a B2B science company bridging novel
raw materials and delivery-system technology to the global cosmetics industry.

Built as a **Django + Wagtail** CMS so non-developers can edit pages and forms, with
a built-in **lead/contact backend** in the admin. Server-rendered for strong SEO.

- **Framework:** Django 5.2 (LTS) + Wagtail 7
- **DB:** PostgreSQL (Supabase in production; SQLite locally)
- **Styling:** Tailwind CSS (standalone CLI — no Node) + Alpine.js
- **Email:** Resend via django-anymail
- **Host:** Railway (Docker); media on Supabase Storage (optional)

## Pages

Home · Delivery Systems · Cosmetic Formulation · Ingredients Portfolio ·
Partner With Us · About · Contact (two audience intake forms).

All content is editable in the Wagtail admin (`/admin/`). Page sections are built
from reusable StreamField blocks; the two contact forms feed the **Leads** CRM
(`/django-admin/leads/lead/`, with CSV export) and email a notification on submit.

---

## Local development

Requires Python 3.12 and (recommended) [uv](https://github.com/astral-sh/uv).

```bash
# 1. Environment
uv venv --python 3.12
uv pip install -r requirements-dev.txt

# 2. Local env (defaults give SQLite + console email — no secrets needed)
cp .env.example .env   # or just create .env with DJANGO_SETTINGS_MODULE=greengold.settings.dev

# 3. Build CSS (downloads of the Tailwind binary: see scripts/build_css.sh)
./scripts/build_css.sh            # one-off  (or: ./scripts/build_css.sh --watch)

# 4. Database + starter content
.venv/bin/python manage.py migrate
.venv/bin/python manage.py seed_site        # creates the page tree with on-brand copy
.venv/bin/python manage.py createsuperuser   # for the admin

# 5. Run
.venv/bin/python manage.py runserver
```

Visit `http://localhost:8000/` (site) and `http://localhost:8000/admin/` (Wagtail).

Submitted leads (console-email locally) appear under **Django admin → Leads**.

## Tests

```bash
.venv/bin/python -m pytest
```

---

## Deployment

### 1. Supabase (database, + optional media storage)

1. Create a Supabase project.
2. Copy the **pooled** connection string → this is `DATABASE_URL`
   (`postgres://...@...:6543/postgres`).
3. (Optional) Create a Storage bucket for CMS media and an S3 access key →
   `AWS_STORAGE_BUCKET_NAME`, `AWS_S3_ENDPOINT_URL`, `AWS_ACCESS_KEY_ID`,
   `AWS_SECRET_ACCESS_KEY`. Leave these blank to keep media on the container disk.

### 2. Resend (email)

Create an API key and verify your sending domain → `RESEND_API_KEY`,
`DEFAULT_FROM_EMAIL`, `CONTACT_TO_EMAIL`.

### 3. Railway

This repo ships a `Dockerfile` and `railway.json`. Create a Railway service from
the repo and set these environment variables (see `.env.example`):

| Variable | Notes |
|----------|-------|
| `DJANGO_SETTINGS_MODULE` | `greengold.settings.production` |
| `SECRET_KEY` | long random string |
| `ALLOWED_HOSTS` | e.g. `greengoldbioscience.com,*.up.railway.app` |
| `CSRF_TRUSTED_ORIGINS` | e.g. `https://greengoldbioscience.com,https://*.up.railway.app` |
| `DATABASE_URL` | Supabase pooled connection string |
| `RESEND_API_KEY`, `DEFAULT_FROM_EMAIL`, `CONTACT_TO_EMAIL` | email |
| `WAGTAILADMIN_BASE_URL` | e.g. `https://greengoldbioscience.com` |
| `AWS_*` | only if using Supabase Storage for media |

The container runs `migrate` then `gunicorn` (binds `$PORT`). After the first
deploy, create an admin user and seed content via the Railway shell:

```bash
python manage.py createsuperuser
python manage.py seed_site   # optional: only for a fresh site
```

Point your domain at the Railway service and you're live.

> CSS note: `greengold/static/css/site.css` is committed and collected at image
> build, so the production image needs neither Node nor the Tailwind binary.
> Re-run `./scripts/build_css.sh` and commit the result whenever templates change.
