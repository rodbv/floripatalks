# Azure Deployment TL;DR - Flash Card Concepts

**Purpose**: Concise concept-focused guide for understanding Azure deployment processes. Focus on **what**, **when**, and **why** - not commands.

**Created**: 2025-12-11  
**For**: Flash card creation and concept memorization

---

## Core Concepts

### 1. Service Principal vs Personal Account

**What**: Service Principal is a dedicated service account for automated systems (like CI/CD) to authenticate with Azure.

**When**: Always use for production CI/CD pipelines.

**Why**:
- More secure than personal credentials
- Can be scoped to specific resources (least privilege)
- Can be rotated/revoked independently
- Doesn't require your personal account

**Key Point**: Service Principal = service account, not your personal Azure account.

---

### 2. App Registration vs Service Principal

**What**:
- **App Registration**: The "application definition" in Azure AD (like a blueprint)
- **Service Principal**: The actual identity that gets permissions (like an instance of the blueprint)

**When**: App Registration is created first, Service Principal is created automatically when first used.

**Why**: They're linked but different objects. You use App Registration Object ID for some things, Service Principal Object ID for role assignments.

**Key Point**: App Registration = definition, Service Principal = actual identity with permissions.

---

### 3. Role-Based Access Control (RBAC)

**What**: Azure's permission system that controls what each identity can do.

**When**: Always assign roles to service principals (never subscription-wide for security).

