import os
import re
import urllib.request
import urllib.parse
from pathlib import Path

# Paths
base_dir = Path("/Users/mac/Desktop/ryder-pro/template-1")
pages_dir = base_dir / "pages"
shared_dir = base_dir / "shared"
static_dir = base_dir / "static"

css_dir = static_dir / "css" / "vendor"
js_dir = static_dir / "js" / "vendor"
img_dir = static_dir / "images"
fonts_dir = static_dir / "fonts"

for d in [css_dir, js_dir, img_dir, fonts_dir]:
    d.mkdir(parents=True, exist_ok=True)

# URL Pattern
url_pattern = re.compile(r'https://(?:cdn\.prod\.website-files\.com|d3e54v103j8qbb\.cloudfront\.net)/[^\s"\'\)]+')

# User agent to ensure we get woff2 for fonts
req_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

download_cache = {}

def get_target_dir_and_name(url):
    parsed = urllib.parse.urlparse(url)
    path = parsed.path
    filename = os.path.basename(path)
    
    # Handle query strings in filename
    if '?' in filename:
        filename = filename.split('?')[0]
        
    ext = os.path.splitext(filename)[1].lower()
    
    if ext == '.css':
        return css_dir, filename
    elif ext == '.js':
        return js_dir, filename
    elif ext in ['.woff', '.woff2', '.ttf', '.eot']:
        return fonts_dir, filename
    else:
        # Default to images for everything else (svg, png, jpg, avif, etc.)
        return img_dir, filename

def download_file(url):
    if url in download_cache:
        return download_cache[url]
        
    target_dir, filename = get_target_dir_and_name(url)
    target_path = target_dir / filename
    
    # Ensure unique filename if collision occurs (but ideally keep it simple)
    if not target_path.exists():
        try:
            print(f"Downloading: {url}")
            req = urllib.request.Request(url, headers=req_headers)
            with urllib.request.urlopen(req) as response, open(target_path, 'wb') as out_file:
                out_file.write(response.read())
        except Exception as e:
            print(f"Failed to download {url}: {e}")
            
    # Compute relative path from base_dir/static
    rel_path_from_static = target_path.relative_to(static_dir)
    download_cache[url] = str(rel_path_from_static).replace('\\', '/')
    return download_cache[url]

def process_css_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        urls = url_pattern.findall(content)
        modified = False
        
        for url in set(urls):
            rel_path = download_file(url)
            # In CSS (static/css/vendor), relative path to other static files is ../../[rel_path]
            # Actually, if rel_path is like images/img.svg, relative from css/vendor is ../../images/img.svg
            css_rel_path = "../../" + rel_path
            content = content.replace(url, css_rel_path)
            modified = True
            
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
    except Exception as e:
        print(f"Error processing CSS {filepath}: {e}")

def process_html_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 1. Download fonts
        if "fonts.googleapis.com" in content or "WebFont.load" in content:
            # Strip google fonts tags
            content = re.sub(r'<link[^>]+fonts\.googleapis\.com[^>]+>', '', content)
            content = re.sub(r'<link[^>]+fonts\.gstatic\.com[^>]+>', '', content)
            content = re.sub(r'<script[^>]+webfont\.js[^>]+>\s*</script>', '', content)
            content = re.sub(r'<script[^>]*>\s*WebFont\.load[^<]+</script>', '', content)
            
            # Inject our local font css
            depth = len(filepath.relative_to(base_dir).parts) - 1
            rel_prefix = "../" * depth
            font_link = f'<link rel="stylesheet" href="{rel_prefix}static/css/vendor/fonts.css">'
            content = content.replace('</head>', f'    {font_link}\n</head>')
        
        # 2. Find and replace all external URLs
        urls = url_pattern.findall(content)
        modified = False
        
        for url in set(urls):
            rel_path = download_file(url)
            depth = len(filepath.relative_to(base_dir).parts) - 1
            rel_prefix = "../" * depth
            html_rel_path = rel_prefix + "static/" + rel_path
            content = content.replace(url, html_rel_path)
            modified = True
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
    except Exception as e:
        print(f"Error processing HTML {filepath}: {e}")

# Main execution
# 1. Process all HTML files
for path in pages_dir.rglob("*.html"):
    process_html_file(path)

# 2. Process all downloaded CSS files (to catch url() inside them)
for path in css_dir.rglob("*.css"):
    process_css_file(path)

# 3. Handle Google Fonts (Instrument Sans) manually
fonts_css_path = css_dir / "fonts.css"
if not fonts_css_path.exists():
    try:
        print("Downloading Instrument Sans font...")
        font_url = "https://fonts.googleapis.com/css2?family=Instrument+Sans:wght@300;400;500;600;700&display=swap"
        req = urllib.request.Request(font_url, headers=req_headers)
        with urllib.request.urlopen(req) as response:
            font_css = response.read().decode('utf-8')
            
        # Parse font URLs, download them, replace in CSS
        font_urls = re.findall(r'url\((https://[^)]+)\)', font_css)
        for furl in set(font_urls):
            rel_path = download_file(furl) # Will go to static/fonts/
            css_rel_path = "../../" + rel_path
            font_css = font_css.replace(furl, css_rel_path)
            
        with open(fonts_css_path, 'w', encoding='utf-8') as f:
            f.write(font_css)
    except Exception as e:
        print(f"Error handling fonts: {e}")

print("Phase 2 Download Script Completed.")
