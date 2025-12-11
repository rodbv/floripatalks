# Azure App Service Expert Audit Report - Django Deployment

**Date**: 2025-12-11  
**App Name**: floripatalks-app  
**Resource Group**: floripatalks-rg  
**Region**: Brazil South

---

## Executive Summary

This audit compares the current Azure App Service configuration against Microsoft's best practices for Django production deployments. **Critical issues found** that may be preventing middleware execution and causing 301 redirects.

---

## Critical Issues Found

### 🔴 CRITICAL: Always On Disabled
**Current**: `alwaysOn: false`  
**Recommended**: `alwaysOn: true`  
**Impact**:
- App can go to sleep, causing cold starts
- Middleware may not initialize properly on cold starts
- Settings loading may be inconsistent
- **This could explain why middleware logs don't appear**

**Fix**:
```bash
az webapp config set \
  --resource-group floripatalks-rg \
  --name floripatalks-app \
  --always-on true
```

### 🔴 CRITICAL: HTTP/2 Disabled
**Current**: `http20Enabled: false`  
**Recommended**: `http20Enabled: true`  
**Impact**: Performance degradation, but not related to middleware issue

**Fix**:
```bash
az webapp config set \
  --resource-group floripatalks-rg \
  --name floripatalks-app \
  --http20-enabled true
```

### 🟡 WARNING: Detailed Error Logging Disabled
**Current**: `detailedErrorLoggingEnabled: false`  
**Recommended**: `detailedErrorLoggingEnabled: true` (for debugging)  
**Impact**: Can't see detailed error messages that might explain middleware issues

**Fix**:
```bash
az webapp log config \
  --resource-group floripatalks-rg \
  --name floripatalks-app \
  --detailed-error-messages true \
  --failed-request-tracing true
```

### 🟡 WARNING: HTTP Logging Disabled
**Current**: `httpLoggingEnabled: false`  
**Recommended**: `httpLoggingEnabled: true`  
**Impact**: Missing HTTP request/response logs

**Fix**:
```bash
az webapp log config \
  --resource-group floripatalks-rg \
  --name floripatalks-app \
  --web-server-logging filesystem
```

---

## Current Configuration Audit

### ✅ Correctly Configured

1. **HTTPS Only**: `httpsOnly: true` ✅
2. **TLS Version**: `minTlsVersion: 1.2` ✅
3. **FTPS State**: `ftpsState: FtpsOnly` ✅
4. **Python Version**: `PYTHON|3.13` ✅
5. **Startup Command**: `bash startup.sh` ✅
6. **SCM Type**: `GitHubAction` ✅
7. **Application Logging**: `fileSystem: Information` ✅
8. **Environment Variables**: All required vars set ✅
   - `DJANGO_SETTINGS_MODULE=floripatalks.settings.production`
   - `SECRET_KEY` ✅
   - `GOOGLE_CLIENT_ID` ✅
   - `GOOGLE_CLIENT_SECRET` ✅
   - `ALLOWED_HOSTS` ✅

### ⚠️ Needs Attention

1. **Always On**: `false` → Should be `true` 🔴
2. **HTTP/2**: `false` → Should be `true` 🟡
3. **Detailed Error Logging**: `false` → Should be `true` (for debugging) 🟡
4. **HTTP Logging**: `false` → Should be `true` 🟡
5. **Failed Request Tracing**: `null` → Should be `true` (for debugging) 🟡

---

## Django Configuration Audit

### ✅ Correctly Configured

1. **SECURE_PROXY_SSL_HEADER**: `("HTTP_X_FORWARDED_PROTO", "https")` ✅
2. **SECURE_SSL_REDIRECT**: `False` ✅ (Azure handles HTTPS redirect)
3. **DEBUG**: `False` ✅
4. **Middleware Order**: Custom middleware at position 0 ✅
5. **ALLOWED_HOSTS**: Includes Azure domain and health check IPs ✅

### ⚠️ Potential Issues

1. **Middleware Not Executing**: Despite correct configuration, middleware logs don't appear
2. **Settings Loading**: Production.py version marker doesn't appear, but ALLOWED_HOSTS does
3. **Print Statement Suppression**: Diagnostic prints not appearing in logs

---

## Key Findings

### 1. Always On is CRITICAL for Middleware

**Why this matters**:
- When Always On is disabled, Azure can put the app to sleep
- On wake-up, Django settings may load inconsistently
- Middleware initialization may be skipped or incomplete
- **This could explain why middleware logs don't appear**

**Evidence**:
- We see `ALLOWED_HOSTS` message (Django loading)
- But we don't see production.py version marker (should print BEFORE ALLOWED_HOSTS)
- This suggests settings are loading, but print statements aren't executing or being captured

### 2. Gunicorn Worker Initialization

**Current**: 2 workers  
**Observation**: Each worker loads Django settings independently  
**Issue**: If Always On is disabled, workers may not initialize middleware properly

### 3. Settings Loading Sequence

**Expected**:
1. Import base settings
2. Import production settings
3. Print version marker
4. Add middleware to MIDDLEWARE list
5. Print middleware import test
6. Print ALLOWED_HOSTS

**Actual** (from logs):
- ✅ ALLOWED_HOSTS appears
- ❌ Version marker doesn't appear
- ❌ Middleware import test doesn't appear

**Hypothesis**: Print statements are executed but not captured, OR settings are loaded from a cached/compiled state

---

## Recommended Fixes (Priority Order)

