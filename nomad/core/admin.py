from django.contrib import admin
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group

from core.models import User, Company, FeatureCategory, Feature


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
    list_display = ('name', 'type', )
    ordering = ('name',)

    fieldsets = (
        (None, {
            'fields': ('name', )
        }),
        ('Features', {
            'fields':  ('type', 'siret', 'vat_excluded', )
        }),
        ('Location', {
            'fields': ('address', 'zipcode', 'city', )
        })
    )

    inlines = [CompanyUserInline, ]

@admin.register(User)
class UserAdmin(UserAdmin, admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'type', 'is_superuser', 'is_staff', 'last_login',)
    filter_horizontal = ('features', )

    fieldsets = (
        (None, {
            'fields': ('email',
                       ('first_name', 'last_name',),
                       'phone',
                       'password',
                       ('type', 'company'),),
        }),
        ('Features', {
            'fields': ('features', )
        }),
        ('Permissions', {
            'fields': (
                'is_active',
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


class FeatureInline(admin.StackedInline):
    model = Feature
    extra = 3


@admin.register(FeatureCategory)
class FeatureCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'rank', 'multiple_choices', )
    fieldsets = (
        (None, {
            'fields': ('name', ('rank', 'multiple_choices',), )
        })),

    ordering = ('rank', 'name',)
    inlines = [FeatureInline, ]


admin.site.site_header = 'Nomad-Social Dashboard'

# we don't use Django groups
admin.site.unregister(Group)

