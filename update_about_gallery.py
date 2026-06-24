import os

filepath = '/Users/mac/Desktop/ryder-pro/template-1/pages/about/index.html'
with open(filepath, 'r') as f:
    content = f.read()

import re

# We want to replace the inside of <div class="w-layout-grid grid-gallery"> ... </div>
pattern = re.compile(r'(<div class="w-layout-grid grid-gallery">)(.*?)(</section>)', re.DOTALL)

replacement = r'''\1
                {% if gallery_images %}
                <div class="gallery-image-left-side">
                    {% for image in gallery_images|slice:":2" %}
                    <a href="#" style="opacity:0" data-w-id="b81e162b-d0d3-a502-9d0f-81478d08bb2d" class="gallery-lightbox-link {% cycle 'one' 'two' %} w-inline-block w-lightbox">
                        <img src="{{ image.image.url }}" loading="lazy" alt="{{ image.caption }}" class="gallery-lightbox-image" />
                    </a>
                    {% endfor %}
                </div>
                
                {% for image in gallery_images|slice:"2:3" %}
                <a href="#" style="opacity:0" data-w-id="8d70bf70-f7ff-b8cd-fe63-8da0af65901d" class="gallery-lightbox-link three w-inline-block w-lightbox">
                    <img src="{{ image.image.url }}" loading="lazy" alt="{{ image.caption }}" class="gallery-lightbox-image" />
                </a>
                {% endfor %}

                <div id="w-node-f1faa3d6-3ba6-4a62-d414-b2f6c2f350db-ff55faf6" class="gallery-image-right-side">
                    {% for image in gallery_images|slice:"3:5" %}
                    <a href="#" style="opacity:0" data-w-id="f1faa3d6-3ba6-4a62-d414-b2f6c2f350dc" class="gallery-lightbox-link {% cycle 'four' 'five' %} w-inline-block w-lightbox">
                        <img src="{{ image.image.url }}" loading="lazy" alt="{{ image.caption }}" class="gallery-lightbox-image" />
                    </a>
                    {% endfor %}
                </div>
                {% else %}
                    <!-- Fallback if no gallery images -->
                    <p style="text-align: center; width: 100%;">No gallery images uploaded yet.</p>
                {% endif %}
            </div>
        </div>
    \3'''

new_content = pattern.sub(replacement, content)

if content == new_content:
    print("Warning: regex didn't match anything!")
else:
    with open(filepath, 'w') as f:
        f.write(new_content)
    print("Successfully replaced gallery section in about/index.html")
