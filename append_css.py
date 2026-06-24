filepath = '/Users/mac/Desktop/ryder-pro/template-1/static/css/vendor/carent-wbs.webflow.shared.15fbda294.css'

css_to_add = """
.skeleton-pulse {
    background: #e2e8f0;
    background: linear-gradient(90deg, #e2e8f0 25%, #cbd5e1 50%, #e2e8f0 75%);
    background-size: 200% 100%;
    animation: skeleton-loading 1.5s infinite;
    border-radius: 4px;
}
@keyframes skeleton-loading {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}
"""

with open(filepath, 'r') as f:
    content = f.read()

if '.skeleton-pulse' not in content:
    with open(filepath, 'a') as f:
        f.write(css_to_add)
    print("Added .skeleton-pulse to CSS")
else:
    print(".skeleton-pulse already exists in CSS")
