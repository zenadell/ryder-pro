import os
from supabase import create_client, Client

def get_supabase(request=None) -> Client:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if url and key:
        if request:
            from supabase.lib.client_options import SyncClientOptions
            from supabase_auth._sync.storage import SyncSupportedStorage
            
            class DjangoSessionStorage(SyncSupportedStorage):
                def __init__(self, request):
                    self.request = request

                def get_item(self, key: str) -> str | None:
                    return self.request.session.get(key)

                def set_item(self, key: str, value: str) -> None:
                    self.request.session[key] = value
                    self.request.session.modified = True

                def remove_item(self, key: str) -> None:
                    if key in self.request.session:
                        del self.request.session[key]
                        self.request.session.modified = True

            options = SyncClientOptions(storage=DjangoSessionStorage(request))
            return create_client(url, key, options=options)
        return create_client(url, key)
    return None
