"""
Script to generate SECRET_KEY for Django production deployment
"""
import secrets

print("\n" + "="*60)
print("DJANGO SECRET KEY GENERATOR")
print("="*60)
print("\nGenerated SECRET_KEY:")
print("-" * 60)
secret_key = secrets.token_urlsafe(50)
print(secret_key)
print("-" * 60)
print("\nCopy the key above and add it to Vercel as SECRET_KEY")
print("="*60)
