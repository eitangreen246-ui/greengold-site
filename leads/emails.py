import logging

from django.conf import settings
from django.core.mail import EmailMessage

logger = logging.getLogger(__name__)


def send_lead_notification(lead) -> bool:
    """Email the business inbox about a new lead. Returns True on success.

    Never raises — a mail failure must not break the form submission (the lead
    is already saved to the CRM)."""
    subject = f"New {lead.get_audience_display()} enquiry — {lead.name}"
    lines = [
        f"Audience: {lead.get_audience_display()}",
        f"Name: {lead.name}",
        f"Company: {lead.company}",
        f"Email: {lead.email}",
    ]
    if lead.phone:
        lines.append(f"Phone: {lead.phone}")
    if lead.interest:
        lines.append(f"Interest: {lead.get_interest_display()}")
    if lead.product_name:
        lines.append(f"Product/material: {lead.product_name}")
    if lead.target_market:
        lines.append(f"Target market: {lead.target_market}")
    if lead.message:
        lines.append("")
        lines.append(lead.message)
    body = "\n".join(lines)

    try:
        EmailMessage(
            subject=subject,
            body=body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.CONTACT_TO_EMAIL],
            reply_to=[lead.email],
        ).send(fail_silently=False)
        return True
    except Exception:  # noqa: BLE001 — log and continue; lead is already stored
        logger.exception("Failed to send lead notification email for lead id=%s", lead.id)
        return False
