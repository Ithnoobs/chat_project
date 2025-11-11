# Chat Project — Developer README

<p align="left">
  <img src="https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white&style=flat-square" alt="Python" />
  <img src="https://img.shields.io/badge/-Django-092E20?logo=django&logoColor=white&style=flat-square" alt="Django" />
  <img src="https://img.shields.io/badge/-JavaScript-F7DF1E?logo=javascript&logoColor=black&style=flat-square" alt="JavaScript" />
  <img src="https://img.shields.io/badge/-Docker-2496ED?logo=docker&logoColor=white&style=flat-square" alt="Docker" />
  <img src="https://img.shields.io/badge/-PostgreSQL-336791?logo=postgresql&logoColor=white&style=flat-square" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/-Redis-DC382D?logo=redis&logoColor=white&style=flat-square" alt="Redis" />
</p>

This repository is a Django + Channels chat project that uses PostgreSQL and Redis (via Docker) for school assignment. WebSocket connections are served by an ASGI server (Daphne) — ensure you run the ASGI server for WebSocket support.

## Feature Checklist

Track the implementation status of planned features:

- [x] **User Authentication** — Done
  - UserProfile model with online_status tracking
  - Django User model integration
  - Authentication views and forms verified
  
- [x] **Chat Rooms** — Done
  - Room model with public/private types
  - RoomMembership with role-based access (admin, moderator, member)
  - Room creation, listing, and detail views
  
- [x] **Notifications** — Partially Done
  - Notification model with multiple types (mention, message, invite, reply)
  - Generic foreign key for linking to any model
  - Missing: Real-time WebSocket notification dispatch
  
- [ ] **Moderation Tools** — Not Done
  - Report model for flagging inappropriate content
  - ModerationAction model for ban/mute/warn actions
  - Missing: Admin views and enforcement logic
  
- [x] **Chat History** — Done
  - Message model with content storage
  - Parent message field for threading/replies
  - Messages stored with timestamps and sender info
  
- [ ] **File Sharing** — Not Done
  - Attachment model for file uploads
  - File type and size tracking
  - Upload directory structure: `attachments/%Y/%m/%d/`
  
- [x] **Typing Indicators** — Done
  - typing_indicator message type in ChatConsumer
  - WebSocket broadcast of typing status
  - Frontend receives username and is_typing flag
  
- [x] **Online Status** — Done
  - online_status field in UserProfile (online/away/offline)
  - last_seen timestamp tracking
  - Auto-updated on profile save

## Prerequisites
- Python 3.10+ (use your project virtual environment)
- Docker & Docker Compose (for PostgreSQL and Redis)

## Quick start (Windows / PowerShell)

1. Create and activate a virtual environment (if you haven't already):

```powershell
python -m venv venv
.\\venv\\Scripts\\Activate.ps1
```

2. Install Python dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

3. Start supporting services (Postgres, Redis):

```powershell
# run from project root
docker-compose up -d
```

4. Apply migrations and create a superuser:

```powershell
python manage.py migrate
python manage.py createsuperuser
```

5. Collect static files (required when serving static files with Daphne/WhiteNoise):

```powershell
# collects admin CSS/JS and app static files into the folder configured by STATIC_ROOT
python manage.py collectstatic --noinput
```

6. Run the ASGI server (Daphne) so WebSockets work:

```powershell
# start Daphne on localhost:8000
python -m daphne -b 127.0.0.1 -p 8000 chat_project.asgi:application
```

7. Open the site in your browser:

Visit http://127.0.0.1:8000

Quick admin styling note:
- If you only need to use the admin quickly and don't care about WebSockets while editing content, you can run the Django development server instead (it serves static files automatically):

```powershell
python manage.py runserver
```

If you get an error on login like "User has no profile", create a profile for that user in the Django shell:

```powershell
python manage.py shell
```

Then in the shell (Using admin as an example):

```python
from django.contrib.auth.models import User
from apps.authentication.models import UserProfile
user = User.objects.get(username='admin')
UserProfile.objects.get_or_create(user=user)
exit()
```

Notes
- Using `python manage.py runserver` may work for basic HTTP, but to reliably accept WebSocket upgrade requests you should run an ASGI server such as Daphne or Uvicorn as shown above.
- If WebSocket requests return 404: ensure the ASGI server is running (Daphne), and that any proxy (nginx) in front forwards Upgrade/Connection headers.

Troubleshooting
- Redis must be running for Channels' channel layer. Check `docker ps` to verify `chat_redis` is up.
- If you see a 404 on `/ws/...`, check that the process listening on port 8000 is Daphne (ASGI). A WSGI server cannot accept WebSocket upgrade requests.

Deploying
- You may include a small CI workflow that installs `requirements.txt` and runs tests.


Optional: development helper script
- See `dev-run.ps1` for a small helper that brings up Docker, runs migrations, and launches Daphne.
- You can now configure the admin username, email, and password via script parameters:

```powershell
./dev-run.ps1 -AdminUsername "myadmin" -AdminEmail "myadmin@example.com" -AdminPassword "MySecret123"
```
If not specified, the defaults are:
- Username: `admin`
- Email: `admin@example.com`
- Password: `Admin123`
