import os
from dotenv import load_dotenv
load_dotenv()

url = os.environ.get('DATABASE_URL', '')
if url:
    print("PostgreSQL is configured!")
    print("Engine: postgresql")
    print("Host:", url.split('@')[1].split('/')[0] if '@' in url else 'unknown')
else:
    print("DATABASE_URL not set - SQLite fallback would be used")
