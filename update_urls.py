import os

urls_path = '/Users/mac/Desktop/ryder-pro/ryder_pro/urls.py'

content = """
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

handler404 = 'core.views.custom_404_view'

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""

with open(urls_path, 'w') as f:
    f.write(content.strip())

print("urls.py updated")
