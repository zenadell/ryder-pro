import re

pages = [
    {
        "file": "template-1/pages/privacy/index.html",
        "title": '{{ site_content.privacy_hero_title|default:"Privacy Policy" }}',
        "content": """
    <h5>Collecting Personal Information</h5>
    <p>At Ryder Pro, we collect personal information such as your name, email address, phone number, and payment details when you book a car or create an account. This information is necessary to provide our luxury car rental services, verify your identity, and ensure a smooth booking process.</p>
    <h5>Use of Your Information</h5>
    <p>We use your information to manage your bookings, communicate with you regarding your reservations, and improve our services. We may also send you promotional emails about new vehicles or special offers, which you can opt out of at any time.</p>
    <h5>Sharing Personal Information</h5>
    <p>We do not sell your personal information. We may share your data with trusted third-party service providers who assist us in operating our website, processing payments, or delivering your vehicle. All third parties are strictly bound by confidentiality agreements.</p>
"""
    },
    {
        "file": "template-1/pages/terms/index.html",
        "title": '{{ site_content.terms_hero_title|default:"Terms of Service" }}',
        "content": """
    <h5>Acceptance of Terms</h5>
    <p>By accessing and using the Ryder Pro platform, you agree to be bound by these Terms of Service. If you do not agree to these terms, please do not use our services.</p>
    <h5>Rental Agreement</h5>
    <p>All vehicle rentals are subject to our standard rental agreement, which must be signed upon vehicle delivery or pickup. You must be at least 21 years old and hold a valid driver's license and insurance to rent a vehicle from Ryder Pro.</p>
    <h5>Cancellation Policy</h5>
    <p>Reservations can be cancelled up to 48 hours before the scheduled rental period for a full refund. Cancellations made within 48 hours may be subject to a cancellation fee. No-shows will be charged the full rental amount.</p>
"""
    },
    {
        "file": "template-1/pages/utilities/instructions/index.html",
        "title": 'Website Instructions',
        "content": """
    <h5>Booking a Vehicle</h5>
    <p>To book a vehicle, navigate to the <strong>Cars</strong> page, browse our premium selection, and click 'Book Now' on your desired vehicle. You will be guided through a simple checkout process to secure your reservation.</p>
    <h5>Trading In Your Car</h5>
    <p>If you wish to trade in your current vehicle, visit the <strong>Trade-In</strong> section. Fill out the details of your car, and our team will provide you with a competitive estimate.</p>
    <h5>Tracking Your Delivery</h5>
    <p>For vehicles being delivered to your location, you can track the status in real-time. Simply enter your Tracking ID on the <strong>Track Order</strong> page to see the current location and estimated time of arrival.</p>
"""
    },
    {
        "file": "template-1/pages/utilities/licenses/index.html",
        "title": 'Licenses & Attributions',
        "content": """
    <h5>Typography</h5>
    <p>The Ryder Pro website uses the <strong>Instrument Sans</strong> font family, which is licensed under the SIL Open Font License. This allows for free commercial use.</p>
    <h5>Images & Assets</h5>
    <p>All vehicle images and lifestyle photography used on this website are either generated via AI, sourced from premium stock photo libraries with appropriate commercial licenses, or provided directly by the vehicle manufacturers for promotional use.</p>
    <h5>Software</h5>
    <p>This platform is powered by the Django web framework and utilizes various open-source libraries. We are grateful to the open-source community for their contributions.</p>
"""
    }
]

for page in pages:
    file_path = page["file"]
    with open(file_path, "r") as f:
        content = f.read()
    
    # Replace title block
    content = re.sub(r'<h1 class="hero-inner-title">\s*.*?\s*</h1>', f'<h1 class="hero-inner-title">\n                    {page["title"]}\n                </h1>', content, flags=re.DOTALL)
    
    # Replace head <title>
    title_text = page["title"].replace('{{ site_content.privacy_hero_title|default:"', '').replace('{{ site_content.terms_hero_title|default:"', '').replace('"}', '').replace('"}}', '')
    content = re.sub(r'<title>\s*.*?\s*</title>', f'<title>{title_text} | Ryder Pro</title>', content, flags=re.DOTALL)
    
    # Replace richtext content
    pattern = re.compile(r'(<div class="rich-text w-richtext">).*?(</div>\s*</div>\s*</div>)', re.DOTALL)
    content = pattern.sub(rf'\1\n{page["content"]}\n\2', content)
    
    with open(file_path, "w") as f:
        f.write(content)
    print(f"Updated {file_path}")

