import re

with open('/Users/mac/Desktop/ryder-pro/template-1/pages/cars/all-cars/index.html', 'r') as f:
    content = f.read()

# 1. Update Hero Title
content = re.sub(
    r'<h1 class="car-hero-title">\s*Cars\s*</h1>',
    r'<h1 class="car-hero-title">\n                    {{ site_content.cars_hero_title|default:"Cars" }}\n                </h1>',
    content
)

# 2. Update Categories Loop
category_loop = """                        {% if categories %}
                            {% for category in categories %}
                            <div role="listitem" class="w-dyn-item">
                                <a aria-label="link" href="?category={{ category.slug }}" class="car-rental-link w-inline-block {% if current_category == category.slug %}w--current{% endif %}">
                                    <div>{{ category.name }}</div>
                                </a>
                            </div>
                            {% endfor %}
                        {% else %}
                            <div role="listitem" class="w-dyn-item"><a href="#" class="car-rental-link w-inline-block"><div>Business</div></a></div>
                            <div role="listitem" class="w-dyn-item"><a href="#" class="car-rental-link w-inline-block"><div>Family</div></a></div>
                        {% endif %}"""

content = re.sub(
    r'<div role="list" class="car-rental-list w-dyn-items">.*?</div>\s*</div>\s*</div>',
    r'<div role="list" class="car-rental-list w-dyn-items">\n' + category_loop + '\n                        </div>\n                    </div>',
    content,
    flags=re.DOTALL
)

# 3. Update Car Grid Loop
vehicle_loop = """                {% if vehicles %}
                    {% for vehicle in vehicles %}
                    <div data-w-id="6e09673c-58af-3608-4c1d-c0a0989ce47c" style="opacity:0" role="listitem" class="w-dyn-item">
                        <a aria-label="Link" data-w-id="6e09673c-58af-3608-4c1d-c0a0989ce47d" href="{% url 'car_detail' vehicle.slug %}" class="car-item w-inline-block">
                            <div class="car-image-wrap">
                                <img src="{% if vehicle.main_image %}{{ vehicle.main_image.url }}{% else %}../../../static/images/675d246a08777aecdb41d97f_car-01.avif{% endif %}" loading="eager" alt="{{ vehicle.name }}" class="car-image" />
                            </div>
                            <div>
                                <div class="car-title-wrap">
                                    <h2 class="car-title">
                                        {{ vehicle.name }}
                                    </h2>
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
                    {% include "skeletons/vehicle_card_skeleton.html" %}
                    {% include "skeletons/vehicle_card_skeleton.html" %}
                {% endif %}"""

content = re.sub(
    r'<div role="list" class="grid-car w-dyn-items">.*?</div>\s*</div>\s*</div>\s*</section>',
    r'<div role="list" class="grid-car w-dyn-items">\n' + vehicle_loop + '\n                </div>\n            </div>\n        </div>\n    </section>',
    content,
    flags=re.DOTALL
)

with open('/Users/mac/Desktop/ryder-pro/template-1/pages/cars/all-cars/index.html', 'w') as f:
    f.write(content)

print("All Cars page processed")
