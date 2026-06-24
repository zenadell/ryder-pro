import re

with open('/Users/mac/Desktop/ryder-pro/template-1/pages/utilities/404/index.html', 'r') as f:
    content = f.read()

# Replace 404 message
content = re.sub(
    r'<h1 class="utility-title">\s*Page not found\s*</h1>',
    r'<h1 class="utility-title">\n                            {{ site_content.not_found_title|default:"Page not found" }}\n                        </h1>',
    content
)

content = re.sub(
    r'<p class="no-margin-bottom">\s*The page you are looking for doesn&#x27;t exist or has been moved.\s*</p>',
    r'<p class="no-margin-bottom">\n                            {{ site_content.not_found_desc|default:"The page you are looking for doesn\'t exist or has been moved." }}\n                        </p>',
    content
)

content = re.sub(
    r'<div class="button-icon-text one">\s*Go to home\s*</div>\s*<div class="button-icon-text two">\s*Go to home\s*</div>',
    r'<div class="button-icon-text one">\n                                        {{ site_content.not_found_button|default:"Go to home" }}\n                                    </div>\n                                    <div class="button-icon-text two">\n                                        {{ site_content.not_found_button|default:"Go to home" }}\n                                    </div>',
    content
)

with open('/Users/mac/Desktop/ryder-pro/template-1/pages/utilities/404/index.html', 'w') as f:
    f.write(content)

print("404 page processed")
