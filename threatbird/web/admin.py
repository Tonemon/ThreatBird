from django.contrib import admin

from .models import Company, Billing, Subscription

# Register your models here.
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "modified", "group", "url", "active",)
    ordering = ("-id",)


@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "created_at", "modified", "company", "old_company", "active",)
    ordering = ("-id",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "created_at", "modified", "company", "old_company", "subscription", "active", "hidden",)
    ordering = ("-id",)
