# QIMA Booking — Django rebuild

This package consolidates the original multi-interface project into one Django dashboard, one shared booking service, and one background automation worker. The existing `automation/main.py` is retained rather than rewritten.

## Included
- Django authentication and dashboard
- Upload form for booking Excel, booking list Excel, optional technical-info Excel, and PO PDFs
- Database-backed run queue and single polling worker
- Per-run workspaces, logs, and status history
- Docker packaging with persistent data volumes
- Dry-run default to reduce accidental portal actions

## Important limitation in the source automation
The retained QIMA script currently navigates to Inspection Details and records `DONE` when dry-run is disabled; its own source comments say the final inspection-details/review submission step is not implemented. Therefore a completed worker process must not be interpreted as a confirmed QIMA booking. Keep `QIMA_DRY_RUN=true` until the real workflow is reviewed and completed.

## Run locally for development
1. Install Python 3.11 and the requirements.
2. Copy `.env.example` to `.env` and set a strong `DJANGO_SECRET_KEY`, `QIMA_USER`, and `QIMA_PASS`.
3. Run `python manage.py migrate`.
4. Run `python manage.py createsuperuser` to create a login.
5. In one terminal run `python manage.py runserver`; in another run `python manage.py run_booking_worker`.
6. Visit `http://127.0.0.1:8000/`.

## Deploy with Docker
1. Copy `.env.example` to `.env`; configure a strong `DJANGO_SECRET_KEY`, `DJANGO_ALLOWED_HOSTS`, `CSRF_TRUSTED_ORIGINS`, `QIMA_USER`, and `QIMA_PASS`.
2. Create an admin account after the services start: `docker compose exec web python manage.py createsuperuser`.
3. Start: `docker compose up -d --build`.
4. Open `http://SERVER_IP:8000` for a temporary test only. For production, put the service behind HTTPS and do not expose it publicly without TLS and hardened host settings.

## Worker behavior
Run exactly one `run_booking_worker` instance to keep browser automation sequential. It polls queued runs and creates a separate workspace per run. Uploaded files and logs are retained in the persistent data volume; set retention and backups appropriate to your organization.

## Before production
- Complete and test the final QIMA submission/review workflow.
- Add HTTPS reverse proxy and secure cookies; configure trusted hosts and origins.
- Consider PostgreSQL for concurrent production usage (settings support `DB_ENGINE=postgresql`).
- Add a retention policy, audit logs, and tests against sanitized sample workbooks.
- Never commit `.env` or real portal credentials.
