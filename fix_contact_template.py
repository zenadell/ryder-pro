import os
import re

filepath = '/Users/mac/Desktop/ryder-pro/template-1/pages/contact/index.html'

with open(filepath, 'r') as f:
    content = f.read()

replacements = {
    '{{ site_content.contact_hero_title|default:"Contact us!" }}': '{% if site_content.contact_hero_title %}{{ site_content.contact_hero_title }}{% else %}<div class="skeleton-pulse" style="width:200px; height:48px; border-radius:4px; display:inline-block;"></div>{% endif %}',
    '{{ site_content.contact_hero_desc|default:"Whether you have questions, feedback, or need assistance, our team is here to help. Reach out to us through any of the channels below, and we’ll get back to you as soon as possible." }}': '{% if site_content.contact_hero_desc %}{{ site_content.contact_hero_desc }}{% else %}<div class="skeleton-pulse" style="width:100%; height:48px; border-radius:4px;"></div>{% endif %}',
    '{{ site_content.contact_email|default:\'example@gmail.com\' }}': '{% if site_content.contact_email %}{{ site_content.contact_email }}{% else %}<div class="skeleton-pulse" style="width:150px; height:20px; border-radius:4px;"></div>{% endif %}',
    '{{ site_content.contact_email|default:"example@gmail.com" }}': '{% if site_content.contact_email %}{{ site_content.contact_email }}{% else %}<div class="skeleton-pulse" style="width:150px; height:20px; border-radius:4px; display:inline-block;"></div>{% endif %}',
    '{{ site_content.contact_phone|default:\'+91125888666\' }}': '{% if site_content.contact_phone %}{{ site_content.contact_phone }}{% else %}<div class="skeleton-pulse" style="width:120px; height:20px; border-radius:4px;"></div>{% endif %}',
    '{{ site_content.contact_phone|default:"(+91) 125 888 666" }}': '{% if site_content.contact_phone %}{{ site_content.contact_phone }}{% else %}<div class="skeleton-pulse" style="width:120px; height:20px; border-radius:4px; display:inline-block;"></div>{% endif %}',
    '{{ site_content.contact_address|default:"Chicago HQ Estica Cop. Macomb, MI 48042" }}': '{% if site_content.contact_address %}{{ site_content.contact_address }}{% else %}<div class="skeleton-pulse" style="width:100%; height:40px; border-radius:4px;"></div>{% endif %}',
    '{{ site_content.contact_hours_1|default:"Mon - Thu: 11am - 7pm" }}': '{% if site_content.contact_hours_1 %}{{ site_content.contact_hours_1 }}{% else %}<div class="skeleton-pulse" style="width:160px; height:20px; border-radius:4px; margin-bottom:4px;"></div>{% endif %}',
    '{{ site_content.contact_hours_2|default:"Sat: 11am - 2pm" }}': '{% if site_content.contact_hours_2 %}{{ site_content.contact_hours_2 }}{% else %}<div class="skeleton-pulse" style="width:120px; height:20px; border-radius:4px;"></div>{% endif %}'
}

for old_str, new_str in replacements.items():
    content = content.replace(old_str, new_str)

# Also fix the /car to {% url 'all_cars' %}
# But we should do it globally for all pages later. For now, do it in contact page:
content = content.replace('href="/car"', 'href="{% url \'all_cars\' %}"')

with open(filepath, 'w') as f:
    f.write(content)

print("Contact page updated successfully")
