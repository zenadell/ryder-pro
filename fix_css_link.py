import re

files_to_fix = [
    "template-1/pages/utilities/instructions/index.html",
    "template-1/pages/utilities/licenses/index.html",
    "template-1/pages/utilities/style-guide/index.html"
]

for filepath in files_to_fix:
    try:
        with open(filepath, "r") as f:
            content = f.read()
            
        content = content.replace(
            "Ryder Pro-wbs.webflow.shared.15fbda294.css", 
            "carent-wbs.webflow.shared.15fbda294.css"
        )
        content = content.replace(
            "ryder pro-wbs.webflow.shared", 
            "carent-wbs.webflow.shared"
        )
        
        with open(filepath, "w") as f:
            f.write(content)
        print(f"Fixed CSS link in {filepath}")
    except Exception as e:
        print(e)
        
