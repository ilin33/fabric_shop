from django.contrib import admin
from .models import SiteInfo, Testimonial, SocialLink, DeliveryAndPayment

admin.site.register(SiteInfo)
admin.site.register(Testimonial)

@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('platform', 'url')


admin.site.register(DeliveryAndPayment)