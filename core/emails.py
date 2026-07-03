from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags

def send_ryder_email(to_email, subject, template_name, context):
    """
    Sends a beautiful HTML email using the provided template and context.
    """
    html_content = render_to_string(template_name, context)
    text_content = strip_tags(html_content)
    
    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email]
    )
    msg.attach_alternative(html_content, "text/html")
    
    try:
        msg.send(fail_silently=False)
        return True
    except Exception as e:
        print(f"Failed to send email to {to_email}: {str(e)}")
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

