# Vercel Deployment Instructions

## Required Environment Variables

For production deployment on Vercel, you MUST set the following environment variables in your Vercel project settings:

### 1. DATABASE_URL (REQUIRED)
Since Vercel is serverless and doesn't support SQLite, you need to use an external PostgreSQL database.

**Recommended Free PostgreSQL Providers:**
- **Neon** (https://neon.tech) - Free tier with 512MB storage
- **Supabase** (https://supabase.com) - Free tier with 500MB storage
- **ElephantSQL** (https://www.elephantsql.com) - Free tier with 20MB storage

**Format:**
```
DATABASE_URL=postgresql://username:password@host:port/database
```

### 2. SECRET_KEY (REQUIRED)
Generate a secure SECRET_KEY for production:

```python
# Run this in Python to generate a secure key:
import secrets
print(secrets.token_urlsafe(50))
```

Then set it in Vercel:
```
SECRET_KEY=your-generated-secret-key-here
```

### 3. DEBUG (REQUIRED)
```
DEBUG=False
```

### 4. ALLOWED_HOSTS (Optional - already configured with wildcards)
If you want to restrict hosts:
```
ALLOWED_HOSTS=your-domain.vercel.app
```

## How to Set Environment Variables in Vercel

1. Go to your Vercel project dashboard
2. Click on **Settings** tab
3. Click on **Environment Variables** in the left sidebar
4. Add each variable:
   - Name: `DATABASE_URL`
   - Value: `postgresql://...` (your database URL)
   - Environment: Production (or all)
5. Click **Save**
6. Redeploy your application

## After Setting Up

1. Set all environment variables in Vercel
2. Trigger a new deployment (push to main branch)
3. The application should work correctly

## Current Deploy Status

✅ vercel.json configured
✅ WSGI application set up
✅ Static files configured with WhiteNoise
✅ Database configuration supports PostgreSQL
✅ Settings optimized for production

❌ **ACTION REQUIRED:** Set DATABASE_URL environment variable in Vercel
