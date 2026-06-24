import os

path = "/Users/mac/Desktop/ryder-pro/template-1/pages/dashboard/index.html"
with open(path, "r") as f:
    content = f.read()

# Replace hardcoded white with text-main where applicable
content = content.replace("rgba(255,255,255,", "rgba(0,0,0,")
content = content.replace("color: white;", "color: #ffffff;") # except for active buttons which stay white

# The search bar had color: white
content = content.replace("color: #ffffff;\n            outline: none;", "color: var(--text-main);\n            outline: none;")
# brand color
content = content.replace("color: #ffffff;\n            text-decoration: none;", "color: var(--text-main);\n            text-decoration: none;")
# nav-item hover color
content = content.replace("background-color: rgba(0,0,0,0.05);\n            color: #ffffff;", "background-color: rgba(0,0,0,0.05);\n            color: var(--text-main);")

# Update shadows to be lighter
content = content.replace("box-shadow: 0 10px 30px rgba(0,0,0,0.2);", "box-shadow: 0 10px 30px rgba(0,0,0,0.05);")
content = content.replace("box-shadow: 0 4px 15px rgba(124, 58, 237, 0.3);", "box-shadow: 0 4px 15px rgba(204, 0, 0, 0.3);")

with open(path, "w") as f:
    f.write(content)
