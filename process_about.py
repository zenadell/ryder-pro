import re

with open('/Users/mac/Desktop/ryder-pro/template-1/pages/about/index.html', 'r') as f:
    content = f.read()

# 1. Hero Section
content = re.sub(
    r'<h1([^>]*)>\s*Who we are\s*</h1>',
    r'<h1\1>\n                    {{ site_content.about_hero_title|default:"Who we are" }}\n                </h1>',
    content
)
content = re.sub(
    r'<p([^>]*)>\s*Founded with a passion for making city travel easy and accessible[^<]*</p>',
    r'<p\1>\n                    {{ site_content.about_hero_desc|default:"Founded with a passion for making city travel easy and accessible, we have grown to become a trusted car rental service in the area. Our mission is to provide seamless and affordable transportation options for every occasion, from daily commutes to special events. With a fleet of diverse, well-maintained vehicles and a commitment to customer satisfaction, we strive to make every rental experience smooth and stress-free." }}\n                </p>',
    content
)

# Replace counter values
content = re.sub(
    r'<h2 class="heading-h1">\s*15\+\s*</h2>\s*<div>\s*Happy customers who have trusted us\s*</div>',
    r'<h2 class="heading-h1">\n                        {{ site_content.about_stat_1_value|default:"15+" }}\n                    </h2>\n                    <div>\n                        {{ site_content.about_stat_1_label|default:"Years of Experience" }}\n                    </div>',
    content
)
content = re.sub(
    r'<h2 class="heading-h1">\s*99%\s*</h2>\s*<div>\s*Our customers agree with our offer value\s*</div>',
    r'<h2 class="heading-h1">\n                        {{ site_content.about_stat_2_value|default:"99%" }}\n                    </h2>\n                    <div>\n                        {{ site_content.about_stat_2_label|default:"Customer Satisfaction" }}\n                    </div>',
    content
)
content = re.sub(
    r'<h2 class="heading-h1">\s*5,000\+\s*</h2>\s*<div>\s*Trusted by thousands of satisfied clients\s*</div>',
    r'<h2 class="heading-h1">\n                        {{ site_content.about_stat_3_value|default:"5,000+" }}\n                    </h2>\n                    <div>\n                        {{ site_content.about_stat_3_label|default:"Vehicles Available" }}\n                    </div>',
    content
)
content = re.sub(
    r'<h2 class="heading-h1">\s*24/7\s*</h2>\s*<div>\s*Our dedicated support team is available\s*</div>',
    r'<h2 class="heading-h1">\n                        {{ site_content.about_stat_4_value|default:"24/7" }}\n                    </h2>\n                    <div>\n                        {{ site_content.about_stat_4_label|default:"Customer Support" }}\n                    </div>',
    content
)

# 2. About Image
content = re.sub(
    r'<img src="../../static/images/67529bc6c0fcb65bc955d353_about-01.avif"\s*loading="eager" data-w-id="aed80a0d-6104-2281-7168-34d93de2791d" alt="About Image"\s*class="about-image" />',
    r'<img src="{% if site_content.about_hero_image %}{{ site_content.about_hero_image.url }}{% else %}../../static/images/67529bc6c0fcb65bc955d353_about-01.avif{% endif %}"\n                loading="eager" data-w-id="aed80a0d-6104-2281-7168-34d93de2791d" alt="About Image"\n                class="about-image" />',
    content
)

