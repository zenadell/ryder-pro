import os
import re

template_dir = '/Users/mac/Desktop/ryder-pro/template-1'

def add_opacity(match):
    # match.group(0) is the entire tag e.g. <div data-w-id="123" class="hero-wrap">
    tag = match.group(0)
    # Don't add to dropdowns, navs, tabs, buttons if they shouldn't be fully hidden
    if any(x in tag for x in ['w-dropdown', 'w-nav', 'button', 'w-tab']):
        return tag
    # If it already has a style attribute, we would need to append.
    # For simplicity, if it has style="", we replace it. If not, we add it.
    if 'style="' in tag:
        return tag.replace('style="', 'style="opacity:0; ')
    else:
        return tag.replace('data-w-id=', 'style="opacity:0" data-w-id=')

for root, dirs, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Find all tags with data-w-id
            # This regex matches <... data-w-id="..." ...>
            new_content = re.sub(r'<[^>]*?data-w-id="[^"]*"[^>]*?>', add_opacity, content)
            
            if new_content != content:
                with open(filepath, 'w') as f:
                    f.write(new_content)

print("Restored opacity:0!")
