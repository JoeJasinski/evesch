from django.contrib import admin
from evesch.euser.models import eUser,UserIM,UserGroup
from django.contrib.auth.admin import UserAdmin 

class eUserAdmin(UserAdmin):
    pass
class UserIMAdmin(admin.ModelAdmin):
    list_display = ['im_name','im_protocol_type','im_privacy','im_isDefault']
class UserGroupAdmin(admin.ModelAdmin):
    list_display = ['group_name','group_hash','org_name',]

admin.site.register(eUser, eUserAdmin)
admin.site.register(UserIM, UserIMAdmin)
admin.site.register(UserGroup, UserGroupAdmin)