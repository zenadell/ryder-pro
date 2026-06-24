import os

filepath = '/Users/mac/Desktop/ryder-pro/template-1/pages/contact/index.html'
with open(filepath, 'r') as f:
    content = f.read()

# Fix form names
content = content.replace('name="Phone-No"', 'name="phone"')
content = content.replace('name="Message"', 'name="message"')

# Inject django messages handling above the form
messages_block = """
                        {% if messages %}
                        <div style="margin-bottom: 20px;">
                            {% for message in messages %}
                                <div style="padding: 15px; border-radius: 5px; {% if message.tags == 'success' %}background-color: #d4edda; color: #155724;{% else %}background-color: #f8d7da; color: #721c24;{% endif %}">
                                    {{ message }}
                                </div>
                            {% endfor %}
                        </div>
                        {% endif %}
                        <form
"""

content = content.replace('<form', messages_block, 1)

with open(filepath, 'w') as f:
    f.write(content)
print("Updated contact/index.html")
