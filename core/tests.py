from io import BytesIO
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.contrib import admin
from django.core import mail
from django.test import SimpleTestCase, override_settings

from .models import JobApplication


class JobApplicationDeliveryTests(SimpleTestCase):
    @override_settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend')
    def test_job_application_confirmation_is_sent_to_applicant(self):
        from .emails import send_job_application_email

        job = SimpleNamespace(
            title='Fleet Coordinator',
            category='Operations',
            location='Lagos',
        )

        sent = send_job_application_email(
            applicant_email='applicant@example.com',
            applicant_name='Jane Applicant',
            job=job,
        )

        self.assertTrue(sent)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['applicant@example.com'])
        self.assertIn('Fleet Coordinator', mail.outbox[0].subject)


class JobApplicationResumeTests(SimpleTestCase):
    @patch('core.models.JobApplication')
    def test_resume_is_streamed_from_configured_storage(self, job_application_model):
        from .admin import JobApplicationAdmin

        resume = Mock()
        resume.name = 'resumes/jane-applicant.pdf'
        resume.open.return_value = BytesIO(b'%PDF-1.4 resume')
        application = SimpleNamespace(resume=resume)
        job_application_model.objects.filter.return_value.first.return_value = application
        model_admin = JobApplicationAdmin(JobApplication, admin.site)

        response = model_admin.download_resume_view(request=Mock(), application_id=7)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')
        self.assertIn('attachment;', response['Content-Disposition'])
        self.assertEqual(b''.join(response.streaming_content), b'%PDF-1.4 resume')

    @patch('core.models.JobApplication')
    def test_office_resume_opens_in_a_web_viewer(self, job_application_model):
        from .admin import JobApplicationAdmin

        resume = Mock()
        resume.name = 'resumes/jane-applicant.docx'
        resume.url = 'https://files.example.com/resumes/jane-applicant.docx'
        application = SimpleNamespace(resume=resume)
        job_application_model.objects.filter.return_value.first.return_value = application
        model_admin = JobApplicationAdmin(JobApplication, admin.site)

        response = model_admin.view_resume_view(request=Mock(), application_id=7)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(response['Location'].startswith('https://view.officeapps.live.com/'))
