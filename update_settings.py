import os

settings_path = '/Users/mac/Desktop/ryder-pro/ryder_pro/settings.py'

with open(settings_path, 'r') as f:
    content = f.read()

# Add core to INSTALLED_APPS
content = content.replace(
    "'django.contrib.staticfiles',",
    "'django.contrib.staticfiles',\n    'core',"
)

# Update TEMPLATES DIRS
content = content.replace(
    "'DIRS': [],",
    "'DIRS': [BASE_DIR / 'template-1'],"
)

# Update STATIC and MEDIA settings
static_media_settings = """
STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'template-1' / 'static',
    BASE_DIR / 'template-1' / 'shared',
]

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'
"""

content = content.replace(
    "STATIC_URL = 'static/'",
    static_media_settings
)

with open(settings_path, 'w') as f:
    f.write(content)
