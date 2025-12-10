from allauth.socialaccount.providers.mediawiki.provider import settings
from django.shortcuts import render
from .models import SiteSetting, ContactInfo

# Create your views here.

def contact_page(request):
    try:
        site_settings = SiteSetting.objects.get()
    except SiteSetting.DoesNotExist:
        site_settings = None

    try:
        contact_info = ContactInfo.objects.first()
    except ContactInfo.DoesNotExist:
        contact_info = None

    context = {
        'settings': site_settings,
        'contact_info': contact_info,
    }
    return render(request, 'core/contact.html', context)