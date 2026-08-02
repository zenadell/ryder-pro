from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags

import json
import logging
import threading
from urllib.request import Request, urlopen


logger = logging.getLogger(__name__)


def _send_message(msg, to_email):
    """Send through Resend when configured, otherwise use Django SMTP."""
    resend_api_key = getattr(settings, 'RESEND_API_KEY', '')
    if not resend_api_key:
        return msg.send(fail_silently=False)

    html_content = next(
        (content for content, content_type in msg.alternatives if content_type == 'text/html'),
        None,
    )
    payload = {
        'from': msg.from_email,
        'to': [to_email],
        'subject': msg.subject,
        'text': msg.body,
    }
    if html_content:
        payload['html'] = html_content

    request = Request(
        'https://api.resend.com/emails',
        data=json.dumps(payload).encode('utf-8'),
        headers={
            'Authorization': f'Bearer {resend_api_key}',
            'Content-Type': 'application/json',
            'User-Agent': 'Ryder-Pro/1.0',
        },
        method='POST',
    )
    with urlopen(request, timeout=settings.EMAIL_TIMEOUT) as response:
        if response.status not in (200, 201):
            raise RuntimeError(f'Resend returned HTTP {response.status}')
    return 1


def _send_email_thread(msg, to_email):
    try:
        _send_message(msg, to_email)
    except Exception:
        logger.exception("Email delivery failed for %s", to_email)

def send_ryder_email(to_email, subject, template_name, context):
    """
    Sends a beautiful HTML email using the provided template and context.

    Email delivery is a non-critical side effect. This function must NEVER raise
    into its callers: a failure to render or queue a receipt email should not be
    able to break the payment/deposit flow that triggered it (e.g. crediting a
    wallet and then being reported to the user as "failed" because the receipt
    template blew up). Any error here is logged and swallowed.
    """
    try:
        html_content = render_to_string(template_name, context)
        text_content = strip_tags(html_content)

        msg = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email]
        )
        msg.attach_alternative(html_content, "text/html")

        # Send email in a background thread to avoid blocking the request
        thread = threading.Thread(target=_send_email_thread, args=(msg, to_email))
        thread.start()
        return True
    except Exception as e:
        print(f"Failed to build/queue email to {to_email}: {str(e)}")
        return False

def send_welcome_email(user):
    context = {
        'name': user.first_name or 'there',
    }
    return send_ryder_email(
        user.email,
        "Welcome to Ryder Pro!",
        'emails/welcome.html',
        context
    )

def send_payment_receipt(user, amount, purpose, reference):
    context = {
        'name': user.first_name or 'there',
        'amount': amount,
        'purpose': purpose,
        'reference': reference,
    }
    return send_ryder_email(
        user.email,
        f"Payment Receipt: {purpose}",
        'emails/payment_receipt.html',
        context
    )

def send_application_received(user, application_type, details):
    context = {
        'name': user.first_name or 'there',
        'application_type': application_type,
        'details': details,
    }
    return send_ryder_email(
        user.email,
        f"Application Received: {application_type}",
        'emails/application_received.html',
        context
    )

def send_withdrawal_notice(user, amount, is_fee_pending):
    context = {
        'name': user.first_name or 'there',
        'amount': amount,
        'is_fee_pending': is_fee_pending,
    }
    subject = "Withdrawal Request Received"
    if is_fee_pending:
        subject = "Action Required: Withdrawal Fee Pending"
        
    return send_ryder_email(
        user.email,
        subject,
        'emails/withdrawal_notice.html',
        context
    )

def send_failed_payment_notice(user, amount, purpose, reference, reason):
    context = {
        'name': user.first_name or 'there',
        'amount': amount,
        'purpose': purpose,
        'reference': reference,
        'reason': reason,
    }
    return send_ryder_email(
        user.email,
        f"Payment Verification Failed: {purpose}",
        'emails/failed_payment.html',
        context
    )


def send_job_application_email(applicant_email, applicant_name, job):
    """Send and report the confirmation email for a job application."""
    from django.utils import timezone
    from django.template.loader import render_to_string
    from django.utils.html import strip_tags
    from django.core.mail import EmailMultiAlternatives
    from django.conf import settings as email_settings

    try:
        context = {
            'name': applicant_name,
            'job_title': job.title,
            'job_category': job.category,
            'job_location': job.location,
            'submitted_at': timezone.now().strftime('%B %d, %Y at %I:%M %p'),
        }

        html_content = render_to_string('emails/job_application_received.html', context)
        text_content = strip_tags(html_content)
        msg = EmailMultiAlternatives(
            subject=f"Application Received: {job.title} at Ryder Pro",
            body=text_content,
            from_email=email_settings.DEFAULT_FROM_EMAIL,
            to=[applicant_email]
        )
        msg.attach_alternative(html_content, "text/html")
        delivered = _send_message(msg, applicant_email)
        if delivered != 1:
            raise RuntimeError(f"Email backend accepted {delivered} recipients")
        return True
    except Exception:
        logger.exception("Job application confirmation email failed for %s", applicant_email)
        return False
