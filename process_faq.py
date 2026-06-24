import re

with open('/Users/mac/Desktop/ryder-pro/template-1/pages/faq/index.html', 'r') as f:
    content = f.read()

# Hero title
content = re.sub(
    r'<h1 class="hero-inner-title">\s*Frequently asked questions\s*</h1>',
    r'<h1 class="hero-inner-title">\n                    {{ site_content.faq_hero_title|default:"Frequently asked questions" }}\n                </h1>',
    content
)

# FAQ 1
content = re.sub(
    r'<h2 class="accordion-title">\s*What documents are required to rent a car\?\s*</h2>',
    r'<h2 class="accordion-title">\n                            {{ site_content.faq_1_question|default:"What documents are required to rent a car?" }}\n                        </h2>',
    content
)
content = re.sub(
    r'<p>\s*You’ll need a valid driver’s license.*?vehicle type.\s*</p>',
    r'<p>\n                                {{ site_content.faq_1_answer|default:"You’ll need a valid driver’s license, a government-issued ID, and a credit or debit card. Some rentals may require additional documents based on location or vehicle type." }}\n                            </p>',
    content
)

# FAQ 2
content = re.sub(
    r'<h2 class="accordion-title">\s*How do I book a car rental\?\s*</h2>',
    r'<h2 class="accordion-title">\n                            {{ site_content.faq_2_question|default:"How do I book a car rental?" }}\n                        </h2>',
    content
)
content = re.sub(
    r'<p>\s*You can book directly on our website.*?drop-off locations.\s*</p>',
    r'<p>\n                                {{ site_content.faq_2_answer|default:"You can book directly on our website, mobile app, or by visiting our rental office. Select your preferred car, rental duration, and pickup/drop-off locations." }}\n                            </p>',
    content
)

# FAQ 3
content = re.sub(
    r'<h2 class="accordion-title">\s*Is there a free trial available\?\s*</h2>',
    r'<h2 class="accordion-title">\n                            {{ site_content.faq_3_question|default:"Is there a free trial available?" }}\n                        </h2>',
    content
)
content = re.sub(
    r'<p>\s*Basic insurance is included.*?time of booking.\s*</p>',
    r'<p>\n                                {{ site_content.faq_3_answer|default:"Basic insurance is included in most rentals. Additional coverage options, like collision damage waivers, can be purchased at the time of booking." }}\n                            </p>',
    content
)

# FAQ 4
content = re.sub(
    r'<h2 class="accordion-title">\s*Can someone else drive the rental car\?\s*</h2>',
    r'<h2 class="accordion-title">\n                            {{ site_content.faq_4_question|default:"Can someone else drive the rental car?" }}\n                        </h2>',
    content
)
content = re.sub(
    r'<p class="no-margin-bottom">\s*Yes, but they must be added.*?fees may apply.\s*</p>',
    r'<p class="no-margin-bottom">\n                                {{ site_content.faq_4_answer|default:"Yes, but they must be added as an authorized driver on the rental agreement. Additional driver fees may apply." }}\n                            </p>',
    content
)

with open('/Users/mac/Desktop/ryder-pro/template-1/pages/faq/index.html', 'w') as f:
    f.write(content)

print("FAQ page processed")
