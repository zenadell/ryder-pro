import os

pages = {
    "template-1/pages/privacy/index.html": {
        "title": "Privacy Policy",
        "desc": "How we protect your data and privacy at Ryder Pro.",
        "content": """
        <div class="legal-card">
            <h3 class="legal-heading">Collecting Personal Information</h3>
            <p class="legal-text">At Ryder Pro, we collect personal information such as your name, email address, phone number, and payment details when you book a car or create an account. This information is strictly necessary to provide our luxury car rental services, verify your identity, and ensure a smooth booking process.</p>
        </div>
        <div class="legal-card">
            <h3 class="legal-heading">Use of Your Information</h3>
            <p class="legal-text">We use your information to manage your bookings, communicate with you regarding your reservations, and improve our services. We may also send you promotional emails about new vehicles or special offers, which you can securely opt out of at any time.</p>
        </div>
        <div class="legal-card">
            <h3 class="legal-heading">Sharing Personal Information</h3>
            <p class="legal-text">We do not sell your personal information under any circumstances. We may share your data with trusted third-party service providers who assist us in operating our website, processing secure payments, or delivering your vehicle. All third parties are strictly bound by confidentiality agreements.</p>
        </div>
        """
    },
    "template-1/pages/terms/index.html": {
        "title": "Terms of Service",
        "desc": "The rules and guidelines for using the Ryder Pro platform.",
        "content": """
        <div class="legal-card">
            <h3 class="legal-heading">Acceptance of Terms</h3>
            <p class="legal-text">By accessing and using the Ryder Pro platform, you agree to be bound by these Terms of Service. If you do not agree to these terms in full, please do not use our services or book vehicles through our platform.</p>
        </div>
        <div class="legal-card">
            <h3 class="legal-heading">Rental Agreement</h3>
            <p class="legal-text">All vehicle rentals are subject to our standard rental agreement, which must be signed upon vehicle delivery or pickup. You must be at least 21 years old and hold a valid driver's license and full-coverage insurance to rent a vehicle from Ryder Pro.</p>
        </div>
        <div class="legal-card">
            <h3 class="legal-heading">Cancellation Policy</h3>
            <p class="legal-text">Reservations can be cancelled up to 48 hours before the scheduled rental period for a full refund. Cancellations made within 48 hours may be subject to a cancellation fee equivalent to one day's rental. No-shows will be charged the full rental amount.</p>
        </div>
        """
    },
    "template-1/pages/utilities/instructions/index.html": {
        "title": "How to Use Ryder Pro",
        "desc": "Your quick-start guide to renting, tracking, and trading vehicles.",
        "content": """
        <div class="legal-card">
            <h3 class="legal-heading">Booking a Vehicle</h3>
            <p class="legal-text">To book a vehicle, navigate to the <strong>Browse Cars</strong> page, explore our premium selection, and click 'Book Now' on your desired vehicle. You will be guided through a secure checkout process to finalize your reservation dates and delivery location.</p>
        </div>
        <div class="legal-card">
            <h3 class="legal-heading">Trading In Your Car</h3>
            <p class="legal-text">If you wish to trade in your current vehicle, visit the <strong>Trade-In</strong> section from the navigation menu. Fill out the details of your car, and our expert valuation team will provide you with a competitive estimate within 24 hours.</p>
        </div>
        <div class="legal-card">
            <h3 class="legal-heading">Tracking Your Delivery</h3>
            <p class="legal-text">For vehicles being delivered directly to your location, you can track the status in real-time. Simply enter your unique Tracking ID on the <strong>Track Order</strong> page to see the current location and estimated time of arrival of your luxury rental.</p>
        </div>
        """
    },
    "template-1/pages/utilities/licenses/index.html": {
        "title": "Licenses & Attributions",
        "desc": "Credits for the assets and typography that power Ryder Pro.",
        "content": """
        <div class="legal-card">
            <h3 class="legal-heading">Typography</h3>
            <p class="legal-text">The Ryder Pro website proudly uses the <strong>Instrument Sans</strong> font family, which is licensed under the SIL Open Font License. This allows for free commercial use and provides our site with its sleek, modern typography.</p>
        </div>
        <div class="legal-card">
            <h3 class="legal-heading">Images & Assets</h3>
            <p class="legal-text">All vehicle images and lifestyle photography used on this website are either generated via state-of-the-art AI, sourced from premium stock photo libraries with appropriate commercial licenses, or provided directly by the vehicle manufacturers for promotional use.</p>
        </div>
        <div class="legal-card">
            <h3 class="legal-heading">Open Source Software</h3>
            <p class="legal-text">This platform is powered by the Django web framework and utilizes various open-source libraries. We are immensely grateful to the global open-source community for their continuous contributions to modern web development.</p>
        </div>
        """
    }
}

template = """{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <title>__TITLE__ | Ryder Pro</title>
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <link href="{% static 'css/vendor/carent-wbs.webflow.shared.15fbda294.css' %}" rel="stylesheet" type="text/css" />
    <link rel="stylesheet" href="{% static 'base.css' %}">
    <link rel="stylesheet" href="{% static 'css/vendor/fonts.css' %}">
    <style>
        /* Modern Ryder Pro Legal Pages Styling */
        body {
            background-color: #f8f9fa;
            font-family: 'Instrument Sans', sans-serif;
            color: #111;
        }
        
        .legal-hero {
            background-color: #000;
            color: #fff;
            padding: 100px 20px;
            text-align: center;
            border-bottom: 5px solid #d90429;
        }
        
        .legal-hero h1 {
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 15px;
            letter-spacing: -0.5px;
        }
        
        .legal-hero p {
            font-size: 1.2rem;
            opacity: 0.8;
            max-width: 600px;
            margin: 0 auto;
        }

        .legal-container {
            max-width: 800px;
            margin: -50px auto 100px;
            padding: 0 20px;
            position: relative;
            z-index: 10;
        }

        .legal-card {
            background: #ffffff;
            border-radius: 12px;
            padding: 40px;
            margin-bottom: 30px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.05);
            border-left: 6px solid #d90429;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .legal-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 50px rgba(217, 4, 41, 0.1);
        }

        .legal-heading {
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 15px;
            color: #000;
        }

        .legal-text {
            font-size: 1.1rem;
            line-height: 1.8;
            color: #555;
            margin: 0;
        }
        
        @media (max-width: 768px) {
            .legal-hero { padding: 80px 20px; }
            .legal-container { margin-top: -30px; }
            .legal-card { padding: 25px; }
        }
    </style>
</head>
<body>
    {% include 'partials/navbar.html' %}

    <div class="legal-hero">
        <h1>__TITLE__</h1>
        <p>__DESC__</p>
    </div>

    <div class="legal-container">
        __CONTENT__
    </div>

    {% include 'partials/footer.html' %}
</body>
</html>
"""

for path, data in pages.items():
    html_content = template.replace("__TITLE__", data["title"])
    html_content = html_content.replace("__DESC__", data["desc"])
    html_content = html_content.replace("__CONTENT__", data["content"])
    
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(html_content)
    print(f"Designed {path}")

