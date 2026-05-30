import pytest

from leads.models import Lead


@pytest.mark.django_db
def test_lead_str_includes_name_and_audience():
    lead = Lead.objects.create(audience="partner", name="Zed", email="z@z.com")
    text = str(lead)
    assert "Zed" in text
    assert "Raw-material manufacturer" in text


@pytest.mark.django_db
def test_lead_defaults_to_new_status():
    lead = Lead.objects.create(audience="manufacturer", name="A", email="a@b.com")
    assert lead.status == "new"
