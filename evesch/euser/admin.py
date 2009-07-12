from django.contrib import admin
from euser.models import User,UserIM,UserGroup

class UserAdmin(admin.ModelAdmin):
    list_display = ['username','last_name','first_name','gender']
class UserIMAdmin(admin.ModelAdmin):
    list_display = ['im_name','im_protocol_type','im_privacy','im_isDefault']
class UserGroupAdmin(admin.ModelAdmin):
    list_display = ['group_name','group_hash','org_name',]

admin.site.register(User, UserAdmin)
admin.site.register(UserIM, UserIMAdmin)
admin.site.register(UserGroup, UserGroupAdmin)