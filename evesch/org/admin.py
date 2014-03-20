from django.contrib import admin
from evesch.org.models import Organization

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ['id','org_name','org_short_name','org_desc','org_email']

admin.site.register(Organization, OrganizationAdmin)
