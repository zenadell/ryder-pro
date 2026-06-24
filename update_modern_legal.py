import os

pages = {
    "template-1/pages/privacy/index.html": {
        "title": "Privacy Policy",
        "desc": "Comprehensive outline of how Ryder Pro protects, manages, and secures your personal data.",
        "content": """
        <div class="legal-card">
            <h3 class="legal-heading">1. Collection of Personal Information</h3>
            <p class="legal-text">At Ryder Pro, we prioritize the confidentiality of our clients. We collect personal information such as your full name, email address, phone number, physical address, and payment details when you book a vehicle or register an account. Additionally, we may collect driving history and insurance details as required by local jurisdictions to fulfill our luxury car rental services. This information is strictly necessary to verify your identity, process your payments securely, and ensure a seamless, high-end booking experience.</p>
        </div>
        <div class="legal-card">
            <h3 class="legal-heading">2. Use of Your Information</h3>
            <p class="legal-text">We utilize your collected data primarily to manage your vehicle reservations, communicate essential details regarding your bookings, and provide dedicated customer support. Furthermore, we may use your information to personalize your experience on our platform, analyze usage trends to improve our services, and send you exclusive promotional offers about our new fleet additions. You retain the right to securely opt out of any non-essential marketing communications at any time via your account settings.</p>
        </div>
        <div class="legal-card">
            <h3 class="legal-heading">3. Data Security and Storage</h3>
            <p class="legal-text">We employ enterprise-grade security protocols, including industry-standard SSL encryption and secure servers, to protect your sensitive information from unauthorized access, disclosure, or alteration. All payment data is processed through highly secure, PCI-compliant third-party gateways. We do not store your credit card details directly on our servers, ensuring maximum security for your financial information.</p>
        </div>
        <div class="legal-card">
            <h3 class="legal-heading">4. Sharing Personal Information</h3>
            <p class="legal-text">Ryder Pro does not sell, rent, or trade your personal information under any circumstances. We may, however, share your data with trusted third-party service providers who assist us in operating our website, conducting our business, or servicing you. These parties are strictly bound by non-disclosure agreements and are prohibited from using your personal information for any secondary purposes.</p>
        </div>
        """
    },
    "template-1/pages/terms/index.html": {
        "title": "Terms of Service",
        "desc": "The official rules and guidelines governing the use of the Ryder Pro platform and services.",
        "content": """
        <div class="legal-card">
            <h3 class="legal-heading">1. Acceptance of Terms</h3>
            <p class="legal-text">By accessing, browsing, and using the Ryder Pro platform, you acknowledge that you have read, understood, and unconditionally agree to be bound by these Terms of Service. If you do not agree to these terms in full, you are prohibited from using our services, registering an account, or booking vehicles through our platform.</p>
        </div>
        <div class="legal-card">
            <h3 class="legal-heading">2. Eligibility and Rental Agreement</h3>
            <p class="legal-text">All vehicle rentals are subject to our comprehensive standard rental agreement, which must be physically or digitally signed upon vehicle delivery or pickup. To be eligible to rent a luxury vehicle from Ryder Pro, you must be at least 21 years of age, possess a valid, unexpired driver's license, and hold full-coverage insurance. Additional age restrictions may apply for certain exotic or high-performance vehicles in our fleet.</p>
        </div>
        <div class="legal-card">
            <h3 class="legal-heading">3. Vehicle Usage and Restrictions</h3>
            <p class="legal-text">Rented vehicles must be operated safely and within the confines of the law. They are strictly prohibited from being used for racing, off-roading, towing, or any illegal activities. Smoking and transporting pets (without prior written consent and appropriate protective measures) are strictly forbidden within any Ryder Pro vehicle. Violations of these usage policies may result in immediate termination of the rental agreement and substantial cleaning or repair fees.</p>
        </div>
        <div class="legal-card">
            <h3 class="legal-heading">4. Cancellation and Refund Policy</h3>
            <p class="legal-text">Reservations may be cancelled up to 48 hours before the scheduled rental period for a full and prompt refund. Cancellations made within the 48-hour window may be subject to a cancellation fee equivalent to one day's rental rate. No-shows or failure to produce valid documentation at the time of pickup will result in the forfeiture of the entire rental amount.</p>
        </div>
        """
    },
    "template-1/pages/utilities/instructions/index.html": {
        "title": "How to Use Ryder Pro",
        "desc": "Your comprehensive quick-start guide to renting, tracking, and trading premium vehicles.",
        "content": """
        <div class="legal-card">
            <h3 class="legal-heading">1. Booking a Premium Vehicle</h3>
            <p class="legal-text">Securing your dream car with Ryder Pro is designed to be effortless. To begin, navigate to our <a href="{% url 'all_cars' %}" style="color: #d90429; text-decoration: underline; font-weight: 600;">Browse Cars</a> page and explore our meticulously curated fleet of luxury and exotic vehicles. Once you have selected your desired vehicle, click 'Book Now' to initiate the reservation. You will be smoothly guided through our secure checkout process, where you can select your rental dates, specify delivery locations, and finalize your booking.</p>
        </div>
        <div class="legal-card">
            <h3 class="legal-heading">2. Trading In Your Current Vehicle</h3>
            <p class="legal-text">If you wish to seamlessly upgrade your lifestyle by trading in your current vehicle, visit the dedicated <a href="{% url 'trade_in' %}" style="color: #d90429; text-decoration: underline; font-weight: 600;">Trade-In</a> section accessible from our main navigation menu. Simply provide the make, model, year, and condition of your car. Our expert valuation team will rigorously review the details and provide you with a highly competitive estimate within 24 hours.</p>
        </div>
        <div class="legal-card">
            <h3 class="legal-heading">3. Real-Time Delivery Tracking</h3>
            <p class="legal-text">For clients opting for our exclusive white-glove delivery service, you can monitor your vehicle's transit in real-time. Once your vehicle is dispatched, you will receive a unique Tracking ID. Enter this identifier on our <a href="{% url 'shipment_tracking' %}" style="color: #d90429; text-decoration: underline; font-weight: 600;">Track Order</a> page to view the precise current location and the highly accurate estimated time of arrival of your luxury rental right to your doorstep.</p>
        </div>
        <div class="legal-card">
            <h3 class="legal-heading">4. Managing Your Account</h3>
            <p class="legal-text">By creating a Ryder Pro account, you gain access to a powerful personalized dashboard. Here, you can effortlessly view your upcoming reservations, manage your payment methods, review past rental history, and access exclusive loyalty rewards. Keeping your profile updated ensures a faster, more streamlined checkout experience for all future bookings.</p>
        </div>
        """
    },
    "template-1/pages/utilities/licenses/index.html": {
        "title": "Licenses & Attributions",
        "desc": "Official credits and acknowledgments for the digital assets, typography, and software that power the Ryder Pro experience.",
        "content": """
        <div class="legal-card">
            <h3 class="legal-heading">1. Typography and Fonts</h3>
            <p class="legal-text">The Ryder Pro digital platform proudly utilizes the <strong>Instrument Sans</strong> font family to deliver our sleek, highly legible, and modern typographic experience. This typeface is fully licensed under the SIL Open Font License, which gracefully permits unrestricted commercial application while supporting the open-source typography community.</p>
        </div>
        <div class="legal-card">
            <h3 class="legal-heading">2. Images, Photography, and Media Assets</h3>
            <p class="legal-text">The stunning vehicle imagery, high-definition background photography, and lifestyle media featured throughout this website are meticulously curated. They are either generated via state-of-the-art AI modeling, licensed from premium stock photography libraries with full commercial rights, or officially provided by the respective vehicle manufacturers strictly for promotional and informational use.</p>
        </div>
        <div class="legal-card">
            <h3 class="legal-heading">3. Open Source Software and Frameworks</h3>
            <p class="legal-text">The robust backend architecture of Ryder Pro is powered by the Python-based Django web framework. Our frontend leverages cutting-edge CSS/JS libraries to ensure a responsive and highly dynamic user interface. We are immensely grateful to the global open-source community, whose continuous contributions to modern web development make sophisticated platforms like ours possible.</p>
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
            background-color: #000 !important;
            padding: 120px 20px;
            text-align: center;
            border-bottom: 5px solid #d90429;
            position: relative;
        }
        
        .legal-hero h1 {
            color: #ffffff !important;
            font-size: 3.5rem;
            font-weight: 700;
            margin-bottom: 15px;
            letter-spacing: -0.5px;
        }
        
        .legal-hero p {
            color: #ffffff !important;
            font-size: 1.2rem;
            opacity: 0.9;
            max-width: 600px;
            margin: 0 auto;
        }

        .legal-container {
            max-width: 850px;
            margin: -60px auto 100px;
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
            font-size: 1.15rem;
            line-height: 1.8;
            color: #444;
            margin: 0;
        }
        
        @media (max-width: 768px) {
            .legal-hero { padding: 90px 20px; }
            .legal-hero h1 { font-size: 2.5rem; }
            .legal-container { margin-top: -30px; }
            .legal-card { padding: 30px; }
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

