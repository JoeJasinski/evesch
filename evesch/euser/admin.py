from django.contrib import admin
from euser.models import User,UserEmail,UserIM,UserGroup

class UserAdmin(admin.ModelAdmin):
    list_display = ['username','last_name','first_name','gender','email_addresses']
class UserEmailAdmin(admin.ModelAdmin):
    list_display = ['email_label','email_address','email_type','email_privacy','email_isDefault']
class UserIMAdmin(admin.ModelAdmin):
    list_display = ['im_name','im_protocol_type','im_privacy','im_isDefault']
class UserGroupAdmin(admin.ModelAdmin):
    list_display = ['group_name','group_hash','org_name',]

admin.site.register(User, UserAdmin)
admin.site.register(UserEmail, UserEmailAdmin)
admin.site.register(UserIM, UserIMAdmin)
admin.site.register(UserGroup, UserGroupAdmin)