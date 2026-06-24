import os
import re
from pathlib import Path

base_dir = Path("/Users/mac/Desktop/ryder-pro/template-1/pages")

def strip_identity(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 1. Remove Webflow comments
        content = re.sub(r'<!--\s*This site was created in Webflow[^>]*-->\n?', '', content)
        content = re.sub(r'<!--\s*Last Published:[^>]*-->\n?', '', content)

        # 2. Remove generator meta
        content = re.sub(r'<meta[^>]*content="Webflow"[^>]*name="generator"[^>]*>\n?', '', content)

        # 3. Remove data-wf-domain, data-wf-site, data-wf-page from html tag
        content = re.sub(r'\sdata-wf-domain="[^"]*"', '', content)
        content = re.sub(r'\sdata-wf-site="[^"]*"', '', content)
        content = re.sub(r'\sdata-wf-page="[^"]*"', '', content)

        # 4. Clean up <title> tags to remove Webflow template references
        content = re.sub(r'<title>(.*?)(?:-|\|)?\s*Webflow HTML website template</title>', r'<title>\1 | Ryder Pro</title>', content, flags=re.IGNORECASE)
        # Fix titles that ended up with just " | Ryder Pro" if group 1 was empty
        content = re.sub(r'<title>\s*\|\s*Ryder Pro</title>', r'<title>Ryder Pro</title>', content)
        
        # 5. Clean up og:title and twitter:title
        content = re.sub(r'content="([^"]*)(?:-|\|)?\s*Webflow HTML website template"', r'content="\1 | Ryder Pro"', content, flags=re.IGNORECASE)
        content = re.sub(r'content="\s*\|\s*Ryder Pro"', r'content="Ryder Pro"', content)

        # 6. Remove "Powered by Webflow" footer text
        content = re.sub(r',\s*Powered by\s*<a[^>]*href="https://webflow\.com/"[^>]*>\s*Webflow\s*</a>', '', content)

        # 7. Remove "More Templates" badge
        content = re.sub(r'<a[^>]*href="[^"]*webflow\.com/templates/[^"]*"[^>]*>.*?</a>', '', content, flags=re.DOTALL)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

for path in base_dir.rglob("*.html"):
    strip_identity(path)

print("Phase 3 Identity Stripping Completed.")
