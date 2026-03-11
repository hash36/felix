# Django REST Framework Starter

Minimal Django REST Framework project with the backend isolated under `backend/` and Django apps grouped in `backend/apps/`.

## Project layout

- `backend/manage.py`: Django management entry point
- `backend/config/`: project settings and root URL configuration
- `backend/apps/health/`: health endpoint app
- `backend/apps/users/`: custom user model and auth endpoints
- `backend/requirements.txt`: Python dependencies

Current endpoint:

```text
GET /health/
POST /auth/token/
```

Expected response:

```json
{"status": "ok"}
```

## Prerequisites

- Python 3.12+
- `venv` available locally

## Local setup

Create and activate a virtual environment from the repository root:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

Apply database migrations:

```bash
cd backend
python manage.py migrate
```

## Run the app

From `backend/`, start the development server:

```bash
cd backend
python manage.py runserver
```

The app will be available at `http://127.0.0.1:8000`.

Check the health endpoint:

```bash
curl http://127.0.0.1:8000/health/
```

Create a local user for token testing:

```bash
cd backend
python manage.py createsuperuser
```

Request an auth token:

```bash
curl -X POST http://127.0.0.1:8000/auth/token/ \
	-H "Content-Type: application/json" \
	-d '{"username": "your-username", "password": "your-password"}'
```

## Run tests

```bash
cd backend
python manage.py test
```

## Development notes

- Project-level routing lives in `backend/config/urls.py`
- App-level routing for the health endpoint lives in `backend/apps/health/urls.py`
- The health view lives in `backend/apps/health/views.py`
- The custom user model lives in `backend/apps/users/models.py`
- Token authentication is configured in `backend/config/settings.py`
- Database configuration uses SQLite by default in `backend/config/settings.py`

## Typical workflow

1. Activate the virtual environment.
2. Install or update dependencies with `pip install -r backend/requirements.txt`.
3. Work from `backend/` when running Django management commands.
4. Run `python manage.py migrate` after model changes.
5. Start the server with `python manage.py runserver`.
6. Use `python manage.py createsuperuser` if you need a login for local token testing.
7. Run `python manage.py test` before opening a PR.

## Adding a new endpoint

For new features, create a new app under `backend/apps/` instead of adding unrelated endpoints to the health app.

Typical flow:

1. Create a Django app inside `backend/apps/`.
2. Add views, serializers, and tests inside that app.
3. Add an app-level `urls.py` and include it from `backend/config/urls.py`.
4. Register the app in `backend/config/settings.py`.

## Authentication

- Django uses a custom user model defined in `backend/apps/users/models.py`
- DRF defaults to token authentication for API endpoints
- The health endpoint is intentionally public
- New API endpoints will require a valid token unless they explicitly override permissions

To send a token with a request:

```bash
curl http://127.0.0.1:8000/some/protected/endpoint/ \
	-H "Authorization: Token <your-token>"
```