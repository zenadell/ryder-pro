import re

with open('/Users/mac/Desktop/ryder-pro/template-1/pages/home/index.html', 'r') as f:
    content = f.read()

replacement = """            <div class="grid-review">
                {% if reviews %}
                    {% for review in reviews %}
                    <div data-w-id="bbd7b119-9496-b88a-c62d-c82092719fcf" style="opacity:0" class="review-item">
                        <div class="review-content-wrap">
                            <div>
                                <img src="../../static/images/6752790ec11ba7f2aecb9bc9_rating.svg"
                                    loading="eager" alt="Rating" class="review-star-image" />
                                <div class="div-block">
                                    <p class="no-margin-bottom">
                                        {{ review.body }}
                                    </p>
                                </div>
                            </div>
                            <div class="review-name-wrap">
                                <img src="{% if review.author_image %}{{ review.author_image.url }}{% else %}../../static/images/67527a5b36657f93c6bb3b2b_review-01.avif{% endif %}"
                                    loading="eager" alt="{{ review.author_name }}" class="review-profile-image" />
                                <h3 class="review-profile-name">
                                    {{ review.author_name }}
                                </h3>
                            </div>
                        </div>
                    </div>
                    {% endfor %}
                {% else %}
                    {% include "skeletons/review_card_skeleton.html" %}
                {% endif %}
            </div>"""

grid_pattern = re.compile(r'<div class="grid-review">.*?</div>\s*</div>\s*</section>', re.DOTALL)

match = grid_pattern.search(content)
if match:
    new_content = content[:match.start()] + replacement + "\n        </div>\n    </section>" + content[match.end():]
    with open('/Users/mac/Desktop/ryder-pro/template-1/pages/home/index.html', 'w') as f:
        f.write(new_content)
    print("Success")
else:
    print("Failed to match grid_pattern")
