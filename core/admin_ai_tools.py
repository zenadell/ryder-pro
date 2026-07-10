import json
from django.apps import apps
from django.core.serializers import serialize
from django.db.models import Model
from datetime import datetime, date, time
from uuid import UUID

def get_model_class(model_name: str):
    """
    Find a Django model by its class name across allowed apps.
    Allowed apps: core, accounts, auth
    """
    allowed_apps = ['core', 'accounts', 'auth']
    for app_label in allowed_apps:
        try:
            model = apps.get_model(app_label, model_name)
            return model
        except LookupError:
            continue
    raise ValueError(f"Model '{model_name}' not found or not permitted.")

def json_serializable(val):
    if isinstance(val, (datetime, date, time)):
        return val.isoformat()
    if isinstance(val, UUID):
        return str(val)
    if isinstance(val, Model):
        return val.pk
    return val

def list_models():
    """
    Returns a list of all models and their fields.
    """
    allowed_apps = ['core', 'accounts', 'auth']
    result = []
    
    for app_label in allowed_apps:
        app_config = apps.get_app_config(app_label)
        for model in app_config.get_models():
            model_info = {
                "model_name": model.__name__,
                "app": app_label,
                "fields": [f.name for f in model._meta.fields]
            }
            result.append(model_info)
            
    return json.dumps(result)

def query_records(model_name: str, filters: dict = None, limit: int = 50):
    """
    Query records from a specific model.
    """
    try:
        model = get_model_class(model_name)
        qs = model.objects.all()
        
        if filters:
            qs = qs.filter(**filters)
            
        qs = qs[:limit]
        
        # Serialize the queryset to a list of dicts
        data = []
        for obj in qs:
            obj_data = {}
            for field in model._meta.fields:
                try:
                    val = getattr(obj, field.name)
                    obj_data[field.name] = json_serializable(val)
                except Exception:
                    pass
            data.append(obj_data)
            
        return json.dumps({"status": "success", "count": len(data), "data": data})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def create_record(model_name: str, data: dict):
    """
    Create a new record in a specific model.
    """
    try:
        model = get_model_class(model_name)
        
        # Special handling for User model password
        if model.__name__ == 'User' and 'password' in data:
            password = data.pop('password')
            obj = model.objects.create(**data)
            obj.set_password(password)
            obj.save()
        else:
            obj = model.objects.create(**data)
            
        return json.dumps({"status": "success", "message": f"Created {model_name} with ID {obj.pk}", "id": obj.pk})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def update_record(model_name: str, record_id, data: dict):
    """
    Update an existing record.
    """
    try:
        model = get_model_class(model_name)
        obj = model.objects.get(pk=record_id)
        
        if model.__name__ == 'User' and 'password' in data:
            password = data.pop('password')
            obj.set_password(password)
            
        for key, value in data.items():
            setattr(obj, key, value)
            
        obj.save()
        return json.dumps({"status": "success", "message": f"Updated {model_name} with ID {record_id}"})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def delete_record(model_name: str, record_id):
    """
    Delete an existing record.
    """
    try:
        model = get_model_class(model_name)
        obj = model.objects.get(pk=record_id)
        
        # If deleting a User, also delete from Supabase auth.users
        if model.__name__ == 'User':
            email = obj.email
            from django.db import connection
            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM auth.users WHERE email = %s', [email])
                
        obj.delete()
        return json.dumps({"status": "success", "message": f"Deleted {model_name} with ID {record_id}"})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

import os
from django.conf import settings


def _safe_full_path(filepath: str):
    """Resolve `filepath` inside the project and refuse anything that escapes it
    (absolute paths, `..` traversal). Returns the absolute path or raises."""
    base_dir = os.path.realpath(str(settings.BASE_DIR))
    full_path = os.path.realpath(os.path.join(base_dir, filepath or ''))
    if full_path != base_dir and not full_path.startswith(base_dir + os.sep):
        raise ValueError("Path is outside the project directory and is not allowed.")
    return full_path


def read_file(filepath: str):
    """
    Read the contents of a file (useful for reading templates/html).
    """
    try:
        full_path = _safe_full_path(filepath)
        if not os.path.isfile(full_path):
            return json.dumps({"status": "error", "message": "File not found."})

        with open(full_path, 'r', encoding='utf-8') as f:
            content = f.read()
        # Guard against returning an enormous file that would blow up the AI's context.
        if len(content) > 24000:
            content = content[:24000] + "\n... [truncated — file is longer]"
        return json.dumps({"status": "success", "content": content})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})

def edit_file(filepath: str, content: str):
    """
    Overwrite a file with new content.
    """
    try:
        full_path = _safe_full_path(filepath)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        with open(full_path, 'w', encoding='utf-8') as f:
            f.write(content or '')
        return json.dumps({"status": "success", "message": f"File {filepath} updated successfully."})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})
