# 301 Redirect Fix - What Actually Solved It

**Date**: 2025-12-12  
**Status**: ✅ **RESOLVED**

---

## The Problem

All requests were returning `301 Moved Permanently` redirects, even for HTTPS requests. This created redirect loops and prevented the application from working.

---

## Root Cause

Azure App Service acts as a **reverse proxy**:
1. **External traffic** → Azure Load Balancer (HTTPS)
2. **Azure Load Balancer** → Django App (HTTP internally)
3. Azure sets `X-Forwarded-Proto: https` header to tell Django the original request was HTTPS

**The Issue**: Django didn't know to trust this header, so it thought all requests were HTTP and tried to redirect them to HTTPS, causing 301 loops.

---

## The Solution (Two Critical Settings)

### 1. `SECURE_PROXY_SSL_HEADER` - Tell Django to Trust Azure's Headers

**Location**: `floripatalks/settings/production.py` line 34

```python
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
```

**What it does**:
- Tells Django: "When you see `HTTP_X_FORWARDED_PROTO=https` in the request headers, trust that the original request was HTTPS"
- This is how Django knows requests are secure even though they arrive as HTTP internally

**Why it's needed**:
- Azure terminates SSL at the load balancer
- Requests reach Django as HTTP (not HTTPS)
- Without this setting, Django's `request.is_secure()` returns `False`
- Django's `SecurityMiddleware` then tries to redirect HTTP → HTTPS → **301 loop**

### 2. `SECURE_SSL_REDIRECT = False` - Don't Double-Redirect

**Location**: `floripatalks/settings/production.py` line 37

```python
SECURE_SSL_REDIRECT = False
```

**What it does**:
- Disables Django's built-in HTTP → HTTPS redirect
- Azure already handles this at the platform level (via `httpsOnly: true`)

**Why it's needed**:
- Azure's load balancer redirects HTTP → HTTPS **before** requests reach Django
- If Django also redirects, you get double redirects or loops
- Setting this to `False` lets Azure handle the redirect (which it does automatically)

---

## Supporting Fix: Ensure Production Settings Are Loaded

### The Problem
Django entry points (`wsgi.py`, `manage.py`, `asgi.py`) were defaulting to `floripatalks.settings`, which loads `development.py` via `__init__.py`:

```python
# floripatalks/settings/__init__.py
from .development import *  # ← This was being loaded!
```

**This caused THREE critical issues**:

1. **Development settings loaded** (`DEBUG = True`, `ALLOWED_HOSTS = ["localhost"]`)
2. **Custom middleware not in MIDDLEWARE list** (was only added in production settings)
3. **Security settings missing** (`SECURE_PROXY_SSL_HEADER`, `SECURE_SSL_REDIRECT`)

### The Fix
Changed all entry points to default to `floripatalks.settings.production`:

**`floripatalks/wsgi.py`** (line 16):
```python
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "floripatalks.settings.production")
```

**`manage.py`** (line 11):
```python
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "floripatalks.settings.production")
```

**`floripatalks/asgi.py`** (line 15):
```python
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "floripatalks.settings.production")
```

**Why this matters**:
- Ensures production settings (with the two critical settings above) are always loaded
- Even if `DJANGO_SETTINGS_MODULE` environment variable isn't set, production settings are used
- **Prevents development settings from being loaded in production** (which would cause `DEBUG = True`, wrong `ALLOWED_HOSTS`, missing security settings)

### Why Development Settings Were a Problem

**`floripatalks/settings/__init__.py`**:
```python
# Settings package
# Default to development settings
from .development import *  # ← Loads development.py
```

**`floripatalks/settings/development.py`**:
```python
DEBUG = True  # ← Wrong for production!
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]  # ← Wrong for Azure!
# Missing SECURE_PROXY_SSL_HEADER
# Missing SECURE_SSL_REDIRECT = False
# Custom middleware (AzureProxyHeaderMiddleware) was only in production.py
```

**Impact**:
- `DEBUG = True` in production is a **security risk** and can cause performance issues
- `ALLOWED_HOSTS = ["localhost"]` would reject Azure hostnames → `DisallowedHost` errors
- Missing `SECURE_PROXY_SSL_HEADER` → Django doesn't trust Azure's headers → 301 redirects
- Missing `SECURE_SSL_REDIRECT = False` → Django tries to redirect → double redirects
- **Custom middleware not loaded** → Middleware was only added in `production.py`, so when `development.py` loaded, middleware wasn't in `MIDDLEWARE` list → explains why middleware logs never appeared!

### Why This Explains the Middleware Issue

**The custom middleware** (`core.middleware.AzureProxyHeaderMiddleware`) was only added in `production.py`:

```python
# floripatalks/settings/production.py (before we removed it)
MIDDLEWARE.insert(0, "core.middleware.AzureProxyHeaderMiddleware")
```

