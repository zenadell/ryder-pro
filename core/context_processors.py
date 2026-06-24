from .models import SiteContent

def site_content(request):
    """
    Injects all SiteContent keys/values into the global template context.
    """
    content = SiteContent.objects.all()
    content_dict = {}
    for item in content:
        if item.video:
            content_dict[item.key] = item.video.url
            content_dict[f"{item.key}_is_video"] = True
        elif item.image:
            content_dict[item.key] = item.image.url
            content_dict[f"{item.key}_is_image"] = True
        else:
            content_dict[item.key] = item.value
    return {'site_content': content_dict}
