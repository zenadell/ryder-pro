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

    # Normalise payment_mode so free-text values still work. Whatever is stored
    # ("crypto", "crypto only", "Crypto", "card payment only", "both", ...) is
    # mapped to one of card / crypto / both for the checkout logic.
    pm = (content_dict.get('payment_mode') or 'both').strip().lower()
    has_card, has_crypto = ('card' in pm), ('crypto' in pm)
    if has_card and not has_crypto:
        content_dict['payment_mode'] = 'card'
    elif has_crypto and not has_card:
        content_dict['payment_mode'] = 'crypto'
    else:
        content_dict['payment_mode'] = 'both'

    # Start the self-ping keep-alive thread on first request (if not already running)
    try:
        from .views import _start_keep_alive
        _start_keep_alive()
    except Exception:
        pass

    return {'site_content': content_dict}
