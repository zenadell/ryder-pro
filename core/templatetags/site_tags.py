from django import template
from core.models import SiteContent

register = template.Library()

@register.simple_tag
def get_auth_media():
    try:
        content = SiteContent.objects.get(key='auth_page_media')
        if content.video:
            return {'type': 'video', 'url': content.video.url}
        if content.image:
            return {'type': 'image', 'url': content.image.url}
    except SiteContent.DoesNotExist:
        pass
    
    return {'type': 'image', 'url': '/static/images/desktop_auth_bg.png'}
