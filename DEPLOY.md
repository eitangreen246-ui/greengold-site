# Going Live — Deployment Guide (client-owned infra, your code)

## Ownership model for this project

| Thing | Owner | Notes |
|-------|-------|-------|
| **Source code** | **You** (`eitan green` GitHub, private repo) | You keep full control of the code. |
| **Railway** (hosting) | **Client** | You create it with the client's email, then hand over. |
| **Supabase** (database + image storage) | **Client** | Same — created with client's email. |
| **Resend** (email) | **Client** | Same. Emails send from the client's domain. |
| **Deploys** | Automatic | The client's Railway is connected to **your** GitHub repo; every `git push` auto-deploys. |

**Two things to coordinate up front:**
1. **Email verification** — sign-up confirmation emails for Railway/Supabase/Resend go to the
   **client's inbox**. Either set these up while you have access to that inbox, or have the
   client forward you the confirmation links/codes.
2. **Payment** — Railway and Supabase need a payment method for production use. The **client
   adds their own card** (don't enter the client's payment details for them). Do this during
   setup or at handover.

---

## Step 1 — Code → your GitHub (private)

```bash
cd ~/Desktop/greengold-site
./scripts/build_css.sh          # bake in latest styles
git init
git add .
git commit -m "Initial GreenGold website"
```

Create an empty **private** repo under your `eitan green` account at https://github.com/new
(name e.g. `greengold-site`, no README). Then:

```bash
git remote add origin https://github.com/<your-username>/greengold-site.git
git branch -M main
git push -u origin main
```

The repo stays private and under your account — the client never needs GitHub access.

---

## Step 2 — Create the client's Supabase (database)

Sign up at https://supabase.com **using the client's email**.

1. **New project** → name it, choose a region near the client's users, set a strong
   **database password** (save it).
2. After it provisions, click **Connect** → copy the **Session pooler** connection string:
   ```
   postgresql://postgres.<ref>:[YOUR-PASSWORD]@aws-0-<region>.pooler.supabase.com:5432/postgres
   ```
3. Put the real password in. This is your `DATABASE_URL` (used in Step 5).

> Use the **Session pooler** string (port 5432), not Transaction pooler (6543) — it works
> cleanly with Django's persistent connections.

---

## Step 3 — Create the client's Resend (email)

Sign up at https://resend.com **using the client's email**.

1. **API Keys → Create API Key** → copy it (`re_...`) → this is `RESEND_API_KEY`.
2. **Domains** → add the client's domain (`greengoldbioscience.com`) and create the DNS
   records they show at the domain registrar. Once verified, send from
   `hello@greengoldbioscience.com`.
3. *Testing before the domain is verified:* use `onboarding@resend.dev` as the sender to
   deliver to your own address, then switch to the client's domain later.

Values for Step 5:
- `RESEND_API_KEY` = `re_...`
- `DEFAULT_FROM_EMAIL` = `GreenGold Bioscience <hello@greengoldbioscience.com>`
- `CONTACT_TO_EMAIL` = the inbox where the client wants lead notifications

---

## Step 4 — (Recommended) Image storage on Supabase

CMS-uploaded images are wiped on each redeploy unless stored externally. Set this up before
the client starts uploading photos. *(All current site graphics are built-in SVGs, so launch
works without it.)*

1. Supabase → **Storage → New bucket** → name `media`, **Public**.
2. Supabase → Storage **S3 connection** → create S3 access keys.
3. Values for Step 5:
   - `AWS_STORAGE_BUCKET_NAME` = `media`
   - `AWS_S3_ENDPOINT_URL` = `https://<project-ref>.supabase.co/storage/v1/s3`
   - `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
   - `AWS_S3_REGION_NAME` = the project region (e.g. `eu-central-1`)

---

## Step 5 — Create the client's Railway + connect YOUR repo (auto-deploy)

Sign up at https://railway.app **using the client's email**.

### 5a. Connect your GitHub repo
1. **New Project → Deploy from GitHub repo**.
2. Click **Configure GitHub App** → in the GitHub window, **sign in as your own
   `eitan green` account** → grant Railway access to **only** the `greengold-site` repo.
3. Back in Railway, select `greengold-site`. Railway detects the `Dockerfile` and builds.

This links the client's Railway to your repo. Result: **every `git push` to `main`
auto-deploys** — and the client never gets read access to your source.

### 5b. Set environment variables
Service → **Variables**. Generate a secret key first:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(64))"
```

