Param(
    [int]$Port = 8000
)

Write-Host "Starting Postgres and Redis (docker-compose)..."
docker-compose up -d

Write-Host "Activating virtualenv if present..."
if (Test-Path .\venv\Scripts\Activate.ps1) {
    . .\venv\Scripts\Activate.ps1
} else {
    Write-Host "No local virtualenv activation script found at .\venv\Scripts\Activate.ps1. Make sure you've activated your environment manually if needed."
}

Write-Host "Installing Python requirements (if needed)..."
python -m pip install -r requirements.txt

Write-Host "Applying migrations..."
python manage.py migrate

Write-Host "Running Daphne on 127.0.0.1:$Port..."
python -m daphne -b 127.0.0.1 -p $Port chat_project.asgi:application
