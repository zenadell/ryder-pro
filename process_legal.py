import re
import os

# Privacy Page
with open('/Users/mac/Desktop/ryder-pro/template-1/pages/privacy/index.html', 'r') as f:
    privacy_content = f.read()

privacy_content = re.sub(
    r'<h1 class="hero-inner-title">\s*Privacy policy\s*</h1>',
    r'<h1 class="hero-inner-title">\n                    {{ site_content.privacy_hero_title|default:"Privacy policy" }}\n                </h1>',
    privacy_content
)

privacy_content = re.sub(
    r'<div class="rich-text-content w-richtext">.*?</div>\s*</div>\s*</div>\s*</section>',
    r'<div class="rich-text-content w-richtext">\n                    {{ site_content.privacy_content|safe|default:"<p>Privacy policy content goes here.</p>" }}\n                </div>\n            </div>\n        </div>\n    </section>',
    privacy_content,
    flags=re.DOTALL
)

with open('/Users/mac/Desktop/ryder-pro/template-1/pages/privacy/index.html', 'w') as f:
    f.write(privacy_content)

# Terms Page
with open('/Users/mac/Desktop/ryder-pro/template-1/pages/terms/index.html', 'r') as f:
    terms_content = f.read()

terms_content = re.sub(
    r'<h1 class="hero-inner-title">\s*Terms and conditions\s*</h1>',
    r'<h1 class="hero-inner-title">\n                    {{ site_content.terms_hero_title|default:"Terms and conditions" }}\n                </h1>',
    terms_content
)

terms_content = re.sub(
    r'<div class="rich-text-content w-richtext">.*?</div>\s*</div>\s*</div>\s*</section>',
    r'<div class="rich-text-content w-richtext">\n                    {{ site_content.terms_content|safe|default:"<p>Terms and conditions content goes here.</p>" }}\n                </div>\n            </div>\n        </div>\n    </section>',
    terms_content,
    flags=re.DOTALL
)

with open('/Users/mac/Desktop/ryder-pro/template-1/pages/terms/index.html', 'w') as f:
    f.write(terms_content)

print("Legal pages processed")
