import os

filepath = '/Users/mac/Desktop/ryder-pro/template-1/static/css/vendor/carent-wbs.webflow.shared.15fbda294.css'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Update variables
content = content.replace(
    '--color--primary-1: #fdde35;', 
    '--color--primary-1: #d31122;\n  --color--primary-dark: #9b0000;'
)

# 2. Update .button text color (black -> white)
# Originally:
# .button {
#   border-radius: var(--border-radius--button);
#   background-color: var(--color--primary-1);
#   font-family: var(--font-family--body);
#   color: var(--color--black);
content = content.replace(
    '.button {\n  border-radius: var(--border-radius--button);\n  background-color: var(--color--primary-1);\n  font-family: var(--font-family--body);\n  color: var(--color--black);',
    '.button {\n  border-radius: var(--border-radius--button);\n  background-color: var(--color--primary-1);\n  font-family: var(--font-family--body);\n  color: var(--color--white);'
)

# 3. Update .button:hover
# Originally:
# .button:hover {
#   background-color: var(--color--black);
#   color: var(--color--primary-1);
# }
content = content.replace(
    '.button:hover {\n  background-color: var(--color--black);\n  color: var(--color--primary-1);\n}',
    '.button:hover {\n  background-color: var(--color--primary-dark);\n  color: var(--color--white);\n}'
)

# 4. Update .button variant (black button -> red text on hover?)
# .button:hover:where(.w-variant-c8816823-2458-226a-b871-09f799993209) {
#   background-color: var(--color--primary-1);
#   color: var(--color--black);
# }
content = content.replace(
    '.button:hover:where(.w-variant-c8816823-2458-226a-b871-09f799993209) {\n  background-color: var(--color--primary-1);\n  color: var(--color--black);\n}',
    '.button:hover:where(.w-variant-c8816823-2458-226a-b871-09f799993209) {\n  background-color: var(--color--primary-1);\n  color: var(--color--white);\n}'
)

# 5. Update .button variant (gray button -> red text on hover?)
# .button:hover:where(.w-variant-7bd8a981-91cf-b486-f91f-90f7289c6dc8) {
#   background-color: var(--color--black);
#   color: var(--color--primary-1);
# }
# For gray button, hover can still be black with red text. That's fine.

# 6. Update .text-mark
# .text-mark {
#   background-color: var(--color--primary-1);
#   color: var(--color--black);
content = content.replace(
    '.text-mark {\n  background-color: var(--color--primary-1);\n  color: var(--color--black);',
    '.text-mark {\n  background-color: var(--color--primary-1);\n  color: var(--color--white);'
)

# 7. Update button-icon background hover
# .button-icon-hover-icon {
#   background-color: var(--color--black);
# }
# .button-icon:hover .button-icon-hover-icon {
#   background-color: var(--color--primary-1);
content = content.replace(
    '.button-icon-hover-icon {\n  background-color: var(--color--black);\n}',
    '.button-icon-hover-icon {\n  background-color: var(--color--primary-1);\n}'
)
content = content.replace(
    '.button-icon:hover .button-icon-hover-icon {\n  background-color: var(--color--primary-1);',
    '.button-icon:hover .button-icon-hover-icon {\n  background-color: var(--color--primary-dark);'
)

with open(filepath, 'w') as f:
    f.write(content)

print("Updated CSS color theme to Red/White.")
