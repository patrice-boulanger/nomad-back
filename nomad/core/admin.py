from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group

from core.models import User, Company


class CompanyUserInline(admin.TabularInline):
    model = User
    fieldsets = (
        (None, {
            'fields': ('first_name', 'last_name', 'phone', )
        }),
    )

    def has_add_permission(self, request, obj):
        return False

    def has_change_permission(self, request, obj=None):
        return False

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    ordering = ('name',)

    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        ('Features', {
            'fields':  ('type', 'siret', 'vat_excluded',)
        }),
        ('Location', {
            'fields': ('address', 'zipcode', 'city', )
        })
    )

    inlines = [CompanyUserInline, ]

@admin.register(User)
class UserAdmin(UserAdmin, admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'type', 'is_superuser', 'is_staff', 'last_login',)

    fieldsets = (
        (None, {
            'fields': ('email',
                       ('first_name', 'last_name',),
                       'phone',
                       'password',)
        }),
        ('Permissions', {
            'fields': (
                'is_active',
                ('type', 'company'),
                'is_staff', 'is_superuser',),
        }),
        ('Dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )

    ordering = ('email',)

# we don't use Django groups
admin.site.site_header = 'Nomad-Social Dashboard'
admin.site.unregister(Group)

