import re

file_path = "template-1/pages/home/index.html"
with open(file_path, "r") as f:
    content = f.read()

# New CSS block
new_css = """
/* Modern Card Redesign (Reference A Style) */
.scroll-track .car-item {
    width: 380px;
    background: #ffffff;
    border-radius: 36px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.1);
    transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease;
    flex-shrink: 0;
    display: flex;
    flex-direction: column;
    text-decoration: none;
    color: #111;
    padding: 8px; /* Inner border effect */
}
.scroll-track .car-item:hover {
    transform: translateY(-8px) scale(1.02);
    box-shadow: 0 30px 60px rgba(0,0,0,0.15);
}

.scroll-track .car-image-container {
    width: 100%;
    height: 320px;
    background: #f4f4f5; /* Soft modern gray backdrop */
    border-radius: 28px 28px 20px 20px;
    position: relative;
    overflow: hidden;
}

.scroll-track .car-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.6s cubic-bezier(0.25, 1, 0.5, 1);
}

.scroll-track .car-item:hover .car-image {
    transform: scale(1.05);
}

.scroll-track .car-floating-price {
    position: absolute;
    top: 16px;
    right: 16px;
    background: #ffffff;
    color: #121212;
    padding: 10px 18px;
    border-radius: 24px;
    font-weight: 800;
    font-size: 18px;
    box-shadow: 0 10px 20px rgba(0,0,0,0.08);
    z-index: 10;
}

.scroll-track .car-body-new {
    padding: 24px 16px 16px 16px;
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.scroll-track .car-body-top {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #f0f0f0;
    padding-bottom: 16px;
}

.scroll-track .car-title-new {
    font-size: 24px;
    font-weight: 700;
    color: #121212;
    margin: 0;
    letter-spacing: -0.5px;
}

.scroll-track .car-order-btn {
    font-size: 14px;
    font-weight: 600;
    color: #121212;
    text-transform: capitalize;
    display: flex;
    align-items: center;
    gap: 4px;
    transition: color 0.3s ease;
}

.scroll-track .car-item:hover .car-order-btn {
    color: #e60000;
}

.scroll-track .car-tags-row {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
}

.scroll-track .car-tag {
    background: #f4f4f5;
    padding: 8px 14px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 600;
    color: #666;
    text-transform: capitalize;
}
"""

# Replace old css blocks
content = re.sub(r'/\* Premium Card Redesign \*/.*?/\* Fallback JS', '/* Fallback JS', content, flags=re.DOTALL)
# Inject new css before </style>
content = content.replace('</style>', new_css + '\n</style>')

# Replace the HTML loop
new_loop = """{% for vehicle in vehicles %}
                        <a href="{{ vehicle.get_absolute_url|default:'#' }}" class="car-item w-inline-block">
                            <div class="car-image-container">
                                <div class="car-floating-price">
                                    ${{ vehicle.price_per_day }}
                                </div>
                                <img src="{% if vehicle.main_image %}{{ vehicle.main_image.url }}{% else %}data:image/gif;base64,R0lGODlhAQABAAD/ACwAAAAAAQABAAACADs={% endif %}"
                                    loading="eager"
                                    alt="{{ vehicle.name }}" class="car-image {% if not vehicle.main_image %}skeleton-pulse{% endif %}" />
                            </div>
                            <div class="car-body-new">
                                <div class="car-body-top">
                                    <h3 class="car-title-new">{{ vehicle.name }}</h3>
                                    <div class="car-order-btn">Order Now ↗</div>
                                </div>
                                <div class="car-tags-row">
                                    <div class="car-tag">{{ vehicle.seats }} Seats</div>
                                    <div class="car-tag">{{ vehicle.transmission|default:"Auto" }}</div>
                                    <div class="car-tag">{{ vehicle.luggage|default:"2 Bags" }}</div>
                                    <div class="car-tag">{{ vehicle.fuel_type|default:"Petrol" }}</div>
                                </div>
                            </div>
                        </a>
                    {% endfor %}"""

# Regex to find the old loop
loop_pattern = re.compile(r'{%\s*for vehicle in vehicles\s*%}.*?{%\s*endfor\s*%}', re.DOTALL)
content = loop_pattern.sub(new_loop, content)

with open(file_path, "w") as f:
    f.write(content)

print("Modern cards injected.")
