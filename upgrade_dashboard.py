import re

file_path = "template-1/pages/dashboard/index.html"
with open(file_path, "r") as f:
    content = f.read()

# --- CSS UPDATES ---

# 1. Update Garage CSS (Shadows, Overlays, Typography)
content = content.replace("box-shadow: 0 10px 40px rgba(0,0,0,0.3);", "box-shadow: 0 10px 40px rgba(0,0,0,0.5), 0 0 40px rgba(16, 185, 129, 0.05);")
content = content.replace("background: linear-gradient(to bottom, rgba(0,0,0,0.1) 0%, var(--card-bg) 100%);", "background: linear-gradient(to bottom, transparent 0%, rgba(28,28,30,0.8) 70%, var(--card-bg) 100%);")
content = content.replace("background: rgba(0,0,0,0.4);", "background: rgba(28,28,30,0.6);")
content = content.replace("color: rgba(255,255,255,0.7);", "color: rgba(255,255,255,0.9); font-weight: 500;")

# 2. Add specific style for the SVG circles inside the CSS
svg_css = """
        .circle-bg { fill: none; stroke: rgba(255,255,255,0.05); stroke-width: 2.5; }
        .circle { fill: none; stroke-width: 2.5; stroke-linecap: round; animation: progress 1s ease-out forwards; }
        .circle.finance { stroke: url(#financeGradient); }
        .percentage.large { font-size: 8px; font-weight: 700; fill: #fff; text-anchor: middle; dominant-baseline: middle; }
"""
# Replace existing SVG css
content = re.sub(r"\s*\.circle-bg\s*\{.*?\}(?=\s*\.percentage)", svg_css, content, flags=re.DOTALL)


# 3. Add Make Payment button CSS
btn_css = """
        .btn-pay.full-width {
            width: 100%;
            text-align: center;
            padding: 14px;
            border-radius: 14px;
            font-size: 15px;
            font-weight: 600;
            display: inline-block;
            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
            color: #ffffff;
            text-decoration: none;
            box-shadow: 0 4px 15px rgba(16, 185, 129, 0.3);
            transition: all 0.3s ease;
            border: none;
        }
        .btn-pay.full-width:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(16, 185, 129, 0.5);
            background: linear-gradient(135deg, #34d399 0%, #10b981 100%);
        }
"""
content = re.sub(r"\s*\.btn-pay\.full-width\s*\{.*?\}(?=\s*\.btn-paid)", btn_css, content, flags=re.DOTALL)


# 4. Improve Table CSS
table_css = """
        table { width: 100%; border-collapse: separate; border-spacing: 0; }
        th, td { padding: 18px 15px; text-align: left; border-bottom: 1px solid rgba(255,255,255,0.03); }
        th { color: var(--text-muted); font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
        tbody tr { transition: background-color 0.2s ease; }
        tbody tr:hover { background-color: rgba(255,255,255,0.02); }
        td { font-size: 14px; color: rgba(255,255,255,0.9); }
"""
content = re.sub(r"\s*table\s*\{.*?\}(?=\s*\.status-badge)", table_css, content, flags=re.DOTALL)


# --- HTML UPDATES ---

# Update the SVG to include gradients, fill="none", and correct dominant-baseline
old_svg = """<svg viewBox="0 0 36 36" class="circular-chart large">
                                    <path class="circle-bg"
                                        d="M18 2.0845
                                        a 15.9155 15.9155 0 0 1 0 31.831
                                        a 15.9155 15.9155 0 0 1 0 -31.831"
                                    />
                                    <path class="circle finance finance-circle-ui"
                                        stroke-dasharray="0, 100"
                                        d="M18 2.0845
                                        a 15.9155 15.9155 0 0 1 0 31.831
                                        a 15.9155 15.9155 0 0 1 0 -31.831"
                                    />
                                    <text x="18" y="21.5" class="percentage large finance-text-ui">0%</text>
                                </svg>"""

new_svg = """<svg viewBox="0 0 36 36" class="circular-chart large">
                                    <defs>
                                        <linearGradient id="financeGradient" x1="0%" y1="0%" x2="100%" y2="0%">
                                            <stop offset="0%" stop-color="#34d399" />
                                            <stop offset="100%" stop-color="#059669" />
                                        </linearGradient>
                                    </defs>
                                    <path class="circle-bg" fill="none"
                                        d="M18 2.0845
                                        a 15.9155 15.9155 0 0 1 0 31.831
                                        a 15.9155 15.9155 0 0 1 0 -31.831"
                                    />
                                    <path class="circle finance finance-circle-ui" fill="none"
                                        stroke-dasharray="0, 100"
                                        d="M18 2.0845
                                        a 15.9155 15.9155 0 0 1 0 31.831
                                        a 15.9155 15.9155 0 0 1 0 -31.831"
                                    />
                                    <text x="18" y="20" class="percentage large finance-text-ui">0%</text>
                                </svg>"""

content = content.replace(old_svg, new_svg)

with open(file_path, "w") as f:
    f.write(content)

print("Upgrade script executed")
