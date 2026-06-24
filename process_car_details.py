import re

with open('/Users/mac/Desktop/ryder-pro/template-1/pages/cars/car-details/index.html', 'r') as f:
    content = f.read()

# 1. Car Image and Details
content = re.sub(
    r'<img src="../../../static/images/675d246a08777aecdb41d97f_car-01.avif"\s*loading="eager" alt="" class="car-detail-image" />',
    r'<img src="{% if vehicle.main_image %}{{ vehicle.main_image.url }}{% else %}../../../static/images/675d246a08777aecdb41d97f_car-01.avif{% endif %}" loading="eager" alt="{{ vehicle.name }}" class="car-detail-image" />',
    content
)

content = re.sub(
    r'<h1 class="car-detail-title">\s*Compact city cruiser\s*</h1>',
    r'<h1 class="car-detail-title">\n                            {{ vehicle.name }}\n                        </h1>',
    content
)

content = re.sub(
    r'<div class="car-info-wrap">\s*<div class="car-category-text">\s*Audi\s*</div>\s*<div class="car-category-text">\s*Q3\s*</div>\s*<div class="car-category-text last-border-removed">\s*2017\s*</div>\s*</div>',
    r'<div class="car-info-wrap">\n                            <div class="car-category-text">\n                                {{ vehicle.make }}\n                            </div>\n                            <div class="car-category-text">\n                                {{ vehicle.model }}\n                            </div>\n                            <div class="car-category-text last-border-removed">\n                                {{ vehicle.year }}\n                            </div>\n                        </div>',
    content
)

content = re.sub(
    r'<p class="car-detail-description">\s*A compact city cruiser is a stylish.*?spaces.\s*</p>',
    r'<p class="car-detail-description">\n                            {{ vehicle.description }}\n                        </p>',
    content,
    flags=re.DOTALL
)

content = re.sub(
    r'<h2 class="car-price">\s*\$150\s*</h2>',
    r'<h2 class="car-price">\n                                ${{ vehicle.price_per_day }}\n                            </h2>',
    content
)

# Meta block
content = re.sub(
    r'<div class="car-meta-value">\s*4\s*</div>',
    r'<div class="car-meta-value">\n                                    {{ vehicle.seats }}\n                                </div>',
    content,
    count=1
)
content = re.sub(
    r'<div class="car-meta-value">\s*Manual\s*</div>',
    r'<div class="car-meta-value">\n                                    {{ vehicle.transmission }}\n                                </div>',
    content,
    count=1
)
content = re.sub(
    r'<div class="car-meta-value">\s*2 bags\s*</div>',
    r'<div class="car-meta-value">\n                                    {{ vehicle.luggage }}\n                                </div>',
    content,
    count=1
)
content = re.sub(
    r'<div class="car-meta-value">\s*Petrol\s*</div>',
    r'<div class="car-meta-value">\n                                    {{ vehicle.fuel_type }}\n                                </div>',
    content,
    count=1
)

# Vehicle features
feature_loop = """                        {% if vehicle_features %}
                            {% for feature in vehicle_features %}
                            <div class="car-feature-item">
                                <img src="../../../static/images/67540ae437014405c0e5c837_list-icon.svg" loading="eager" alt="" class="car-feature-icon" />
                                <div>{{ feature.name }}</div>
                            </div>
                            {% endfor %}
                        {% else %}
                            <div class="car-feature-item">
                                <div>No features listed.</div>
                            </div>
                        {% endif %}"""

content = re.sub(
    r'<div data-w-id="008a0945-a587-ab03-92d1-04ea53c11401" style="opacity:0"\s*class="w-layout-grid grid-car-feature">.*?</div>\s*</div>\s*</div>\s*</div>\s*</section>',
    r'<div data-w-id="008a0945-a587-ab03-92d1-04ea53c11401" style="opacity:0" class="w-layout-grid grid-car-feature">\n' + feature_loop + '\n                        </div>\n                    </div>\n                </div>\n            </div>\n        </div>\n    </section>',
    content,
    flags=re.DOTALL
)

# Vehicle Gallery
gallery_loop = """                <div role="list" class="grid-vehicle-gallery w-dyn-items">
                    {% if vehicle_images %}
                        {% for image in vehicle_images %}
                        <div id="w-node-_8aa0d768-a557-f2b8-3369-24fd79ab090a-fc8f6efa" data-w-id="8aa0d768-a557-f2b8-3369-24fd79ab090a" style="opacity:0" role="listitem" class="w-dyn-item w-dyn-repeater-item">
                            <a href="#" data-w-id="c1663df0-6696-c7fe-b56f-a8c5ef01df10" class="vehicle-lightbox-link w-inline-block w-lightbox">
                                <img src="{{ image.image.url }}" loading="lazy" style="-webkit-transform:translate3d(0, 0, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-moz-transform:translate3d(0, 0, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-ms-transform:translate3d(0, 0, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);transform:translate3d(0, 0, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0)" alt="{{ vehicle.name }}" class="gallery-lightbox-image" />
                                <script type="application/json" class="w-json">
                                {
                                  "items": [
                                    {
                                      "url": "{{ image.image.url }}",
                                      "type": "image"
                                    }
                                  ],
                                  "group": "Vehicle Gallery Image"
                                }
                                </script>
                            </a>
                        </div>
                        {% endfor %}
                    {% else %}
                        <div class="empty-state"><div>No images found.</div></div>
                    {% endif %}
                </div>"""

