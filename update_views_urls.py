import os

views_path = '/Users/mac/Desktop/ryder-pro/core/views.py'
urls_path = '/Users/mac/Desktop/ryder-pro/core/urls.py'

with open(views_path, 'r') as f:
    views_content = f.read()

# Add subscribe_newsletter view
subscribe_view = """
def subscribe_newsletter(request):
    from .forms import NewsletterForm
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully subscribed to our newsletter!')
        else:
            if 'email' in form.errors:
                messages.error(request, 'This email is already subscribed or invalid.')
            else:
                messages.error(request, 'An error occurred while subscribing.')
    
    # Redirect back to where the user came from
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('home')
"""

if 'def subscribe_newsletter' not in views_content:
    views_content += subscribe_view
    with open(views_path, 'w') as f:
        f.write(views_content)
    print("Updated views.py")

with open(urls_path, 'r') as f:
    urls_content = f.read()

if "path('subscribe/'" not in urls_content:
    new_url = "    path('subscribe/', views.subscribe_newsletter, name='subscribe'),\n]"
    urls_content = urls_content.replace(']', new_url)
    with open(urls_path, 'w') as f:
        f.write(urls_content)
    print("Updated urls.py")
