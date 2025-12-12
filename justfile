# FloripaTalks - Common Tasks
# Use `just <task>` to run commands

# Show all available tasks
default:
    @just --list

# Run Django management commands
# Usage: just manage <command> [args...]
# Example: just manage migrate, just manage createsuperuser
manage *args:
    uv run python manage.py {{args}}

# Run database migrations
migrate:
    uv run python manage.py migrate

# Create new migrations
makemigrations *args:
    uv run python manage.py makemigrations {{args}}

# Make migrations and migrate in one command
mmm *args:
    @echo "Creating migrations..."
    uv run python manage.py makemigrations {{args}}
    @echo "Applying migrations..."
    uv run python manage.py migrate

# Run development server
dev:
    uv run python manage.py runserver

# Alias for dev
run:
    just dev

# Run Django shell
shell:
    uv run python manage.py shell

# Run tests
test *args:
    uv run pytest {{args}}

# Run tests with coverage
test-cov:
    uv run pytest --cov --cov-report=html

# Run linting (ruff)
lint:
    uv run ruff check .

# Run formatting (ruff)
format:
    uv run ruff format .

# Check formatting without modifying files
format-check:
    uv run ruff format --check .

# Run all pre-commit checks (linting + formatting)
check:
    @echo "Running linting checks..."
    uv run ruff check .
    @echo "Running format checks..."
    uv run ruff format --check .
    @echo "✅ All checks passed!"

# Run all pre-commit checks with auto-fix
check-fix:
    @echo "Running linting checks with auto-fix..."
    uv run ruff check --fix .
    @echo "Running format auto-fix..."
    uv run ruff format .
    @echo "✅ All checks fixed!"

# Run pre-commit hooks manually (all files)
pre-commit:
    uv run pre-commit run --all-files

# Run pre-commit hooks manually (staged files only)
pre-commit-staged:
    uv run pre-commit run

# Install/update dependencies
sync:
    uv sync

# Add a new dependency
add package:
    uv add {{package}}

# Remove a dependency
remove package:
    uv remove {{package}}

# Regenerate requirements.txt from uv.lock
# This should be run after adding/removing dependencies to keep requirements.txt in sync
# Usage: just update-requirements
update-requirements:
    @echo "Regenerating requirements.txt from uv.lock..."
    uv export --format requirements-txt --no-dev -o requirements.txt
    @echo "✅ requirements.txt updated!"
    @echo "⚠️  Remember to commit this file to keep it in sync with uv.lock"

# Create superuser
superuser:
    uv run python manage.py createsuperuser

# Collect static files
collectstatic:
    uv run python manage.py collectstatic --noinput

# Show Django version
version:
    uv run python manage.py --version

# SSH into Azure App Service
# Requires: Azure CLI installed and logged in (az login)
# Requires: SSH enabled in Azure Portal (Configuration → General settings → SSH → On)
# Usage: just ssh
ssh:
    @echo "Connecting to Azure App Service via SSH..."
    @echo "Note: If this fails, try: just logs (to check startup issues)"
    az webapp ssh \
        --resource-group floripatalks-rg \
        --name floripatalks-app

# View Azure App Service logs (startup, application, etc.)
# Usage: just logs
azlogs:
    @echo "Streaming Azure App Service logs (Ctrl+C to stop)..."
    az webapp log tail \
        --resource-group floripatalks-rg \
        --name floripatalks-app