**But when `development.py` loaded** (via `floripatalks.settings`), the middleware wasn't added, so:
- Middleware wasn't in the `MIDDLEWARE` list
- Django never instantiated it
- `__init__` and `__call__` methods never ran
- **This explains why middleware logs never appeared!**

### Why This Explains "Django Hot Reload"

**`DEBUG = True`** in development settings enables:
- Django's auto-reload feature (watches for file changes)
- Detailed error pages (security risk in production)
- Development-only middleware and features

**In production with Gunicorn**, `DEBUG = True` doesn't enable hot reload (Gunicorn doesn't support it), but it:
- Exposes sensitive information in error pages
- Causes performance issues
- Enables development-only features that shouldn't run in production

---

## What We Tried That Didn't Work

### ❌ Custom Middleware (Removed)
- **What**: Created `core.middleware.AzureProxyHeaderMiddleware` to set `HTTP_X_FORWARDED_PROTO` header
- **Why it failed**:
  - Middleware was only added in `production.py`
  - But `development.py` was being loaded (via `floripatalks.settings`)
  - So middleware was never in the `MIDDLEWARE` list → never executed
  - **This explains why middleware logs never appeared!**
- **Lesson**:
  - Use Django's built-in settings instead of custom middleware when possible
  - **Always ensure production settings are loaded** (not development settings)

### ❌ `SECURE_SSL_REDIRECT = True` (Wrong)
- **What**: Tried enabling Django's HTTPS redirect
- **Why it failed**: Created double redirects (Azure redirects, then Django redirects)
- **Lesson**: Let Azure handle platform-level redirects, disable Django's redirect

---

## The Complete Fix (Minimal Changes)

### File: `floripatalks/settings/production.py`

```python
# Security settings for production
# Azure App Service terminates SSL at the load balancer, so we trust proxy headers
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")  # ✅ KEY FIX #1
# Azure handles HTTPS redirection at the platform level (via httpsOnly setting)
# Disable Django's redirect to avoid double-redirects
SECURE_SSL_REDIRECT = False  # ✅ KEY FIX #2
```

### Files: `wsgi.py`, `manage.py`, `asgi.py`

```python
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "floripatalks.settings.production")  # ✅ KEY FIX #3
```

---

## How It Works Now

1. **User requests** `https://floripatalks-app.azurewebsites.net/`
2. **Azure Load Balancer**:
   - Terminates SSL
   - Adds header: `X-Forwarded-Proto: https`
   - Forwards to Django as HTTP
3. **Django receives request**:
   - Sees `HTTP_X_FORWARDED_PROTO=https` in headers
   - `SECURE_PROXY_SSL_HEADER` tells Django to trust this header
   - `request.is_secure()` returns `True` ✅
   - No redirect needed → **200 OK** ✅

---

## Key Takeaways

1. **`SECURE_PROXY_SSL_HEADER`** is **essential** when behind a reverse proxy (Azure, nginx, etc.)
   - Without it, Django can't tell if requests are secure
   - This causes `SecurityMiddleware` to redirect everything

2. **`SECURE_SSL_REDIRECT = False`** when the platform handles redirects
   - Azure's `httpsOnly: true` already redirects HTTP → HTTPS
   - Django shouldn't also redirect (double redirects)

3. **Always default to production settings** in entry points
   - Prevents accidentally loading development settings
   - Ensures security settings are always applied
   - **Critical**: `floripatalks.settings` → loads `development.py` (wrong for production!)
   - **Correct**: `floripatalks.settings.production` → loads production settings
   - **This explains why middleware wasn't loaded** (middleware was only in production.py, but development.py was being loaded)

4. **Use built-in Django settings** over custom middleware
   - Django's `SECURE_PROXY_SSL_HEADER` is the official way to handle this
   - Custom middleware adds complexity and potential failure points

5. **Why development settings caused the middleware issue**:
   - Custom middleware (`core.middleware.AzureProxyHeaderMiddleware`) was only added in production settings
   - When development settings loaded, middleware wasn't in `MIDDLEWARE` list
   - This explains why middleware logs never appeared - it wasn't even registered!

6. **Why `DEBUG = True` in production is dangerous**:
   - Exposes sensitive information in error pages
   - Causes performance issues
   - Enables development-only features that shouldn't run in production
   - (Note: Gunicorn doesn't support hot reload, but `DEBUG = True` still causes other issues)

---

## References

- [Django: SECURE_PROXY_SSL_HEADER](https://docs.djangoproject.com/en/stable/ref/settings/#secure-proxy-ssl-header)
- [Django: SECURE_SSL_REDIRECT](https://docs.djangoproject.com/en/stable/ref/settings/#secure-ssl-redirect)
- [Azure App Service: HTTPS and SSL](https://learn.microsoft.com/en-us/azure/app-service/configure-ssl-bindings)
- [Django Behind a Proxy](https://docs.djangoproject.com/en/stable/ref/settings/#std-setting-SECURE_PROXY_SSL_HEADER)
