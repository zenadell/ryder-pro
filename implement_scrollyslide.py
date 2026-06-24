import re

file_path = "template-1/pages/home/index.html"
with open(file_path, "r") as f:
    content = f.read()

# CSS to inject
css_block = """
<style>
/* Premium Scrollyslide CSS */
.scroll-track-wrapper {
    height: 300vh; /* Adjust scrolling duration */
    view-timeline-name: --horizontal-scroll;
    view-timeline-axis: block;
    position: relative;
    background-color: var(--color--light-1);
    /* Color animation */
    animation: dark-bg linear both;
    animation-timeline: --horizontal-scroll;
    animation-range: contain 0% contain 20%;
}
@keyframes dark-bg {
    to { background-color: #121212; }
}

.scroll-track-sticky {
    position: sticky;
    top: 0;
    height: 100vh;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    justify-content: center;
}

.scroll-track-container {
    width: 100vw;
    margin-top: 40px;
    /* align the start of the slider with the container */
    padding-left: max(5vw, calc((100vw - 1200px) / 2));
}

.scroll-track {
    display: flex;
    gap: 40px;
    width: max-content;
    padding-right: 10vw; /* End padding */
    animation: move-track linear both;
    animation-timeline: --horizontal-scroll;
    animation-range: contain 0% contain 100%;
}
@keyframes move-track {
    to { transform: translateX(calc(-100% + 100vw)); }
}

.scroll-section-title {
    animation: text-light linear both;
    animation-timeline: --horizontal-scroll;
    animation-range: contain 0% contain 20%;
}
@keyframes text-light {
    to { color: #ffffff; }
}

/* Enhancing the cards to look premium on dark bg */
.scroll-track .car-item {
    width: 400px;
    background: #ffffff;
    border-radius: 20px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.1);
    transition: transform 0.4s ease, box-shadow 0.4s ease;
    flex-shrink: 0;
}
.scroll-track .car-item:hover {
    transform: translateY(-10px) scale(1.02);
    box-shadow: 0 30px 60px rgba(0,0,0,0.2);
}
</style>

<!-- Fallback JS for browsers without CSS animation-timeline -->
<script>
document.addEventListener("DOMContentLoaded", () => {
    if (!CSS.supports('animation-timeline: view()')) {
        const wrapper = document.querySelector('.scroll-track-wrapper');
        const track = document.querySelector('.scroll-track');
        const title = document.querySelector('.scroll-section-title');
        
        window.addEventListener('scroll', () => {
            const rect = wrapper.getBoundingClientRect();
            const top = rect.top;
            const height = rect.height;
            const windowHeight = window.innerHeight;
            
            // "contain" range means the sticky element is currently stuck
            // which happens when top <= 0 and top >= -(height - windowHeight)
            let progress = 0;
            if (top > 0) progress = 0;
            else if (top < -(height - windowHeight)) progress = 1;
            else progress = Math.abs(top) / (height - windowHeight);
            
            // Apply track translation manually
            track.style.transform = `translateX(calc(${progress} * (-100% + 100vw)))`;
            
            // Background color animation manual fallback
            if (progress > 0.2) {
                wrapper.style.backgroundColor = '#121212';
                if(title) title.style.color = '#ffffff';
            } else {
                const ratio = progress / 0.2; // 0 to 1
                const dark = Math.round(255 - (255 - 18) * ratio); // 18 is ~0x12
                wrapper.style.backgroundColor = `rgb(${dark}, ${dark}, ${dark})`;
                if(title) title.style.color = `rgb(${dark}, ${dark}, ${dark})`; // wait, from black to white
            }
        });
    }
});
</script>
"""

# Extract the old slider wrapper content between `<div class="car-slider-wrapper">` and `</section>`
# and replace it with the new scroll-driven structure.

match = re.search(r'(<div\s+data-w-id="ca0f153d-18d4-8385-4350-c9b265ca2633"\s*class="section-title section-title-wrap">.*?</h2>)', content, re.DOTALL)
if match:
    old_title_block = match.group(1)
    new_title_block = old_title_block.replace('<h2 class="no-margin-bottom">', '<h2 class="no-margin-bottom scroll-section-title">')
    content = content.replace(old_title_block, new_title_block)

old_section_pattern = re.compile(r'(<section class="car-section section-spacing-bottom">)(.*?)(<div\s+data-w-id="1e1243a6-cfcf-9982-185e-3e21c2156f38"\s*class="car-slider-wrapper">)(.*?)(</section>)', re.DOTALL)

# We need to extract the vehicle loop block.
loop_match = re.search(r'({%\s*if vehicles\s*%}.*?{%\s*endif\s*%})', content, re.DOTALL)
if loop_match:
    vehicle_loop_content = loop_match.group(1)
    # clean up the w-slide wrappers inside the vehicle loop
    vehicle_loop_content = vehicle_loop_content.replace('<div class="car-slide w-slide">', '')
    vehicle_loop_content = vehicle_loop_content.replace('<div class="car-collection-list-wrapper w-dyn-list">', '')
    vehicle_loop_content = vehicle_loop_content.replace('<div role="list" class="car-collection-list w-dyn-items">', '')
    vehicle_loop_content = vehicle_loop_content.replace('<div role="listitem" class="car-collection-item w-dyn-item">', '')
    
    # We need to remove the closing divs for those 4 wrappers, which are right after the </a>
    vehicle_loop_content = re.sub(r'</a>\s*</div>\s*</div>\s*</div>\s*</div>', '</a>', vehicle_loop_content)
    
    new_section_html = f"""
{css_block}
<section class="scroll-track-wrapper">
    <div class="scroll-track-sticky">
        <div class="w-layout-blockcontainer container w-container">
            <div data-w-id="ca0f153d-18d4-8385-4350-c9b265ca2633" class="section-title section-title-wrap">
                <h2 class="no-margin-bottom scroll-section-title">
                    Our rental car collection
                </h2>
                <a data-wf--button-icon--variant="base-button" data-w-id="9def5a63-20c2-3afd-c41c-34faed04ca6f" href="{{% url 'all_cars' %}}" class="button-icon w-inline-block">
                    <div class="button-icon-text-wrap">
                        <div class="button-text-wrap">
                            <div class="button-icon-text one">View all vehicles</div>
                            <div class="button-icon-text two">View all vehicles</div>
                        </div>
                    </div>
                    <div class="button-icon-square">
                        <img src="{{% static 'images/676682bf44c92e272152469e_arrow-01.svg' %}}" loading="eager" alt="" class="button-icon-image" />
                        <img src="{{% static 'images/676682bf44c92e272152469e_arrow-01.svg' %}}" loading="eager" alt="" class="button-icon-hover-icon" />
                    </div>
                </a>
            </div>
        </div>
        <div class="scroll-track-container">
            <div class="scroll-track">
                {vehicle_loop_content}
            </div>
        </div>
    </div>
</section>
"""

    content = old_section_pattern.sub(new_section_html, content)
    
    with open(file_path, "w") as f:
        f.write(content)
    print("Scrollyslide implemented")
else:
    print("Could not find vehicle loop")

