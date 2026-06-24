import os
import django
from django.template.loader import render_to_string

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ryder_pro.settings')
django.setup()

output = render_to_string('home/index.html')
lines = output.split('\n')
for i, line in enumerate(lines):
    if "carent-wbs.webflow" in line:
        print(f"Line {i} exactly:")
        for ch in line:
            print(f"{ch} ({ord(ch)})", end=" ")
        print()
