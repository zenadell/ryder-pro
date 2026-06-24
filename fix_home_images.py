import re

filepath = '/Users/mac/Desktop/ryder-pro/template-1/pages/home/index.html'

with open(filepath, 'r') as f:
    content = f.read()

# Replace vehicle.primary_image with vehicle.main_image
content = content.replace('vehicle.primary_image', 'vehicle.main_image')

transparent_pixel = "data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs="
content = content.replace('../../static/images/fallback.png', transparent_pixel)

# Vehicle images: add skeleton-pulse
content = re.sub(
    r'(<img src="\{% if vehicle\.main_image %\}.*?alt="\{\{ vehicle\.name \}\}" class="car-image)(\s*"/>|\s*">)',
    r'\1 {% if not vehicle.main_image %}skeleton-pulse{% endif %}" />',
    content,
    flags=re.DOTALL
)

# Category images: add skeleton-pulse
# <img src="{% if category.image %}{{ category.image.url }}{% else %}data:image...{% endif %}" loading="eager" alt="{{ category.name }}" class="rental-category-image" />
content = re.sub(
    r'(<img src="\{% if category\.image %\}.*?alt="\{\{ category\.name \}\}" class="rental-category-image)(\s*"/>|\s*">)',
    r'\1 {% if not category.image %}skeleton-pulse{% endif %}" />',
    content,
    flags=re.DOTALL
)

with open(filepath, 'w') as f:
    f.write(content)

print("Fixed vehicle and category images with skeleton-pulse!")
