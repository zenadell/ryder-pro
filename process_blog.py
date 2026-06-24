import re

with open('/Users/mac/Desktop/ryder-pro/template-1/pages/blog/index.html', 'r') as f:
    content = f.read()

# Hero title
content = re.sub(
    r'<h1 class="hero-inner-title">\s*Blog\s*</h1>',
    r'<h1 class="hero-inner-title">\n                    {{ site_content.blog_hero_title|default:"Blog" }}\n                </h1>',
    content
)

# Blog loop
blog_loop = """                    {% if posts %}
                        {% for post in posts %}
                        <div data-w-id="fdcfe016-9ab4-e8cc-dd2a-cf2b4285c068" style="opacity:0" role="listitem" class="w-dyn-item">
                            <a aria-label="link" data-w-id="bdaee6ef-901d-c4db-781c-96a966ae9542" href="{% url 'blog_detail' post.slug %}" class="blog-item w-inline-block">
                                <div class="blog-image-wrap">
                                    <img src="{% if post.featured_image %}{{ post.featured_image.url }}{% else %}../../static/images/6756d83824c7926c0721ffda_blog-01.avif{% endif %}" loading="eager" style="-webkit-transform:translate3d(0, 0, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-moz-transform:translate3d(0, 0, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-ms-transform:translate3d(0, 0, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);transform:translate3d(0, 0, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0)" alt="{{ post.title }}" class="blog-image" />
                                </div>
                                <div>
                                    <h2 class="blog-title">
                                        {{ post.title }}
                                    </h2>
                                    <div class="blog-date">
                                        {{ post.published_at|date:"F j, Y" }}
                                    </div>
                                </div>
                            </a>
                        </div>
                        {% endfor %}
                    {% else %}
                        {% include "skeletons/blog_skeleton.html" %}
                    {% endif %}"""

content = re.sub(
    r'<div role="list" class="grid-blog w-dyn-items">.*?</div>\s*</div>\s*</div>\s*</section>',
    r'<div role="list" class="grid-blog w-dyn-items">\n' + blog_loop + '\n                </div>\n            </div>\n        </div>\n    </section>',
    content,
    flags=re.DOTALL
)

with open('/Users/mac/Desktop/ryder-pro/template-1/pages/blog/index.html', 'w') as f:
    f.write(content)

print("Blog page processed")
