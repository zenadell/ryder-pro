import os
import shutil

mapping = {
    "about.html": "pages/about/index.html",
    "contact.html": "pages/contact/index.html",
    "fqa.html": "pages/faq/index.html",
    "home.html": "pages/home/index.html",
    "privacy.html": "pages/privacy/index.html",
    "terms-condition.html": "pages/terms/index.html",
    "blog/blog.html": "pages/blog/index.html",
    "blog/blog-page.html": "pages/blog/blog-page/index.html",
    "cars/all-car-page.html": "pages/cars/all-cars/index.html",
    "cars/car-details-page/car-1.html": "pages/cars/car-details/index.html",
    "cars/adventure-cars.html": "pages/cars/adventure/index.html",
    "cars/business-cars.html": "pages/cars/business/index.html",
    "cars/famliy-cars.html": "pages/cars/family/index.html",
    "cars/wedding-cars.html": "pages/cars/wedding/index.html",
    "../coming-soon.html": "pages/utilities/coming-soon/index.html",
    "../error-404.html": "pages/utilities/404/index.html",
    "../protect-pass-401.html": "pages/utilities/access/index.html"
}

base_dir = "/Users/mac/Desktop/ryder-pro/template-1"

for src, dest in mapping.items():
    src_path = os.path.join(base_dir, src)
    dest_path = os.path.join(base_dir, dest)
    
    if os.path.exists(src_path):
        # Read the HTML, add references, and write to dest
        with open(src_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Calculate relative path to shared folder
        depth = dest.count('/') - 1
        rel_prefix = '../' * depth
        
        css_ref = f'<link rel="stylesheet" href="{rel_prefix}shared/base.css">'
        page_css_ref = '<link rel="stylesheet" href="style.css">'
        js_ref = f'<script src="{rel_prefix}shared/base.js"></script>'
        page_js_ref = '<script src="script.js"></script>'
        
        # Insert before </head>
        content = content.replace('</head>', f'{css_ref}\n    {page_css_ref}\n</head>')
        
        # Insert before </body>
        content = content.replace('</body>', f'{js_ref}\n    {page_js_ref}\n</body>')
        
        # Ensure destination dir exists
        os.makedirs(os.path.dirname(dest_path), exist_ok=True)
        
        with open(dest_path, 'w', encoding='utf-8') as f:
            f.write(content)
            
        print(f"Copied {src} -> {dest}")
        
        # Remove original source file
        os.remove(src_path)
    else:
        print(f"File not found: {src_path}")
