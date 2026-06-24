import os
import re

filepath = '/Users/mac/Desktop/ryder-pro/template-1/pages/partials/footer.html'
with open(filepath, 'r') as f:
    content = f.read()

# Replace method="get" with method="POST" action="{% url 'subscribe' %}"
content = re.sub(r'method="get"', 'method="POST" action="{% url \'subscribe\' %}"', content)

# Inject CSRF token
if '{% csrf_token %}' not in content:
    content = re.sub(r'(<form[^>]*>)', r'\1\n{% csrf_token %}', content)

# Inject message handling in footer
if '{% if messages %}' not in content:
    messages_block = """
                            {% if messages %}
                            <div style="margin-bottom: 20px;">
                                {% for message in messages %}
                                    <div style="padding: 10px; border-radius: 5px; {% if message.tags == 'success' %}background-color: #d4edda; color: #155724;{% else %}background-color: #f8d7da; color: #721c24;{% endif %}">
                                        {{ message }}
                                    </div>
                                {% endfor %}
                            </div>
                            {% endif %}
                            <div class="no-margin-bottom w-form">
"""
    content = content.replace('<div class="no-margin-bottom w-form">', messages_block, 1)

# Replace name="Footer-Email" with name="email"
content = content.replace('name="Footer-Email"', 'name="email"')

with open(filepath, 'w') as f:
    f.write(content)
print("Fixed footer partial")