# 3. Mission Section
content = re.sub(
    r'<h2 class="mission-title">\s*Our mission\s*</h2>\s*<p>\s*Our mission is to provide exceptional car rental services[^<]*</p>',
    r'<h2 class="mission-title">\n                        {{ site_content.about_mission_title|default:"Our mission" }}\n                    </h2>\n                    <p>\n                        {{ site_content.about_mission_desc|default:"Our mission is to provide exceptional car rental services that make urban travel easy, affordable, and enjoyable. We aim to create a seamless experience by offering a diverse fleet of vehicles, flexible rental options, and outstanding customer support. We are committed to being your trusted partner in city travel, ensuring every journey is smooth, convenient, and tailored to your needs." }}\n                    </p>',
    content
)
content = re.sub(
    r'<h2 class="mission-title">\s*Our values\s*</h2>\s*<ul role="list" class="value-list">',
    r'<h2 class="mission-title">\n                        {{ site_content.about_values_title|default:"Our values" }}\n                    </h2>\n                    <ul role="list" class="value-list">',
    content
)
# For values, we can just replace the whole list items since they are static
values_replacement = """                        <li class="value-list-item">
                            <span class="value-list-title"> {{ site_content.about_value_1_title|default:"Customer Focus:" }} </span>
                            {{ site_content.about_value_1_desc|default:"We put our customers at the heart of everything we do. Your satisfaction is our top priority." }}
                        </li>
                        <li class="value-list-item">
                            <span class="value-list-title"> {{ site_content.about_value_2_title|default:"Integrity:" }} </span>
                            {{ site_content.about_value_2_desc|default:"Honesty and transparency are the cornerstones of our business. No hidden fees." }}
                        </li>
                        <li class="value-list-item">
                            <span class="value-list-title"> {{ site_content.about_value_3_title|default:"Reliability:" }} </span>
                            {{ site_content.about_value_3_desc|default:"Our customers rely on us for safe and dependable transportation." }}
                        </li>"""

content = re.sub(
    r'<li class="value-list-item">\s*<span class="value-list-title"> Customer Focus:\s*</span>.*?</li>.*?<li class="value-list-item">\s*<span class="value-list-title"> Sustainability:\s*</span>.*?</li>',
    values_replacement,
    content,
    flags=re.DOTALL
)

# 4. Team Section
# We'll replace the inside of .w-dyn-items
team_loop = """                    {% if team_members %}
                        {% for member in team_members %}
                        <div data-w-id="496ef019-b04a-5fe5-0885-84700206979b" style="opacity:0" role="listitem" class="w-dyn-item">
                            <div data-w-id="5bc9e42f-63c2-a2bf-fe01-41bd3186389c" class="team-item">
                                <div class="team-image-wrapper">
                                    <div class="team-image-wrap w-inline-block">
                                        <img src="{% if member.image %}{{ member.image.url }}{% else %}../../static/images/6756d26dcda3411ebd097aa0_team-01.avif{% endif %}" loading="eager" alt="{{ member.name }}" class="team-image" />
                                    </div>
                                    <div data-w-id="f8e2740a-05cc-a196-ac90-200c956878d2" class="team-social-wrapper">
                                        <div class="team-black-overlay w-inline-block"></div>
                                        <div class="social-icon-wrap">
                                            {% if member.facebook_link %}
                                            <a href="{{ member.facebook_link }}" target="_blank" class="social-link w-inline-block"> <img src="../../static/images/674ef43c2f257b9d04bb0dbc_facebook.svg" loading="eager" alt="" class="social-icon" /> </a>
                                            {% endif %}
                                            {% if member.linkedin_link %}
                                            <a href="{{ member.linkedin_link }}" target="_blank" class="social-link w-inline-block"> <img src="../../static/images/674ef43ceb71924c1a5c3383_linkedin.svg" loading="eager" alt="" class="social-icon" /> </a>
                                            {% endif %}
                                            {% if member.twitter_link %}
                                            <a href="{{ member.twitter_link }}" target="_blank" class="social-link w-inline-block"> <img src="../../static/images/674ef43c1e847fe6a19fcbd1_twitter-x.svg" loading="eager" width="20" alt="" class="social-icon" /> </a>
                                            {% endif %}
                                        </div>
                                    </div>
                                </div>
                                <div class="team-title-wrap w-inline-block">
                                    <h3 data-w-id="6ce298ab-5dca-493d-689d-600e20941533" class="team-title">
                                        {{ member.name }}
                                    </h3>
                                    <div>
                                        {{ member.role }}
                                    </div>
                                </div>
                            </div>
                        </div>
                        {% endfor %}
                    {% else %}
                        {% include "skeletons/team_skeleton.html" %}
                    {% endif %}"""

content = re.sub(
    r'<div role="list" class="grid-team w-dyn-items">.*?</div>\s*</div>\s*</div>\s*</section>',
    r'<div role="list" class="grid-team w-dyn-items">\n' + team_loop + '\n                    </div>\n                </div>\n            </div>\n        </section>',
    content,
    flags=re.DOTALL
)

with open('/Users/mac/Desktop/ryder-pro/template-1/pages/about/index.html', 'w') as f:
    f.write(content)

print("About page processed")
