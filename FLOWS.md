# User Flows

## Persona 1: Admin

The admin sets up the app, creates events, and monitors who has signed up.

### 1. Start the app

```bash
source venv/bin/activate
cd backend
python manage.py migrate
python manage.py runserver
```

The API is now available at `http://127.0.0.1:8000`.

### 2. Create the admin user

Run this once to create an admin account with `is_staff=True`:

```bash
python manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
user = User.objects.create_user(
    username='admin',
    email='admin@example.com',
    password='yourpassword',
    is_staff=True,
)
print('Admin created:', user.username)
"
```

### 3. Obtain an admin token

```bash
curl -X POST http://127.0.0.1:8000/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "yourpassword"}'
```

Response:

```json
{"token": "abc123..."}
```

Save this token — it will be used in every subsequent admin request.

### 4. Create a new event

```bash
curl -X POST http://127.0.0.1:8000/events/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token abc123..." \
  -d '{"name": "Launch Party"}'
```

Response:

```json
{"id": 1, "name": "Launch Party", "participants": []}
```

Note the `id` — you will need it to reference this event later.

### 5. Get the list of participants

Once people have signed up, retrieve the full participant list:

```bash
curl http://127.0.0.1:8000/events/1/participants/ \
  -H "Authorization: Token abc123..."
```

Response:

```json
[
  {"id": 2, "email": "alice@example.com", "first_name": "Alice", "last_name": "Smith"}
]
```

---

## Persona 2: The Admin's Friend (Regular User)

The admin's friend wants to join an event. They start with no account and end up registered as a participant.

### 1. Create an account

```bash
curl -X POST http://127.0.0.1:8000/users/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "email": "alice@example.com",
    "first_name": "Alice",
    "last_name": "Smith",
    "password": "alicepassword"
  }'
```

Response:

```json
{
  "username": "alice",
  "email": "alice@example.com",
  "first_name": "Alice",
  "last_name": "Smith",
  "token": "xyz789..."
}
```

The token is returned immediately — no separate login step needed.

### 2. Sign up for the event

Use the token from registration and the event `id` shared by the admin:

```bash
curl -X POST http://127.0.0.1:8000/events/1/participants/ \
  -H "Authorization: Token xyz789..."
```

Response:

```json
{"id": 1, "name": "Launch Party"}
```

The response returns the updated event summary for the participant action.

### 3. (Optional) Obtain a fresh token later

If the user needs to log in again on a different device:

```bash
curl -X POST http://127.0.0.1:8000/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "alice", "password": "alicepassword"}'
```
