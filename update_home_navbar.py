import re

with open('/Users/mac/Desktop/ryder-pro/template-1/pages/home/index.html', 'r') as f:
    content = f.read()

replacement = """                        <a href="{% url 'car_list' %}" class="nav-link w-nav-link">
                            {{ site_content.nav_link_1_label|default:"Browse Vehicles" }}
                        </a>
                        <a href="{% url 'contact' %}" class="nav-link w-nav-link">
                            {{ site_content.nav_link_2_label|default:"Apply for Financing" }}
                        </a>
                        <div data-delay="0" data-hover="true" data-w-id="b6b150f4-e3d2-2fe0-8369-a6943ebc4cd9"
                            class="w-dropdown">
                            <div class="dropdown-toggle nav-link w-dropdown-toggle">
                                <div>
                                    {{ site_content.nav_dropdown_label|default:"More" }}
                                </div>
                                <div class="dropdown-icon w-icon-dropdown-toggle">
                                </div>
                            </div>
                            <nav class="dropdown-list w-dropdown-list">
                                <div id="w-node-b6b150f4-e3d2-2fe0-8369-a6943ebc4ce4-18a8ef3c"
                                    class="dropdown-list-wrap">
                                    <a href="{% url 'about' %}" class="dropdown-link w-dropdown-link">
                                        {{ site_content.nav_link_3_label|default:"Apply for Jobs" }}
                                    </a>
                                    <a href="/faqs" class="dropdown-link w-dropdown-link"> FAQs
                                    </a>
                                </div>
                            </nav>
                        </div>"""

start_marker = r'<a href="/" aria-current="page" class="nav-link w-nav-link w--current"> Home\s*</a>\s*<a href="/about" class="nav-link w-nav-link"> About\s*</a>\s*<div data-delay="0" data-hover="true" data-w-id="b6b150f4-e3d2-2fe0-8369-a6943ebc4cd9"'
end_marker = r'<a href="/car" class="nav-link w-nav-link"> Cars\s*</a>\s*<a href="/contact" class="nav-link w-nav-link"> Contact\s*</a>'

# Find the start block
start_match = re.search(r'<nav role="navigation"[^>]*>\s*', content)
end_match = re.search(r'</nav>\s*</div>\s*<div id="w-node-e6ff9f79-f479-fa42-6f69-a3df18a8ef7b-18a8ef3c" class="right-button-wrap">', content)

if start_match and end_match:
    new_content = content[:start_match.end()] + replacement + "\n                    </nav>\n                </div>\n                <div id=\"w-node-e6ff9f79-f479-fa42-6f69-a3df18a8ef7b-18a8ef3c\" class=\"right-button-wrap\">" + content[end_match.end():]
    with open('/Users/mac/Desktop/ryder-pro/template-1/pages/home/index.html', 'w') as f:
        f.write(new_content)
    print("Success")
else:
    print("Failed to match")
