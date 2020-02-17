from django.contrib import admin
from django.contrib.auth.models import Group
from todo.forms.userForms import UserCreationForm, UserChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from todo.models import Profile,List
# from tenants.utility import tenant_schema_from_request, set_tenant_schema_for_request

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm
    model = Profile
    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name', 'last_name', 'is_admin', 'is_verified','is_active', 'created_at','updated_at')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

@admin.register(List)
class ListAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'is_done', 'priority', 'created_by', 'created_at')

    # def get_queryset(self, request, *args, **kwargs):
    #     set_tenant_schema_for_request(self.request)
    #     queryset = super().get_queryset(request, *args, **kwargs)
    #     tenant = tenant_from_request(request)
    #     queryset = queryset.filter(tenant=tenant)
    #     return queryset
        
    # def save_model(self, request, obj, form, change):
    #     set_tenant_schema_for_request(self.request)
    #     tenant = tenant_from_request(request)
    #     obj.tenant = tenant
    #     super().save_model(request, obj, form, change)

admin.site.register(Profile,UserAdmin)
admin.site.unregister(Group)
# admin.site.register(List)