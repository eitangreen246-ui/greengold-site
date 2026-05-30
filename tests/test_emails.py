import pytest

from leads.emails import send_lead_notification
from leads.models import Lead


@pytest.mark.django_db
def test_send_lead_notification(mailoutbox, settings):
    settings.CONTACT_TO_EMAIL = "leads@example.com"
    lead = Lead.objects.create(
        audience="manufacturer", name="Jane", email="jane@x.com",
        company="C", message="Hello",
    )
    ok = send_lead_notification(lead)
    assert ok is True
    assert len(mailoutbox) == 1
    msg = mailoutbox[0]
    assert msg.to == ["leads@example.com"]
    assert msg.reply_to == ["jane@x.com"]
    assert "Jane" in msg.subject
    assert "Hello" in msg.body
