import os

template_dir = '/Users/mac/Desktop/ryder-pro/template-1/pages'

for root, _, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()
            
            if 'href="/car"' in content:
                content = content.replace('href="/car"', 'href="{% url \'all_cars\' %}"')
                with open(filepath, 'w') as f:
                    f.write(content)
                print(f"Fixed {filepath}")

print("Done fixing /car links")
