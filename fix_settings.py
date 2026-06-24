import os

settings_path = '/Users/mac/Desktop/ryder-pro/ryder_pro/settings.py'

with open(settings_path, 'r') as f:
    content = f.read()

content = content.replace(
    "BASE_DIR / 'template-1'",
    "BASE_DIR / 'template-1' / 'pages'"
)

with open(settings_path, 'w') as f:
    f.write(content)

print("settings.py fixed")
