filepath = '/Users/mac/Desktop/ryder-pro/template-1/pages/utilities/link-in-bio/index.html'

with open(filepath, 'r') as f:
    content = f.read()

content = content.replace("\\'", "'")

with open(filepath, 'w') as f:
    f.write(content)
print("Fixed escaped quotes in link-in-bio")
