import pytest

from leads.forms import ManufacturerForm, PartnerForm


def _mfr_data(**overrides):
    data = {
        "name": "Dr Jane Cohen",
        "email": "jane@labcorp.example",
        "company": "LabCorp Cosmetics",
        "interest": "delivery_systems",
        "message": "We need a liposome system.",
        "website": "",
    }
    data.update(overrides)
    return data


def _partner_data(**overrides):
    data = {
        "name": "Sam Levi",
        "email": "sam@biotech.example",
        "company": "BioCorp",
        "product_name": "Marine peptide",
        "target_market": "EU skincare",
        "message": "",
        "website": "",
    }
    data.update(overrides)
    return data


@pytest.mark.django_db
def test_manufacturer_form_valid_sets_audience():
    form = ManufacturerForm(data=_mfr_data())
    assert form.is_valid(), form.errors
    lead = form.save()
    assert lead.audience == "manufacturer"
    assert lead.interest == "delivery_systems"


@pytest.mark.django_db
def test_manufacturer_form_requires_email():
    form = ManufacturerForm(data=_mfr_data(email=""))
    assert not form.is_valid()
    assert "email" in form.errors


def test_honeypot_blocks_spam():
    form = ManufacturerForm(data=_mfr_data(website="http://spam.example"))
    assert not form.is_valid()
    assert "website" in form.errors


@pytest.mark.django_db
def test_partner_form_valid_sets_audience():
    form = PartnerForm(data=_partner_data())
    assert form.is_valid(), form.errors
    lead = form.save()
    assert lead.audience == "partner"
    assert lead.product_name == "Marine peptide"


def test_partner_form_requires_product():
    form = PartnerForm(data=_partner_data(product_name=""))
    assert not form.is_valid()
    assert "product_name" in form.errors
