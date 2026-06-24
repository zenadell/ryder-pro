import re

filepath = '/Users/mac/Desktop/ryder-pro/template-1/pages/home/index.html'

with open(filepath, 'r') as f:
    content = f.read()

# 1. Add background color to the first category link
old_link = 'class="rental-category-link w-inline-block">'
new_link = 'class="rental-category-link {% if forloop.first %}bg-primary-1{% endif %} w-inline-block">'
content = content.replace(old_link, new_link)

# 2. Add aspect-ratio: 1/1; to the rental category image
old_img_class = 'class="rental-category-image {% if not category.image %}skeleton-pulse{% endif %}" />'
new_img_class = 'style="aspect-ratio: 1/1;" class="rental-category-image {% if not category.image %}skeleton-pulse{% endif %}" />'
content = content.replace(old_img_class, new_img_class)

with open(filepath, 'w') as f:
    f.write(content)

print("Fixed category styles")
