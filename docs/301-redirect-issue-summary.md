# 301 Redirect Issue - Investigation Summary

**Date**: 2025-12-11  
**Status**: IN PROGRESS - Middleware not running in Azure  
**Issue**: All requests returning 301 redirects, causing redirect loops

---

## Problem Description

All HTTP requests to the Azure App Service are returning `301` redirects, causing redirect loops. This affects:
- Home page (`/`)
- Admin page (`/admin`)
- Health checks (`/robots933456.txt`)
- All other routes

**Symptoms**:
- Requests from `169.254.129.1` (Azure health check IP) return `301`
- Requests from browsers return `301`
- No middleware logs appearing in Azure logs
- Middleware code is correct but not executing

---

## Root Cause Hypothesis

The middleware (`core.middleware.AzureProxyHeaderMiddleware`) is **not running** in Azure, even though:
- ✅ Code is correctly written
- ✅ Middleware is correctly wired in `MIDDLEWARE` list
- ✅ Works perfectly locally
- ✅ Latest code is deployed (startup.sh version marker appears)

**Why this causes 301s**:
1. Azure App Service terminates SSL at the load balancer
2. Requests reach Django as HTTP (not HTTPS)
3. Django's `SECURE_PROXY_SSL_HEADER` looks for `HTTP_X_FORWARDED_PROTO` in `request.META`
4. If missing, Django treats requests as HTTP and redirects to HTTPS → `301` loop
5. The middleware should set `HTTP_X_FORWARDED_PROTO=https` but **it's not running**

---

## What We've Tried

### 1. Fixed Middleware Code (Multiple Times)
- ✅ Changed from `request.headers` to `request.META` (Django uses META)
- ✅ Fixed to check `HTTP_X_FORWARDED_PROTO` in `request.META`
- ✅ Added comprehensive error handling
- ✅ Added extensive logging (print + stderr + logger)

### 2. Added Diagnostic Code
- ✅ Version markers in `startup.sh` (✅ **WORKING** - appears in logs)
- ✅ Version markers in `production.py` (❌ **NOT APPEARING** in logs)
- ✅ Module load print in `middleware.py` (❌ **NOT APPEARING** in logs)
- ✅ Import test in `production.py` (❌ **NOT APPEARING** in logs)
- ✅ `__init__` logging in middleware (❌ **NOT APPEARING** in logs)
- ✅ `__call__` logging in middleware (❌ **NOT APPEARING** in logs)

### 3. Configuration Changes
- ✅ `SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")`
- ✅ `SECURE_SSL_REDIRECT = False` (Azure handles HTTPS redirect)
- ✅ Middleware added to `MIDDLEWARE` list at position 0
- ✅ Enabled application logging in Azure (`az webapp log config`)

---

## Current State

### What's Working ✅
- `startup.sh` version marker appears in logs
- Django is loading (we see `✅ ALLOWED_HOSTS configured`)
- Gunicorn is starting successfully
- Code is deployed (startup.sh confirms latest version)

### What's NOT Working ❌
- **Production.py version marker NOT appearing** (should print when Django loads settings)
- **Middleware module load message NOT appearing** (should print when module is imported)
- **Middleware import test NOT appearing** (should print in production.py)
- **Middleware __init__ NOT appearing** (should print when Django instantiates middleware)
- **Middleware __call__ NOT appearing** (should print on each request)
- **Still getting 301 redirects**

### Key Observation
We see `✅ ALLOWED_HOSTS configured: 6 host(s)` which means Django IS loading `production.py`, but:
- The version marker print (line 14-19) is NOT appearing
- The middleware import test (line 34-46) is NOT appearing
- The middleware module load (line 16-18 in middleware.py) is NOT appearing

This suggests either:
1. The print statements are being suppressed/buffered
2. There's an error preventing the code from executing
3. Django is loading settings from a different location
4. The files aren't actually being deployed (unlikely since startup.sh works)

---

## Files Modified

### `core/middleware.py`
- **Purpose**: Sets `HTTP_X_FORWARDED_PROTO=https` if missing
- **Key Code**: Checks `request.META["HTTP_X_FORWARDED_PROTO"]` (NOT `request.headers`)
- **Status**: Code is correct, but not running in Azure
- **Diagnostics Added**:
  - Module load print (line 16-18)
  - `__init__` error handling (line 31-47)
  - `__call__` logging (line 49-98)

### `floripatalks/settings/production.py`
- **Purpose**: Production settings with middleware configuration
- **Key Code**:
  - Adds middleware to `MIDDLEWARE` list (line 48)
  - Tests middleware import (line 34-46)
  - Version marker (line 13-19)
- **Status**: Code is correct, but prints not appearing in Azure
- **Diagnostics Added**:
  - Version marker (line 13-19)
  - Import test (line 34-46)
  - MIDDLEWARE list verification (line 52-55)

### `startup.sh`
- **Purpose**: Application startup script
- **Status**: ✅ **WORKING** - version marker appears in logs
- **Diagnostics Added**: Version marker at startup

---

## Next Steps to Investigate

### 1. Verify Files Are Actually Deployed
```bash
# Check if production.py and middleware.py are in the deployment package
# The rsync command in .github/workflows/main_floripatalks-app.yml should include them
# But verify they're not being excluded somehow
```

### 2. Check for Import Errors
- The middleware import test should show errors if there are any
- But since we're not seeing the test output, maybe there's an error preventing production.py from loading?

