# OAuth Setup Instructions for Google and LinkedIn SSO

This document provides detailed instructions for setting up Google and LinkedIn OAuth credentials for django-allauth, aligned with the latest django-allauth documentation (2024-2025).

## Prerequisites

- Django-allauth is already configured in `floripatalks/settings/base.py`
- Site object with id=1 has been created (completed via migration)
- You have access to Google Cloud Console and LinkedIn Developer Portal

---

## Step 1: Google OAuth Setup

### 1.1 Create Google OAuth 2.0 Credentials

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/
   - Sign in with your Google account

2. **Create or Select a Project**
   - Click the project dropdown at the top
   - Click "New Project" or select an existing project
   - Give it a name (e.g., "FloripaTalks")
   - Click "Create"

3. **Configure OAuth Consent Screen** (Required first step)
   - Go to "APIs & Services" > "OAuth consent screen"
   - Choose "External" (unless you have a Google Workspace account)
   - Fill in:
     - App name: `FloripaTalks`
     - User support email: Your email
     - Developer contact: Your email
   - Click "Save and Continue"
   - Add scopes: `email`, `profile`, `openid`
   - Click "Save and Continue"
   - Add test users (required for development/testing - add your email)
   - Click "Save and Continue" > "Back to Dashboard"

4. **Create OAuth 2.0 Credentials**
   - Go to "APIs & Services" > "Credentials"
   - Click "Create Credentials" > "OAuth client ID"
   - Application type: "Web application"
   - Name: `FloripaTalks Web Client`
   - Authorized JavaScript origins:
     - `http://localhost:8000` (for development)
     - `https://yourdomain.com` (for production - add when deploying)
   - Authorized redirect URIs:
     - `http://localhost:8000/accounts/google/login/callback/` (for development)
     - `https://yourdomain.com/accounts/google/login/callback/` (for production)
   - Click "Create"

5. **Copy Credentials**
   - You'll see a popup with:
     - **Client ID**: Copy this (looks like: `123456789-abcdefg.apps.googleusercontent.com`)
     - **Client secret**: Copy this (looks like: `GOCSPX-abcdefghijklmnopqrstuvwxyz`)
   - Save these securely - you won't be able to see the secret again!

### 1.2 Django Configuration

The Google provider is already configured in `floripatalks/settings/base.py` with the latest recommended settings:

```python
SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "SCOPE": ["profile", "email"],
        "AUTH_PARAMS": {"access_type": "online"},
        "APP": {
            "client_id": "",  # Set via GOOGLE_CLIENT_ID environment variable
            "secret": "",  # Set via GOOGLE_CLIENT_SECRET environment variable
        },
        # OAUTH_PKCE_ENABLED is recommended for enhanced security
        # Add this if you want to enable PKCE (recommended):
        # "OAUTH_PKCE_ENABLED": True,
    },
}
```

**Important**: This project uses the **settings-based configuration** (not database-based). This means:
- ✅ **Environment variables are sufficient** - no need to add SocialApplication records in Django admin
- ✅ Credentials are loaded from `.env` file automatically
- ✅ No database setup required for OAuth credentials

**Note**: PKCE (Proof Key for Code Exchange) is recommended for enhanced security. To enable it, uncomment the `OAUTH_PKCE_ENABLED` line in `floripatalks/settings/base.py`.

### 1.3 Set Environment Variables

**For Development (local):**

The project uses `python-dotenv` to automatically load environment variables from a `.env` file.

1. **Create a `.env` file** in the project root (copy from `.env.example`):
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file** and add your credentials:
   ```bash
   # Google OAuth 2.0 Credentials
   GOOGLE_CLIENT_ID=your-google-client-id-here
   GOOGLE_CLIENT_SECRET=your-google-client-secret-here
   ```

3. **The `.env` file is automatically loaded** when Django starts (via `floripatalks/settings/development.py`)

**Alternative: Shell Environment Variables**

If you prefer using shell environment variables instead of `.env` file:

```bash
# Add to your shell profile (~/.zshrc, ~/.bashrc, etc.)
export GOOGLE_CLIENT_ID="your-google-client-id-here"
export GOOGLE_CLIENT_SECRET="your-google-client-secret-here"

# Then reload your shell
source ~/.zshrc  # or source ~/.bashrc
```

**For Production:**

