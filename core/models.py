from django.db import models
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.settings.models import BaseGenericSetting, register_setting


@register_setting
class BrandSettings(BaseGenericSetting):
    """Editable, site-wide brand/contact details (used in footer & contact page)."""

    contact_email = models.EmailField(
        blank=True,
        default="hello@greengoldbioscience.com",
        help_text="Public contact email shown in the footer and contact page.",
    )
    phone = models.CharField(max_length=40, blank=True)
    address = models.CharField(
        max_length=255, blank=True, default="Kibbutz Dafna, Israel"
    )
    linkedin_url = models.URLField(blank=True, verbose_name="LinkedIn URL")

    panels = [
        FieldPanel("contact_email"),
        FieldPanel("phone"),
        FieldPanel("address"),
        FieldPanel("linkedin_url"),
    ]

    class Meta:
        verbose_name = "Brand & contact details"
