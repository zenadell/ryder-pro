import re

with open('template-1/pages/dashboard/index.html', 'r') as f:
    content = f.read()

# 1. Insert dashboard-tab start before top-cards
content = content.replace(
    '<div class="top-cards">', 
    '<div id="dashboard-tab" class="tab-content" style="display: block;">\n        <div class="top-cards">'
)

# 2. Extract shipments section
shipment_pattern = re.compile(r'(<div class="table-section">\s*<h3>Active Shipments</h3>.*?</div>\s*)(?=</div>\s*<script)', re.DOTALL)
shipment_match = shipment_pattern.search(content)
if shipment_match:
    shipment_html = shipment_match.group(1)
    # Remove shipment from original place
    content = content.replace(shipment_html, '')
    
    # We want to put shipment_html right after garage-section ends, which is right before financing-apps
    financing_pattern = re.compile(r'(<div class="table-section">\s*<h3>Financing Applications</h3>)')
    content = content.replace(
        '<div class="table-section">\n            <h3>Financing Applications</h3>',
        shipment_html + '\n        </div><!-- end dashboard-tab -->\n\n        <div id="financing-tab" class="tab-content" style="display: none;">\n        <div class="table-section">\n            <h3>Financing Applications</h3>'
    )

# 3. Separate Financing and Trade-In from Jobs
# Jobs starts at
content = content.replace(
    '<div class="table-section">\n            <h3>Job Applications</h3>',
    '</div><!-- end financing-tab -->\n\n        <div id="jobs-tab" class="tab-content" style="display: none;">\n        <div class="table-section">\n            <h3>Job Applications</h3>'
)

# Trade-in starts at. We need to close jobs-tab before Trade-in, but wait, Trade-in belongs to Financing!
# So Trade-In needs to be moved to financing-tab, OR we just put Trade-In before Job Applications.
# Let's extract Trade-in and put it after Financing.
trade_pattern = re.compile(r'(<div class="table-section">\s*<h3>Trade-In & Swap Requests</h3>.*?</div>\s*)', re.DOTALL)
trade_match = trade_pattern.search(content)
if trade_match:
    trade_html = trade_match.group(1)
    content = content.replace(trade_html, '')
    # Insert it right before jobs-tab starts
    content = content.replace(
        '</div><!-- end financing-tab -->',
        trade_html + '\n        </div><!-- end financing-tab -->'
    )

# 4. Rentals Tab
content = content.replace(
    '<div class="table-section">\n            <h3>Active & Past Rentals</h3>',
    '</div><!-- end jobs-tab -->\n\n        <div id="rentals-tab" class="tab-content" style="display: none;">\n        <div class="table-section">\n            <h3>Active & Past Rentals</h3>'
)

# 5. Settings Tab
settings_html = """
        </div><!-- end rentals-tab -->

        <div id="settings-tab" class="tab-content" style="display: none;">
            <div class="table-section">
                <h3 style="margin-bottom: 20px;">Profile Settings</h3>
                <form id="settingsForm" method="POST" action="/dashboard/update-settings/" style="max-width: 600px; display: flex; flex-direction: column; gap: 20px;">
                    <input type="hidden" name="csrfmiddlewaretoken" value="{{ csrf_token }}">
                    <div style="display: flex; gap: 20px;">
                        <div style="flex: 1;">
                            <label style="color: var(--text-muted); font-size: 14px; margin-bottom: 8px; display: block;">First Name</label>
                            <input type="text" name="first_name" value="{{ request.user.first_name }}" class="search-bar" style="width: 100%;" />
                        </div>
                        <div style="flex: 1;">
                            <label style="color: var(--text-muted); font-size: 14px; margin-bottom: 8px; display: block;">Last Name</label>
                            <input type="text" name="last_name" value="{{ request.user.last_name }}" class="search-bar" style="width: 100%;" />
                        </div>
                    </div>
                    <div>
                        <label style="color: var(--text-muted); font-size: 14px; margin-bottom: 8px; display: block;">Email Address</label>
                        <input type="email" name="email" value="{{ request.user.email }}" class="search-bar" style="width: 100%;" />
                    </div>
                    <div>
                        <button type="submit" class="btn-home" style="background: var(--accent-gradient); border: none; cursor: pointer; padding: 12px 25px;">Save Changes</button>
                    </div>
                </form>
            </div>
"""

content = content.replace('<!-- Main Content -->', '<style>.tab-content { display: none; } .tab-content.active { display: block; }</style>\n    <!-- Main Content -->')

# Replace the very end of rentals table (which is before the closing main-content div)
# Since Shipments was moved, the rentals div is the last one before the closing </div> of main-content.
# Find the end of rentals
rentals_end_pattern = re.compile(r'(You have no active or past rentals.</p>\s*{% endif %}\s*</div>\s*)(?=</div>\s*<script)', re.DOTALL)
rentals_end_match = rentals_end_pattern.search(content)

if rentals_end_match:
    content = content.replace(rentals_end_match.group(1), rentals_end_match.group(1) + settings_html)
else:
    print("Could not find rentals end")

with open('template-1/pages/dashboard/index.html', 'w') as f:
    f.write(content)

print("Restructured HTML successfully")
