import re

def update_page(file_path, title, description, content_html):
    with open(file_path, "r") as f:
        content = f.read()
    
    # Replace title
    content = re.sub(r'<title>.*?</title>', f'<title>{title} | Ryder Pro</title>', content, flags=re.DOTALL)
    
    # Replace main h1
    content = re.sub(r'<h1 class="page-title">.*?</h1>', f'<h1 class="page-title">{title}</h1>', content, flags=re.DOTALL)
    
    # Replace description paragraph below h1
    content = re.sub(r'<p class="page-description">.*?</p>', f'<p class="page-description">{description}</p>', content, flags=re.DOTALL)
    
    # Replace the body content inside rich-text wrapper
    # It starts with <div class="w-richtext"> and ends with </div>
    # But regex on nested divs is hard, so we'll just replace everything inside the rich-text div
    pattern = re.compile(r'(<div class="w-richtext">).*?(</div>\s*</div>\s*</div>\s*</section>)', re.DOTALL)
    content = pattern.sub(rf'\1\n{content_html}\n\2', content)
    
    with open(file_path, "w") as f:
        f.write(content)

instructions_html = """
<h2>Website Instructions</h2>
<p>Welcome to Ryder Pro! Here is a brief guide on how to navigate our platform:</p>
<ul>
    <li><strong>Booking a Car:</strong> Navigate to the Cars page, select your desired vehicle, and click 'Order Now'.</li>
    <li><strong>Trade-In:</strong> Head to our Trade-In section to get a quick estimate for your current vehicle.</li>
    <li><strong>Tracking:</strong> Use your tracking ID on the Track Order page to follow your rental delivery.</li>
</ul>
<p>If you need further assistance, please contact our support team.</p>
"""

licenses_html = """
<h2>Image & Font Licenses</h2>
<p>All graphical assets, icons, and fonts used on this website are either properly licensed or fall under public domain / open source licenses.</p>
<h3>Typography</h3>
<p>We use Google Fonts (Instrument Sans) which is licensed under the SIL Open Font License.</p>
<h3>Images</h3>
<p>Car photography and lifestyle images are sourced from premium stock providers and are fully licensed for commercial use by Ryder Pro.</p>
"""

update_page("template-1/pages/utilities/instructions/index.html", "Instructions", "Learn how to navigate and use the Ryder Pro platform.", instructions_html)
update_page("template-1/pages/utilities/licenses/index.html", "Licenses", "Details regarding the typography, images, and assets used on this site.", licenses_html)

print("Utility pages created and updated")
