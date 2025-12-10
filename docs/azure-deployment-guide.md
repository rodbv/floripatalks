# Azure Deployment Guide for FloripaTalks

**Created**: 2025-01-XX  
**Purpose**: Hands-on guide for deploying FloripaTalks Django application to Azure with CI/CD

## AZ-204 Exam Topics Covered

This guide provides hands-on experience with these **Azure Developer Associate (AZ-204)** exam topics:

- ✅ **Azure App Service** (Compute): Deploy and configure web apps
- ✅ **Azure Resource Groups**: Organize and manage Azure resources
- ✅ **Application Settings/Environment Variables**: Configure app configuration
- ✅ **GitHub Actions CI/CD**: Automated deployment pipelines
- ✅ **SSL/TLS Certificates**: App Service managed certificates
- ✅ **Application Insights** (optional): Monitoring and diagnostics
- ✅ **Azure Key Vault** (optional): Secret management
- ✅ **Deployment Slots** (optional): Zero-downtime deployments
- ✅ **Azure Blob Storage** (optional): Store static/media files
- ✅ **Azure Functions** (optional): Serverless computing
- ✅ **Azure Service Bus** (optional): Message queues

**Assumes**: You understand cloud concepts (SSL, domains, CI/CD, etc.). This guide focuses on Azure-specific implementation.

## Executive Summary

**Recommended Solution**: **Azure App Service** (Python runtime)

**Why**: Simplest deployment option, native Django support, built-in CI/CD, very low cost for small applications, minimal configuration required.

**Estimated Monthly Cost**: $0-15 USD

---

## Deployment Options Comparison

### Option 1: Azure App Service (Recommended) ⭐

**Best for**: Simple, cost-effective Django deployment with minimal configuration

**Pros**:
- ✅ Native Python/Django support - no Docker required
- ✅ Built-in CI/CD integration with GitHub
- ✅ Free tier available (F1 - 1GB RAM, 1GB storage)
- ✅ Automatic HTTPS/SSL certificates
- ✅ Built-in scaling (manual or auto)
- ✅ Easy environment variable management
- ✅ Integrated logging and monitoring
- ✅ Supports custom domains
- ✅ Deployment slots for zero-downtime deployments

**Cons**:
- ⚠️ Less control than containerized solutions
- ⚠️ Free tier has limitations (60 minutes/day compute time, shared infrastructure)

**Cost**:
- **Free Tier (F1)**: $0/month (60 minutes/day compute, 1GB storage)
- **Basic Tier (B1)**: ~$13/month (unlimited compute, 1.75GB RAM, 10GB storage)
- **Standard Tier (S1)**: ~$70/month (better performance, auto-scaling)

**Complexity**: ⭐⭐☆☆☆ (Very Simple)

---

### Option 2: Azure Container Apps

**Best for**: Containerized applications, microservices

**Pros**:
- ✅ Serverless container hosting
- ✅ Pay-per-use pricing
- ✅ Auto-scaling to zero
- ✅ Good for containerized apps

**Cons**:
- ❌ Requires Dockerfile and containerization
- ❌ More complex setup
- ❌ Less mature than App Service
- ❌ CI/CD requires container registry

**Cost**: ~$0.000012/vCPU-second + $0.0000015/GB-second (very low for low traffic)

**Complexity**: ⭐⭐⭐☆☆ (Moderate)

---

### Option 3: Azure Static Web Apps + Azure Functions

**Best for**: Static frontend with serverless backend

**Cons**:
- ❌ Not suitable for Django (designed for static sites + serverless functions)
- ❌ Would require significant refactoring

**Complexity**: ❌ Not applicable

---

## Recommended Architecture: Azure App Service

### Components Needed

1. **Azure App Service** (Web App)
   - Hosts Django application
   - Python 3.12 runtime
   - Handles HTTP requests
   - **Region**: Brazil South (for Brazilian users - lower latency)

2. **SQLite Database** (Recommended for this project)
   - File-based database stored in persistent storage
   - Free (no additional database service needed)
   - Suitable for low-to-medium traffic

3. **Azure Blob Storage** (Optional, for media files)
   - Static files can be served by App Service
   - Media files (user uploads) should use Blob Storage
   - Cost: ~$0.02/GB/month

4. **GitHub Actions** (CI/CD)
   - Free for public repositories
   - Auto-deploy on merge to main branch

---

## Cost Breakdown (Estimated)

### Recommended Setup (Free Tier)

- **App Service (F1 Free)**: $0/month
  - 60 minutes/day compute time (sufficient for low-to-medium traffic)
  - 1GB storage (includes SQLite database)
  - **Free SSL on `*.azurewebsites.net` domain** (out of the box, automatic)
  - Shared infrastructure
  - **Region**: Brazil South
- **Database**: SQLite (free, stored in persistent storage)
- **Blob Storage (Standard)**: ~$1/month (for media files and backups, optional)
- **Total**: ~$0-1/month

**Note**:
- SSL certificates are automatically provided for `*.azurewebsites.net` domains at no additional cost
- Your app will be accessible at `https://floripatalks-app.azurewebsites.net` with a valid SSL certificate
- Free tier is suitable for production if traffic is low-to-medium (<1000 requests/day)

### Scaling Up (If Needed)

- **App Service (B1 Basic)**: ~$13/month
  - Unlimited compute
  - 1.75GB RAM
  - 10GB storage
  - **Free SSL on `*.azurewebsites.net` domain**
  - **Region**: Brazil South
- **Total**: ~$13-14/month

**Upgrade when**: You exceed 60 minutes/day compute time or need more resources

### Scaling Up (Medium Traffic)

- **App Service (S1 Standard)**: ~$70/month
  - Better performance
  - Auto-scaling
  - 50GB storage
  - **Region**: Brazil South
- **Database**: SQLite (free)
- **Blob Storage**: ~$2/month (for media files)
- **Total**: ~$72/month

**Note**: SQLite is suitable for most applications with moderate traffic (<100 concurrent users). The database file is stored in persistent storage and survives restarts.

---

## Security Features (Built-in)

1. **HTTPS/SSL**: Free SSL certificates on `*.azurewebsites.net` domains (automatic, no config)
2. **Managed Identity**: Access Azure resources without storing credentials
3. **Application Settings**: Secure environment variable storage (encrypted at rest)
4. **Azure Key Vault** (Optional): Advanced secret management
5. **Network Security**: Built-in DDoS protection, firewall rules

---

## CI/CD Setup with GitHub Actions

### Automatic Deployment Flow

1. Developer merges PR to `main` branch
2. GitHub Actions workflow triggers
3. Workflow:
   - Runs tests
   - Collects static files
   - Deploys to Azure App Service
4. Application automatically restarts with new code
5. Zero-downtime deployment (if using deployment slots)

