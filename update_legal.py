import re

files = [
    "template-1/pages/privacy/index.html",
    "template-1/pages/terms/index.html"
]

for file_path in files:
    try:
        with open(file_path, "r") as f:
            content = f.read()
        
        # Replace common placeholders
        content = re.sub(r'Carent|Webestica|Your Company Name', 'Ryder Pro', content, flags=re.IGNORECASE)
        content = re.sub(r'carent\.com|webestica\.com', 'ryder-pro.com', content, flags=re.IGNORECASE)
        
        with open(file_path, "w") as f:
            f.write(content)
        print(f"Updated {file_path}")
    except Exception as e:
        print(f"Failed on {file_path}: {e}")

