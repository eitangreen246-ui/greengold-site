import pytest

from leads.models import Lead

PATHS = [
    "/",
    "/delivery-systems/",
    "/formulation/",
    "/ingredients/",
    "/partner/",
    "/about/",
    "/contact/",
]


@pytest.mark.parametrize("path", PATHS)
def test_pages_render(client, seeded, path):
    response = client.get(path)
    assert response.status_code == 200


def test_home_shows_tagline_and_paths(client, seeded):
    content = client.get("/").content.decode()
    assert "Bridging Science to Tomorrow" in content
    assert "cosmetics manufacturer" in content
    assert "raw-material manufacturer" in content


def test_seo_meta_present(client, seeded):
    content = client.get("/about/").content.decode()
    assert "<title>" in content
    assert 'name="description"' in content
    assert 'property="og:title"' in content


def test_sitemap_and_robots(client, seeded):
    assert client.get("/sitemap.xml").status_code == 200
    robots = client.get("/robots.txt")
    assert robots.status_code == 200
    assert "Sitemap:" in robots.content.decode()


def test_contact_post_creates_lead_and_redirects(client, seeded):
    data = {
        "form_type": "manufacturer",
        "m-name": "Test User",
        "m-email": "test@example.com",
        "m-company": "TestCo",
        "m-interest": "formulation",
        "m-message": "Hi",
        "m-website": "",
    }
    response = client.post("/contact/", data)
    assert response.status_code == 302
    assert Lead.objects.filter(email="test@example.com", audience="manufacturer").exists()


def test_contact_honeypot_blocks_lead(client, seeded):
    data = {
        "form_type": "manufacturer",
        "m-name": "Bot",
        "m-email": "bot@spam.example",
        "m-company": "SpamCo",
        "m-message": "spam",
        "m-website": "http://spam.example",
    }
    response = client.post("/contact/", data)
    assert response.status_code == 200  # re-rendered, not redirected
    assert not Lead.objects.filter(email="bot@spam.example").exists()