Set these as environment variables in your hosting platform (Heroku, AWS, etc.). Do not use `.env` file in production.

---

## Step 2: LinkedIn OAuth Setup

### 2.1 Create LinkedIn Application

**Note**: This project uses LinkedIn's OpenID Connect provider (the modern, recommended approach). The deprecated `linkedin_oauth2` provider is no longer used.

1. **Go to LinkedIn Developer Portal**
   - Visit: https://www.linkedin.com/developers/
   - Sign in with your LinkedIn account

2. **Create a New App**
   - Click "Create app"
   - Fill in the form:
     - **App name**: `FloripaTalks`
     - **LinkedIn Page**: Select your company page or create one
     - **App logo**: Upload a logo (optional)
     - **App usage**: Select "Sign In with LinkedIn using OpenID Connect"
     - **Website URL**: `http://localhost:8000` (for development)
     - **Privacy policy URL**: Your privacy policy URL (required)
     - **User agreement URL**: Your terms of service URL (required)
   - Check the terms and click "Create app"

3. **Configure OAuth Settings**
   - In your app, go to the "Auth" tab
   - Under "Redirect URLs", add:
     - `http://localhost:8000/accounts/openid_connect/linkedin/login/callback/` (for development)
     - `https://yourdomain.com/accounts/openid_connect/linkedin/login/callback/` (for production)
   - Click "Update"

4. **Get Credentials**
   - In the "Auth" tab, you'll see:
     - **Client ID**: Copy this
     - **Client Secret**: Click "Show" and copy this
   - Save these securely!

5. **Request API Access (if needed)**
   - Go to "Products" tab
   - Request access to:
     - "Sign In with LinkedIn using OpenID Connect" (should be auto-approved)
     - "Email Address" (if not already included)

### 2.2 Django Configuration

The LinkedIn provider is configured in `floripatalks/settings/base.py` using OpenID Connect:

```python
INSTALLED_APPS = [
    # ...
    "allauth.socialaccount.providers.openid_connect",  # Used for LinkedIn
    # ...
]

SOCIALACCOUNT_PROVIDERS = {
    # ...
    "openid_connect": {
        "APPS": [
            {
                "provider_id": "linkedin",
                "name": "LinkedIn",
                "client_id": "",  # Set via LINKEDIN_CLIENT_ID environment variable
                "secret": "",  # Set via LINKEDIN_CLIENT_SECRET environment variable
                "settings": {
                    "server_url": "https://www.linkedin.com/oauth",
                },
            }
        ]
    },
}
```

**Important**: This project uses the **settings-based configuration** (not database-based). This means:
- ✅ **Environment variables are sufficient** - no need to add SocialApplication records in Django admin
- ✅ Credentials are loaded from `.env` file automatically
- ✅ No database setup required for OAuth credentials

### 2.3 Set Environment Variables

**For Development (local):**

Add LinkedIn credentials to your `.env` file:

```bash
# LinkedIn OAuth 2.0 Credentials
LINKEDIN_CLIENT_ID=your-linkedin-client-id-here
LINKEDIN_CLIENT_SECRET=your-linkedin-client-secret-here
```

The `.env` file is automatically loaded when Django starts.

**Alternative: Shell Environment Variables**

If you prefer using shell environment variables:

```bash
export LINKEDIN_CLIENT_ID="your-linkedin-client-id-here"
export LINKEDIN_CLIENT_SECRET="your-linkedin-client-secret-here"
source ~/.zshrc  # or source ~/.bashrc
```

**For Production:**

Set these as environment variables in your hosting platform.

---

## Step 3: Verify Configuration

### 3.1 Check Environment Variables

Verify your environment variables are set:

```bash
echo $GOOGLE_CLIENT_ID
echo $GOOGLE_CLIENT_SECRET
echo $LINKEDIN_CLIENT_ID
echo $LINKEDIN_CLIENT_SECRET
```

### 3.2 Test the Configuration

1. **Start Django development server:**
   ```bash
   uv run python manage.py runserver
   ```

2. **Visit the login page:**
   - Go to: http://localhost:8000/accounts/login/
   - You should see "Sign in with Google" and "Sign in with LinkedIn" buttons

3. **Test Google Login:**
   - Click "Sign in with Google"
   - You should be redirected to Google's OAuth consent screen
   - After authorizing, you should be redirected back to your site

