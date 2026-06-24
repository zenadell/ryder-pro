import os
import re

home_path = '/Users/mac/Desktop/ryder-pro/template-1/pages/home/index.html'
partials_dir = '/Users/mac/Desktop/ryder-pro/template-1/pages/partials'
pages_dir = '/Users/mac/Desktop/ryder-pro/template-1/pages'

if not os.path.exists(partials_dir):
    os.makedirs(partials_dir)

# Read home file
with open(home_path, 'r') as f:
    home_content = f.read()

# Extract footer block
# Since we know it's <footer class="footer"> ... </footer>
footer_match = re.search(r'(<footer class="footer">.*?</footer>)', home_content, flags=re.DOTALL)
if not footer_match:
    print("Could not find footer in home/index.html")
    exit(1)

footer_html = footer_match.group(1)

# Modify footer to add CSRF and form action
# The form is like: <form id="wf-form-Footer-Subscribe-Form" name="wf-form-Footer-Subscribe-Form" data-name="Footer Subscribe Form" method="get" class="footer-subscribe-form" data-wf-page-id="...">
# Let's replace 'method="get"' with 'method="POST" action="{% url \'subscribe\' %}"'
# If method="get" is not exactly there, we can just inject into the form tag.
form_match = re.search(r'<form\s+id="wf-form-Footer-Subscribe-Form"[^>]*>', footer_html)
if form_match:
    form_tag = form_match.group(0)
    # remove existing method and action
    form_tag = re.sub(r'\smethod="[^"]*"', '', form_tag)
    form_tag = re.sub(r'\saction="[^"]*"', '', form_tag)
    # add method="POST" action="{% url 'subscribe' %}"
    new_form_tag = form_tag[:-1] + ' method="POST" action="{% url \'subscribe\' %}">'
    footer_html = footer_html.replace(form_tag, new_form_tag)
    
    # inject csrf token after form tag
    footer_html = footer_html.replace(new_form_tag, new_form_tag + '\n{% csrf_token %}')
    
    # inject name="email" into the email input field
    # <input class="form-input footer-input w-input" maxlength="256" name="Email" data-name="Email" placeholder="Your e-mail here" type="email" id="Email" required="" />
    # We should replace name="Email" with name="email"
    footer_html = footer_html.replace('name="Email"', 'name="email"')

# Write footer.html
footer_path = os.path.join(partials_dir, 'footer.html')
with open(footer_path, 'w') as f:
    f.write(footer_html)
print("Created partials/footer.html")

# Replace in all pages
for root, _, files in os.walk(pages_dir):
    for file in files:
        if file.endswith('.html') and 'partials' not in root:
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Find footer and replace
            page_footer_match = re.search(r'(<footer class="footer">.*?</footer>)', content, flags=re.DOTALL)
            if page_footer_match:
                content = content.replace(page_footer_match.group(1), "{% include 'partials/footer.html' %}")
                with open(filepath, 'w') as f:
                    f.write(content)
                print(f"Replaced footer in {filepath}")

print("Done extracting and replacing footer.")
