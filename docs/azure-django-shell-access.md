# Accessing Django Shell in Azure App Service

**Purpose**: Guide on how to access Django shell in Azure App Service to run management commands like `createsuperuser`

---

## Methods to Access Django Shell

### Method 1: Using Azure Portal SSH (Recommended) ⭐

**What**: Direct SSH access to your App Service container

**Why**: Most straightforward method, full terminal access

**Steps**:

1. **Enable SSH** (REQUIRED - must be enabled first):
   - Azure Portal → Your App Service (`floripatalks-app`)
   - **Configuration** → **General settings**
   - Scroll down to find **SSH** setting
   - Set **SSH** to **On** (if it's Off)
   - Click **Save** → **Continue**
   - **Important**: You may need to restart the app after enabling SSH

2. **Connect via SSH**:
   - Go to **Development Tools** → **SSH** (or **Advanced Tools** → **Go** → **SSH**)
   - Click **SSH** link
   - This opens an SSH terminal in your browser

3. **Navigate to your app directory**:
   ```bash
   cd /home/site/wwwroot
   ```

4. **Activate Python environment** (if using virtual environment):
   ```bash
   source /home/site/wwwroot/.venv/bin/activate
   # Or if using system Python:
   # python3 manage.py ...
   ```

5. **Run Django shell or createsuperuser**:
   ```bash
   # For Django shell:
   python manage.py shell

   # For createsuperuser:
   python manage.py createsuperuser
   ```

6. **Follow prompts**:
   ```
   Username: admin
   Email address: admin@example.com
   Password:
   Password (again):
   Superuser created successfully.
   ```

---

### Method 2: Using Azure Portal Console (Kudu)

**What**: Web-based console access via Kudu (Advanced Tools)

**Why**: No SSH setup needed, works immediately

**Steps**:

1. **Open Kudu Console**:
   - Azure Portal → Your App Service
   - **Development Tools** → **Advanced Tools** → **Go**
   - Or navigate directly to: `https://floripatalks-app.scm.azurewebsites.net`

2. **Open Debug Console**:
   - Click **Debug console** → **CMD** (or **PowerShell**)
   - This opens a file browser and terminal

3. **Navigate to app directory**:
   - Click on `site` → `wwwroot`
   - Or use terminal: `cd D:\home\site\wwwroot` (Windows) or `/home/site/wwwroot` (Linux)

4. **Run Django commands**:
   ```bash
   python manage.py createsuperuser
   ```

**Note**: Paths may differ slightly between Windows and Linux App Service plans.

---

### Method 3: Using Azure Cloud Shell with Azure CLI

**What**: Use Azure CLI from Cloud Shell to execute commands remotely

**Why**: Good if you prefer command-line tools, can script commands

**Steps**:

1. **Open Azure Cloud Shell**:
   - Azure Portal → Click Cloud Shell icon (`>_`) in top menu
   - Choose **Bash**

2. **SSH into App Service**:
   ```bash
   az webapp ssh \
     --resource-group floripatalks-rg \
     --name floripatalks-app
   ```

3. **Once connected, run Django commands**:
   ```bash
   cd /home/site/wwwroot
   python manage.py createsuperuser
   ```

---

### Method 4: Using Azure CLI from Local Machine

**What**: SSH into App Service from your local terminal

**Why**: If you have Azure CLI installed locally

**Prerequisites**: Azure CLI installed and logged in

**Steps**:

```bash
# Login to Azure
az login

# SSH into App Service
az webapp ssh \
  --resource-group floripatalks-rg \
  --name floripatalks-app

# Once connected:
cd /home/site/wwwroot
python manage.py createsuperuser
```

---

## Important Notes

### Environment Variables

**What**: Django needs environment variables to load production settings

**Why**: Your `production.py` requires `SECRET_KEY`, `GOOGLE_CLIENT_ID`, etc.

**Solution**: These should already be set in Azure App Service → **Configuration** → **Application settings**

If you get errors about missing environment variables:
1. Check Azure Portal → App Service → **Configuration** → **Application settings**
2. Ensure these are set:
   - `DJANGO_SETTINGS_MODULE=floripatalks.settings.production`
   - `SECRET_KEY=...`
   - `GOOGLE_CLIENT_ID=...`
   - `GOOGLE_CLIENT_SECRET=...`
   - `ALLOWED_HOSTS=...`

### Python Path

**What**: You need to use the correct Python interpreter

**Why**: Azure App Service may have multiple Python versions

**Solution**:
- Try `python manage.py` first
- If that doesn't work, try `python3 manage.py`
- Or use full path: `/usr/bin/python3 manage.py`

### Database Location

**What**: SQLite database file location in Azure

**Why**: Need to know where the database is stored

**Location**: `/home/site/wwwroot/db.sqlite3` (Linux) or `D:\home\site\wwwroot\db.sqlite3` (Windows)

---

## Quick Reference: Common Django Commands in Azure

```bash
# Create superuser
python manage.py createsuperuser

# Django shell
python manage.py shell

# Run migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput

# Check Django version
python manage.py --version

# List all management commands
python manage.py help
```

---

## Troubleshooting

### "Command not found: python"

**Solution**: Try `python3` instead:
```bash
python3 manage.py createsuperuser
```

### "Module not found" or Import Errors

**Cause**: Virtual environment not activated or dependencies not installed

**Solution**:
```bash
# Activate virtual environment (if exists)
source /home/site/wwwroot/.venv/bin/activate

# Or install dependencies
pip install -r requirements.txt
# Or with uv:
uv sync
```

### "SECRET_KEY environment variable must be set"

**Cause**: Environment variables not configured in Azure

**Solution**:
1. Azure Portal → App Service → **Configuration** → **Application settings**
2. Add missing environment variables
3. Click **Save** → **Continue**
4. Restart the app if needed

### "Permission denied" when creating superuser

**Cause**: Database file permissions

**Solution**: Check database file permissions:
```bash
ls -la /home/site/wwwroot/db.sqlite3
# Should be readable/writable by the app user
```

---

## Security Best Practices

### After Creating Superuser

1. **Use Strong Password**: Don't use default or weak passwords
2. **Limit Admin Access**: Only create superusers when needed
3. **Use Environment Variables**: Never hardcode credentials
4. **Rotate Credentials**: Change passwords periodically

### Alternative: Create Superuser via Management Command

Instead of interactive `createsuperuser`, you can create a non-interactive command:

```python
# In Django shell or custom management command
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.create_superuser('admin', 'admin@example.com', 'secure-password')
```

**Note**: This is less secure (password in command history), but useful for automation.

---

## Summary

**Easiest Method**: Azure Portal → **SSH** → Connect → `python manage.py createsuperuser`

**Most Reliable**: Azure Portal → **Advanced Tools** → **Kudu Console** → Debug Console

**For Automation**: Azure Cloud Shell with `az webapp ssh`

All methods achieve the same goal: accessing Django's management commands in your Azure App Service environment.
