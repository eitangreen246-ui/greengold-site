import pytest
from django.core.management import call_command


@pytest.fixture
def seeded(db):
    """Build the full page tree once for tests that need real pages."""
    call_command("seed_site")
