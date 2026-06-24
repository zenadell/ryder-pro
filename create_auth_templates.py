import os

base_template = """{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8" />
    <title>TITLE_VAR | Ryder Pro</title>
    <meta content="width=device-width, initial-scale=1" name="viewport" />
    <link href="{% static 'css/vendor/carent-wbs.webflow.shared.15fbda294.css' %}" rel="stylesheet" type="text/css" />
    <link rel="stylesheet" href="{% static 'base.css' %}">
    <link rel="stylesheet" href="{% static 'contact/style.css' %}">
    <link rel="stylesheet" href="{% static 'css/vendor/fonts.css' %}">
</head>
<body>
    {% include 'partials/navbar.html' %}
    
    <section class="contact-hero-section section-spacing">
        <div class="w-layout-blockcontainer container w-container" style="max-width: 600px; margin: 0 auto;">
            <div class="contact-hero-title-wrap" style="text-align: center;">
                <h1 class="heading-lg">TITLE_VAR</h1>
                <p class="no-margin-bottom">SUBTITLE_VAR</p>
            </div>
            <div class="contact-form-wrapper" style="margin-top: 40px;">
                <div class="no-margin-bottom w-form">
                    {% if messages %}
                    <div style="margin-bottom: 20px;">
                        {% for message in messages %}
                            <div style="padding: 15px; border-radius: 5px; {% if message.tags == 'success' %}background-color: #d4edda; color: #155724;{% else %}background-color: #f8d7da; color: #721c24;{% endif %}">
                                {{ message }}
                            </div>
                        {% endfor %}
                    </div>
                    {% endif %}
                    
                    FORM_CONTENT_VAR
                    
                </div>
            </div>
        </div>
    </section>

    {% include 'partials/footer.html' %}
    
    <script src="{% static 'js/vendor/jquery-3.5.1.min.dc5e7f18c8.js' %}"></script>
    <script src="{% static 'base.js' %}"></script>
</body>
</html>
"""

login_form = """
<form method="POST" action="{% url 'login' %}">
    {% csrf_token %}
    {% if form.errors %}
        <div style="padding: 15px; border-radius: 5px; background-color: #f8d7da; color: #721c24; margin-bottom: 20px;">
            Your username and password didn't match. Please try again.
        </div>
    {% endif %}
    <div class="input-group">
        <label for="username">Username</label>
        <input class="form-input w-input" name="username" type="text" id="username" required />
    </div>
    <div class="input-group">
        <label for="password">Password</label>
        <input class="form-input w-input" name="password" type="password" id="password" required />
    </div>
    <input type="submit" class="button-submit contact-button w-button" value="Log In" style="width: 100%;" />
    
    <div style="text-align: center; margin-top: 20px;">
        Don't have an account? <a href="{% url 'signup' %}" style="color: var(--color--primary-1);">Sign up here</a>
    </div>
</form>
"""

signup_form = """
<form method="POST" action="{% url 'signup' %}">
    {% csrf_token %}
    
    {% for field in form %}
        <div class="input-group">
            <label for="{{ field.id_for_label }}">{{ field.label }}</label>
            <input class="form-input w-input" name="{{ field.html_name }}" type="{% if 'password' in field.name %}password{% else %}text{% endif %}" id="{{ field.id_for_label }}" required />
            {% if field.help_text %}
                <small style="color: #666; font-size: 12px; margin-top: 5px; display: block;">{{ field.help_text }}</small>
            {% endif %}
        </div>
    {% endfor %}
    
    <input type="submit" class="button-submit contact-button w-button" value="Create Account" style="width: 100%; margin-top: 20px;" />
    
    <div style="text-align: center; margin-top: 20px;">
        Already have an account? <a href="{% url 'login' %}" style="color: var(--color--primary-1);">Log in here</a>
    </div>
</form>
"""

accounts_dir = '/Users/mac/Desktop/ryder-pro/template-1/pages/accounts'
os.makedirs(accounts_dir, exist_ok=True)

with open(os.path.join(accounts_dir, 'login.html'), 'w') as f:
    f.write(base_template.replace('TITLE_VAR', 'Log In').replace('SUBTITLE_VAR', 'Welcome back to Ryder Pro').replace('FORM_CONTENT_VAR', login_form))

with open(os.path.join(accounts_dir, 'signup.html'), 'w') as f:
    f.write(base_template.replace('TITLE_VAR', 'Sign Up').replace('SUBTITLE_VAR', 'Create an account to manage your bookings').replace('FORM_CONTENT_VAR', signup_form))

print("Created login and signup templates.")
