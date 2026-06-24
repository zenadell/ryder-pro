filepath = '/Users/mac/Desktop/ryder-pro/template-1/pages/home/index.html'
with open(filepath, 'r') as f:
    content = f.read()

# Fix car image
old_car_img = 'class="car-image" />'
new_car_img = 'class="car-image {% if not vehicle.main_image %}skeleton-pulse{% endif %}" />'
content = content.replace(old_car_img, new_car_img)

# Fix category image
old_cat_img = 'class="rental-category-image" />'
new_cat_img = 'class="rental-category-image {% if not category.image %}skeleton-pulse{% endif %}" />'
content = content.replace(old_cat_img, new_cat_img)

with open(filepath, 'w') as f:
    f.write(content)
print("Added skeleton-pulse class!")
