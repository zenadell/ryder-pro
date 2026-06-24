import os
import sys

# Add the project path to sys.path so we can load Django settings
sys.path.append('/Users/mac/Desktop/ryder-pro')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ryder_pro.settings')

import django
django.setup()

import cloudinary
import cloudinary.uploader

# Force load .env manually if needed
from dotenv import load_dotenv
load_dotenv()

media_dir = '/Users/mac/Desktop/ryder-pro/media'

print("Starting Cloudinary Upload...")
count = 0
for root, dirs, files in os.walk(media_dir):
    for file in files:
        if file.startswith('.'): continue
        
        file_path = os.path.join(root, file)
        relative_path = os.path.relpath(file_path, media_dir)
        
        # Cloudinary uses the relative path (including extension) as the public_id
        # when using django-cloudinary-storage.
        print(f"Uploading {relative_path}...")
        
        _, ext = os.path.splitext(file_path)
        
        try:
            if ext.lower() in ['.mp4', '.mov', '.avi', '.webm']:
                cloudinary.uploader.upload(file_path, resource_type="video", public_id=relative_path, unique_filename=False, overwrite=True)
            elif ext.lower() in ['.pdf', '.doc', '.docx', '.txt']:
                cloudinary.uploader.upload(file_path, resource_type="raw", public_id=relative_path, unique_filename=False, overwrite=True)
            else:
                cloudinary.uploader.upload(file_path, resource_type="image", public_id=relative_path, unique_filename=False, overwrite=True)
            print(f"Success: {relative_path}")
            count += 1
        except Exception as e:
            print(f"Failed to upload {relative_path}: {e}")

print(f"Finished uploading {count} files.")
