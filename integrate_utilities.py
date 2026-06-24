import re
import os

source_files = {
    "utilities/instructions.html": "template-1/pages/utilities/instructions/index.html",
    "utilities/licences.html": "template-1/pages/utilities/licenses/index.html"
}

# The standard head injection for Django templates
head_replacements = [
    (r'https://cdn\.prod\.website-files\.com/[^"]+/css/[^"]+\.css', "{% static 'base.css' %}")
]

for src, dest in source_files.items():
    with open(src, "r") as f:
        content = f.read()
    
    # 1. Add {% load static %}
    content = "{% load static %}\n" + content
    
    # 2. Fix CSS links
    content = re.sub(r'<link href="https://cdn\.prod\.website-files\.com/[^"]+/css/[^"]+\.css".*?>', '<link rel="stylesheet" href="{% static \'base.css\' %}">', content, flags=re.DOTALL)
    
    # 3. Replace Navbar
    # Search for <div data-animation="default" ... class="navbar ..."> ... </header>
    # Wait, the navbar in Webflow usually ends with </header> or </div> 
    # Since regex is tricky, let's just do a simple replacement if possible.
    # Alternatively, the user's templates might just be full HTML. 
    # We can replace the whole <div data-animation="default" class="navbar...</div>  (might be hard)
    # Let's just use a simple regex to replace the navbar.
    content = re.sub(r'<div data-animation="default".*?<div class="navbar-container w-container">.*?</div>\s*</div>\s*</div>', "{% include 'partials/navbar.html' %}", content, flags=re.DOTALL)
    
    # Wait, some navbars use <div data-animation="default" class="navbar ..."> and end with </div>.
    # A safer way to replace the navbar is to find the navbar wrapper and the footer wrapper and replace them.
    content = re.sub(r'<div data-animation="default" class="navbar.*?<div class="nav-button-wrap">.*?</a>\s*</div>\s*</div>\s*</div>\s*</div>', "{% include 'partials/navbar.html' %}", content, flags=re.DOTALL)

    # 4. Replace Footer
    content = re.sub(r'<footer class="footer">.*?</footer>', "{% include 'partials/footer.html' %}", content, flags=re.DOTALL)
    
    # 5. Fix JS paths
    content = re.sub(r'<script src="https://d3e54v103j8qbb\.cloudfront\.net/js/jquery-3\.5\.1\.min\.dc5e7f18c8\.js\?site=.*?".*?></script>', '<script src="{% static \'js/vendor/jquery-3.5.1.min.dc5e7f18c8.js\' %}"></script>', content, flags=re.DOTALL)
    content = re.sub(r'<script src="https://cdn\.prod\.website-files\.com/.*?/js/webflow\..*?\.js".*?></script>', '<script src="{% static \'base.js\' %}"></script>', content, flags=re.DOTALL)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    
    with open(dest, "w") as f:
        f.write(content)
    print(f"Integrated {src} into {dest}")

