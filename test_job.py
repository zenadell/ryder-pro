import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'ryder_pro.settings'
django.setup()

from core.models import Job, JobApplication
from django.core.files.uploadedfile import SimpleUploadedFile

jobs = Job.objects.all()
if not jobs.exists():
    job = Job.objects.create(title="Test Job", description="Test", requirements="Test", location="Remote", category="Tech", is_featured=True)
else:
    job = jobs.first()

from core.forms import JobApplicationForm

form = JobApplicationForm(
    data={'full_name': 'Test User', 'email': 'test@example.com', 'phone': '123456'},
    files={'resume': SimpleUploadedFile('resume.pdf', b'file_content', content_type='application/pdf')}
)

if form.is_valid():
    app = form.save(commit=False)
    app.job = job
    app.save()
    print("Application saved successfully")
else:
    print("Form errors:", form.errors)
