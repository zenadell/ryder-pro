import re

file_path = "template-1/pages/home/index.html"
with open(file_path, "r") as f:
    content = f.read()

# CSS to inject
new_css = """
/* Premium Card Redesign */
.scroll-track .car-item {
    width: 400px;
    background: #ffffff;
    border-radius: 24px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.15);
    transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease;
    flex-shrink: 0;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    text-decoration: none;
    color: #111;
    border: 1px solid rgba(0,0,0,0.05);
}
.scroll-track .car-item:hover {
    transform: translateY(-12px) scale(1.02);
    box-shadow: 0 30px 60px rgba(0,0,0,0.25);
}

.scroll-track .car-image-wrap {
    width: 100%;
    height: 225px; /* 16:9 ratio */
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden;
    background: #f0f0f0;
}

.scroll-track .car-image {
    width: 100% !important;
    height: 100% !important;
    object-fit: cover !important;
    transition: transform 0.6s cubic-bezier(0.25, 1, 0.5, 1);
}

.scroll-track .car-item:hover .car-image {
    transform: scale(1.08) !important;
}

.scroll-track .car-body {
    padding: 24px;
    display: flex;
    flex-direction: column;
    flex-grow: 1;
}

.scroll-track .car-title-wrap {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 20px;
    gap: 15px;
}

.scroll-track .car-title {
    font-size: 22px;
    font-weight: 800;
    margin: 0;
    line-height: 1.2;
    color: #121212;
    letter-spacing: -0.5px;
}

.scroll-track .car-price-wrap {
    text-align: right;
    flex-shrink: 0;
}

.scroll-track .car-rent-price {
    font-size: 22px;
    font-weight: 800;
    color: #e60000;
    line-height: 1;
}

.scroll-track .car-rent-text {
    font-size: 11px;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-top: 4px;
    font-weight: 600;
}

.scroll-track .car-divider {
    height: 1px;
    background: #f0f0f0;
    margin: 0 0 20px 0;
}

.scroll-track .grid-car-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.scroll-track .car-meta-item {
    display: flex;
    align-items: center;
    gap: 8px;
    background: #f8f8f8;
    padding: 8px 14px;
    border-radius: 12px;
    border: 1px solid #f0f0f0;
}

.scroll-track .car-meta-icon {
    width: 18px;
    height: 18px;
    opacity: 0.8;
}

.scroll-track .car-meta-value {
    font-size: 14px;
    font-weight: 700;
    color: #111;
}

.scroll-track .text-small {
    display: none !important;
}
"""

# Find the old CSS for cards and replace it, or just append the new CSS to the style block.
# I'll replace the `.scroll-track .car-item` definition with this new block.
old_css_pattern = re.compile(r'\.scroll-track \.car-item \{.*?\n\}', re.DOTALL)
content = old_css_pattern.sub("", content)

old_hover_pattern = re.compile(r'\.scroll-track \.car-item:hover \{.*?\n\}', re.DOTALL)
content = old_hover_pattern.sub("", content)

# Inject the new css right before </style>
content = content.replace("</style>", new_css + "\n</style>")

# Update the HTML to add `car-body` class
# The div immediately following `<div class="car-image-wrap">...</div>` needs to be `<div class="car-body">`
# We can do this with a targeted replace.
content = content.replace(
    '                            </div>\n                            <div>\n                                <div class="car-title-wrap">',
    '                            </div>\n                            <div class="car-body">\n                                <div class="car-title-wrap">'
)

with open(file_path, "w") as f:
    f.write(content)

print("Cards upgraded")
