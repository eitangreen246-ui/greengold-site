from django.db import models
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from .blocks import ContentStream


class ContentPage(Page):
    """Flexible content page used for Delivery Systems, Formulation, Ingredients,
    Partner With Us, and About. All content is editable via the hero fields + body."""

    hero_badge = models.CharField(
        max_length=80, blank=True,
        help_text="Small label above the title, e.g. 'For cosmetics manufacturers'.",
    )
    hero_heading = models.CharField(max_length=200, blank=True)
    hero_intro = models.TextField(blank=True)
    hero_cta_label = models.CharField(max_length=60, blank=True)
    hero_cta_page = models.ForeignKey(
        "wagtailcore.Page", null=True, blank=True, on_delete=models.SET_NULL, related_name="+"
    )

    body = StreamField(ContentStream(), blank=True, use_json_field=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("hero_badge"),
                FieldPanel("hero_heading"),
                FieldPanel("hero_intro"),
                FieldPanel("hero_cta_label"),
                FieldPanel("hero_cta_page"),
            ],
            heading="Hero",
        ),
        FieldPanel("body"),
    ]


class ContactPage(Page):
    """Contact / Get Started — hosts the two audience intake forms.

    Form handling, validation, lead storage and email are wired up in the leads
    app (serve() override) in a later phase; the page owns the editable copy."""

    max_count = 1

    hero_heading = models.CharField(max_length=200, default="Get started")
    hero_intro = models.TextField(
        blank=True,
        default="Tell us who you are and what you're working on — we'll route your enquiry to the right specialist.",
    )

    manufacturer_form_title = models.CharField(
        max_length=120, default="I'm a cosmetics manufacturer"
    )
    manufacturer_form_intro = models.TextField(
        blank=True,
        default="Delivery systems, formulation, or a unique ingredient — tell us about your project.",
    )
    partner_form_title = models.CharField(
        max_length=120, default="I'm a raw-material manufacturer"
    )
    partner_form_intro = models.TextField(
        blank=True,
        default="Looking for distribution and cosmetic-market access? Share your product and target market.",
    )
    thank_you_text = models.CharField(
        max_length=200,
        default="Thank you — we've received your enquiry and will be in touch shortly.",
    )

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [FieldPanel("hero_heading"), FieldPanel("hero_intro")], heading="Hero"
        ),
        MultiFieldPanel(
            [FieldPanel("manufacturer_form_title"), FieldPanel("manufacturer_form_intro")],
            heading="Manufacturer form copy",
        ),
        MultiFieldPanel(
            [FieldPanel("partner_form_title"), FieldPanel("partner_form_intro")],
            heading="Partner form copy",
        ),
        FieldPanel("thank_you_text"),
    ]

    def serve(self, request, *args, **kwargs):
        from django.shortcuts import redirect
        from django.template.response import TemplateResponse

        from leads.emails import send_lead_notification
        from leads.forms import ManufacturerForm, PartnerForm

        manufacturer_form = ManufacturerForm(prefix="m")
        partner_form = PartnerForm(prefix="p")

        if request.method == "POST":
            form_type = request.POST.get("form_type")
            if form_type == "manufacturer":
                manufacturer_form = ManufacturerForm(request.POST, prefix="m")
                if manufacturer_form.is_valid():
                    send_lead_notification(manufacturer_form.save())
                    return redirect(f"{self.url}?sent=manufacturer#manufacturer")
            elif form_type == "partner":
                partner_form = PartnerForm(request.POST, prefix="p")
                if partner_form.is_valid():
                    send_lead_notification(partner_form.save())
                    return redirect(f"{self.url}?sent=partner#partner")

        return TemplateResponse(
            request,
            self.get_template(request),
            {
                "page": self,
                "manufacturer_form": manufacturer_form,
                "partner_form": partner_form,
                "sent": request.GET.get("sent"),
            },
        )
