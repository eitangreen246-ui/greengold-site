from django import forms

from .models import Lead

INPUT = (
    "mt-1 block w-full rounded-lg border border-black/15 bg-white px-3.5 py-2.5 text-ink "
    "shadow-sm placeholder:text-ink/40 focus:border-forest focus:outline-none "
    "focus:ring-2 focus:ring-forest/30"
)


class HoneypotMixin(forms.ModelForm):
    """Adds a hidden 'website' field. Bots fill it; humans never see it."""

    website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"tabindex": "-1", "autocomplete": "off", "class": "hidden"}),
        label="Leave this field empty",
    )

    def clean_website(self):
        if self.cleaned_data.get("website"):
            raise forms.ValidationError("Spam detected.")
        return ""


class ManufacturerForm(HoneypotMixin):
    audience_value = "manufacturer"

    class Meta:
        model = Lead
        fields = ["name", "email", "company", "interest", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": INPUT, "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"class": INPUT, "autocomplete": "email"}),
            "company": forms.TextInput(attrs={"class": INPUT, "autocomplete": "organization"}),
            "interest": forms.Select(attrs={"class": INPUT}),
            "message": forms.Textarea(attrs={"class": INPUT, "rows": 4,
                                             "placeholder": "Tell us about your active, product or challenge."}),
        }
        labels = {"interest": "What do you need?", "message": "Project details"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].required = True
        self.fields["email"].required = True
        self.fields["company"].required = True

    def save(self, commit=True):
        lead = super().save(commit=False)
        lead.audience = self.audience_value
        if commit:
            lead.save()
        return lead


class PartnerForm(HoneypotMixin):
    audience_value = "partner"

    class Meta:
        model = Lead
        fields = ["name", "email", "company", "product_name", "target_market", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": INPUT, "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"class": INPUT, "autocomplete": "email"}),
            "company": forms.TextInput(attrs={"class": INPUT, "autocomplete": "organization"}),
            "product_name": forms.TextInput(attrs={"class": INPUT,
                                                   "placeholder": "e.g. marine peptide complex"}),
            "target_market": forms.TextInput(attrs={"class": INPUT,
                                                    "placeholder": "e.g. EU skincare brands"}),
            "message": forms.Textarea(attrs={"class": INPUT, "rows": 4,
                                             "placeholder": "Anything else we should know?"}),
        }
        labels = {"product_name": "Product / material", "target_market": "Target market",
                  "message": "More detail"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["name"].required = True
        self.fields["email"].required = True
        self.fields["company"].required = True
        self.fields["product_name"].required = True

    def save(self, commit=True):
        lead = super().save(commit=False)
        lead.audience = self.audience_value
        if commit:
            lead.save()
        return lead
