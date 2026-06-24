import os
import re

template_dir = '/Users/mac/Desktop/ryder-pro/template-1'

for root, dirs, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()
            
            # 1. Fix the invalid backslashes in background URLs
            content = content.replace("url(\\'", "url('")
            content = content.replace("\\')", "')")
            
            # 2. Fix the invisible content bug by stripping the initial opacity:0
            content = content.replace('style="opacity:0"', '')
            
            with open(filepath, 'w') as f:
                f.write(content)

print("Fixed HTML glitches!")
