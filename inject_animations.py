import os

template_dir = '/Users/mac/Desktop/ryder-pro/template-1/pages'
script_tag = '<script src="{% static \'js/custom-animations.js\' %}"></script>\n</body>'

for root, dirs, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()
            
            if 'custom-animations.js' not in content:
                content = content.replace('</body>', script_tag)
                with open(filepath, 'w') as f:
                    f.write(content)

print("Injected custom-animations.js into all HTML files!")