### Priority 1: Enable Always On (CRITICAL)
```bash
az webapp config set \
  --resource-group floripatalks-rg \
  --name floripatalks-app \
  --always-on true
```

**Why**: This ensures the app stays warm and middleware initializes consistently.

### Priority 2: Enable Detailed Error Logging
```bash
az webapp log config \
  --resource-group floripatalks-rg \
  --name floripatalks-app \
  --detailed-error-messages true \
  --failed-request-tracing true
```

**Why**: This will show us any errors preventing middleware from loading.

### Priority 3: Enable HTTP Logging
```bash
az webapp log config \
  --resource-group floripatalks-rg \
  --name floripatalks-app \
  --web-server-logging filesystem
```

**Why**: Better visibility into request/response cycle.

### Priority 4: Enable HTTP/2
```bash
az webapp config set \
  --resource-group floripatalks-rg \
  --name floripatalks-app \
  --http20-enabled true
```

**Why**: Performance improvement (not related to middleware issue).

---

## Middleware Investigation Strategy

### Step 1: Enable Always On
This is the most likely culprit. Always On ensures:
- App stays warm
- Settings load consistently
- Middleware initializes properly
- No cold start issues

### Step 2: Check Worker Initialization
After enabling Always On, check if middleware `__init__` logs appear when workers boot.

### Step 3: Verify Settings Loading
Check if production.py version marker appears after Always On is enabled.

### Step 4: Test Middleware Execution
After fixes, verify middleware `__call__` logs appear on requests.

---

## Microsoft Best Practices Checklist

### Application Configuration
- ✅ HTTPS Only enabled
- ✅ TLS 1.2 minimum
- ❌ Always On enabled (CRITICAL - currently false)
- ✅ Correct Python version
- ✅ Startup command configured
- ✅ Environment variables set

### Logging & Diagnostics
- ✅ Application logging enabled (filesystem, Information level)
- ❌ Detailed error messages enabled (currently false)
- ❌ Failed request tracing enabled (currently null)
- ❌ HTTP logging enabled (currently false)

### Performance
- ❌ HTTP/2 enabled (currently false)
- ✅ Static files collected
- ✅ Gunicorn configured correctly

### Security
- ✅ HTTPS Only
- ✅ TLS 1.2 minimum
- ✅ FTPS Only
- ✅ DEBUG=False
- ✅ SECURE_PROXY_SSL_HEADER configured
- ✅ SECURE_SSL_REDIRECT=False (Azure handles redirect)

---

## Commands to Apply All Fixes

```bash
# Enable Always On (CRITICAL)
az webapp config set \
  --resource-group floripatalks-rg \
  --name floripatalks-app \
  --always-on true

# Enable HTTP/2
az webapp config set \
  --resource-group floripatalks-rg \
  --name floripatalks-app \
  --http20-enabled true

# Enable detailed logging
az webapp log config \
  --resource-group floripatalks-rg \
  --name floripatalks-app \
  --detailed-error-messages true \
  --failed-request-tracing true \
  --web-server-logging filesystem

# Restart app to apply changes
az webapp restart \
  --resource-group floripatalks-rg \
  --name floripatalks-app
```

---

## Expected Behavior After Fixes

### After Enabling Always On:
1. App stays warm (no cold starts)
2. Settings load consistently
3. Middleware initializes on each worker boot
4. We should see:
   - Production.py version marker
   - Middleware import test
   - Middleware `__init__` logs
   - Middleware `__call__` logs

### After Enabling Detailed Logging:
1. Any errors preventing middleware execution will be visible
2. Failed request traces will show middleware execution path
3. HTTP logs will show request/response details

---

## Current vs Recommended Configuration

| Setting | Current | Recommended | Status |
|---------|---------|-------------|--------|
| Always On | `false` | `true` | 🔴 CRITICAL |
| HTTP/2 | `false` | `true` | 🟡 Recommended |
| Detailed Error Logging | `false` | `true` | 🟡 For Debugging |
| HTTP Logging | `false` | `true` | 🟡 Recommended |
| Failed Request Tracing | `null` | `true` | 🟡 For Debugging |
| HTTPS Only | `true` | `true` | ✅ Correct |
| TLS Version | `1.2` | `1.2` | ✅ Correct |
| Python Version | `3.13` | `3.13` | ✅ Correct |
| Startup Command | `bash startup.sh` | `bash startup.sh` | ✅ Correct |

---

## Next Steps

1. **IMMEDIATE**: Enable Always On (most likely fix for middleware issue)
2. **IMMEDIATE**: Enable detailed error logging (to see any errors)
3. **AFTER FIXES**: Monitor logs for middleware execution
4. **VERIFY**: Check if 301 redirects stop after Always On is enabled
5. **OPTIMIZE**: Enable HTTP/2 and HTTP logging for better performance/monitoring

---

## References

- [Azure App Service Always On](https://learn.microsoft.com/en-us/azure/app-service/configure-common#always-on)
- [Azure App Service Django Deployment](https://learn.microsoft.com/en-us/azure/app-service/quickstart-python)
- [Django Middleware Documentation](https://docs.djangoproject.com/en/stable/topics/http/middleware/)
- [Azure App Service Logging](https://learn.microsoft.com/en-us/azure/app-service/troubleshoot-diagnostic-logs)

---

**Last Updated**: 2025-12-11  
**Next Action**: Enable Always On and detailed logging, then monitor middleware execution