### Required Files

1. **`.github/workflows/azure-deploy.yml`**: GitHub Actions workflow
2. **`requirements.txt`** or use existing `pyproject.toml` with `uv`
3. **`startup.sh`** (optional): Custom startup script for App Service

---

## Step-by-Step Deployment Guide

### Table of Contents (Quick Navigation)

**Core Deployment Steps:**
- [Step 1: Create Azure Resources](#step-1-create-azure-resources-az-204-create-and-manage-azure-resources)
- [Step 2: Configure Application Settings](#step-2-configure-application-settings-az-204-app-configuration)
- [Step 3: Set Up GitHub Actions CI/CD](#step-3-set-up-github-actions-cicd-az-204-implement-cicd)
- [Step 4: Configure GitHub Secrets](#step-4-configure-github-secrets)
- [Step 5: Create Production Settings](#step-5-create-production-settings)
- [Step 6: Create Startup Script (Optional)](#step-6-create-startup-script-optional)
- [Step 7: Initial Deployment](#step-7-initial-deployment)

**Configuration & Setup:**
- [Database: SQLite Configuration](#database-sqlite-configuration)
- [Static and Media Files](#static-and-media-files-az-204-implement-data-storage)
- [Monitoring and Logging](#monitoring-and-logging-az-204-implement-monitoring)

**Cloudflare Setup (Recommended):**
- [Step 1: Create Cloudflare Account](#step-1-create-cloudflare-account)
- [Step 2: Add Your Domain](#step-2-add-your-domain)
- [Step 3: Configure DNS](#step-3-configure-dns)
- [Step 4: Configure Cloudflare Settings](#step-4-configure-cloudflare-settings)
- [Step 5: Point Cloudflare to Azure App Service](#step-5-point-cloudflare-to-azure-app-service)
- [Step 6: Update Azure App Service ALLOWED_HOSTS](#step-6-update-azure-app-service-allowed_hosts)
- [Step 7: (Optional) Restrict Azure to Cloudflare IPs](#step-7-optional-restrict-azure-to-cloudflare-ips)
- [Step 8: Verify Setup](#step-8-verify-setup)

**Database Backup Strategy (Optional):**
- [Step 1: Create Storage Account and Container](#step-1-create-storage-account-and-container)
- [Step 2: Install Required Package](#step-2-install-required-package)
- [Step 3: Create Django Management Command](#step-3-create-django-management-command)
- [Step 4: Configure Environment Variable](#step-4-configure-environment-variable)
- [Step 5: Schedule Automated Backups](#step-5-schedule-automated-backups-every-3-hours)
- [Step 6: Add Pre-Deployment Backup](#step-6-add-pre-deployment-backup)
- [Step 7: Configure GitHub Secrets](#step-7-configure-github-secrets) (in Backup section)
- [Step 8: Manual Weekly/Monthly Backups](#step-8-manual-weeklymonthly-backups)
- [Step 9: Restore from Backup](#step-9-restore-from-backup)

**Additional Learning:**
- [Additional AZ-204 Learning Opportunities](#additional-az-204-learning-opportunities-lowno-cost)
- [Troubleshooting](#troubleshooting)

---

### Prerequisites

1. Azure account (free tier available)
2. GitHub repository
3. Django application ready for production

### Step 1: Create Azure Resources (AZ-204: Create and Manage Azure Resources)

**Via Azure Portal** (Recommended for exam practice):
1. **Create Resource Group**:
   - **What**: A container that holds related Azure resources for your project (like a folder for organizing files)
   - **Why**: Organizes resources together, makes management easier, and allows bulk operations (delete all resources at once)
   - Portal: [Create Resource Group](https://portal.azure.com/#create/Microsoft.ResourceGroup)
   - Or: Search "Resource groups" → Create → Name: `floripatalks-rg`, Region: `Brazil South`

2. **Create App Service Plan**:
   - **What**: Defines the compute resources (CPU, RAM, features) available to your web apps
   - **Why**: Determines pricing tier and capabilities; multiple apps can share one plan to save costs
   - Portal: [Create App Service Plan](https://portal.azure.com/#create/Microsoft.AppServicePlan)
   - Or: Search "App Service plans" → Create → Resource Group: `floripatalks-rg`, Name: `floripatalks-plan`, Region: `Brazil South`, Pricing tier: `Free F1`

3. **Create Web App** (App Service):
   - **What**: The actual web application hosting service that runs your Django app
   - **Why**: Provides managed hosting with automatic scaling, SSL, and deployment features without managing servers
   - Portal: [Create Web App](https://portal.azure.com/#create/Microsoft.WebSite)
   - Or: Search "Web App" → Create → Resource Group: `floripatalks-rg`, Name: `floripatalks-app`, Runtime: `Python 3.12`, Region: `Brazil South`, App Service Plan: `floripatalks-plan`

**Via Azure CLI** (Alternative):
```bash
# Install Azure CLI
# https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

# Login
az login

# Create resource group (container for organizing resources)
az group create --name floripatalks-rg --location brazilsouth

# Create App Service Plan (defines compute resources and pricing tier)
az appservice plan create \
  --name floripatalks-plan \
  --resource-group floripatalks-rg \
  --location brazilsouth \
  --sku FREE

# Create Web App (the actual hosting service for your Django app)
az webapp create \
  --name floripatalks-app \
  --resource-group floripatalks-rg \
  --plan floripatalks-plan \
  --runtime "PYTHON:3.12" \
  --location brazilsouth
```

### Step 2: Configure Application Settings (AZ-204: App Configuration)

**What**: Environment variables stored securely in Azure that your app can access at runtime
**Why**: Keeps secrets out of code, allows different configs per environment (dev/staging/prod), and enables changes without redeploying

**Azure Portal** (Recommended):
- Navigate: [Azure Portal](https://portal.azure.com) → Resource Groups → `floripatalks-rg` → `floripatalks-app` → **Configuration** → **Application settings**
- Click **+ New application setting** for each variable:
  - `DJANGO_SETTINGS_MODULE` = `floripatalks.settings.production`
  - `SECRET_KEY` = `<generate-strong-secret>`
  - `DEBUG` = `False`
  - `ALLOWED_HOSTS` = `floripatalks-app.azurewebsites.net`
  - `GOOGLE_CLIENT_ID` = `<your-google-client-id>`
  - `GOOGLE_CLIENT_SECRET` = `<your-google-client-secret>`
- Click **Save** → **Continue** to apply changes

**Azure CLI** (Alternative):
```bash
az webapp config appsettings set \
  --resource-group floripatalks-rg \
  --name floripatalks-app \
  --settings \
    DJANGO_SETTINGS_MODULE=floripatalks.settings.production \
    SECRET_KEY=<generate-strong-secret> \
    DEBUG=False \
    ALLOWED_HOSTS=floripatalks-app.azurewebsites.net \
    GOOGLE_CLIENT_ID=<your-google-client-id> \
    GOOGLE_CLIENT_SECRET=<your-google-client-secret>
```

**Via Portal** (App Service → Configuration → Application Settings):

```bash
# Django Settings
DJANGO_SETTINGS_MODULE=floripatalks.settings.production
SECRET_KEY=<generate-strong-secret>
DEBUG=False
ALLOWED_HOSTS=floripatalks-app.azurewebsites.net

# Database (using SQLite - no configuration needed, file stored in persistent storage)
# SQLite database will be created automatically at: /home/site/wwwroot/db.sqlite3
# Note: SQLite is stored in persistent storage and survives restarts

# OAuth
GOOGLE_CLIENT_ID=<your-google-client-id>
GOOGLE_CLIENT_SECRET=<your-google-client-secret>

# Azure Storage (if using Blob Storage for media)
AZURE_STORAGE_ACCOUNT_NAME=<storage-account-name>
AZURE_STORAGE_ACCOUNT_KEY=<storage-key>
```

### Step 3: Set Up GitHub Actions CI/CD (AZ-204: Implement CI/CD)

**What**: Automated pipeline that tests, builds, and deploys your app whenever you push code to GitHub
**Why**: Ensures code is tested before deployment, automates repetitive tasks, and enables continuous delivery without manual steps

Create `.github/workflows/azure-deploy.yml`:

```yaml
name: Deploy to Azure App Service

on:
  push:
    branches:
      - main
  workflow_dispatch:

env:
  AZURE_WEBAPP_NAME: floripatalks-app
  PYTHON_VERSION: '3.12'

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest

    steps:
    - uses: actions/checkout@v4

    - name: Set up Python
      uses: actions/setup-python@v5
      with:
        python-version: ${{ env.PYTHON_VERSION }}

    - name: Install uv
      uses: astral-sh/setup-uv@v4
      with:
        version: "latest"

    - name: Install dependencies
      run: |
        uv sync --frozen

    - name: Run tests
      run: |
        uv run pytest

    - name: Collect static files
      run: |
        uv run python manage.py collectstatic --noinput
      env:
        DJANGO_SETTINGS_MODULE: floripatalks.settings.production

    - name: Deploy to Azure Web App
      uses: azure/webapps-deploy@v3
      with:
        app-name: ${{ env.AZURE_WEBAPP_NAME }}
        publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
        package: .
```

### Step 4: Configure GitHub Secrets

**What**: Publish Profile is an XML file containing credentials and connection details needed to deploy to your App Service
**Why**: Allows GitHub Actions to authenticate and deploy to Azure without storing credentials in your code repository

**Get Publish Profile from Azure Portal**:
- Navigate: [Azure Portal](https://portal.azure.com) → Resource Groups → `floripatalks-rg` → `floripatalks-app` → **Get publish profile** (top menu)
- Download the `.PublishSettings` file
- Open the file and copy the entire XML content

**Add to GitHub**:
- Navigate: GitHub Repository → **Settings** → **Secrets and variables** → **Actions**
- Click **New repository secret**
- Name: `AZURE_WEBAPP_PUBLISH_PROFILE`
- Value: Paste the entire XML content from the publish profile
- Click **Add secret**

**Azure CLI Alternative**:
```bash
az webapp deployment list-publishing-profiles \
  --name floripatalks-app \
  --resource-group floripatalks-rg \
  --xml
```

### Step 5: Create Production Settings

**What**: Django settings file specifically for production environment with security optimizations
**Why**: Separates production config from development, enables security features (HTTPS, secure cookies), and prevents debug mode in production

Create `floripatalks/settings/production.py`:

```python
"""
Django production settings for Azure App Service.
"""

from .base import *

# Security
DEBUG = False
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", "").split(",")

# Database (SQLite)
# SQLite database stored in persistent storage (/home/site/wwwroot/)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Note: Azure App Service persistent storage ensures database survives restarts

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Media files (use Azure Blob Storage in production)
# Install: django-storages[azure]
# DEFAULT_FILE_STORAGE = "storages.backends.azure_storage.AzureStorage"
# AZURE_ACCOUNT_NAME = os.environ.get("AZURE_STORAGE_ACCOUNT_NAME")
# AZURE_ACCOUNT_KEY = os.environ.get("AZURE_STORAGE_ACCOUNT_KEY")
# AZURE_CONTAINER = "media"

# Email (use Azure Communication Services or SendGrid)
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# Configure SMTP settings

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
```

### Step 6: Create Startup Script (Optional)

**What**: Bash script that runs when your App Service starts, typically to run migrations and start the web server
**Why**: Automates setup tasks (database migrations, static file collection) and ensures your app is ready before serving traffic

Create `startup.sh` in project root:

```bash
#!/bin/bash
# Azure App Service startup script

# Run migrations
python manage.py migrate --noinput

# Collect static files (if not done in CI/CD)
python manage.py collectstatic --noinput

# Start Gunicorn
gunicorn floripatalks.wsgi:application --bind 0.0.0.0:8000 --workers 2
```

**Configure Startup Command in Azure Portal**:
- Navigate: [Azure Portal](https://portal.azure.com) → Resource Groups → `floripatalks-rg` → `floripatalks-app` → **Configuration** → **General settings**
- Scroll to **Startup Command**
- Enter: `bash startup.sh`
- Click **Save** → **Continue**

### Step 7: Initial Deployment

**What**: The process of uploading your application code to Azure App Service for the first time
**Why**: Makes your app accessible on the internet; after initial deployment, CI/CD handles future updates automatically

**Option A: Manual Deploy via Azure Portal** (First Time):
- Navigate: [Azure Portal](https://portal.azure.com) → Resource Groups → `floripatalks-rg` → `floripatalks-app` → **Deployment Center**
- Source: **Local Git** or **ZIP Deploy**
- For ZIP: Create a ZIP of your project (excluding `__pycache__`, `.venv`, etc.) and upload

**Option B: GitHub Actions** (Recommended, after setup):
- Push to `main` branch
- GitHub Actions will automatically deploy
- Monitor: GitHub Repository → **Actions** tab

---

## Database: SQLite Configuration

### SQLite on Azure App Service

**Pros**:
- ✅ Free (no additional database service)
- ✅ No setup required
- ✅ Good for low-to-medium traffic
- ✅ Persistent storage on App Service (survives restarts)

**Considerations**:
- ⚠️ Single-writer limitation (fine for most web apps)
- ⚠️ Concurrent reads are fine, but writes are serialized
- ⚠️ Suitable for <100 concurrent write operations
- ⚠️ Database file stored in persistent storage (`/home/site/wwwroot/`)

**Setup**:
```python
# In floripatalks/settings/production.py
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # Stored in persistent storage
    }
}
```

**Important**:
- **Live SQLite file**: Stored on App Service persistent storage at `/home/site/wwwroot/db.sqlite3` (survives restarts and deployments)
- **Backups**: Stored in Azure Blob Storage (NOT on App Service filesystem) for durability and protection against App Service failures

---

## Static and Media Files (AZ-204: Implement Data Storage)

**Static Files**:
- App Service serves static files directly
- Run `collectstatic` during deployment
- Files in `staticfiles/` directory

**Media Files** (Optional - AZ-204: Azure Blob Storage):
- **What**: Azure Blob Storage is cloud storage for unstructured data (files, images, videos) with high availability and scalability
- **Why**: Better than App Service filesystem for user uploads because files persist across deployments, scale independently, and are cheaper for large files
- **Create Storage Account**: [Azure Portal](https://portal.azure.com/#create/Microsoft.StorageAccount) → Resource Group: `floripatalks-rg`, Name: `floripatalksstorage`, Region: `Brazil South`, Performance: `Standard`, Redundancy: `LRS`
- **Create Container**: Storage Account → **Containers** → **+ Container** → Name: `media`, Public access: `Blob`
- **Install**: `django-storages[azure]`
- **Configure**: Add to `production.py` (see code example in Step 5)
- **Cost**: ~$0.02/GB/month (very cheap for small apps)
- **Alternative**: App Service filesystem (temporary, not recommended for production)

---

## Monitoring and Logging (AZ-204: Implement Monitoring)

**App Service Logs** (Built-in):
- **Azure Portal**: [Azure Portal](https://portal.azure.com) → Resource Groups → `floripatalks-rg` → `floripatalks-app` → **Log stream** (real-time)
- **Enable Logging**: **Configuration** → **Logging** → **Application Logging (Filesystem)** → **On** → **Save**
- **Application logs**: stdout/stderr
- **HTTP logs**: Request/response logs

**Application Insights** (Optional, recommended - AZ-204: Application Insights):
- **What**: Azure's Application Performance Monitoring (APM) service that tracks performance, errors, and user behavior
- **Why**: Helps identify performance bottlenecks, track errors in production, understand user behavior, and set up alerts for issues
- **Enable**: [Azure Portal](https://portal.azure.com) → Resource Groups → `floripatalks-rg` → `floripatalks-app` → **Application Insights** → **Turn on Application Insights**
- Create new Application Insights resource or use existing
- **Features**: Performance monitoring, error tracking, user analytics, custom metrics
- **Free tier**: 5GB/month data ingestion, 90-day retention

**Metrics** (Built-in):
- **Azure Portal**: [Azure Portal](https://portal.azure.com) → Resource Groups → `floripatalks-rg` → `floripatalks-app` → **Metrics**
- **Available metrics**: CPU, memory, request count, response times, HTTP server errors
- **Create alerts**: **Metrics** → **New alert rule** → Configure condition and action group

---

## Cloudflare Setup (Recommended - Free Security & Performance)

**What**: Cloudflare is a global CDN and security service that sits between users and your app, providing protection and performance optimization
**Why**: Adds free DDoS protection, WAF (blocks attacks), CDN (faster loading), and SSL certificates without additional Azure costs

Cloudflare provides free DDoS protection, WAF, CDN, and security features in front of your Azure App Service.

### Benefits

**Free Tier Includes**:
- ✅ **DDoS Protection**: Unlimited DDoS mitigation
- ✅ **WAF (Web Application Firewall)**: Basic rules to block common attacks
- ✅ **CDN**: Global content delivery network (faster static files)
- ✅ **Free SSL**: SSL certificates for custom domains
- ✅ **Bot Protection**: Basic bot mitigation
- ✅ **Analytics**: Traffic and security analytics
- ✅ **Rate Limiting**: Basic rate limiting rules

**Cost**: $0/month (free tier is very generous)

### Step 1: Create Cloudflare Account

1. Go to [Cloudflare Sign Up](https://dash.cloudflare.com/sign-up)
2. Create a free account
3. Verify your email

### Step 2: Add Your Domain

1. **Cloudflare Dashboard**: Click **Add a Site**
2. Enter your domain (e.g., `example.com` if you have a custom domain, or use a subdomain)
3. Select **Free** plan
4. Click **Continue**

**Important**: Cloudflare requires a custom domain (cannot use `*.azurewebsites.net` directly).

**Options if you don't have a custom domain**:
1. **Use a subdomain you own**: If you own `example.com`, use `talks.example.com`
2. **Skip Cloudflare for now**: Azure App Service has built-in DDoS protection (basic but sufficient for small apps)
3. **Get a free domain**: Some registrars offer free domains (e.g., Freenom, but reliability varies)

**Recommendation**: If you plan to use Cloudflare, set up a custom domain first. Otherwise, Azure's built-in protection is adequate for small apps.

### Step 3: Configure DNS

**What**: DNS (Domain Name System) translates domain names to IP addresses; nameservers tell the internet where to find your domain's DNS records
**Why**: Cloudflare needs to manage your domain's DNS to route traffic through their network and provide security/CDN services

**If using custom domain**:
1. Cloudflare will scan your existing DNS records
2. Review and confirm DNS records
3. Update nameservers at your domain registrar to Cloudflare's nameservers
4. Wait for DNS propagation (usually 1-24 hours)

**If using `*.azurewebsites.net` domain**:
- Cloudflare requires a custom domain, so skip this section if you're only using Azure's default domain

### Step 4: Configure Cloudflare Settings

**What**: Configuration options in Cloudflare dashboard for SSL encryption, security rules, and performance optimizations
**Why**: Ensures secure connections, enables WAF protection, and optimizes content delivery for better performance

**SSL/TLS**:
1. **Cloudflare Dashboard** → Your site → **SSL/TLS**
2. Set encryption mode to **Full (strict)**
3. This ensures end-to-end encryption between Cloudflare and Azure

**Security**:
1. **Security** → **WAF** → Enable basic WAF rules
2. **Security** → **Bot Fight Mode** → Enable (free tier)
3. **Security** → **Rate Limiting** → Configure basic rules (optional)

**Speed**:
1. **Speed** → **Optimization** → Enable **Auto Minify** (CSS, JavaScript, HTML)
2. **Speed** → **Caching** → Set cache level to **Standard**

### Step 5: Point Cloudflare to Azure App Service

**What**: CNAME record is a DNS record that maps your domain to another domain (like an alias)
**Why**: Routes traffic from your custom domain through Cloudflare's network to your Azure App Service, enabling Cloudflare's protection and CDN

1. **Cloudflare Dashboard** → Your site → **DNS** → **Records**
2. Add a CNAME record:
   - **Type**: CNAME
   - **Name**: `@` (or subdomain like `talks`)
   - **Target**: `floripatalks-app.azurewebsites.net`
   - **Proxy status**: ✅ Proxied (orange cloud icon - this enables Cloudflare protection)
   - Click **Save**

### Step 6: Update Azure App Service ALLOWED_HOSTS

**What**: Django security setting that specifies which domain names are allowed to serve your application
**Why**: Prevents HTTP Host header attacks by only accepting requests from trusted domains (your custom domain and Azure domain)

**Azure Portal**:
1. App Service → **Configuration** → **Application settings**
2. Update `ALLOWED_HOSTS` to include:
   - Your custom domain (if using one)
   - `floripatalks-app.azurewebsites.net` (keep this for direct access)
3. Click **Save** → **Continue**

**Example**:
```
ALLOWED_HOSTS=talks.example.com,floripatalks-app.azurewebsites.net
```

### Step 7: (Optional) Restrict Azure to Cloudflare IPs

**What**: Azure Access Restrictions feature that limits which IP addresses can reach your App Service
**Why**: Prevents direct access to your App Service, forcing all traffic through Cloudflare for maximum security and ensuring all requests benefit from Cloudflare's protection

**Azure Portal**:
1. App Service → **Networking** → **Access Restrictions**
2. Click **+ Add rule**
3. **Name**: `Allow Cloudflare Only`
4. **Action**: Allow
5. **Priority**: 100
6. **Source**: Service Tag
7. **Service Tag**: `AzureFrontDoor.Backend` (or use Cloudflare IP ranges)
8. Click **OK**

**Alternative - Use Cloudflare IP Ranges** (More Secure):
1. Get Cloudflare IP ranges: [Cloudflare IPs](https://www.cloudflare.com/ips/)
2. Download IPv4 and IPv6 ranges
3. **Azure Portal** → App Service → **Networking** → **Access Restrictions**
4. For each IP range:
   - Click **+ Add rule**
   - **Name**: `Cloudflare IPv4 Range X` (or IPv6)
   - **Action**: Allow
   - **Priority**: 100-200 (increment for each range)
   - **Source**: IP Address/CIDR
   - **IP Address/CIDR**: Paste Cloudflare IP range (e.g., `173.245.48.0/20`)
   - Click **OK**
5. Add **Deny All** rule at the end:
   - **Name**: `Deny All Other Traffic`
   - **Action**: Deny
   - **Priority**: 2147483647 (highest priority = evaluated last)
   - **Source**: Any
   - Click **OK**

**Note**: This step is optional but recommended for maximum security. It ensures only Cloudflare can reach your App Service directly.

### Step 8: Verify Setup

1. **Test HTTPS**: Visit your site via `https://your-domain.com` (should show Cloudflare SSL)
2. **Check Headers**:
   - Open browser dev tools (F12) → **Network** tab
   - Reload page
   - Click on any request → **Headers** tab
   - Look for `cf-ray` header (confirms Cloudflare is proxying)
   - Look for `server: cloudflare` header
3. **Cloudflare Analytics**:
   - Dashboard → **Analytics** → **Overview**
   - Verify traffic is being recorded
   - Check **Security** tab to see blocked threats
4. **Test Direct Access** (if Step 7 completed):
   - Try accessing `https://floripatalks-app.azurewebsites.net` directly
   - Should be blocked (403 Forbidden) if IP restrictions are working
   - Access via your domain should work normally

### Cloudflare Free Tier Limits

- ✅ Unlimited DDoS protection
- ✅ Basic WAF rules
- ✅ Unlimited bandwidth
- ✅ 100 page rules
- ✅ Basic analytics
- ⚠️ Rate limiting: 1,000 requests/minute per IP (usually sufficient)

### Troubleshooting

**Site not loading**:
- Check DNS propagation: `nslookup your-domain.com`
- Verify CNAME record points to `floripatalks-app.azurewebsites.net`
- Check Cloudflare proxy status (orange cloud icon should be enabled)

**SSL errors**:
- Ensure SSL/TLS mode is set to **Full (strict)**
- Verify Azure App Service has valid SSL certificate
- Wait a few minutes for SSL to propagate

**403 Forbidden from Azure**:
- Check `ALLOWED_HOSTS` includes your domain
- If using IP restrictions, ensure Cloudflare IPs are allowed

### Quick Setup Checklist

- [ ] Created Cloudflare account
- [ ] Added domain to Cloudflare
- [ ] Updated nameservers at domain registrar
- [ ] Configured DNS CNAME record (proxied/orange cloud)
- [ ] Set SSL/TLS mode to **Full (strict)**
- [ ] Enabled WAF and Bot Fight Mode
- [ ] Updated Azure `ALLOWED_HOSTS` with your domain
- [ ] (Optional) Restricted Azure to Cloudflare IPs
- [ ] Verified site loads via custom domain
- [ ] Confirmed `cf-ray` header in browser dev tools
- [ ] Checked Cloudflare Analytics for traffic

**Setup Time**: ~30-60 minutes (mostly waiting for DNS propagation)

---

## Troubleshooting

### Common Issues

1. **Application Not Starting**:
   - Check startup command in App Service settings
   - Review logs in Azure Portal → Log stream
   - Verify `DJANGO_SETTINGS_MODULE` is set

2. **Static Files Not Loading**:
   - Ensure `collectstatic` runs during deployment
   - Check `STATIC_ROOT` and `STATIC_URL` settings
   - Verify files exist in `staticfiles/` directory

4. **Environment Variables Not Working**:
   - Restart App Service after adding variables
   - Check variable names match code
   - Verify no typos

---

## Additional AZ-204 Learning Opportunities (Low/No Cost)

These Azure services can be added to your app for hands-on AZ-204 exam practice without significant cost:

### 1. Azure Key Vault (AZ-204: Implement Secure Cloud Solutions)
**What**: Secure storage service for secrets, keys, and certificates with access control and audit logging
**Why**: Better than App Settings for secrets because it provides centralized management, automatic rotation, and fine-grained access control

**Cost**: Free tier available (first 10,000 operations/month free)

**What to learn**:
- Store secrets (e.g., `SECRET_KEY`, `GOOGLE_CLIENT_SECRET`) in Key Vault instead of App Settings
- Access secrets from App Service using Managed Identity
- Rotate secrets without redeploying

**Implementation**:
- Portal: [Create Key Vault](https://portal.azure.com/#create/Microsoft.KeyVault)
- Grant App Service access via Managed Identity
- Update Django settings to fetch secrets from Key Vault

**AZ-204 Topics**: Managed Identity, Key Vault, Secret Management

---

### 2. Deployment Slots (AZ-204: Implement CI/CD)
**What**: Separate instances of your app (like staging and production) that can run simultaneously and be swapped instantly
**Why**: Enables zero-downtime deployments, allows testing in production-like environment, and provides instant rollback if issues occur

**Cost**: Included in Free tier - no additional cost (available on all tiers)

**What to learn**:
- Create staging slot for testing before production
- Swap slots for zero-downtime deployments
- Test in production-like environment

**Implementation**:
- Portal: App Service → **Deployment slots** → **Add Slot** → Name: `staging`
- Deploy to staging slot first, test, then swap to production

**AZ-204 Topics**: Deployment strategies, Blue-Green deployments

---

### 3. Application Insights (AZ-204: Implement Monitoring)
**What**: Application Performance Monitoring (APM) service that tracks performance metrics, errors, and user behavior
**Why**: Helps identify performance issues, track errors in production, understand user patterns, and set up proactive alerts

**Cost**: Free tier (5GB data ingestion/month, 90-day retention)

**What to learn**:
- Application performance monitoring
- Custom metrics and events
- Log queries (KQL - Kusto Query Language)
- Alert rules and action groups

**Implementation**:
- Portal: App Service → **Application Insights** → **Turn on Application Insights**
- Add custom telemetry in Django code
- Create dashboards and alerts

**AZ-204 Topics**: Application Insights, Log Analytics, KQL queries, Alerts

---

### 4. Azure Blob Storage (AZ-204: Implement Data Storage)
**What**: Cloud storage service for unstructured data (files, images, videos) with high availability and global access
**Why**: Better than App Service filesystem for user uploads because files persist across deployments, scale independently, and are accessible via CDN

**Cost**: ~$0.02/GB/month (very cheap for small apps)

**What to learn**:
- Store media files (user uploads) in Blob Storage
- Configure CORS for cross-origin access
- Access policies and SAS tokens
- Lifecycle management

**Implementation**:
- Portal: [Create Storage Account](https://portal.azure.com/#create/Microsoft.StorageAccount)
- Install `django-storages[azure]`
- Configure Django to use Azure Storage backend

**AZ-204 Topics**: Blob Storage, Storage accounts, CORS, SAS tokens

---

### 5. Azure Functions (AZ-204: Implement Serverless Solutions)
**What**: Serverless compute service that runs code in response to events (HTTP requests, timers, queues) without managing servers
**Why**: Perfect for background tasks, scheduled jobs, and event-driven workflows; scales automatically and only charges for execution time

**Cost**: Consumption plan - 1 million free requests/month, 400,000 GB-seconds compute/month

**What to learn**:
- Serverless architecture
- Event-driven programming
- Function triggers (HTTP, Timer, Queue)
- Bindings (Blob, Cosmos DB, etc.)

**Implementation Ideas**:
- Create a function to send email notifications (when new topic is created)
- Scheduled function for daily reports
- HTTP-triggered function for webhooks

**AZ-204 Topics**: Azure Functions, Serverless computing, Event-driven architecture

---

### 6. Azure Service Bus (AZ-204: Implement Message-Based Solutions)
**What**: Message broker service that enables asynchronous communication between applications using queues and topics
**Why**: Decouples services, enables reliable message delivery, handles high throughput, and supports pub/sub patterns for event-driven architecture

**Cost**: Basic tier ~$0.05/month (very cheap)

**What to learn**:
- Message queues and topics
- Pub/Sub patterns
- Dead-letter queues
- Message sessions

**Implementation Ideas**:
- Queue email notifications
- Decouple heavy operations from web requests
- Implement event-driven architecture

**AZ-204 Topics**: Service Bus, Message queues, Pub/Sub patterns

---

### Recommended Learning Path

1. **Start**: App Service + Application Insights (monitoring)
2. **Next**: Deployment Slots (CI/CD patterns)
3. **Then**: Key Vault (security best practices)
4. **Optional**: Blob Storage (if you need media files)
5. **Advanced**: Azure Functions (serverless patterns)

**Total Additional Cost**: ~$0-1/month (most are free or very cheap)

---

## Recommended Next Steps

1. **Deploy to Azure App Service Free Tier**:
   - Test deployment locally
   - Deploy to free tier (F1)
   - Verify functionality and SSL certificate

2. **Set Up CI/CD**:
   - Create GitHub Actions workflow
   - Test auto-deployment
   - Verify tests run

3. **Add Monitoring** (Optional):
   - Set up Application Insights (free tier available)
   - Configure alerts
   - Monitor usage and costs

4. **Upgrade to Basic Tier** (only if needed):
   - Upgrade when you exceed 60 minutes/day compute time
   - Better performance and unlimited compute

---

## Resources

- [Azure App Service Python Documentation](https://learn.microsoft.com/en-us/azure/app-service/quickstart-python)
- [Django on Azure Tutorial](https://learn.microsoft.com/en-us/azure/app-service/tutorial-python-postgresql-app-django)
- [GitHub Actions for Azure](https://github.com/azure/webapps-deploy)
- [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/)
- [Azure Free Account](https://azure.microsoft.com/en-us/free/)

---

## Database Backup Strategy (Optional - AZ-204: Implement Data Storage)

This section covers automated SQLite database backups to Azure Blob Storage with retention policies.

### Storage Architecture

**Live Database File**:
- **Location**: App Service persistent storage (`/home/site/wwwroot/db.sqlite3`)
- **Why**: App needs direct file access, persistent storage survives restarts
- **Standard Practice**: Live database stays on the server filesystem

**Backup Files**:
- **Location**: Azure Blob Storage (separate from App Service)
- **Why**:
  - More durable and reliable than App Service filesystem
  - Protects against App Service failures or data corruption
  - Cheaper for long-term storage
  - Better separation of concerns (backups separate from live data)
- **Process**: Backups are copied FROM App Service filesystem TO Blob Storage

**Summary**: Live DB on server → Backups in Blob Storage

### Requirements

- **Backup Frequency**: Every 3 hours
- **Pre-Deployment Backup**: Before every deployment
- **Retention Policy**:
  - Last 10 snapshots (3-hourly backups)
  - Last 3 weekly backups
  - Last 1 monthly backup (30 days)
- **Storage**: Azure Blob Storage
- **Naming Convention**: `db_backup_YYYYMMDD_HHMMSS_snapshot.sqlite3`, `db_backup_YYYYMMDD_weekly.sqlite3`, `db_backup_YYYYMMDD_monthly.sqlite3`

### Step 1: Create Storage Account and Container

**What**: Storage Account is Azure's cloud storage service; Container is like a folder within storage for organizing files
**Why**: Provides durable, scalable storage for backups that survives App Service failures and is cheaper than keeping backups on the server

**Azure Portal**:
1. [Create Storage Account](https://portal.azure.com/#create/Microsoft.StorageAccount)
   - Resource Group: `floripatalks-rg`
   - Name: `floripatalksbackups` (must be globally unique)
   - Region: `Brazil South`
   - Performance: `Standard`
   - Redundancy: `LRS` (Locally Redundant Storage - cheapest)
2. Create Container:
   - Storage Account → **Containers** → **+ Container**
   - Name: `db-backups`
   - Public access level: `Private` (no anonymous access)

**Get Connection String**:
- Storage Account → **Access keys** → Copy **Connection string** (key1)

### Step 2: Install Required Package

**What**: Azure Storage Blob SDK package that provides Python libraries to interact with Azure Blob Storage
**Why**: Required to upload backup files to Azure Blob Storage programmatically from your Django app

Add to `pyproject.toml`:
```toml
azure-storage-blob = "^12.0.0"
```

Or install:
```bash
uv add azure-storage-blob
```

### Step 3: Create Django Management Command

**What**: A Django command that can be run via `python manage.py backup_database` to automate database backups
**Why**: Provides a reusable, scriptable way to backup your database with retention policies, can be called from CI/CD or scheduled tasks

Create `core/management/commands/backup_database.py`:

```python
"""
Django management command to backup SQLite database to Azure Blob Storage.

This command:
1. Copies the live SQLite file from App Service filesystem (/home/site/wwwroot/db.sqlite3)
2. Uploads it to Azure Blob Storage
3. Cleans up old backups based on retention policy

Usage:
    python manage.py backup_database [--type snapshot|weekly|monthly]

Note: Can be run directly on App Service (via SSH) or from GitHub Actions (after downloading file)
"""

import os
import shutil
from datetime import datetime
from pathlib import Path

from azure.core.exceptions import AzureError
from azure.storage.blob import BlobServiceClient
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Backup SQLite database to Azure Blob Storage"

    def add_arguments(self, parser):
        parser.add_argument(
            "--type",
            type=str,
            choices=["snapshot", "weekly", "monthly"],
            default="snapshot",
            help="Backup type: snapshot (3-hourly), weekly, or monthly",
        )

    def handle(self, *args, **options):
        backup_type = options["type"]
        db_path = Path(settings.DATABASES["default"]["NAME"])

        if not db_path.exists():
            self.stdout.write(self.style.ERROR(f"Database file not found: {db_path}"))
            return

        # Generate filename based on type
        now = datetime.now()
        if backup_type == "snapshot":
            filename = f"db_backup_{now.strftime('%Y%m%d_%H%M%S')}_snapshot.sqlite3"
        elif backup_type == "weekly":
            filename = f"db_backup_{now.strftime('%Y%m%d')}_weekly.sqlite3"
        else:  # monthly
            filename = f"db_backup_{now.strftime('%Y%m%d')}_monthly.sqlite3"

        # Get Azure Storage connection string
        connection_string = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
        if not connection_string:
            self.stdout.write(
                self.style.ERROR("AZURE_STORAGE_CONNECTION_STRING not set")
            )
            return

        container_name = "db-backups"

        try:
            # Copy database to temporary location
            temp_backup = Path(f"/tmp/{filename}")
            shutil.copy2(db_path, temp_backup)

            # Upload to Azure Blob Storage
            blob_service_client = BlobServiceClient.from_connection_string(
                connection_string
            )
            container_client = blob_service_client.get_container_client(container_name)

            with open(temp_backup, "rb") as data:
                container_client.upload_blob(name=filename, data=data, overwrite=True)

            # Clean up temporary file
            temp_backup.unlink()

            self.stdout.write(
                self.style.SUCCESS(f"✅ Backup created: {filename} ({backup_type})")
            )

            # Clean up old backups based on retention policy
            self._cleanup_old_backups(container_client, backup_type)

        except AzureError as e:
            self.stdout.write(self.style.ERROR(f"Azure Storage error: {e}"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Backup failed: {e}"))

    def _cleanup_old_backups(self, container_client, backup_type):
        """Clean up old backups based on retention policy."""
        blobs = list(container_client.list_blobs())

        if backup_type == "snapshot":
            # Keep last 10 snapshots
            snapshots = sorted(
                [b for b in blobs if "_snapshot.sqlite3" in b.name],
                key=lambda x: x.name,
                reverse=True,
            )
            for blob in snapshots[10:]:
                container_client.delete_blob(blob.name)
                self.stdout.write(f"🗑️  Deleted old snapshot: {blob.name}")

        elif backup_type == "weekly":
            # Keep last 3 weeklies
            weeklies = sorted(
                [b for b in blobs if "_weekly.sqlite3" in b.name],
                key=lambda x: x.name,
                reverse=True,
            )
            for blob in weeklies[3:]:
                container_client.delete_blob(blob.name)
                self.stdout.write(f"🗑️  Deleted old weekly: {blob.name}")

        elif backup_type == "monthly":
            # Keep last 1 monthly
            monthlies = sorted(
                [b for b in blobs if "_monthly.sqlite3" in b.name],
                key=lambda x: x.name,
                reverse=True,
            )
            for blob in monthlies[1:]:
                container_client.delete_blob(blob.name)
                self.stdout.write(f"🗑️  Deleted old monthly: {blob.name}")
```

### Step 4: Configure Environment Variable

**What**: Connection string that contains credentials and endpoint information to connect to your Azure Storage Account
**Why**: Allows your backup script to authenticate and upload files to Blob Storage without hardcoding credentials

**Azure Portal**:
- App Service → **Configuration** → **Application settings**
- Add: `AZURE_STORAGE_CONNECTION_STRING` = `<connection-string-from-storage-account>`
- Click **Save** → **Continue**

### Step 5: Schedule Automated Backups (Every 3 Hours)

**What**: GitHub Actions scheduled workflow runs automatically on a cron schedule (every 3 hours) to trigger backups
**Why**: Ensures regular backups without manual intervention, runs in the cloud (no local machine needed), and provides backup history in GitHub

**Option A: GitHub Actions Scheduled Workflow** (Recommended)

Create `.github/workflows/backup-database.yml`:

```yaml
name: Backup Database

on:
  schedule:
    # Every 3 hours (UTC): 00:00, 03:00, 06:00, 09:00, 12:00, 15:00, 18:00, 21:00
    - cron: "0 */3 * * *"
  workflow_dispatch: # Manual trigger

jobs:
  backup:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"

      - name: Install uv
        uses: astral-sh/setup-uv@v4
        with:
          version: "latest"

      - name: Install dependencies
        run: uv sync --frozen

      - name: Install Azure CLI
        uses: azure/setup-az-cli@v3

      - name: Login to Azure
        uses: azure/login@v2
        with:
          creds: ${{ secrets.AZURE_CREDENTIALS }}

      - name: Download database from App Service
        run: |
          az webapp deployment source download \
            --resource-group floripatalks-rg \
            --name floripatalks-app \
            --output db.sqlite3

      - name: Run backup command
        run: |
          uv run python manage.py backup_database --type snapshot
        env:
          AZURE_STORAGE_CONNECTION_STRING: ${{ secrets.AZURE_STORAGE_CONNECTION_STRING }}
          DJANGO_SETTINGS_MODULE: floripatalks.settings.production
```

**Option B: Azure Functions Timer Trigger** (Alternative)

Create an Azure Function that runs every 3 hours and calls your backup endpoint. This runs directly on Azure infrastructure.

**Option C: Run on App Service via SSH** (Simplest for testing)

1. **Enable SSH**: App Service → **Configuration** → **General settings** → **SSH** → **On**
2. **SSH into App Service**: App Service → **SSH** → Connect
3. **Run backup manually**: `python manage.py backup_database --type snapshot`
4. **Schedule via cron** (if supported) or use Azure Functions to trigger HTTP endpoint

### Step 6: Add Pre-Deployment Backup

**What**: Backup step added to CI/CD pipeline that runs before code deployment to preserve database state
**Why**: Protects against deployment failures that might corrupt the database, allows rollback to pre-deployment state if needed

Update `.github/workflows/azure-deploy.yml` to backup before deployment:

```yaml
# Add this step BEFORE "Deploy to Azure Web App"
- name: Backup database before deployment
  run: |
    # Download database
    az webapp deployment source download \
      --resource-group floripatalks-rg \
      --name floripatalks-app \
      --output db.sqlite3

    # Run backup
    uv run python manage.py backup_database --type snapshot
  env:
    AZURE_STORAGE_CONNECTION_STRING: ${{ secrets.AZURE_STORAGE_CONNECTION_STRING }}
    DJANGO_SETTINGS_MODULE: floripatalks.settings.production
  continue-on-error: true # Don't fail deployment if backup fails
```

### Step 7: Configure GitHub Secrets

**What**: Secure storage in GitHub for sensitive values (connection strings, credentials) that can be accessed by GitHub Actions workflows
**Why**: Keeps secrets out of your code repository, allows CI/CD to authenticate with Azure services securely

**GitHub**: Repository → **Settings** → **Secrets and variables** → **Actions**

Add these secrets:

1. **`AZURE_STORAGE_CONNECTION_STRING`**:
   - Get from: Storage Account → **Access keys** → **Connection string** (key1)
   - Value: `DefaultEndpointsProtocol=https;AccountName=...`

2. **`AZURE_CREDENTIALS`** (for Azure login):
   - Create service principal:
   ```bash
   az ad sp create-for-rbac --name floripatalks-github-actions \
     --role contributor \
     --scopes /subscriptions/<subscription-id>/resourceGroups/floripatalks-rg \
     --sdk-auth
   ```
   - Copy entire JSON output to GitHub secret `AZURE_CREDENTIALS`

### Step 8: Manual Weekly/Monthly Backups

**What**: Separate GitHub Actions workflows that run on a schedule (weekly/monthly) to create long-term backup archives
**Why**: Provides different retention periods (keep weeklies longer than daily snapshots) and ensures long-term data preservation

Create scheduled workflows for weekly and monthly backups:

**Weekly Backup** (`.github/workflows/backup-weekly.yml`):
```yaml
name: Weekly Database Backup

on:
  schedule:
    - cron: "0 0 * * 0" # Every Sunday at midnight UTC
  workflow_dispatch:

jobs:
  backup:
    runs-on: ubuntu-latest
    steps:
      # ... same steps as backup-database.yml but use:
      - name: Run weekly backup
        run: uv run python manage.py backup_database --type weekly
```

**Monthly Backup** (`.github/workflows/backup-monthly.yml`):
```yaml
name: Monthly Database Backup

on:
  schedule:
    - cron: "0 0 1 * *" # First day of month at midnight UTC
  workflow_dispatch:

jobs:
  backup:
    runs-on: ubuntu-latest
    steps:
      # ... same steps but use:
      - name: Run monthly backup
        run: uv run python manage.py backup_database --type monthly
```

### Step 9: Restore from Backup

**What**: Process of downloading a backup file from Blob Storage and replacing the live database file on App Service
**Why**: Enables recovery from data corruption, accidental deletions, or deployment issues by restoring to a previous database state

**Azure Portal**:
1. Storage Account → **Containers** → `db-backups`
2. Select backup file → **Download**
3. Upload to App Service via **SSH** or **Kudu Console**:
   - App Service → **SSH** or **Advanced Tools** → **Go**
   - Navigate to `/home/site/wwwroot/`
   - Upload downloaded backup file
   - Rename to `db.sqlite3`

**Via Azure CLI**:
```bash
# Download backup
az storage blob download \
  --account-name floripatalksbackups \
  --container-name db-backups \
  --name db_backup_20250115_120000_snapshot.sqlite3 \
  --file db.sqlite3

# Upload to App Service
az webapp deployment source config-zip \
  --resource-group floripatalks-rg \
  --name floripatalks-app \
  --src db.sqlite3
```

### Cost Estimate

- **Storage Account (LRS)**: ~$0.018/GB/month
- **Example**: 100MB database × 10 snapshots + 3 weeklies + 1 monthly = ~1.4GB
- **Monthly Cost**: ~$0.03/month (negligible)

### Verification

**Test Backup**:
```bash
# On App Service (via SSH or locally)
python manage.py backup_database --type snapshot
```

**Check Backups**:
- **Azure Portal**: Storage Account → **Containers** → `db-backups` → View all backup files

---

## Summary

**Simplest Path**: Azure App Service with:
- **Free tier (F1)** - $0/month (includes free SSL)
- GitHub Actions for CI/CD
- SQLite database (free, included in App Service storage)
- **Region**: Brazil South (optimal for Brazilian users)
- **Total: ~$0-1/month** (free tier + optional Blob Storage)

**Complexity**: Low - Most setup can be done via Azure Portal UI  
**Time to Deploy**: 1-2 hours for initial setup  
**Maintenance**: Minimal - Azure handles infrastructure

**Important Notes**:
- Free tier includes free SSL certificates for `*.azurewebsites.net` domains
- SQLite is suitable for most web applications with moderate traffic
- Database file is stored in persistent storage (survives restarts)
- Upgrade to Basic tier ($13/month) only if you exceed 60 minutes/day compute time
- **Recommended**: Add Cloudflare (free) for enhanced DDoS protection, WAF, and CDN (see Cloudflare Setup section)
