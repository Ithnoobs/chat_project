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

5. Run the ASGI server (Daphne) so WebSockets work:

```powershell
# start Daphne on localhost:8000
python -m daphne -b 127.0.0.1 -p 8000 chat_project.asgi:application
```

6. Open the site in your browser:

Visit http://127.0.0.1:8000

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

License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
