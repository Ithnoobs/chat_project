
Param(
    [int]$Port = 8000,
    [string]$AdminUsername = "admin",
    [string]$AdminEmail = "admin@example.com",
    [string]$AdminPassword = "Admin123"
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

if ($LASTEXITCODE -ne 0) {
    Write-Error "migrations failed (exit code $LASTEXITCODE). Aborting."
    exit 1
}


Write-Host "Ensuring admin user exists (username: $AdminUsername)..."
$adminScript = @"
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','chat_project.settings')
import django
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ.get('ADMIN_USERNAME', 'admin')
email = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
password = os.environ.get('ADMIN_PASSWORD', 'Admin123')
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print('Created admin user')
else:
    print('Admin user already exists')
"@


# Set environment variables for admin credentials
$env:ADMIN_USERNAME = $AdminUsername
$env:ADMIN_EMAIL = $AdminEmail
$env:ADMIN_PASSWORD = $AdminPassword

$adminScriptPath = Join-Path $PWD 'create_admin.py'
$adminScript | Out-File -FilePath $adminScriptPath -Encoding utf8
python $adminScriptPath
if ($LASTEXITCODE -ne 0) {
    Write-Warning "Creating admin user failed (exit code $LASTEXITCODE). You may need to create it manually."
} else {
    Write-Host "Admin user check completed."
}
Remove-Item -Path $adminScriptPath -ErrorAction SilentlyContinue

# Clean up environment variables
Remove-Item Env:ADMIN_USERNAME -ErrorAction SilentlyContinue
Remove-Item Env:ADMIN_EMAIL -ErrorAction SilentlyContinue
Remove-Item Env:ADMIN_PASSWORD -ErrorAction SilentlyContinue

Write-Host "Collecting static files..."
# Collect admin CSS/JS and app static files (required when using Daphne + WhiteNoise)
python manage.py collectstatic --noinput
if ($LASTEXITCODE -ne 0) {
    Write-Error "collectstatic failed (exit code $LASTEXITCODE). Aborting."
    exit 1
}

Write-Host "Running Daphne on 127.0.0.1:$Port..."
python -m daphne -b 127.0.0.1 -p $Port chat_project.asgi:application
