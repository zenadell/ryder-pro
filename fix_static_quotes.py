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
            
            # Remove literal backslashes from static tags
            content = content.replace("{% static \\'", "{% static '")
            content = content.replace("\\' %}", "' %}")
            
            if content != original_content:
                with open(filepath, 'w') as f:
                    f.write(content)
                print(f"Fixed quotes in {filepath}")

print("Quotes fixed.")
