from django.db import models


class Lead(models.Model):
    """A contact-form submission. Doubles as the lightweight CRM record
    (managed in the Django admin)."""

    AUDIENCE_CHOICES = [
        ("manufacturer", "Cosmetics manufacturer"),
        ("partner", "Raw-material manufacturer"),
    ]
    INTEREST_CHOICES = [
        ("delivery_systems", "Delivery systems"),
        ("formulation", "Formulation"),
        ("ingredient", "Unique ingredient"),
        ("other", "Other / not sure"),
    ]
    STATUS_CHOICES = [
        ("new", "New"),
        ("contacted", "Contacted"),
        ("qualified", "Qualified"),
        ("closed", "Closed"),
    ]

    audience = models.CharField(max_length=20, choices=AUDIENCE_CHOICES)
    name = models.CharField(max_length=120)
    email = models.EmailField()
    company = models.CharField(max_length=160, blank=True)
    phone = models.CharField(max_length=40, blank=True)

    # Manufacturer-specific
    interest = models.CharField(max_length=30, choices=INTEREST_CHOICES, blank=True)

    # Partner-specific
    product_name = models.CharField(max_length=160, blank=True)
    target_market = models.CharField(max_length=160, blank=True)

    message = models.TextField(blank=True)

    # CRM fields
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")
    notes = models.TextField(blank=True, help_text="Internal notes (not shown to the lead).")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.get_audience_display()})"