**Why**:
- Principle of least privilege (only give what's needed)
- Resource group scope is more secure than subscription scope
- Contributor role allows deployment but not subscription management

**Key Point**: Scope permissions to resource group level, not subscription level.

---

### 4. GitHub Secrets

**What**: Encrypted storage in GitHub for sensitive values (credentials, connection strings).

**When**: Store all Azure credentials and secrets here, never in code.

**Why**:
- Encrypted and never exposed in logs
- Only accessible to GitHub Actions workflows
- Can be rotated without code changes
- Keeps secrets out of repository

**Key Point**: Secrets in GitHub = secure, secrets in code = security risk.

---

### 5. CI/CD Pipeline Flow

**What**: Automated process that runs on every code push: test → build → deploy.

**When**: Triggers automatically when code is pushed to `main` branch.

**Why**:
- Ensures code is tested before deployment
- Automates repetitive tasks
- Catches bugs early
- Enables continuous delivery

**Key Steps** (in order):
1. Checkout code
2. Set up Python environment
3. Install dependencies
4. Run tests (fail fast if broken)
5. Collect static files
6. Authenticate to Azure
7. Configure startup command (if needed)
8. Deploy to Azure

**Key Point**: Tests run BEFORE deployment to catch issues early.

---

### 6. Static File Collection

**What**: Django command that gathers all static files (CSS, JS, images) into one directory.

**When**: During CI/CD deployment, before deploying to Azure.

**Why**:
- Django needs static files in one location for serving
- Production settings require environment variables
- Dummy values are safe because `collectstatic` doesn't use secrets

**Key Point**: Static files collected in CI/CD, not on the server (faster, more reliable).

---

### 7. Startup Script vs Auto-Generated Script

**What**:
- **Custom Startup Script**: Your `startup.sh` with environment validation, migrations, etc.
- **Auto-Generated Script**: Azure's Oryx build system creates one when it detects Django

**When**: Azure may auto-generate a script, ignoring your `startup.txt` file.

**Why**:
- Oryx tries to be helpful but bypasses your custom logic
- Explicit configuration ensures your script runs
- Your script has better error handling and validation

**Key Point**: Explicitly configure startup command in workflow, don't rely on auto-detection.

---

### 8. SCM Container (Kudu)

**What**: Source Control Manager container that handles deployments and management operations in Azure App Service.

**When**: Restarts when you change app configuration (like startup command).

**Why**:
- Needs to restart to apply configuration changes
- If deployment starts during restart, it can fail
- Must wait for container to stabilize before deploying

**Key Point**: Configuration changes cause SCM restart → wait before deploying → avoid conflicts.

---

### 9. Idempotent Configuration

**What**: Check if configuration is already set correctly before changing it.

**When**: Before setting startup command or other configurations in CI/CD.

**Why**:
- Avoids unnecessary SCM container restarts
- Faster deployments (skips if already correct)
- Prevents deployment conflicts

**Key Point**: Check first, only change if needed → fewer restarts → more reliable deployments.

---

### 10. Environment Variables in Production

**What**: Configuration values stored securely in Azure App Service (not in code).

**When**: Set in Azure Portal before first deployment, update as needed.

**Why**:
- Keeps secrets out of code repository
- Different values per environment (dev/staging/prod)
- Can change without redeploying code
- Startup script validates they exist (fails fast if missing)

**Required Variables**:
- `DJANGO_SETTINGS_MODULE`: Which Django settings to use
- `SECRET_KEY`: Django's secret key (never commit this)
- `GOOGLE_CLIENT_ID` & `GOOGLE_CLIENT_SECRET`: OAuth credentials
- `ALLOWED_HOSTS`: Which domains can access the app

**Key Point**: Secrets in environment variables, not code → secure and flexible.

---

### 11. Startup Script Responsibilities

**What**: Script that runs when Azure App Service starts your application.

**When**: Every time the app container starts (deployment, restart, scale).

**Why**: Ensures app is ready before serving traffic.

**What It Does** (in order):
1. Validates environment variables (fails fast if missing)
2. Installs dependencies (if needed)
3. Runs database migrations
4. Collects static files (backup, already done in CI/CD)
5. Starts Gunicorn web server

**Key Point**: Startup script = app initialization + validation + server startup.

---

### 12. Gunicorn (WSGI Server)

**What**: Production-ready web server that runs your Django application.

**When**: Always in production (never use Django's `runserver` in production).

**Why**:
- Handles multiple requests simultaneously (workers)
- Production-optimized
- More secure than development server
- Required for production Django apps

**Key Point**: Gunicorn = production server, `runserver` = development only.

---

### 13. Deployment Process Flow

**What**: The sequence of events from code push to live application.

**When**: Triggered by push to `main` branch.

**Flow**:
1. Developer pushes code to GitHub
2. GitHub Actions workflow triggers
3. Code is checked out on GitHub runner
4. Tests run (if tests fail, deployment stops)
5. Static files collected
6. Authenticate to Azure (using service principal)
7. Configure startup command (if needed, with delay)
8. Deploy code to Azure App Service
9. Azure App Service restarts
10. Startup script runs (migrations, validation, start server)
11. App is live

**Key Point**: Push → Test → Build → Deploy → Start → Live.

---

### 14. Why Explicit Startup Command Configuration

**What**: Setting startup command directly via Azure CLI in workflow, not relying on `startup.txt`.

**When**: In every deployment workflow.

**Why**:
- More reliable than `startup.txt` (can be ignored by Oryx)
- Version controlled (in workflow file)
- Consistent across deployments
- Includes idempotent check and delay

**Key Point**: Explicit > implicit → more reliable deployments.

---

### 15. Configuration Change Timing

**What**: The order and timing of configuration changes vs deployments.

**When**: Always configure before deploying, with delay if needed.

**Why**:
- Configuration changes cause SCM container restart
- Deployment during restart can fail
- Delay allows container to stabilize

**Best Practice**:
- Check if configuration is already correct (idempotent)
- Only change if needed
- Wait 10-15 seconds after change before deploying

**Key Point**: Configure → Wait → Deploy → Avoid conflicts.

---

## Process Summary

### Initial Setup (One-Time)
1. Create Azure resources (Resource Group, App Service Plan, Web App)
2. Create App Registration (service account identity)
3. Create Client Secret (password for service account)
4. Assign Contributor role to Service Principal (at resource group scope)
5. Store credentials in GitHub Secrets (JSON format)
6. Configure environment variables in Azure App Service
7. Set up GitHub Actions workflow

### Ongoing Deployment (Automatic)
1. Push code to `main` branch
2. GitHub Actions runs tests
3. If tests pass, deploy to Azure
4. Azure restarts app
5. Startup script validates and initializes
6. App is live

### When Things Go Wrong
1. Check GitHub Actions logs (for CI/CD issues)
2. Check Azure App Service logs (for runtime issues)
3. Verify environment variables are set
4. Verify startup command is configured correctly
5. Check SCM container status (if deployment conflicts)

---

## Key Principles

1. **Security First**: Service principal, secrets in GitHub, least privilege
2. **Fail Fast**: Tests before deployment, validation in startup script
3. **Explicit > Implicit**: Explicit configuration, not auto-detection
4. **Idempotent Operations**: Check before changing, avoid unnecessary restarts
5. **Separation of Concerns**: CI/CD credentials separate from app secrets
6. **Reproducibility**: Lock files ensure consistent builds

---

## Common Mistakes to Avoid

1. ❌ Using personal Azure account for CI/CD
2. ❌ Storing secrets in code
3. ❌ Subscription-wide role assignments
4. ❌ Deploying during SCM container restart
5. ❌ Relying on auto-generated startup scripts
6. ❌ Skipping tests in CI/CD
7. ❌ Using Django's `runserver` in production
8. ❌ Not validating environment variables

---

## Quick Reference: What Happens When

- **Push to main** → GitHub Actions triggers
- **Tests fail** → Deployment stops
- **Configuration changes** → SCM container restarts
- **Deployment starts** → Code uploaded to Azure
- **App restarts** → Startup script runs
- **Startup script fails** → App doesn't start (check logs)
- **Environment variables missing** → Startup script fails fast with clear error

---

**Last Updated**: 2025-12-11  
**Purpose**: Concept memorization for Azure deployment processes
