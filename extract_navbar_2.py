import os

template_dir = '/Users/mac/Desktop/ryder-pro/template-1/pages/'
for root, dirs, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html') and file != 'navbar.html':
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()

            if '<div data-animation="default"' in content and 'class="navbar w-nav"' in content:
                # Find start
                start_idx = content.find('<div data-animation="default"')
                # Find end of navbar
                # It usually ends before the first <section> or a specific div
                # We can just look for the first </nav> and then closing divs, but it's tricky.
                # A safer way: count open/close <div> tags from start_idx
                
                temp_content = content[start_idx:]
                div_count = 0
                end_idx = 0
                i = 0
                while i < len(temp_content):
                    if temp_content[i:i+4] == '<div':
                        div_count += 1
                        i += 4
                    elif temp_content[i:i+6] == '</div>':
                        div_count -= 1
                        i += 6
                        if div_count == 0:
                            end_idx = start_idx + i
                            break
                    else:
                        i += 1
                
                if end_idx > start_idx:
                    navbar_code = content[start_idx:end_idx]
                    new_content = content[:start_idx] + "{% include 'partials/navbar.html' %}" + content[end_idx:]
                    with open(filepath, 'w') as f:
                        f.write(new_content)
                    print(f"Updated {filepath}")
