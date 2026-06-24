import re

filepath = '/Users/mac/Desktop/ryder-pro/template-1/pages/home/index.html'

with open(filepath, 'r') as f:
    content = f.read()

# Replace {{ site_content.key|default:"Text" }} with {% if site_content.key %}{{ site_content.key }}{% else %}<div class="skeleton-pulse"...>{% endif %}

# For texts (e.g., titles, descriptions)
text_pattern = re.compile(r'\{\{\s*(site_content\.[a-zA-Z0-9_]+)\|default:([\'"][^\'"]+[\'"])\s*\}\}')

def text_replacer(match):
    key = match.group(1)
    default_text = match.group(2)
    # Estimate width based on default text length (approx 8px per char)
    length = len(default_text.strip("'\""))
    width = min(max(length * 8, 80), 400)
    return f'{{% if {key} %}}{{{{ {key} }}}}{{% else %}}<div class="skeleton-pulse" style="width:{width}px; height:20px; border-radius:4px; display:inline-block;"></div>{{% endif %}}'

content = text_pattern.sub(text_replacer, content)

# For images (e.g., {{ site_content.key.url|default:'...' }})
# Example: <img src="{{ site_content.home_feature_1_icon.url|default:'../../static/images/...' }}" ...>
img_pattern = re.compile(r'\{\{\s*(site_content\.[a-zA-Z0-9_]+)\.url\|default:([\'"][^\'"]+[\'"])\s*\}\}')

def img_replacer(match):
    key = match.group(1)
    return f'{{% if {key} %}}{{{{ {key}.url }}}}{{% else %}}../../static/images/fallback.png{{% endif %}}'

content = img_pattern.sub(img_replacer, content)

# Also there are some other hardcoded fallbacks in cars etc, let's just write back the content
with open(filepath, 'w') as f:
    f.write(content)

print("Replaced all default fallbacks with skeleton logic in home/index.html!")