content = re.sub(
    r'<div role="list" class="grid-vehicle-gallery w-dyn-items">.*?</div>\s*<div class="empty-state w-dyn-hide w-dyn-empty">.*?</div>',
    gallery_loop,
    content,
    flags=re.DOTALL
)

# Review Slider
review_loop = """                            <div class="review-mask w-slider-mask">
                                {% if vehicle_reviews %}
                                    {% for review in vehicle_reviews %}
                                    <div class="review-slide w-slide">
                                        <div class="review-slide-item">
                                            <div class="review-slide-content-wrap">
                                                <div>
                                                    <img src="../../../static/images/6752790ec11ba7f2aecb9bc9_rating.svg" loading="eager" alt="" class="review-star-image" />
                                                    <div class="div-block">
                                                        <h3 class="review-title">
                                                            {{ review.title }}
                                                        </h3>
                                                        <p class="no-margin-bottom">
                                                            {{ review.content }}
                                                        </p>
                                                    </div>
                                                </div>
                                                <div class="review-name-wrap">
                                                    <img src="{% if review.reviewer_image %}{{ review.reviewer_image.url }}{% else %}../../../static/images/67527a5b36657f93c6bb3b2b_review-01.avif{% endif %}" loading="eager" alt="{{ review.reviewer_name }}" class="review-image" />
                                                    <div class="reviewer-name-wrap">
                                                        <h4 class="reviewer-name">
                                                            {{ review.reviewer_name }}
                                                        </h4>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    {% endfor %}
                                {% else %}
                                    <div class="review-slide w-slide">
                                        <div class="review-slide-item">
                                            <p>No reviews yet for this vehicle.</p>
                                        </div>
                                    </div>
                                {% endif %}
                            </div>"""

content = re.sub(
    r'<div class="review-mask w-slider-mask">.*?</div>\s*<div class="review-left-arrow w-slider-arrow-left">',
    review_loop + '\n                            <div class="review-left-arrow w-slider-arrow-left">',
    content,
    flags=re.DOTALL
)

# Recent Cars
recent_car_loop = """                <div role="list" class="grid-car w-dyn-items">
                    {% if recent_vehicles %}
                        {% for vehicle in recent_vehicles %}
                        <div role="listitem" class="w-dyn-item">
                            <a data-w-id="b10814b3-e4a9-a641-b9bd-557884d8422e" href="{% url 'car_detail' vehicle.slug %}" class="car-item w-inline-block">
                                <div class="car-image-wrap">
                                    <img src="{% if vehicle.main_image %}{{ vehicle.main_image.url }}{% else %}../../../static/images/675d247c699d5c8508c0ae11_car-02.avif{% endif %}" loading="eager" alt="{{ vehicle.name }}" class="car-image" />
                                </div>
                                <div>
                                    <div class="car-title-wrap">
                                        <h3 class="car-title">
                                            {{ vehicle.name }}
                                        </h3>
                                        <div class="car-price-wrap">
                                            <div class="car-rent-price">
                                                ${{ vehicle.price_per_day }}
                                            </div>
                                            <div class="car-rent-text">
                                                /Per day
                                            </div>
                                        </div>
                                    </div>
                                    <div class="car-divider"></div>
                                    <div class="grid-car-meta">
                                        <div class="car-meta-item">
                                            <img src="../../../static/images/6750396b4ddf4c46d50f6cc4_car-seat.svg" loading="eager" alt="" class="car-meta-icon" />
                                            <div>
                                                <div class="text-small">Seat</div>
                                                <div class="car-meta-value">{{ vehicle.seats }}</div>
                                            </div>
                                        </div>
                                        <div class="car-meta-item">
                                            <img src="../../../static/images/6750396bcc42b344a21c720d_gearbox.svg" loading="eager" alt="" class="car-meta-icon" />
                                            <div>
                                                <div class="text-small">Gearbox</div>
                                                <div class="car-meta-value">{{ vehicle.transmission }}</div>
                                            </div>
                                        </div>
                                        <div class="car-meta-item">
                                            <img src="../../../static/images/6750396bef54164e709fd920_luggage.svg" loading="eager" alt="" class="car-meta-icon" />
                                            <div>
                                                <div class="text-small">Luggage</div>
                                                <div class="car-meta-value">{{ vehicle.luggage }}</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </a>
                        </div>
                        {% endfor %}
                    {% else %}
                        {% include "skeletons/vehicle_card_skeleton.html" %}
                    {% endif %}
                </div>"""

content = re.sub(
    r'<div role="list" class="grid-car w-dyn-items">.*?</div>\s*</div>\s*</div>\s*</section>',
    recent_car_loop + '\n            </div>\n        </div>\n    </section>',
    content,
    flags=re.DOTALL
)

with open('/Users/mac/Desktop/ryder-pro/template-1/pages/cars/car-details/index.html', 'w') as f:
    f.write(content)

print("Car Details page processed")
