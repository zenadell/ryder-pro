import os
import re

template_dir = '/Users/mac/Desktop/ryder-pro/template-1'

for root, dirs, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()
            
            original_content = content
            
            # Remove integrity and crossorigin attributes
            content = re.sub(r'\s*integrity="[^"]+"\s*', ' ', content)
            content = re.sub(r'\s*crossorigin="anonymous"\s*', ' ', content)
            
            # Also fix the JS paths that were missed
            # <script src="script.js"></script>
            if 'script.js' in content:
                # get the relative path inside pages
                rel_path = os.path.relpath(filepath, os.path.join(template_dir, 'pages'))
                page_dir = os.path.dirname(rel_path)
                content = re.sub(r'src="script\.js"', f'src="{{% static \'{page_dir}/script.js\' %}}"', content)
            
            # <script src="../shared/base.js"></script>
            content = re.sub(r'src="(?:\.\./)+shared/([^"]+)"', r'src="{% static \'\1\' %}"', content)
            
            # Fix any single quotes accidentally left by fix_static_tags.py on the JS tags
            content = content.replace("{% static \\'", "{% static '")
            content = content.replace("\\' %}", "' %}")
            
            if content != original_content:
                with open(filepath, 'w') as f:
                    f.write(content)
                print(f"Stripped integrity from {filepath}")

print("Integrity stripped.")
