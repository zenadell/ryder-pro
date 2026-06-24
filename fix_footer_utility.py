import re

file_path = "template-1/pages/partials/footer.html"
with open(file_path, "r") as f:
    content = f.read()

# We need to replace the Utility Pages grid
old_grid = """                            <div class="w-layout-grid grid-footer-link">
                                <div class="footer-link-wrap">
                                    <a href="/utility-pages/style-guide" class="footer-link"> Style Guide
                                    </a>
                                    <a href="/utility-pages/instructions" class="footer-link"> Instructions
                                    </a>
                                    <a href="/utility-pages/licenses" class="footer-link"> Licenses
                                    </a>
                                    <a href="/utility-pages/changelog" class="footer-link"> Changelog
                                    </a>
                                    <a href="/utility-pages/link-in-bio" class="footer-link"> Link in Bio
                                    </a>
                                </div>
                                <div class="footer-link-wrap">
                                    <a href="/utility-pages/coming-soon" class="footer-link"> Coming Soon
                                    </a>
                                    <a href="https://carent-wbs.webflow.io/401" class="footer-link"> Password Protected
                                    </a>
                                    <a href="https://carent-wbs.webflow.io/404" class="footer-link"> Error 404
                                    </a>
                                </div>
                            </div>"""

new_grid = """                            <div class="w-layout-grid grid-footer-link">
                                <div class="footer-link-wrap">
                                    <a href="/instructions" class="footer-link"> Instructions
                                    </a>
                                    <a href="/licenses" class="footer-link"> Licenses
                                    </a>
                                    <a href="/utility-pages/link-in-bio" class="footer-link"> Link in Bio
                                    </a>
                                </div>
                                <div class="footer-link-wrap">
                                    <a href="/privacy" class="footer-link"> Privacy Policy
                                    </a>
                                    <a href="/terms" class="footer-link"> Terms of Service
                                    </a>
                                </div>
                            </div>"""

# Ensure exact whitespace replacement isn't an issue
content = re.sub(r'<div class="w-layout-grid grid-footer-link">.*?</div>\s*</div>\s*</div>\s*</div>', new_grid + '\n                        </div>\n                    </div>\n                </div>', content, flags=re.DOTALL)

with open(file_path, "w") as f:
    f.write(content)

print("Footer updated")
