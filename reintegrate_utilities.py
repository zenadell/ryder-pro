import re
import os

source_files = {
    "utilities/instructions.html": "template-1/pages/utilities/instructions/index.html",
    "utilities/licences.html": "template-1/pages/utilities/licenses/index.html",
    "utilities/style-guild.html": "template-1/pages/utilities/style-guide/index.html"
}

css_injection = """    <link href="{% static 'css/vendor/carent-wbs.webflow.shared.15fbda294.css' %}" rel="stylesheet" type="text/css" />
    <link rel="stylesheet" href="{% static 'base.css' %}">
    <link rel="stylesheet" href="{% static 'css/vendor/fonts.css' %}">"""

for src, dest in source_files.items():
    if not os.path.exists(src):
        continue
    with open(src, "r") as f:
        content = f.read()
    
    # 1. Add {% load static %}
    content = "{% load static %}\n" + content
    
    # 2. Fix CSS links
    content = re.sub(r'<link href="https://cdn\.prod\.website-files\.com/[^"]+/css/[^"]+\.css".*?>', css_injection, content, flags=re.DOTALL)
    
    # Replace Webflow title with Django title
    title = src.split("/")[-1].split(".")[0].replace("-", " ").title()
    content = re.sub(r'<title>.*?</title>', f'<title>{title} | Ryder Pro</title>', content, flags=re.DOTALL)

    # 3. Replace Navbar
    # The navbar starts with <div data-animation="default" ... class="navbar w-nav">
    # and ends before <div class="hero-inner text-center"> or <div class="hero-inner">
    content = re.sub(r'<div data-animation="default".*?class="navbar w-nav">.*?<div class="hero-inner', "{% include 'partials/navbar.html' %}\n    <div class=\"hero-inner", content, flags=re.DOTALL)
    
    # 4. Replace Footer
    content = re.sub(r'<footer class="footer">.*?</footer>', "{% include 'partials/footer.html' %}", content, flags=re.DOTALL)
    
    # 5. Replace Webestica / Carent
    content = re.sub(r'Webestica', 'Ryder Pro', content, flags=re.IGNORECASE)
    content = re.sub(r'Carent', 'Ryder Pro', content, flags=re.IGNORECASE)

    # 6. Fix JS paths
    content = re.sub(r'<script src="https://d3e54v103j8qbb\.cloudfront\.net/js/jquery-3\.5\.1\.min\.dc5e7f18c8\.js\?site=.*?".*?></script>', '<script src="{% static \'js/vendor/jquery-3.5.1.min.dc5e7f18c8.js\' %}"></script>', content, flags=re.DOTALL)
    content = re.sub(r'<script src="https://cdn\.prod\.website-files\.com/.*?/js/webflow\..*?\.js".*?></script>', '<script src="{% static \'base.js\' %}"></script>', content, flags=re.DOTALL)
    
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    with open(dest, "w") as f:
        f.write(content)
    print(f"Reintegrated {src} into {dest}")

