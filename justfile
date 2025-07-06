# Justfile for Django project management
# Usage: just <command>

# Default recipe to show available commands
default:
    just --list

# Development server
dev:
    uv run python manage.py runserver

# Development server with django-extensions (enhanced)
run:
    uv run python manage.py runserver_plus

# Run manage.py
manage *args:
    uv run python manage.py {{args}}

# Shell with all models pre-loaded
shell:
    uv run python manage.py shell_plus

# Shell with IPython
shell-ipython:
    uv run python manage.py shell_plus --ipython

# Create superuser
superuser:
    uv run python manage.py createsuperuser

# Make migrations
makemigrations:
    uv run python manage.py makemigrations

# Apply migrations
migrate:
    uv run python manage.py migrate

# Show migrations status
showmigrations:
    uv run python manage.py showmigrations

# Collect static files
collectstatic:
    uv run python manage.py collectstatic --noinput

# Check for problems
check:
    uv run python manage.py check

# Validate templates
validate-templates:
    uv run python manage.py validate_templates

# Generate model graph (requires graphviz)
graph-models:
    uv run python manage.py graph_models -a -o models.png

# Run tests
test:
    uv run python manage.py test

# Run tests with coverage
test-cov:
    uv run python -m pytest --cov=. --cov-report=html

# Clean up Python cache files
clean:
    find . -type f -name "*.pyc" -delete
    find . -type d -name "__pycache__" -delete
    find . -type d -name "*.egg-info" -exec rm -rf {} +
    rm -rf .pytest_cache/
    rm -rf htmlcov/

# Install dependencies
install:
    uv sync

# Update dependencies
update:
    uv lock --upgrade
    uv sync

# Install development dependencies
install-dev:
    uv sync --extra dev

# Format code with ruff
format:
    uv run ruff format .

# Lint code with ruff
lint:
    uv run ruff check .

# Format and lint code
format-lint:
    uv run ruff check --fix .
    uv run ruff format .

# Type check with mypy
typecheck:
    uv run mypy .

# Install pre-commit hooks
pre-commit-install:
    uv run pre-commit install

# Run pre-commit on all files
pre-commit-all:
    uv run pre-commit run --all-files

# Database backup
backup:
    uv run python manage.py dumpdata > backup_$(date +%Y%m%d_%H%M%S).json

# Database restore
restore file:
    uv run python manage.py loaddata {{file}}

# Reset database (DANGER: deletes all data)
reset-db:
    rm -f db.sqlite3
    uv run python manage.py migrate
    echo "Database reset complete. Run 'just superuser' to create admin user."

# Show project info
info:
    echo "Django version:"
    uv run python -c "import django; print(django.get_version())"
    echo "\nInstalled apps:"
    uv run python manage.py check --list-tags

# Open Django admin in browser
admin:
    open http://localhost:8000/admin/

# Start development environment (server + shell)
dev-env: run
    echo "Starting development environment..."
    echo "Server running at http://localhost:8000"
    echo "Admin at http://localhost:8000/admin"
    echo "Use 'just shell' in another terminal for Django shell"
