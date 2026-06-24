from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from ryder_pro.supabase_client import get_supabase

class SupabaseAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        supabase = get_supabase()
        if not supabase:
            return super().authenticate(request, username, password, **kwargs)
            
        try:
            # Try logging into Supabase with the username (which might be an email) and password
            res = supabase.auth.sign_in_with_password({"email": username, "password": password})
            if res.user:
                # Find or create the local Django user
                user, created = User.objects.get_or_create(username=username)
                if created:
                    user.email = username
                    user.set_unusable_password()
                    user.save()
                return user
        except Exception as e:
            # Maybe the username is an actual username, not email.
            try:
                local_user = User.objects.get(username=username)
                res = supabase.auth.sign_in_with_password({"email": local_user.email, "password": password})
                if res.user:
                    return local_user
            except Exception:
                pass
                
        # Fallback to local authentication
        return super().authenticate(request, username, password, **kwargs)
