# Testing Google SSO Authentication

This guide walks you through testing Google SSO authentication in the FloripaTalks application.

## Prerequisites

✅ **Completed**:
- Google OAuth credentials are set in `.env` file
- django-allauth is configured
- Site object (id=1) exists in database

## Step-by-Step Testing

### 1. Start the Django Development Server

```bash
uv run python manage.py runserver
```

You should see:
```
✅ Loaded environment variables from /path/to/.env
Starting development server at http://127.0.0.1:8000/
```

### 2. Access the Login Page

Open your browser and navigate to:

**http://localhost:8000/accounts/login/**

You should see:
- A login form (for email/password login)
- A "Sign in with Google" button/link
- A "Sign in with LinkedIn" button/link (if LinkedIn credentials are set)

### 3. Test Google SSO

1. **Click "Sign in with Google"** (or visit directly: http://localhost:8000/accounts/google/login/)

2. **You'll be redirected to Google's OAuth consent screen**:
   - Google will show what permissions the app is requesting
   - You'll see your app name (FloripaTalks)
   - Click "Continue" or "Allow"

3. **Google will redirect you back** to:
   - `http://localhost:8000/accounts/google/login/callback/`
   - Then automatically to your `LOGIN_REDIRECT_URL` (currently `/`)

4. **You should now be logged in**:
   - Your Gmail account is associated with a user account
   - You can check this in Django admin: http://localhost:8000/admin/
   - Go to "Social accounts" to see the connection

### 4. Verify Your Account

**Option A: Check Django Admin**

1. Go to http://localhost:8000/admin/
2. Navigate to **"Social accounts"** → **"Social accounts"**
3. You should see your Google account linked to a user

**Option B: Check via Django Shell**

```bash
uv run python manage.py shell
```

```python
from accounts.models import User
from allauth.socialaccount.models import SocialAccount

# Check users
users = User.objects.all()
for user in users:
    print(f"User: {user.email} ({user.username})")

# Check social accounts
social_accounts = SocialAccount.objects.all()
for sa in social_accounts:
    print(f"Provider: {sa.provider}, User: {sa.user.email}, UID: {sa.uid}")
```

### 5. Test Logout

1. Visit: http://localhost:8000/accounts/logout/
2. You should be logged out and redirected to `/`

### 6. Test Login Again

1. Visit: http://localhost:8000/accounts/login/
2. Click "Sign in with Google"
3. If you're already authorized, Google may skip the consent screen
4. You should be logged in again with the same account

## Troubleshooting

### "Invalid client" or "Redirect URI mismatch"

**Check your Google OAuth settings**:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to your OAuth 2.0 Client
3. Verify **Authorized redirect URIs** includes:
   - `http://localhost:8000/accounts/google/login/callback/`
   - (Note the trailing slash!)

### "Access blocked" or "App not verified"

**For development**:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Navigate to **OAuth consent screen**
3. Add your Gmail address as a **Test user**
4. Try logging in again

### No "Sign in with Google" button appears

**Check**:
1. Environment variables are loaded (check server console output)
2. Google Client ID is set: `echo $GOOGLE_CLIENT_ID`
3. Restart Django server after changing `.env` file

### Error: "No such app" or OAuth not working

**Verify**:
- ✅ `.env` file exists and has correct format (no quotes, no `export`)
- ✅ Google credentials are set in `.env`
- ✅ Django server was restarted after setting `.env`
- ✅ Check console output for "✅ Loaded environment variables"

### Can't see social accounts in admin

**Check**:
1. You're logged in as a superuser
2. Run migrations: `uv run python manage.py migrate`
3. Social accounts are created automatically when you log in via SSO

## Quick Test Commands

```bash
# Check if credentials are loaded
uv run python manage.py shell
>>> from django.conf import settings
>>> settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id']
# Should show your client ID (not empty)

# Check existing social accounts
>>> from allauth.socialaccount.models import SocialAccount
>>> SocialAccount.objects.all()
# Should show your Google account after first login
```

## Expected Flow

1. **User visits**: `/accounts/login/`
2. **Clicks**: "Sign in with Google"
3. **Redirected to**: Google OAuth consent screen
4. **User authorizes**: Clicks "Allow"
5. **Redirected to**: `/accounts/google/login/callback/`
6. **django-allauth**:
   - Creates User account (if first time)
   - Creates SocialAccount linking Google to User
   - Logs user in
7. **Redirected to**: `/` (home page, logged in)

## Next Steps

After successful login:
- ✅ Your Gmail account is associated with a User in the database
- ✅ You can use this account to create topics, vote, comment, etc.
- ✅ The account persists - you can log in again anytime
- ✅ Check Django admin to see the user and social account records

---

**Note**: No need to add SocialApplication records in Django admin. The settings-based configuration with environment variables is sufficient.
