import re

file_path = "template-1/pages/utilities/link-in-bio/index.html"
with open(file_path, "r") as f:
    content = f.read()

# Injecting Custom Premium CSS into the Head
custom_css = """
    <style>
        /* Premium Link-in-Bio Styles */
        body {
            background-color: #ffffff;
            color: #121212;
            font-family: 'Instrument Sans', sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: flex-start;
            min-height: 100vh;
        }
        
        .premium-bio-container {
            width: 100%;
            max-width: 480px;
            padding: 60px 24px;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }
        
        .bio-logo-wrap {
            width: 100px;
            height: 100px;
            background: #121212;
            border-radius: 50%;
            display: flex;
            justify-content: center;
            align-items: center;
            margin-bottom: 24px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }
        
        .bio-logo-wrap img {
            width: 50px;
            height: auto;
            filter: brightness(0) invert(1);
        }
        
        .bio-title {
            font-size: 32px;
            font-weight: 800;
            margin: 0 0 12px 0;
            letter-spacing: -1px;
            color: #121212;
        }
        
        .bio-description {
            font-size: 16px;
            color: #666;
            margin: 0 0 40px 0;
            line-height: 1.5;
        }
        
        .bio-links-grid {
            display: flex;
            flex-direction: column;
            gap: 16px;
            width: 100%;
        }
        
        .bio-btn {
            background: #ffffff;
            color: #121212;
            border: 2px solid #121212;
            padding: 18px 24px;
            border-radius: 100px;
            font-size: 16px;
            font-weight: 700;
            text-decoration: none;
            transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1);
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
            overflow: hidden;
        }
        
        .bio-btn.primary {
            background: #e60000;
            color: #ffffff;
            border-color: #e60000;
        }
        
        .bio-btn:hover {
            transform: translateY(-4px);
            box-shadow: 0 15px 25px rgba(230, 0, 0, 0.2);
        }
        
        .bio-btn.primary:hover {
            background: #cc0000;
            border-color: #cc0000;
        }
        
        .bio-socials {
            margin-top: 60px;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 16px;
        }
        
        .bio-socials p {
            font-size: 14px;
            font-weight: 600;
            color: #999;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin: 0;
        }
        
        .social-icons-row {
            display: flex;
            gap: 20px;
        }
        
        .social-icon-btn {
            width: 48px;
            height: 48px;
            border-radius: 50%;
            background: #f4f4f4;
            display: flex;
            justify-content: center;
            align-items: center;
            transition: all 0.3s ease;
        }
        
        .social-icon-btn:hover {
            background: #e60000;
        }
        
        .social-icon-btn img {
            width: 20px;
            height: 20px;
            transition: all 0.3s ease;
            filter: invert(0);
        }
        
        .social-icon-btn:hover img {
            filter: brightness(0) invert(1);
        }
        
    </style>
"""

new_html = """
    <div class="premium-bio-container">
        <a href="/" class="bio-logo-wrap">
            <img src="https://cdn.prod.website-files.com/66dc179a1d6aa88848a4efac/674ef89828115d51cf830fb1_logo-icon.svg" alt="Ryder Pro Logo" />
        </a>
        <h1 class="bio-title">Ryder Pro</h1>
        <p class="bio-description">Premium car rental experiences. Browse our wide selection of luxury vehicles and electric cars.</p>
        
        <div class="bio-links-grid">
            <a href="{% url 'all_cars' %}" class="bio-btn primary">
                Book Your Dream Car
            </a>
            <a href="/" class="bio-btn">
                Visit our Website
            </a>
            <a href="/blog" class="bio-btn">
                Read our Blog
            </a>
            <a href="/contact" class="bio-btn">
                Contact Support
            </a>
        </div>
        
        <div class="bio-socials">
            <p>Follow Us</p>
            <div class="social-icons-row">
                <a href="#" class="social-icon-btn">
                    <img src="https://cdn.prod.website-files.com/66dc179a1d6aa88848a4efac/674ef5a1e5492efe3a216c65_instagram-01.svg" alt="Instagram" />
                </a>
                <a href="#" class="social-icon-btn">
                    <img src="https://cdn.prod.website-files.com/66dc179a1d6aa88848a4efac/674ef5a14bd1a7ce84a50844_facebook-01.svg" alt="Facebook" />
                </a>
                <a href="#" class="social-icon-btn">
                    <img src="https://cdn.prod.website-files.com/66dc179a1d6aa88848a4efac/674ef5a1f6a1d478cf338dc9_x-01.svg" alt="X" />
                </a>
            </div>
        </div>
    </div>
"""

# Inject CSS before </head>
content = content.replace('</head>', custom_css + '\n</head>')

# Replace everything inside <body>...</body> with new_html
body_pattern = re.compile(r'<body>.*?</body>', re.DOTALL)
content = body_pattern.sub(f'<body>\n{new_html}\n</body>', content)

with open(file_path, "w") as f:
    f.write(content)

print("Link in Bio styled")
