from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm

from .models import Company, User, Billing, Subscription

# Register your models here.
@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "modified", "url", "active",)
    ordering = ("-id",)


@admin.register(Billing)
class BillingAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "created_at", "modified", "company", "old_company", "active",)
    ordering = ("-id",)


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "created_at", "modified", "company", "old_company", "subscription", "active", "hidden",)
    ordering = ("-id",)



# Merging the official Django auth admin with the custom user model
class NewUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

class NewUserAdmin(UserAdmin):
    form = NewUserChangeForm

    list_display = UserAdmin.list_display + ("company", "company_joined",)

    fieldsets = UserAdmin.fieldsets + (
        ("Company related", {'fields': ('company', 'company_joined',)}),
    )

admin.site.register(User, NewUserAdmin)

