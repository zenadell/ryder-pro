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
        obj.delete()
        return json.dumps({"status": "success", "message": f"Deleted {model_name} with ID {record_id}"})
    except Exception as e:
        return json.dumps({"status": "error", "message": str(e)})
