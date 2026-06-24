import os

template_dir = '/Users/mac/Desktop/ryder-pro/template-1'

replacements = {
    r"{% url \'newsletter_subscribe\' %}": "{% url 'home' %}",
    r"{% url 'newsletter_subscribe' %}": "{% url 'home' %}",
    r"{% url 'car_list' %}": "{% url 'all_cars' %}",
    r"{% url 'contact_submit' %}": "{% url 'contact' %}",
    r"{% url 'blog_list' %}": "{% url 'blog' %}",
    r"{% url 'car_detail'": "{% url 'car_details'",
}

for root, dirs, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()
            
            original_content = content
            for old, new in replacements.items():
                content = content.replace(old, new)
                
            if content != original_content:
                with open(filepath, 'w') as f:
                    f.write(content)
                print(f"Fixed {filepath}")

print("URL fixes applied.")
