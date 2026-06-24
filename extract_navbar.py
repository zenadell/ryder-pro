import os
import re
import glob

navbar_html = """{% load static %}
<div data-animation="default" data-collapse="medium" data-duration="400" data-easing="ease" data-easing2="ease"
    role="banner" class="navbar w-nav">
    <div class="container-full w-container">
        <div class="w-layout-grid grid-nav">
            <a href="/" id="w-node-e6ff9f79-f479-fa42-6f69-a3df18a8ef3f-18a8ef3c" class="brand w-nav-brand"> <img
                    src="{% static 'images/6750187eaaf2527a45e1761d_dark-carrent.svg' %}"
                    loading="lazy" alt="" class="header-logo" />
            </a>
            <div id="w-node-e6ff9f79-f479-fa42-6f69-a3df18a8ef64-18a8ef3c" class="right-nav">
                <nav role="navigation" id="w-node-e6ff9f79-f479-fa42-6f69-a3df18a8ef41-18a8ef3c"
                    class="nav-menu w-nav-menu">
                    <a href="/" class="nav-link w-nav-link"> Home </a>
                    <a href="/about" class="nav-link w-nav-link"> About </a>
                    <div data-delay="0" data-hover="true" data-w-id="b6b150f4-e3d2-2fe0-8369-a6943ebc4cd9"
                        class="w-dropdown">
                        <div class="dropdown-toggle nav-link w-dropdown-toggle">
                            <div>Pages</div>
                            <div class="dropdown-icon w-icon-dropdown-toggle"></div>
                        </div>
                        <nav class="dropdown-list w-dropdown-list">
                            <div id="w-node-b6b150f4-e3d2-2fe0-8369-a6943ebc4ce4-18a8ef3c"
                                class="dropdown-list-wrap">
                                <a href="/" class="dropdown-link w-dropdown-link"> Home </a>
                                <a href="/about" class="dropdown-link w-dropdown-link"> About </a>
                                <a href="{% url 'all_cars' %}" class="dropdown-link w-dropdown-link"> Cars </a>
                                <a href="/contact" class="dropdown-link w-dropdown-link"> Contact </a>
                                <a href="/blog" class="dropdown-link w-dropdown-link"> Blog </a>
                                <a href="/faqs" class="dropdown-link w-dropdown-link"> FAQs </a>
                                <a href="/terms-conditions" class="dropdown-link w-dropdown-link"> Terms &amp; Conditions </a>
                                <a href="/privacy-policy" class="dropdown-link w-dropdown-link"> Privacy Policy </a>
                            </div>
                        </nav>
                    </div>
                    <a href="{% url 'all_cars' %}" class="nav-link w-nav-link"> Cars </a>
                    <a href="/contact" class="nav-link w-nav-link"> Contact </a>
                    {% if user.is_authenticated %}
                        <form action="{% url 'logout' %}" method="post" style="display:inline;">
                            {% csrf_token %}
                            <button type="submit" class="nav-link w-nav-link" style="background:none;border:none;cursor:pointer;"> Log Out </button>
                        </form>
                    {% else %}
                        <a href="{% url 'login' %}" class="nav-link w-nav-link"> Log In </a>
                        <a href="{% url 'signup' %}" class="nav-link w-nav-link"> Sign Up </a>
                    {% endif %}
                </nav>
                <div class="menu-button w-nav-button">
                    <div class="w-icon-nav-menu"></div>
                </div>
            </div>
        </div>
    </div>
</div>
"""

os.makedirs('/Users/mac/Desktop/ryder-pro/template-1/pages/partials', exist_ok=True)
with open('/Users/mac/Desktop/ryder-pro/template-1/pages/partials/navbar.html', 'w') as f:
    f.write(navbar_html)

# Pattern to find the navbar block
# We know it starts with `<div data-animation="default"` ... `role="banner" class="navbar w-nav">`
# and ends when its root div is closed.
# We will use regex to find this block and replace it.

pattern = re.compile(
    r'<div\s+data-animation="default"\s+data-collapse="medium".*?role="banner"\s+class="navbar w-nav">\s*<div\s+class="container-full w-container">.*?<!--\s*Navbar\s*End\s*-->|<div\s+data-animation="default"\s+data-collapse="medium".*?role="banner"\s+class="navbar w-nav">\s*<div\s+class="container-full w-container">[\s\S]*?<div\s+class="w-icon-nav-menu">\s*</div>\s*</div>\s*</div>\s*</div>\s*</div>\s*</div>',
    re.IGNORECASE | re.MULTILINE
)

template_dir = '/Users/mac/Desktop/ryder-pro/template-1/pages/'
for root, dirs, files in os.walk(template_dir):
    for file in files:
        if file.endswith('.html') and file != 'navbar.html':
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()

            # Attempt replacement
            new_content, count = pattern.subn('{% include \'partials/navbar.html\' %}', content)
            
            if count > 0:
                with open(filepath, 'w') as f:
                    f.write(new_content)
                print(f"Updated {filepath}")
            else:
                # Some might have slightly different formatting, let's try a fallback replace
                # We can just look for the start and the specific end div sequence.
                pass

print("Navbar extraction script completed.")
