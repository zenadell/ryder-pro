import re

filepath = '/Users/mac/Desktop/ryder-pro/template-1/pages/utilities/link-in-bio/index.html'

with open(filepath, 'r') as f:
    content = f.read()

# Add {% load static %}
if '{% load static %}' not in content:
    content = '{% load static %}\n' + content

# Replace image URLs
content = re.sub(r'src="(?:[^"]*?/)?images/([^"]+)"', r'src="{% static \'images/\1\' %}"', content)
content = re.sub(r'content="(?:[^"]*?/)?images/([^"]+)"', r'content="{% static \'images/\1\' %}"', content)

# Replace CSS URLs
content = re.sub(r'href="(?:[^"]*?/)?css/([^"]+)"', r'href="{% static \'css/\1\' %}"', content)

# Replace JS URLs
content = re.sub(r'src="(?:[^"]*?/)?js/([^"]+)"', r'src="{% static \'js/\1\' %}"', content)

# Also link the base CSS
if 'base.css' not in content:
    content = content.replace('</head>', '    <link rel="stylesheet" href="{% static \'base.css\' %}">\n</head>')

with open(filepath, 'w') as f:
    f.write(content)
print("Fixed static tags in link-in-bio!")
