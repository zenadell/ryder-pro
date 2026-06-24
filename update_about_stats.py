import re

filepath = '/Users/mac/Desktop/ryder-pro/template-1/pages/about/index.html'

with open(filepath, 'r') as f:
    content = f.read()

# Replace the stats and their labels with if/else blocks for skeleton loaders
replacements = [
    (r'\{\{\s*site_content.about_stat_1_value\|default:"15\+"\s*\}\}', 
     '{% if site_content.about_stat_1_value %}{{ site_content.about_stat_1_value }}{% else %}<div class="skeleton-pulse" style="width:80px; height:60px; border-radius:8px; display:inline-block;"></div>{% endif %}'),
    (r'\{\{\s*site_content.about_stat_1_label\|default:"Years of Experience"\s*\}\}',
     '{% if site_content.about_stat_1_label %}{{ site_content.about_stat_1_label }}{% else %}<div class="skeleton-pulse" style="width:120px; height:20px; border-radius:4px; margin-top:8px;"></div>{% endif %}'),
    
    (r'\{\{\s*site_content.about_stat_2_value\|default:"99%"\s*\}\}', 
     '{% if site_content.about_stat_2_value %}{{ site_content.about_stat_2_value }}{% else %}<div class="skeleton-pulse" style="width:80px; height:60px; border-radius:8px; display:inline-block;"></div>{% endif %}'),
    (r'\{\{\s*site_content.about_stat_2_label\|default:"Customer Satisfaction"\s*\}\}',
     '{% if site_content.about_stat_2_label %}{{ site_content.about_stat_2_label }}{% else %}<div class="skeleton-pulse" style="width:120px; height:20px; border-radius:4px; margin-top:8px;"></div>{% endif %}'),
    
    (r'\{\{\s*site_content.about_stat_3_value\|default:"5,000\+"\s*\}\}', 
     '{% if site_content.about_stat_3_value %}{{ site_content.about_stat_3_value }}{% else %}<div class="skeleton-pulse" style="width:80px; height:60px; border-radius:8px; display:inline-block;"></div>{% endif %}'),
    (r'\{\{\s*site_content.about_stat_3_label\|default:"Vehicles Available"\s*\}\}',
     '{% if site_content.about_stat_3_label %}{{ site_content.about_stat_3_label }}{% else %}<div class="skeleton-pulse" style="width:120px; height:20px; border-radius:4px; margin-top:8px;"></div>{% endif %}'),
    
    (r'\{\{\s*site_content.about_stat_4_value\|default:"24/7"\s*\}\}', 
     '{% if site_content.about_stat_4_value %}{{ site_content.about_stat_4_value }}{% else %}<div class="skeleton-pulse" style="width:80px; height:60px; border-radius:8px; display:inline-block;"></div>{% endif %}'),
    (r'\{\{\s*site_content.about_stat_4_label\|default:"Customer Support"\s*\}\}',
     '{% if site_content.about_stat_4_label %}{{ site_content.about_stat_4_label }}{% else %}<div class="skeleton-pulse" style="width:120px; height:20px; border-radius:4px; margin-top:8px;"></div>{% endif %}'),
]

for pattern, replacement in replacements:
    content = re.sub(pattern, replacement, content)

with open(filepath, 'w') as f:
    f.write(content)

print("Updated about stats with skeletons!")
