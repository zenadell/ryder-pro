import re

with open('/Users/mac/Desktop/ryder-pro/template-1/pages/home/index.html', 'r') as f:
    content = f.read()

# Define the replacement template
replacement = """                            {% if vehicles %}
                                {% for vehicle in vehicles %}
                                <div class="car-slide w-slide">
                                    <div class="car-collection-list-wrapper w-dyn-list">
                                        <div role="list" class="car-collection-list w-dyn-items">
                                            <div role="listitem" class="car-collection-item w-dyn-item">
                                                <a data-w-id="b4e49330-e116-9446-b679-b13ab9f5db15"
                                                    href="{{ vehicle.get_absolute_url|default:'#' }}" class="car-item w-inline-block">
                                                    <div class="car-image-wrap">
                                                        <img src="{% if vehicle.primary_image %}{{ vehicle.primary_image.url }}{% else %}../../static/images/fallback.png{% endif %}"
                                                            loading="eager"
                                                            style="-webkit-transform:translate3d(0, 0, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-moz-transform:translate3d(0, 0, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-ms-transform:translate3d(0, 0, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);transform:translate3d(0, 0, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0)"
                                                            alt="{{ vehicle.name }}" class="car-image" />
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
                                                        <div class="car-divider">
                                                        </div>
                                                        <div class="grid-car-meta">
                                                            <div class="car-meta-item">
                                                                <img src="../../static/images/6750396b4ddf4c46d50f6cc4_car-seat.svg"
                                                                    loading="eager" alt="Seat" class="car-meta-icon" />
                                                                <div>
                                                                    <div class="text-small">
                                                                        Seat
                                                                    </div>
                                                                    <div class="car-meta-value">
                                                                        {{ vehicle.seats }}
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <div class="car-meta-item">
                                                                <img src="../../static/images/6750396bcc42b344a21c720d_gearbox.svg"
                                                                    loading="eager" alt="Gearbox" class="car-meta-icon" />
                                                                <div>
                                                                    <div class="text-small">
                                                                        Gearbox
                                                                    </div>
                                                                    <div class="car-meta-value">
                                                                        {{ vehicle.get_gearbox_display }}
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <div class="car-meta-item">
                                                                <img src="../../static/images/6750396bef54164e709fd920_luggage.svg"
                                                                    loading="eager" alt="Luggage" class="car-meta-icon" />
                                                                <div>
                                                                    <div class="text-small">
                                                                        Luggage
                                                                    </div>
                                                                    <div class="car-meta-value">
                                                                        {{ vehicle.luggage_capacity }} bags
                                                                    </div>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </a>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                {% endfor %}
                            {% else %}
                                {% include "skeletons/vehicle_card_skeleton.html" %}
                            {% endif %}
"""

# The start marker is the first car-slide div
start_marker = r'<div class="car-slide w-slide">\s*<div class="car-collection-list-wrapper w-dyn-list">'
# The end marker is right before the car-slider-arrow left
end_marker = r'</div>\s*<div class="car-slider-arrow w-slider-arrow-left">'

# Find start and end indices
start_match = re.search(start_marker, content)
end_match = re.search(end_marker, content)

if start_match and end_match:
    # We want to replace from start_match.start() to end_match.start()
    new_content = content[:start_match.start()] + replacement + content[end_match.start():]
    with open('/Users/mac/Desktop/ryder-pro/template-1/pages/home/index.html', 'w') as f:
        f.write(new_content)
    print("Success")
else:
    print("Failed to match")
    if not start_match: print("Start not found")
    if not end_match: print("End not found")
