from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse
from .forms import CustomUserCreationForm
from ryder_pro.supabase_client import get_supabase

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            
            supabase = get_supabase(request)
            if supabase:
                try:
                    res = supabase.auth.sign_up({
                        "email": email, 
                        "password": password,
                        "options": {"data": {"first_name": first_name, "last_name": last_name}}
                    })
                except Exception as e:
                    messages.error(request, f"Supabase Error: {str(e)}")
                    return render(request, 'accounts/signup.html', {'form': form})
            
            user = form.save()
            user.email = email
            user.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to Ryder Pro.')
            return redirect('dashboard')
        else:
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{field.label}: {error}")
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'accounts/signup.html', {'form': form})

def oauth_login(request, provider):
    supabase = get_supabase(request)
    if not supabase:
        messages.error(request, "Supabase is not configured.")
        return redirect('login')
        
    try:
        res = supabase.auth.sign_in_with_oauth({
            "provider": provider,
            "options": {
                "redirect_to": request.build_absolute_uri(reverse('oauth_callback')),
            }
        })
        return redirect(res.url)
    except Exception as e:
        messages.error(request, f"Failed to connect to {provider}: {str(e)}")
        return redirect('login')

def oauth_callback(request):
    supabase = get_supabase(request)
    code = request.GET.get('code')
    if code and supabase:
        try:
            res = supabase.auth.exchange_code_for_session({"auth_code": code})
            if res.user:
                email = res.user.email
                user, created = User.objects.get_or_create(username=email)
                if created:
                    user.email = email
                    user.set_unusable_password()
                    user.save()
                login(request, user)
                messages.success(request, 'Successfully logged in!')
                return redirect('dashboard')
        except Exception as e:
            messages.error(request, f"Authentication failed: {str(e)}")
            return redirect('login')
            
    return render(request, 'accounts/oauth_callback.html')
