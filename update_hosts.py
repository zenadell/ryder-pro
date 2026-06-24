import os

settings_path = '/Users/mac/Desktop/ryder-pro/ryder_pro/settings.py'

with open(settings_path, 'r') as f:
    content = f.read()

content = content.replace(
    "ALLOWED_HOSTS = []",
    "ALLOWED_HOSTS = ['*']"
)

with open(settings_path, 'w') as f:
    f.write(content)

print("ALLOWED_HOSTS updated")
