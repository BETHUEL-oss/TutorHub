from django.contrib import admin
from .models import SiteSetting, ContactInfo

# Register your models here.
@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not SiteSetting.objects.exists()

    list_display = ('site_name', 'is_maintenance_mode')
    fieldsets = (
    ('General Site Settings', {
        'fields': ('site_name', 'is_maintenance_mode'),
    }),
    )

@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ('email', 'phone', 'support_hours')