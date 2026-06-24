import re

file_path = "template-1/pages/dashboard/index.html"
with open(file_path, "r") as f:
    content = f.read()

# 1. Replace CSS variables for dark theme
content = re.sub(
    r"--bg-color: #f7f7f7;",
    "--bg-color: #121212;",
    content
)
content = re.sub(
    r"--sidebar-bg: #ffffff;",
    "--sidebar-bg: #1c1c1e;",
    content
)
content = re.sub(
    r"--card-bg: #ffffff;",
    "--card-bg: #1c1c1e;",
    content
)
content = re.sub(
    r"--text-main: #111111;",
    "--text-main: #ffffff;",
    content
)
content = re.sub(
    r"--text-muted: #666666;",
    "--text-muted: #a0a0a0;",
    content
)

# Replace table section styles for dark theme
content = re.sub(r"rgba\(0,0,0,0\.05\)", "rgba(255,255,255,0.05)", content)
content = re.sub(r"rgba\(0,0,0,0\.1\)", "rgba(255,255,255,0.1)", content)
content = re.sub(r"rgba\(0,0,0,0\.03\)", "rgba(255,255,255,0.03)", content)
content = re.sub(r"background-color: #f7f9fc;", "background-color: #121212;", content)
content = re.sub(r"background: rgba\(255, 255, 255, 0\.9\);", "background: rgba(28, 28, 30, 0.9);", content)

# 2. Add New Garage CSS
new_css = """
        /* Premium Garage CSS */
        .garage-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }
        .garage-card {
            background-color: var(--card-bg);
            border-radius: 24px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.05);
            display: flex;
            flex-direction: column;
        }
        .garage-cover {
            position: relative;
            width: 100%;
            height: 220px;
        }
        .garage-cover img {
            width: 100%;
            height: 100%;
            object-fit: cover;
            display: block;
        }
        .garage-cover-overlay {
            position: absolute;
            top: 0; left: 0; right: 0; bottom: 0;
            background: linear-gradient(to bottom, rgba(0,0,0,0.1) 0%, var(--card-bg) 100%);
        }
        .garage-header {
            position: absolute;
            top: 20px;
            left: 20px;
            right: 20px;
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            z-index: 2;
            background: rgba(0,0,0,0.4);
            backdrop-filter: blur(10px);
            padding: 12px 16px;
            border-radius: 16px;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .garage-title {
            font-size: 18px;
            font-weight: 700;
            color: #fff;
            margin-bottom: 2px;
            letter-spacing: -0.5px;
        }
        .garage-subtitle {
            font-size: 12px;
            color: rgba(255,255,255,0.7);
        }
        .garage-body {
            padding: 0 25px 25px 25px;
            flex: 1;
            display: flex;
            flex-direction: column;
            position: relative;
            z-index: 3;
            margin-top: -20px;
        }
        .progress-container {
            display: flex;
            align-items: center;
            gap: 25px;
            background: rgba(255,255,255,0.02);
            border: 1px solid rgba(255,255,255,0.04);
            border-radius: 20px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .circular-chart.large {
            width: 100px;
            height: 100px;
        }
        .percentage.large {
            font-size: 8px;
            font-weight: 700;
            fill: #fff;
        }
        .progress-stats {
            flex: 1;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .stat-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 14px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
            padding-bottom: 6px;
        }
        .stat-row:last-child {
            border-bottom: none;
            padding-bottom: 0;
        }
        .stat-label {
            color: var(--text-muted);
            font-size: 13px;
        }
        .stat-val {
            font-weight: 700;
            font-family: monospace;
            font-size: 15px;
        }
        .text-white { color: #ffffff; }
        .text-emerald { color: #10b981; }
        .text-rose { color: #ef4444; }
        
        .btn-pay.full-width {
            width: 100%;
            text-align: center;
            padding: 14px;
            border-radius: 14px;
            font-size: 15px;
        }
        .btn-paid {
            background: rgba(16, 185, 129, 0.1);
            color: #10b981;
            border: 1px solid rgba(16, 185, 129, 0.2);
            text-align: center;
            padding: 14px;
            border-radius: 14px;
            font-size: 15px;
            font-weight: 600;
        }
"""
content = re.sub(r"/\* Garage Stage CSS \*/.*?(?=/\* Mobile Responsiveness \*/)", new_css, content, flags=re.DOTALL)


# 3. Replace the HTML garage section
new_html = """        <div class="garage-section">
            <h3 style="margin-bottom: 20px; font-size: 22px; font-weight: 700;">My Garage</h3>
            {% if installment_plans %}
            <div class="garage-grid">
                {% for plan in installment_plans %}
                <div class="garage-card" data-plan-id="{{ plan.id }}" data-paid="{{ plan.down_payment_paid }}" data-total="{{ plan.total_amount }}" data-created="{{ plan.created_at|date:'Y-m-d' }}">
                    <div class="garage-cover">
                        {% if plan.vehicle.main_image %}
                        <img src="{{ plan.vehicle.main_image.url }}" alt="{{ plan.vehicle.name }}" />
                        {% endif %}
                        <div class="garage-cover-overlay"></div>
                        <div class="garage-header">
                            <div>
                                <div class="garage-title">{{ plan.vehicle.name }}</div>
                                <div class="garage-subtitle">
                                    {% if plan.tier == "tier1" %} Drive Now (Tier 1) {% else %} Layaway (Tier 2) {% endif %}
                                </div>
                            </div>
                            <!-- Lock Icon -->
                            <div class="lock-container lock-ui">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                                    <rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect>
                                    <path d="M7 11V7a5 5 0 0 1 10 0v4"></path>
                                </svg>
                            </div>
                        </div>
                    </div>
                    
                    <div class="garage-body">
                        <div class="progress-container">
                            <div class="progress-chart-wrapper">
                                <svg viewBox="0 0 36 36" class="circular-chart large">
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
                                </svg>
                            </div>
                            <div class="progress-stats">
                                <div class="stat-row">
                                    <span class="stat-label">Total Price</span>
                                    <span class="stat-val text-white">${{ plan.total_amount }}</span>
                                </div>
                                <div class="stat-row">
                                    <span class="stat-label">Paid</span>
                                    <span class="stat-val text-emerald">${{ plan.down_payment_paid }}</span>
                                </div>
                                <div class="stat-row">
                                    <span class="stat-label">Remaining</span>
                                    <span class="stat-val text-rose">${{ plan.principal_balance }}</span>
                                </div>
                            </div>
                        </div>
                        
                        <div class="action-row">
                            {% if not plan.is_fully_paid %}
                            <a href="{% url 'make_payment' plan.id %}" class="btn-pay full-width">Make Payment</a>
                            {% else %}
                            <div class="btn-paid full-width">Fully Paid</div>
                            {% endif %}
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
            {% else %}
            <div style="padding: 40px 20px; text-align: center; color: #888; background: var(--card-bg); border-radius: 20px;">
                <p>You have no active installment plans.</p>
                <a href="{% url 'financing' %}" class="btn-home" style="margin-top: 15px; display: inline-block; background: var(--accent-gradient);">Browse Financing</a>
            </div>
            {% endif %}
        </div>
"""
content = re.sub(r'<div class="garage-section">.*?</div>\n(?=\s*<div class="table-section">)', new_html, content, flags=re.DOTALL)

with open(file_path, "w") as f:
    f.write(content)

print("Script generated successfully")
