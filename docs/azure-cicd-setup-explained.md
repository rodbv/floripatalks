# Azure CI/CD Setup Explained

**Created**: 2025-12-10  
**Purpose**: Detailed explanation of what was done to set up CI/CD for FloripaTalks and why each step was necessary

## Overview

This document explains the complete CI/CD setup process for deploying FloripaTalks to Azure App Service using GitHub Actions. It covers authentication, secrets management, role assignments, and the reasoning behind each decision.

---

## Table of Contents

1. [Authentication Method: Service Principal vs Publish Profile](#authentication-method-service-principal-vs-publish-profile)
2. [Creating the Service Principal](#creating-the-service-principal)
3. [Setting Up GitHub Secrets](#setting-up-github-secrets)
4. [Azure Role Assignment](#azure-role-assignment)
5. [GitHub Actions Workflow Configuration](#github-actions-workflow-configuration)
6. [Complete Setup Checklist](#complete-setup-checklist)

---

## Authentication Method: Service Principal vs Publish Profile

### What We Did

We chose to use **Service Principal Authentication** instead of Publish Profile authentication.

### Why

**Publish Profile Authentication:**
- ❌ Requires Basic Authentication to be enabled in Azure App Service
- ❌ Less secure (uses username/password credentials)
- ❌ Can be disabled by Azure security policies
- ❌ Single-purpose (only for deployment)

**Service Principal Authentication:**
- ✅ More secure (uses OAuth2 client credentials)
- ✅ Works even when Basic Auth is disabled
- ✅ Follows Azure security best practices
- ✅ Can be scoped to specific resources (principle of least privilege)
- ✅ Can be used for multiple operations (deployment, backups, etc.)

### When to Use Each

- **Use Service Principal**: Production environments, when Basic Auth is disabled, for multiple operations
- **Use Publish Profile**: Quick testing, when Basic Auth is enabled, simple deployments only

---

## Creating the Service Principal

### What We Did

Created an Azure App Registration that acts as a service account for GitHub Actions to authenticate with Azure.

### Why

GitHub Actions needs credentials to deploy to Azure. Instead of using your personal Azure account, we create a dedicated service account (service principal) that:
- Has limited permissions (only what's needed)
- Can be rotated/revoked independently
- Doesn't require your personal credentials
- Follows security best practices

### Step-by-Step Process

#### Step 1: Create App Registration

**What**: Created an application registration in Azure Active Directory (Microsoft Entra ID)

**Why**: This creates an identity that can authenticate to Azure services

**How**:
1. Azure Portal → **Microsoft Entra ID** → **App registrations** → **New registration**
2. Name: `floripatalks-github-actions`
3. Click **Register**

**Result**: You get:
- **Application (client) ID**: `12e65db4-7a3c-4a51-ad0d-1b5edd21340c` - Used to identify the app
- **Directory (tenant) ID**: `c758e737-0df2-4e79-9799-303fc6ef0838` - Your Azure AD tenant
- **Object ID**: `75983025-85ee-4e8d-aeab-75e97fd0b0dd` - App Registration Object ID

#### Step 2: Create Client Secret

**What**: Generated a password (client secret) for the service principal

**Why**: The service principal needs credentials to authenticate. The client secret is like a password.

**How**:
1. In the App Registration → **Certificates & secrets** → **New client secret**
2. Description: `GitHub Actions`
3. Expires: Choose expiration (e.g., 24 months)
4. Click **Add**
5. **IMPORTANT**: Copy the **Value** immediately (you won't see it again!)

**Result**: Client Secret Value: `YOUR_CLIENT_SECRET_VALUE_HERE` (copy this immediately!)

**Security Note**:
- This secret expires after the chosen period
- You'll need to create a new secret before it expires
- Store it securely (we put it in GitHub Secrets, not in code)

#### Step 3: Service Principal Creation

**What**: Azure automatically creates a Service Principal in "Enterprise Applications" when the App Registration is first used

**Why**: The App Registration is the "application definition", but the Service Principal is the actual identity that gets permissions. They're linked but different objects.

**How**: This happens automatically when you first assign a role or use the app registration

**Result**:
- Service Principal Object ID: `32b8ac0b-5b4c-4252-9e71-b3d63aa7fdd5` (different from App Registration Object ID)
- This is the ID you use for role assignments

---

## Setting Up GitHub Secrets

### What We Did

Stored the Azure credentials as a secret in GitHub so GitHub Actions can authenticate to Azure.

### Why

**Security**:
- Secrets are encrypted and never exposed in logs
- Only GitHub Actions workflows can access them
- Can be rotated without changing code

**Separation of Concerns**:
- Credentials stay out of your code repository
- Different environments can use different secrets
- Easy to update without code changes

### The JSON Structure

**What**: Created a JSON file with all authentication information

**Why**: The `azure/login@v2` action requires credentials in a specific JSON format

**Structure**:
```json
{
  "clientId": "12e65db4-7a3c-4a51-ad0d-1b5edd21340c",           // Application (client) ID
  "clientSecret": "YOUR_CLIENT_SECRET_VALUE_HERE", // Client secret value (from step above)
  "subscriptionId": "8d65175c-b746-4784-bc92-3b4149ebfbce",    // Your Azure subscription
  "tenantId": "c758e737-0df2-4e79-9799-303fc6ef0838",          // Your Azure AD tenant
  "activeDirectoryEndpointUrl": "https://login.microsoftonline.com",
  "resourceManagerEndpointUrl": "https://management.azure.com/",
  "activeDirectoryGraphResourceId": "https://graph.windows.net/",
  "sqlManagementEndpointUrl": "https://management.core.windows.net:8443/",
  "galleryEndpointUrl": "https://gallery.azure.com/",
  "managementEndpointUrl": "https://management.core.windows.net/"
}
```

**What Each Field Means**:
- `clientId`: Identifies which application is authenticating
- `clientSecret`: The password for authentication
- `subscriptionId`: Which Azure subscription to access
- `tenantId`: Which Azure AD tenant (organization) the app belongs to
- Other URLs: Endpoints for different Azure services (standard values, rarely change)

### How to Add to GitHub

1. **GitHub Repository** → **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Name: `AZURE_CREDENTIALS` (must match what the workflow expects)
4. Value: Paste the entire JSON from above
5. Click **Add secret**

**Why This Name**: The workflow file uses `${{ secrets.AZURE_CREDENTIALS }}`, so the secret name must match exactly.

---

## Azure Role Assignment

### What We Did

Gave the service principal permission to deploy to Azure App Service by assigning the "Contributor" role.

### Why

**Role-Based Access Control (RBAC)**:
- Azure uses RBAC to control what each identity can do
- The service principal needs permissions to deploy code
- "Contributor" role allows full management of resources (read, write, delete)

**Principle of Least Privilege**:
- We scoped the role to the resource group level (not subscription-wide)
- The service principal can only manage resources in `floripatalks-rg`
- Can't access other resource groups or subscriptions

### The Role Assignment

**What**: Assigned "Contributor" role to the service principal

**Scope**: Resource group level (`/subscriptions/.../resourceGroups/floripatalks-rg`)

**Why Resource Group Level**:
- ✅ More secure (limited to one resource group)
- ✅ Sufficient for deployment needs
- ✅ Follows security best practices
- ❌ Subscription level would be too broad (could access all resources)

**Command Used** (Azure Cloud Shell):
```bash
az role assignment create \
  --assignee-object-id 32b8ac0b-5b4c-4252-9e71-b3d63aa7fdd5 \
  --role "Contributor" \
  --scope "/subscriptions/8d65175c-b746-4784-bc92-3b4149ebfbce/resourceGroups/floripatalks-rg"
```

**What This Does**:
- `--assignee-object-id`: The service principal (not the app registration) Object ID
- `--role "Contributor"`: Gives full management permissions
- `--scope`: Limits permissions to the resource group only

### Why We Used Cloud Shell

**Problem**: The service principal didn't appear in the Azure Portal's "Select members" search

**Why**:
- Portal search sometimes doesn't find service principals immediately
- Object ID search is more reliable
- Cloud Shell provides direct access to Azure CLI

**Alternative**: Could have waited for propagation (up to 30 minutes) or used PowerShell

---

## GitHub Actions Workflow Configuration

### What We Did

Configured `.github/workflows/main_floripatalks-app.yml` to automatically deploy when code is pushed to the `main` branch.

### Workflow Steps Explained

#### Step 1: Checkout Code
```yaml
- uses: actions/checkout@v4
```
**What**: Downloads your repository code to the GitHub Actions runner  
**Why**: The workflow needs your code to build and deploy it

#### Step 2: Set Up Python
```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: ${{ env.PYTHON_VERSION }}
```
**What**: Installs Python 3.13 on the runner  
**Why**: Your application requires Python to run

#### Step 3: Install uv
```yaml
- name: Install uv
  uses: astral-sh/setup-uv@v4
  with:
    version: "latest"
```
**What**: Installs `uv`, the fast Python package manager  
**Why**: Your project uses `uv` for dependency management (faster than pip)

#### Step 4: Install Dependencies
```yaml
- name: Install dependencies
  run: |
    uv sync --frozen
```
**What**: Installs all Python packages from `uv.lock`  
**Why**:
- `--frozen` ensures exact versions (reproducible builds)
- Requires `uv.lock` to be committed (which we fixed earlier)

#### Step 5: Run Tests
```yaml
- name: Run tests
  run: |
    uv run pytest
```
**What**: Runs your test suite  
**Why**: Ensures code quality before deployment (catches bugs early)

#### Step 6: Collect Static Files
```yaml
- name: Collect static files
  run: |
    uv run python manage.py collectstatic --noinput
  env:
    DJANGO_SETTINGS_MODULE: floripatalks.settings.production
    SECRET_KEY: "dummy-secret-key-for-ci-cd-only-not-used-in-production"
    GOOGLE_CLIENT_ID: "dummy-client-id-for-ci-cd"
    GOOGLE_CLIENT_SECRET: "dummy-client-secret-for-ci-cd"
```
**What**: Collects all static files (CSS, JS, images) into `staticfiles/` directory  
**Why**:
- Django needs static files in one location for serving
- Production settings require environment variables
- Dummy values are safe because `collectstatic` doesn't use them

**Why Dummy Values**:
- Production settings file validates that secrets exist
- `collectstatic` doesn't actually use these secrets
- Real values are set in Azure App Service (not in CI/CD)

#### Step 7: Azure Login
```yaml
- name: Azure Login
  uses: azure/login@v2
  with:
    creds: ${{ secrets.AZURE_CREDENTIALS }}
```
**What**: Authenticates GitHub Actions to Azure using the service principal  
**Why**:
- Required before any Azure operations
- Uses the `AZURE_CREDENTIALS` secret we set up
- Creates an authenticated session for subsequent steps

#### Step 8: Deploy to Azure
```yaml
- name: Deploy to Azure Web App
  uses: azure/webapps-deploy@v3
  with:
    app-name: ${{ env.AZURE_WEBAPP_NAME }}
    resource-group: ${{ env.AZURE_WEBAPP_RESOURCE_GROUP }}
    package: .
```
**What**: Uploads your code to Azure App Service  
**Why**:
- Makes your application accessible on the internet
- Uses the authenticated session from previous step
- `package: .` means "deploy everything in the current directory"

---

## Complete Setup Checklist

### Azure Setup ✅

- [x] **App Registration Created**
  - Name: `floripatalks-github-actions`
  - Application (client) ID: `12e65db4-7a3c-4a51-ad0d-1b5edd21340c`
  - Directory (tenant) ID: `c758e737-0df2-4e79-9799-303fc6ef0838`

- [x] **Client Secret Created**
  - Value: `YOUR_CLIENT_SECRET_VALUE_HERE` (replace with your actual secret)
  - Expiration: Set (remember to rotate before expiry!)

- [x] **Service Principal Created**
  - Object ID: `32b8ac0b-5b4c-4252-9e71-b3d63aa7fdd5`
  - Automatically created when App Registration is used

- [x] **Role Assignment**
  - Role: Contributor
  - Scope: Resource group (`floripatalks-rg`)
  - Assigned via Azure Cloud Shell

### GitHub Setup ✅

- [x] **Secret Created**
  - Name: `AZURE_CREDENTIALS`
  - Value: Complete JSON with all credentials
  - Location: Repository Settings → Secrets and variables → Actions

- [x] **Workflow File**
  - Location: `.github/workflows/main_floripatalks-app.yml`
  - Configured for service principal authentication
  - Includes all necessary steps (tests, static files, deployment)

### Project Setup ✅

- [x] **Dependencies**
  - `uv.lock` committed (was previously gitignored, now tracked)
  - `gunicorn` added to dependencies for production server

- [x] **Startup Configuration**
  - `startup.sh` created (runs migrations, starts Gunicorn)
  - `startup.txt` created (tells Azure to run `startup.sh`)

- [x] **Production Settings**
  - `floripatalks/settings/production.py` configured
  - Requires environment variables (set in Azure App Service)

---

## Security Considerations

### What's Secure ✅

- **Secrets in GitHub**: Encrypted, only accessible to workflows
- **Service Principal**: Limited to resource group scope
- **Client Secret**: Stored securely, can be rotated
- **No Credentials in Code**: All secrets are externalized

### What to Watch Out For ⚠️

- **Client Secret Expiration**: Will expire after set period (24 months in our case)
  - **Action**: Create new secret before expiry, update GitHub secret
- **Role Scope**: Currently at resource group level (good, but verify it's sufficient)
- **Secret Files**: `docs/azure-secrets.txt` and `docs/azure-credentials.json` are gitignored
  - **Action**: Don't commit these files, delete them after setup if desired

### Best Practices Followed ✅

- ✅ Service principal instead of personal credentials
- ✅ Least privilege (resource group scope, not subscription)
- ✅ Secrets stored securely (GitHub Secrets, not code)
- ✅ Separate identity for CI/CD (not your personal account)
- ✅ Reproducible builds (`uv.lock` committed)

---

## Troubleshooting

### Common Issues

**"No credentials found" Error**:
- **Cause**: `AZURE_CREDENTIALS` secret not set in GitHub
- **Fix**: Add the secret in GitHub → Settings → Secrets → Actions

**"Access denied" Error**:
- **Cause**: Service principal doesn't have Contributor role
- **Fix**: Verify role assignment with: `az role assignment list --assignee <object-id>`

**"Service principal not found" in Portal**:
- **Cause**: Portal search sometimes doesn't find service principals
- **Fix**: Use Object ID directly or Azure Cloud Shell

**Deployment succeeds but app doesn't start**:
- **Cause**: Missing environment variables in Azure App Service
- **Fix**: Set `SECRET_KEY`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET` in App Service Configuration

---

## Summary

### What We Built

A complete CI/CD pipeline that:
1. Automatically tests code on every push
2. Collects static files
3. Authenticates to Azure securely
4. Deploys to Azure App Service
5. Runs migrations and starts the server

### Why It Works

- **Service Principal**: Provides secure, scoped authentication
- **GitHub Secrets**: Keeps credentials out of code
- **Role Assignment**: Gives necessary permissions without over-privileging
- **Workflow Configuration**: Automates the entire deployment process

### Key Takeaways

1. **Security First**: Service principal + secrets + least privilege
2. **Automation**: Push to main → automatic deployment
3. **Reproducibility**: Lock files ensure consistent builds
4. **Separation**: CI/CD credentials separate from application secrets

---

## Next Steps

After successful deployment:
1. Monitor deployment logs in GitHub Actions
2. Check Azure App Service logs if issues occur
3. Set up monitoring and alerts
4. Plan for secret rotation before expiration

---

**Last Updated**: 2025-12-10  
**Maintained By**: Development Team
