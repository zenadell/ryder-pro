import re

with open('/Users/mac/Desktop/ryder-pro/template-1/pages/blog/blog-page/index.html', 'r') as f:
    content = f.read()

# Blog Header
content = re.sub(
    r'<div class="blog-badge">\s*December 9, 2024\s*</div>',
    r'<div class="blog-badge">\n                    {{ post.published_at|date:"F j, Y" }}\n                </div>',
    content
)

content = re.sub(
    r'<h1 class="blog-detail-title">\s*Team collaboration for growth\s*</h1>',
    r'<h1 class="blog-detail-title">\n                    {{ post.title }}\n                </h1>',
    content
)

content = re.sub(
    r'<p class="no-margin-bottom">\s*Find out how cross-team collaboration.*?growth goals.\s*</p>',
    r'<p class="no-margin-bottom">\n                    {{ post.excerpt }}\n                </p>',
    content,
    flags=re.DOTALL
)

# Blog Image
content = re.sub(
    r'<img src="../../../static/images/6756d8f6ae6b737e02c62f54_big-blog-05.avif"\s*loading="eager" alt="" class="blog-detail-image" />',
    r'<img src="{% if post.featured_image %}{{ post.featured_image.url }}{% else %}../../../static/images/6756d8f6ae6b737e02c62f54_big-blog-05.avif{% endif %}" loading="eager" alt="{{ post.title }}" class="blog-detail-image" />',
    content
)

# Blog Content
content = re.sub(
    r'<div class="blog-rich-text w-richtext">.*?</div>\s*</div>\s*</div>\s*</section>',
    r'<div class="blog-rich-text w-richtext">\n                    {{ post.content|safe }}\n                </div>\n            </div>\n        </div>\n    </section>',
    content,
    flags=re.DOTALL
)

# Recent Blogs
recent_blog_loop = """                <div role="list" class="grid-blog w-dyn-items">
                    {% if recent_posts %}
                        {% for recent in recent_posts %}
                        <div data-w-id="3f13b910-21e3-f1d5-c14a-3f2104d7846e" style="opacity:0" role="listitem" class="w-dyn-item">
                            <a aria-label="Link" data-w-id="3f13b910-21e3-f1d5-c14a-3f2104d7846f" href="{% url 'blog_detail' recent.slug %}" class="blog-item w-inline-block">
                                <div class="blog-image-wrap">
                                    <img src="{% if recent.featured_image %}{{ recent.featured_image.url }}{% else %}../../../static/images/6756d83824c7926c0721ffda_blog-01.avif{% endif %}" loading="eager" style="-webkit-transform:translate3d(0, 0, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-moz-transform:translate3d(0, 0, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);-ms-transform:translate3d(0, 0, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0);transform:translate3d(0, 0, 0) scale3d(1, 1, 1) rotateX(0) rotateY(0) rotateZ(0) skew(0, 0)" alt="{{ recent.title }}" class="blog-image" />
                                </div>
                                <div>
                                    <h2 class="blog-title">
                                        {{ recent.title }}
                                    </h2>
                                    <div class="blog-date">
                                        {{ recent.published_at|date:"F j, Y" }}
                                    </div>
                                </div>
                            </a>
                        </div>
                        {% endfor %}
                    {% else %}
                        {% include "skeletons/blog_skeleton.html" %}
                    {% endif %}
                </div>"""

content = re.sub(
    r'<div role="list" class="grid-blog w-dyn-items">.*?</div>\s*</div>\s*</div>\s*</section>',
    recent_blog_loop + '\n            </div>\n        </div>\n    </section>',
    content,
    flags=re.DOTALL
)

with open('/Users/mac/Desktop/ryder-pro/template-1/pages/blog/blog-page/index.html', 'w') as f:
    f.write(content)

print("Blog detail page processed")
