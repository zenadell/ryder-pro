import re
import os

# 1. Update core/context_processors.py
cp_path = '/Users/mac/Desktop/ryder-pro/core/context_processors.py'
with open(cp_path, 'r') as f:
    cp_content = f.read()

cp_content = cp_content.replace(
    'content_dict = {item.key: item.value for item in content}',
    '''content_dict = {}
    for item in content:
        if item.image:
            content_dict[item.key] = item.image.url
        else:
            content_dict[item.key] = item.value'''
)
with open(cp_path, 'w') as f:
    f.write(cp_content)

# 2. Update templates to remove .url for site_content variables
import glob

template_dir = '/Users/mac/Desktop/ryder-pro/template-1/pages/'
for root, dirs, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Use regex to replace {{ site_content.KEY.url }} with {{ site_content.KEY }}
            # Also handle {% if site_content.KEY.url %} - wait, the if statement doesn't use .url usually
            # Example: {{ site_content.home_hero_bg.url }} -> {{ site_content.home_hero_bg }}
            new_content = re.sub(r'(site_content\.[a-zA-Z0-9_]+)\.url', r'\1', content)
            
            if new_content != content:
                with open(filepath, 'w') as f:
                    f.write(new_content)
                print(f"Updated {filepath}")

print("Successfully updated templates and context_processors.")
