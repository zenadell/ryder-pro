with open('template-1/pages/rentals/checkout.html', 'r') as f:
    content = f.read()

# Make substitutions to adapt checkout.html to make_payment.html
content = content.replace("Checkout | Ryder Pro", "Make Payment | Ryder Pro")
content = content.replace("Complete your reservation using our secure checkout.", "Process your installment payment securely.")
content = content.replace("action=\"{% url 'rental_checkout' rental.id %}\"", "action=\"\"")

content = content.replace("{{ rental.vehicle.main_image.url }}", "{{ plan.vehicle.main_image.url }}")
content = content.replace("{{ rental.vehicle.make }} {{ rental.vehicle.model }}", "{{ plan.vehicle.make }} {{ plan.vehicle.model }}")
content = content.replace("{{ rental.vehicle.year }}", "{{ plan.vehicle.year }}")

# Remove rental-specific rows and replace with Plan-specific rows
start_idx = content.find('<div class="summary-divider"></div>')
end_idx = content.find('</div>\n            </div>\n        </div>')

new_summary = """<div class="summary-divider"></div>
                    
                    <div class="summary-row">
                        <span style="color: #666;">Tier Status</span>
                        <span style="font-weight: 600;">{% if plan.tier == 'tier1' %}Drive Now (Tier 1){% else %}Layaway (Tier 2){% endif %}</span>
                    </div>
                    <div class="summary-row">
                        <span style="color: #666;">Principal Balance</span>
                        <span style="font-weight: 600;">${{ plan.principal_balance }}</span>
                    </div>
                    <div class="summary-row">
                        <span style="color: #666;">Penalty Interest</span>
                        <span style="font-weight: 600; color: #ef4444;">${{ plan.accumulated_penalty_interest }}</span>
                    </div>
                    
                    <div class="summary-divider"></div>
                    
                    <div class="summary-row total">
                        <span>Total Due</span>
                        <span style="color: #000;">${{ plan.total_balance_due }}</span>
                    </div>
"""
content = content[:start_idx] + new_summary + content[end_idx:]

# Update the Amount to Pay input
content = content.replace("Amount to Pay Now (USD)", "Amount to Pay (USD)")
content = content.replace("value=\"{{ rental.total_cost }}\"", "value=\"{{ plan.total_balance_due }}\" max=\"{{ plan.total_balance_due }}\" min=\"1\"")
content = content.replace("You can pay a portion now to secure the booking, and the rest upon pickup.", "Enter the amount you wish to pay towards your installment plan.")
content = content.replace("name=\"amount_to_pay\"", "name=\"amount\"")
content = content.replace("id=\"id_amount_to_pay\"", "id=\"id_amount\"")

with open('template-1/pages/dashboard/make_payment.html', 'w') as f:
    f.write(content)

