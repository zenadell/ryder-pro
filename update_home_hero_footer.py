import re

with open('/Users/mac/Desktop/ryder-pro/template-1/pages/home/index.html', 'r') as f:
    content = f.read()

# 1. Update Hero inline styles
content = re.sub(
    r'<div class="hero-bg-wrapper">\s*<div class="hero-bg-image-overlay">\s*</div>',
    r'<div class="hero-bg-wrapper" style="background-image: url(\'{% if site_content.home_hero_bg %}{{ site_content.home_hero_bg.url }}{% else %}../../static/images/674f07a7261905eaaf193f4e_hero-bg.avif{% endif %}\');">\n            <div class="hero-bg-image-overlay">\n            </div>',
    content
)

# 2. Update Hero Button
content = re.sub(
    r'<div class="button-icon-text one">\s*Book your ride now\s*</div>\s*<div class="button-icon-text two">\s*Book your ride now\s*</div>',
    r'<div class="button-icon-text one">\n                                {{ site_content.home_hero_button_label|default:"Book your ride now" }}\n                            </div>\n                            <div class="button-icon-text two">\n                                {{ site_content.home_hero_button_label|default:"Book your ride now" }}\n                            </div>',
    content
)

# 3. Update Footer Form
content = re.sub(
    r'<form id="wf-form-Footer-Subscribe-Form"[^>]*>',
    r'<form id="wf-form-Footer-Subscribe-Form" name="wf-form-Footer-Subscribe-Form" data-name="Footer Subscribe Form" method="POST" action="{% url \'newsletter_subscribe\' %}" class="footer-form-wrap">\n                                    {% csrf_token %}',
    content
)

# 4. Update Footer Links
# Instead of replacing all of them, just replace the chunks for "Pages" and "Utility Pages"
footer_links_replacement = """                    <div class="w-layout-grid grid-footer-right">
                        <div>
                            <h2 class="footer-title">
                                {{ site_content.footer_col1_title|default:"Pages" }}
                            </h2>
                            <div class="footer-link-wrap">
                                <a href="{% url 'home' %}" aria-current="page" class="footer-link w--current"> Home </a>
                                <a href="{% url 'about' %}" class="footer-link"> About </a>
                                <a href="{% url 'car_list' %}" class="footer-link"> Cars </a>
                                <a href="{% url 'contact' %}" class="footer-link"> Contact </a>
                                <a href="{% url 'blog_list' %}" class="footer-link"> Blog </a>
                            </div>
                        </div>
                        <div>
                            <h2 class="footer-title">
                                {{ site_content.footer_col2_title|default:"More Links" }}
                            </h2>
                            <div class="w-layout-grid grid-footer-link">
                                <div class="footer-link-wrap">
                                    <a href="/faqs" class="footer-link"> FAQs </a>
                                    <a href="/terms-conditions" class="footer-link"> Terms & Conditions </a>
                                    <a href="/privacy-policy" class="footer-link"> Privacy Policy </a>
                                </div>
                            </div>
                        </div>
                    </div>"""

grid_footer_pattern = re.compile(r'<div class="w-layout-grid grid-footer-right">.*?</div>\s*</div>\s*</div>\s*<div class="footer-copyright-wrap">', re.DOTALL)
match = grid_footer_pattern.search(content)
if match:
    content = content[:match.start()] + footer_links_replacement + "\n                </div>\n                <div class=\"footer-copyright-wrap\">" + content[match.end():]

with open('/Users/mac/Desktop/ryder-pro/template-1/pages/home/index.html', 'w') as f:
    f.write(content)
    
print("Success")