| Variable | Value |
|----------|-------|
| `DJANGO_SETTINGS_MODULE` | `greengold.settings.production` |
| `SECRET_KEY` | the generated string |
| `ALLOWED_HOSTS` | `*.up.railway.app` (add the real domain in Step 7) |
| `CSRF_TRUSTED_ORIGINS` | `https://*.up.railway.app` |
| `DATABASE_URL` | the Supabase string (Step 2) |
| `RESEND_API_KEY` / `DEFAULT_FROM_EMAIL` / `CONTACT_TO_EMAIL` | from Step 3 |
| `WAGTAILADMIN_BASE_URL` | your Railway URL (fill after 5c) |

Add the `AWS_*` variables too if you did Step 4.

### 5c. Get a URL
Service → **Settings → Networking → Generate Domain** → e.g.
`greengold-site-production.up.railway.app`. Put it into `WAGTAILADMIN_BASE_URL`.
The container runs DB migrations automatically on boot.

---

## Step 6 — First-boot setup (admin + content)

Open the service's shell in Railway (or `railway run bash` via the CLI):

```bash
python manage.py createsuperuser     # the client's CMS login
python manage.py seed_site           # starter pages (fresh DB only)
```

Check:
- `https://<app>.up.railway.app/` — the live site
- `/admin/` — Wagtail CMS
- `/django-admin/leads/lead/` — leads/CRM inbox

Submit a test enquiry on `/contact/` and confirm the email reaches `CONTACT_TO_EMAIL`.

---

## Step 7 — Custom domain

1. Railway → **Settings → Networking → Custom Domain** → add
   `www.greengoldbioscience.com` (and the apex if wanted).
2. Add the **CNAME** Railway shows at the client's domain registrar.
3. Update Railway variables to include the real domain:
   - `ALLOWED_HOSTS` = `greengoldbioscience.com,www.greengoldbioscience.com,*.up.railway.app`
   - `CSRF_TRUSTED_ORIGINS` = `https://greengoldbioscience.com,https://www.greengoldbioscience.com`
   - `WAGTAILADMIN_BASE_URL` = `https://www.greengoldbioscience.com`
4. Wagtail admin → **Settings → Sites** → set the hostname to the real domain (so the
   sitemap and canonical URLs use it). HTTPS is automatic.

---

## Step 8 — Hand over to the client

The accounts are already under the client's email, so ownership is theirs. To complete handover:

1. **Client takes control of logins:** have the client do a **password reset** on Railway,
   Supabase, and Resend (links go to their inbox) to set their own passwords, and enable 2FA.
2. **Client adds billing:** the client enters **their own** payment method on Railway and
   Supabase (don't enter their card for them).
3. **Keep deploy access:** leave the GitHub→Railway connection in place so you can keep
   shipping updates with `git push`. If they want you to keep maintaining, the client can
   also invite you as a Railway project member.
4. **Give the client:** the live URL, the `/admin/` URL + their superuser login, and this
   `DEPLOY.md`. Note which account holds what (table at the top).

> Because the Railway↔GitHub link points at *your* repo, the client's site keeps deploying
> from your code. If you ever part ways, they'd reconnect Railway to a repo they control.

---

## Step 9 — Launch checklist

- [ ] All 7 pages load on the live URL
- [ ] Both contact forms submit and the email arrives at `CONTACT_TO_EMAIL`
- [ ] A test lead shows in `/django-admin/leads/lead/`
- [ ] You can log into `/admin/` and edit a page
- [ ] `/sitemap.xml` and `/robots.txt` load
- [ ] Custom domain resolves with HTTPS (padlock)

---

## Updating the site later

**Content** (text, images, page sections, form fields): the client edits in `/admin/` —
no deploy needed.

**Code/design:**
```bash
cd ~/Desktop/greengold-site
./scripts/build_css.sh          # if templates/styles changed
git add . && git commit -m "Describe the change"
git push                         # Railway auto-deploys
```

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| Deploy "healthcheck failed" | Add `SECURE_SSL_REDIRECT=false`, redeploy, confirm it loads, then remove it. |
| `DisallowedHost` error | Add the domain to `ALLOWED_HOSTS`. |
| CSRF error on form submit | Add the `https://` domain to `CSRF_TRUSTED_ORIGINS`. |
| Uploaded CMS images vanish after a deploy | Configure Supabase Storage (Step 4). |
| Emails not arriving | Check `RESEND_API_KEY`, verify the sending domain in Resend, check spam. |
| Database connection errors | Confirm the **Session pooler** string and correct password. |
| Railway can't see the repo | Re-run **Configure GitHub App** (Step 5a) signed in as your GitHub; grant the repo. |
