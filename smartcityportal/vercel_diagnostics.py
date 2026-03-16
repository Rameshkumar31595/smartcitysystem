"""
Vercel Deployment Diagnostics
Run this after deployment to check if everything is configured correctly
"""

print("=" * 60)
print("VERCEL DEPLOYMENT CHECKLIST")
print("=" * 60)

print("\n1. CHECK VERCEL DASHBOARD LOGS:")
print("   → Go to: https://vercel.com/your-project")
print("   → Click latest deployment")
print("   → Check 'Build Logs' tab")
print("   → Check 'Function Logs' tab (after visiting your site)")

print("\n2. VERIFY ENVIRONMENT VARIABLES IN VERCEL:")
print("   ✓ DATABASE_URL is set")
print("   ✓ SECRET_KEY is set")
print("   ✓ DJANGO_SETTINGS_MODULE (optional, defaults to smartcityportal.settings)")

print("\n3. TEST YOUR DEPLOYMENT:")
print("   → Visit: https://your-project.vercel.app/")
print("   → Visit: https://your-project.vercel.app/admin/")
print("   → Visit: https://your-project.vercel.app/accounts/login/")

print("\n4. IF YOU SEE 404 ERROR:")
print("   → Check Function Logs for Python errors")
print("   → Look for 'ModuleNotFoundError' or 'ImportError'")
print("   → Verify Django setup() completed successfully")

print("\n5. IF YOU SEE 500 ERROR:")
print("   → Database connection issue - check DATABASE_URL")
print("   → Missing dependencies - check requirements.txt")
print("   → Check Function Logs for traceback")

print("\n6. COMMON ISSUES:")
print("   ⚠️  Cold Start: First request takes 5-10 seconds")
print("   ⚠️  Timeout: Vercel functions have 10-second limit")
print("   ⚠️  Size Limit: Deployment must be under 250MB")

print("\n7. IF STILL NOT WORKING:")
print("   📧 Copy Function Logs and share them")
print("   🔄 Try redeploying from Vercel dashboard")
print("   🆘 Consider switching to Render.com (5-minute setup)")

print("\n" + "=" * 60)
print("✅ Good luck with your presentation tomorrow!")
print("=" * 60)
