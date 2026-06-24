import re

about_path = '/Users/mac/Desktop/ryder-pro/template-1/pages/about/index.html'
home_path = '/Users/mac/Desktop/ryder-pro/template-1/pages/home/index.html'

with open(about_path, 'r') as f:
    about_html = f.read()

# Extract Navbar
# The navbar starts at <div data-animation="default"... role="banner" class="navbar w-nav">
# and ends at the corresponding </div>. We can use a regex that looks for the start and ends before the next <section>
nav_match = re.search(r'(<div[^>]*role="banner" class="navbar w-nav">.*?)\n\s*<section', about_html, re.DOTALL)
if nav_match:
    about_nav = nav_match.group(1)
    
    # Update the active states for Home
    about_nav = about_nav.replace('href="/" class="nav-link w-nav-link"', 'href="/" aria-current="page" class="nav-link w-nav-link w--current"')
    about_nav = about_nav.replace('href="/about" aria-current="page" class="nav-link w-nav-link w--current"', 'href="/about" class="nav-link w-nav-link"')
    about_nav = about_nav.replace('href="/" class="dropdown-link w-dropdown-link"', 'href="/" aria-current="page" class="dropdown-link w-dropdown-link w--current"')
    about_nav = about_nav.replace('href="/about" aria-current="page"\n                                        class="dropdown-link w-dropdown-link w--current"', 'href="/about" class="dropdown-link w-dropdown-link"')
    about_nav = about_nav.replace('href="/about" aria-current="page"\n                                        class="dropdown-link w-dropdown-link w--current"', 'href="/about" class="dropdown-link w-dropdown-link"')

# Extract Footer
footer_match = re.search(r'(<footer class="footer">.*?</footer>)', about_html, re.DOTALL)
if footer_match:
    about_footer = footer_match.group(1)
    # Update active states for Home
    about_footer = about_footer.replace('href="/" class="footer-link"', 'href="/" aria-current="page" class="footer-link w--current"')
    about_footer = about_footer.replace('href="/about" aria-current="page" class="footer-link w--current"', 'href="/about" class="footer-link"')

with open(home_path, 'r') as f:
    home_html = f.read()

if nav_match and footer_match:
    # Replace navbar in home
    home_html = re.sub(r'<div[^>]*role="banner" class="navbar w-nav">.*?\n\s*<section', about_nav + '\n    <section', home_html, flags=re.DOTALL)
    
    # Replace footer in home
    home_html = re.sub(r'<footer class="footer">.*?</footer>', about_footer, home_html, flags=re.DOTALL)

    with open(home_path, 'w') as f:
        f.write(home_html)
    print("Reverted navbar and footer successfully!")
else:
    print("Failed to extract navbar or footer.")