4. **Test LinkedIn Login:**
   - Click "Sign in with LinkedIn"
   - You should be redirected to LinkedIn's OAuth consent screen
   - After authorizing, you should be redirected back to your site

### 3.3 Troubleshooting

**Issue: "Invalid client" error**
- Check that your Client ID and Secret are correct
- Verify environment variables are loaded (restart your terminal/server)
- For Google: Check that redirect URI matches exactly (including trailing slash)
- For LinkedIn: Check that redirect URI is added in the Auth tab

**Issue: "Redirect URI mismatch"**
- Google: Ensure the redirect URI in Google Console matches exactly: `http://localhost:8000/accounts/google/login/callback/`
- LinkedIn: Ensure the redirect URI in LinkedIn Auth tab matches exactly: `http://localhost:8000/accounts/openid_connect/linkedin/login/callback/`

**Issue: "Access blocked" or "App not verified"**
- Google: For development, add your email as a test user in OAuth consent screen (required!)
- LinkedIn: Ensure your app is not in "Development" mode restrictions (or add test users)

**Issue: Environment variables not loading**
- Make sure you've reloaded your shell after setting variables
- For Django runserver, restart it after setting variables
- Check that variables are exported (not just set locally in one terminal)

**Issue: "PKCE verification failed" (if PKCE enabled)**
- Ensure your Google OAuth client supports PKCE (all new clients do)
- Check that `OAUTH_PKCE_ENABLED` is set correctly in settings

---

## Step 4: Production Configuration

When deploying to production:

1. **Update Redirect URIs:**
   - Google: Add `https://yourdomain.com/accounts/google/login/callback/`
   - LinkedIn: Add `https://yourdomain.com/accounts/openid_connect/linkedin/login/callback/`

2. **Update Authorized JavaScript Origins:**
   - Google: Add `https://yourdomain.com`

3. **Set Production Environment Variables:**
   - Use your hosting platform's environment variable settings
   - Never commit credentials to version control!

4. **Update Site Domain:**
   - In Django admin, go to Sites > Sites
   - Edit the site with id=1
   - Update domain to your production domain
   - Update name if needed

5. **Enable PKCE (Recommended):**
   - Uncomment `OAUTH_PKCE_ENABLED: True` in `floripatalks/settings/base.py` for enhanced security

---

## Security Notes

- **Never commit OAuth credentials to version control**
- Use environment variables for all secrets
- Rotate credentials if they're ever exposed
- Use different credentials for development and production
- Regularly review OAuth app permissions in Google/LinkedIn consoles
- Consider enabling PKCE for Google OAuth (recommended for production)

---

## Additional Resources

- [django-allauth Documentation](https://docs.allauth.org/)
- [django-allauth Google Provider](https://docs.allauth.org/en/latest/socialaccount/providers/google.html)
- [django-allauth LinkedIn Provider](https://docs.allauth.org/en/latest/socialaccount/providers/linkedin.html)
- [django-allauth OpenID Connect Provider](https://docs.allauth.org/en/latest/socialaccount/providers/openid_connect.html)
- [Google OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [LinkedIn OAuth 2.0 Documentation](https://learn.microsoft.com/en-us/linkedin/shared/authentication/authentication)

---

## Quick Reference: Environment Variables

### Using .env File (Recommended for Development)

Create a `.env` file in the project root (copy from `.env.example`):

```bash
# .env file format (no quotes, no export)
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
LINKEDIN_CLIENT_ID=your-linkedin-client-id
LINKEDIN_CLIENT_SECRET=your-linkedin-client-secret
```

The application automatically loads these from the `.env` file when running in development mode (see `floripatalks/settings/development.py`).

### Using Shell Environment Variables (Alternative)

```bash
# Shell profile format (with quotes and export)
export GOOGLE_CLIENT_ID="your-google-client-id"
export GOOGLE_CLIENT_SECRET="your-google-client-secret"
export LINKEDIN_CLIENT_ID="your-linkedin-client-id"
export LINKEDIN_CLIENT_SECRET="your-linkedin-client-secret"
```

**Note**: The `.env` file approach is recommended as it's simpler and doesn't require shell reloading.

---

## Current Configuration Status

- ✅ Google OAuth: Configured with latest recommended settings
- ✅ LinkedIn OAuth: Using OpenID Connect provider (modern, recommended approach)
