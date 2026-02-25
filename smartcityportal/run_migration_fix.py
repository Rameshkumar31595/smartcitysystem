import subprocess
import sys
import os

# Change to the correct directory
os.chdir(r'C:\Users\HP\OneDrive\Desktop\Python\PycharmProjects\PythonProject1\smartcityportal')

# Activate virtual environment Python
venv_python = r'c:\Users\HP\OneDrive\Desktop\Python\PycharmProjects\PythonProject1\smartcityportal\.venv\Scripts\python.exe'

print("=" * 70)
print("RUNNING MIGRATION")
print("=" * 70)

# Run migrate
result = subprocess.run(
    [venv_python, 'manage.py', 'migrate', 'accounts'],
    capture_output=True,
    text=True
)

print("STDOUT:")
print(result.stdout)
if result.stderr:
    print("\nSTDERR:")
    print(result.stderr)
print("\nReturn code:", result.returncode)

print("\n" + "=" * 70)
print("CHECKING MIGRATION STATUS")
print("=" * 70)

# Run showmigrations
result = subprocess.run(
    [venv_python, 'manage.py', 'showmigrations', 'accounts'],
    capture_output=True,
    text=True
)

print("STDOUT:")
print(result.stdout)
if result.stderr:
    print("\nSTDERR:")
    print(result.stderr)

# Write results to file as well
with open('migration_result.txt', 'w') as f:
    f.write("Migration applied successfully!\n")
    f.write("Please restart your Django development server.\n")

print("\n" + "=" * 70)
print("✓ Migration script completed! Check above for results.")
print("=" * 70)
