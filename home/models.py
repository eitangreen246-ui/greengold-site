from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from cms.blocks import ContentStream


class HomePage(Page):
    """Landing page — hero, dual audience path-selection, then composable body."""

    max_count = 1

    tagline = models.CharField(
        max_length=120, default="Bridging Science to Tomorrow's Beauty"
    )
    hero_heading = models.CharField(
        max_length=200,
        default="A scientific bridge between innovation and the cosmetics industry",
    )
    hero_intro = models.TextField(
        blank=True,
        default=(
            "We empower the world's leading cosmetics, dermo-cosmetics and personal-care "
            "manufacturers with custom delivery systems, science-based formulation, and "
            "novel raw materials — backed by data, not promises."
        ),
    )

    # Dual audience path selection ("I am a…")
    path_a_title = models.CharField(max_length=120, default="I'm a cosmetics manufacturer")
    path_a_text = models.CharField(
        max_length=240,
        default="Looking for custom delivery systems, formulation, or unique active ingredients.",
    )
    path_a_label = models.CharField(max_length=60, default="Explore delivery systems")
    path_a_page = models.ForeignKey(
        "wagtailcore.Page", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    path_b_title = models.CharField(max_length=120, default="I'm a raw-material manufacturer")
    path_b_text = models.CharField(
        max_length=240,
        default="Seeking distribution, industry contacts, and cosmetic-market access for your IP.",
    )
    path_b_label = models.CharField(max_length=60, default="Partner with us")
    path_b_page = models.ForeignKey(
        "wagtailcore.Page", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    body = StreamField(ContentStream(), blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("tagline"),
                FieldPanel("hero_heading"),
                FieldPanel("hero_intro"),
            ],
            heading="Hero",
        ),
        MultiFieldPanel(
            [
                FieldPanel("path_a_title"),
                FieldPanel("path_a_text"),
                FieldPanel("path_a_label"),
                FieldPanel("path_a_page"),
            ],
            heading="Audience A — cosmetics manufacturers",
        ),
        MultiFieldPanel(
            [
                FieldPanel("path_b_title"),
                FieldPanel("path_b_text"),
                FieldPanel("path_b_label"),
                FieldPanel("path_b_page"),
            ],
            heading="Audience B — raw-material manufacturers",
        ),
        FieldPanel("body"),
    ]
