import os
import re

template_dir = '/Users/mac/Desktop/ryder-pro/template-1'
pages_dir = os.path.join(template_dir, 'pages')

for root, dirs, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()
            
            original_content = content
            
            # 1. Add {% load static %} if not present
            if '{% load static %}' not in content:
                content = '{% load static %}\n' + content
                
            # 2. Fix static folder paths (e.g., ../../static/ or ../static/)
            content = re.sub(r'(src|href)="(?:\.\./)+static/([^"]+)"', r'\1="{% static \'\2\' %}"', content)
            
            # 3. Fix shared base css (e.g., ../shared/base.css or ../../shared/base.css)
            content = re.sub(r'href="(?:\.\./)+shared/([^"]+)"', r'href="{% static \'\1\' %}"', content)
            
            # 4. Fix style.css local to the page
            if filepath.startswith(pages_dir):
                # get the relative path inside pages
                rel_path = os.path.relpath(filepath, pages_dir)
                page_dir = os.path.dirname(rel_path)
                
                # Replace href="style.css" with {% static 'page_dir/style.css' %}
                # But ensure we only replace exact "style.css"
                content = re.sub(r'href="style\.css"', f'href="{{% static \'{page_dir}/style.css\' %}}"', content)
            
            if content != original_content:
                with open(filepath, 'w') as f:
                    f.write(content)
                print(f"Fixed static tags in {filepath}")

print("Static tags fixed.")
