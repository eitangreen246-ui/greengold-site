import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import Lead


@admin.action(description="Export selected leads to CSV")
def export_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="leads.csv"'
    writer = csv.writer(response)
    writer.writerow([
        "Created", "Audience", "Status", "Name", "Email", "Company", "Phone",
        "Interest", "Product", "Target market", "Message",
    ])
    for lead in queryset:
        writer.writerow([
            lead.created_at.isoformat(), lead.get_audience_display(),
            lead.get_status_display(), lead.name, lead.email, lead.company, lead.phone,
            lead.get_interest_display() if lead.interest else "",
            lead.product_name, lead.target_market, lead.message,
        ])
    return response


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "audience", "company", "email", "status", "created_at")
    list_filter = ("audience", "status", "created_at")
    search_fields = ("name", "email", "company", "product_name", "target_market", "message")
    list_editable = ("status",)
    date_hierarchy = "created_at"
    readonly_fields = (
        "audience", "name", "email", "company", "phone", "interest",
        "product_name", "target_market", "message", "created_at",
    )
    fieldsets = (
        ("Lead", {"fields": (
            "created_at", "audience", "name", "email", "company", "phone",
            "interest", "product_name", "target_market", "message",
        )}),
        ("CRM", {"fields": ("status", "notes")}),
    )
    actions = [export_csv]
