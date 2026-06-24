import os

settings_path = '/Users/mac/Desktop/ryder-pro/ryder_pro/settings.py'

with open(settings_path, 'r') as f:
    content = f.read()

content = content.replace(
    "'django.template.context_processors.request',",
    "'django.template.context_processors.request',\n                'core.context_processors.site_content',"
)

with open(settings_path, 'w') as f:
    f.write(content)

print("Context processor added")