### 3. Check Django Settings Loading
- Django loads settings when:
  - Running `migrate` (we see ALLOWED_HOSTS here)
  - Running `collectstatic` (we see ALLOWED_HOSTS here)
  - Starting Gunicorn workers (we see ALLOWED_HOSTS here)
- But we're NOT seeing the version marker that should print BEFORE ALLOWED_HOSTS
- This suggests the print statements might be executed but not captured

### 4. Check Log Stream Configuration
- Application logging is enabled (`az webapp log config`)
- But maybe stdout/stderr from Django settings loading isn't being captured?
- Try checking different log streams in Azure Portal

### 5. Test Middleware Directly
- SSH into Azure App Service
- Try importing the middleware manually
- Check if there are any import errors
- Verify the files are actually there

### 6. Check for Silent Failures
- Maybe there's an exception being caught somewhere?
- Check if Django is suppressing errors during settings loading
- Look for any error logs we might have missed

### 7. Alternative Approach: Force Middleware Execution
- Instead of relying on Django's middleware system, could we set the header in a different way?
- Maybe in Gunicorn configuration?
- Or in a different middleware that we know is running?

---

## Key Code Locations

### Middleware Check (CORRECT - Uses request.META)
```python
# core/middleware.py line 60-61
has_header = "HTTP_X_FORWARDED_PROTO" in request.META
header_value = request.META.get("HTTP_X_FORWARDED_PROTO", "NOT SET")
```

### Middleware Setting (CORRECT)
```python
# core/middleware.py line 70
request.META["HTTP_X_FORWARDED_PROTO"] = "https"
```

### Settings Configuration (CORRECT)
```python
# floripatalks/settings/production.py line 65
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
```

### Middleware Registration (CORRECT)
```python
# floripatalks/settings/production.py line 48
MIDDLEWARE.insert(0, "core.middleware.AzureProxyHeaderMiddleware")
```

---

## Commands to Check Logs

```bash
# Stream logs from terminal
az webapp log tail \
  --resource-group floripatalks-rg \
  --name floripatalks-app

# Or use justfile command
just azlogs

# Check application logging configuration
az webapp log show \
  --resource-group floripatalks-rg \
  --name floripatalks-app \
  --query "applicationLogs"
```

---

## Expected Log Output (When Working)

When the middleware is working, you should see:

1. **At startup**:
   ```
   ==================================================================================
   🚀 STARTUP.SH VERSION: Latest with middleware debugging (2025-12-11)
   ==================================================================================
   ```

2. **When Django loads settings**:
   ```
   ====================================================================================
   🚀 PRODUCTION SETTINGS LOADED - Latest version with middleware logging
   ====================================================================================
   🔧 Production settings: Adding AzureProxyHeaderMiddleware to MIDDLEWARE...
   ✅ Middleware import test: SUCCESS
   ✅ Production settings: Middleware added. First middleware: core.middleware.AzureProxyHeaderMiddleware
   ```

3. **When middleware module is imported**:
   ```
   ✅ AzureProxyHeaderMiddleware module loaded
   ```

4. **When middleware is instantiated** (for each Gunicorn worker):
   ```
   🔧 AzureProxyHeaderMiddleware.__init__ called
   ✅ AzureProxyHeaderMiddleware.__init__ completed
   ```

5. **On each request**:
   ```
   🚀 AzureProxyHeaderMiddleware: Processing GET / ...
   🔧 AzureProxyHeaderMiddleware: Set HTTP_X_FORWARDED_PROTO=https for / ...
   ```

---

## Current Mystery

**Why are the print statements not appearing?**

We know:
- ✅ Code is deployed (startup.sh version marker works)
- ✅ Django is loading (ALLOWED_HOSTS message appears)
- ❌ But production.py version marker doesn't appear (should print BEFORE ALLOWED_HOSTS)
- ❌ Middleware logs don't appear at all

This suggests the print statements in production.py and middleware.py are either:
1. Not being executed
2. Being suppressed/buffered
3. Going to a different log stream
4. There's an error preventing execution

---

## Quick Test Commands

```bash
# Test middleware locally
cd /Users/rodrigo/code/opensource/floripatalks
uv run python -c "
import os
os.environ['SECRET_KEY']='test'
os.environ['ALLOWED_HOSTS']='test.com'
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'floripatalks.settings.production')
import django
django.setup()
from django.conf import settings
print('MIDDLEWARE:', settings.MIDDLEWARE[:3])
from core.middleware import AzureProxyHeaderMiddleware
print('Middleware imported successfully')
"

# Check if files are in deployment
# Look at .github/workflows/main_floripatalks-app.yml
# The rsync command should include *.py files
```

---

## Related Files

- `core/middleware.py` - The middleware implementation
- `floripatalks/settings/production.py` - Production settings with middleware config
- `startup.sh` - Startup script (working correctly)
- `.github/workflows/main_floripatalks-app.yml` - CI/CD deployment workflow

---

## Notes

- The middleware code is **correct** (uses `request.META`, not `request.headers`)
- The middleware works **perfectly locally**
- The issue is that it's **not running in Azure**
- All diagnostic code has been added but **not appearing in logs**
- This is a **deployment/runtime issue**, not a code issue

---

**Last Updated**: 2025-12-11 04:32 UTC  
**Next Session**: Continue investigating why middleware isn't running in Azure
