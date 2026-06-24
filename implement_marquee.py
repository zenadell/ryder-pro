import re

file_path = "template-1/pages/home/index.html"
with open(file_path, "r") as f:
    content = f.read()

# New CSS for Marquee
new_css = """
/* Dual-Layer JS Marquee Redesign */
.marquee-global-wrapper {
    position: relative;
    width: 100vw;
    margin-left: calc(-50vw + 50%); /* break out of container to go full width */
    overflow: hidden;
    padding: 20px 0;
    display: flex;
    flex-direction: column;
    gap: 32px; /* Perfect space between the two tracks */
}

.marquee-track-container {
    width: 100%;
    overflow: hidden;
    position: relative;
    /* Hide scrollbar */
    -ms-overflow-style: none;
    scrollbar-width: none;
}
.marquee-track-container::-webkit-scrollbar {
    display: none;
}

.marquee-track {
    display: flex;
    gap: 32px; /* Perfect space between cards */
    width: max-content;
    will-change: transform;
}

/* Ensure review items look consistent in the row */
.marquee-track .review-item {
    width: 400px;
    flex-shrink: 0;
    background: #ffffff;
    border-radius: 24px;
    padding: 32px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    border: 1px solid rgba(0,0,0,0.05);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}
"""

new_js = """
<!-- JS Marquee Engine -->
<script>
document.addEventListener("DOMContentLoaded", () => {
    const tracks = document.querySelectorAll('.marquee-track');
    if (!tracks.length) return;
    
    // We expect two tracks: index 0 (Top/Left), index 1 (Bottom/Right)
    const baseSpeed = 1.5;
    const slowSpeed = 0.2; // Incredibly low speed on hover
    
    tracks.forEach((track, index) => {
        // Clone items so we have enough to scroll infinitely
        const items = Array.from(track.children);
        if (items.length === 0) return;
        
        // Clone the array 4 times to ensure we have a massive long list
        for(let i=0; i<4; i++) {
            items.forEach(item => {
                const clone = item.cloneNode(true);
                track.appendChild(clone);
            });
        }
        
        let speedMult = 1.0;
        let currentX = 0;
        // Top track goes left (-1), Bottom track goes right (+1)
        let direction = index === 0 ? -1 : 1;
        
        // Setup Hover Listeners
        track.addEventListener('mouseenter', () => speedMult = slowSpeed);
        track.addEventListener('mouseleave', () => speedMult = 1.0);
        
        // For right-moving track, we need to start translated left so we don't see empty space
        if (direction === 1) {
            currentX = -(track.scrollWidth / 2);
        }
        
        function tick() {
            // Calculate movement
            currentX += (baseSpeed * speedMult * direction);
            
            // Loop condition
            // If moving left (direction = -1) and we scrolled exactly half the content
            if (direction === -1 && Math.abs(currentX) >= track.scrollWidth / 2) {
                currentX = 0;
            }
            // If moving right (direction = 1) and currentX reaches 0
            if (direction === 1 && currentX >= 0) {
                currentX = -(track.scrollWidth / 2);
            }
            
            track.style.transform = `translateX(${currentX}px)`;
            requestAnimationFrame(tick);
        }
        
        // Kick off loop
        requestAnimationFrame(tick);
    });
});
</script>
"""

# Inject CSS and JS
content = content.replace('</style>', new_css + '\n</style>')
content = content.replace('</body>', new_js + '\n</body>')

# Replace the grid-review block
# We need to extract the inner loop
loop_match = re.search(r'({%\s*if reviews\s*%}.*?{%\s*endif\s*%})', content, re.DOTALL)
if loop_match:
    inner_loop = loop_match.group(1)
    
    # We will wrap it in two track containers
    new_html = f"""
            <div class="marquee-global-wrapper">
                <div class="marquee-track-container">
                    <div class="marquee-track" id="marquee-top">
                        {inner_loop}
                    </div>
                </div>
                <div class="marquee-track-container" dir="ltr">
                    <div class="marquee-track" id="marquee-bottom">
                        {inner_loop}
                    </div>
                </div>
            </div>
    """
    
    # Find <div class="grid-review"> and replace it until its closing div
    # Since regex is tricky with nested divs, I'll use a precise replace
    # The grid-review ends right before </div>\n        </div>\n    </section>\n    <section class="counter-section
    pattern = re.compile(r'<div class="grid-review">.*?{% endif %}\s*</div>', re.DOTALL)
    content = pattern.sub(new_html, content)
    
    with open(file_path, "w") as f:
        f.write(content)
    print("Marquee injected")
else:
    print("Could not find reviews loop")

