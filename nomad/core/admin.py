from django.contrib import admin
from django.conf.urls import url
from django.db import models
from django.utils import timezone
from django.utils.html import mark_safe
from django.contrib.auth.admin import UserAdmin, GroupAdmin
from django.contrib.auth.models import Group
from tinymce.widgets import TinyMCE

from core.models import User, Company, FeatureCategory, Feature, Availability, WorkLocation, Mission, Files


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'company', 'start',
                    'end', 'city', 'title', 'state', 'is_matchable',)
    fieldsets = (
        (None, {
            'fields': (
                'title', 'description',
                'company', 'is_matchable', ('driving_license_required',
                                            'year_experience_required'),
                ('start', 'end',),
                ('zipcode', 'city',),
                'features',
            )
        }),
    )

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }

    filter_horizontal = ('features', )
    readonly_fields = ('state', 'city',)
    change_list_template = 'admin/mission/mission_change_list.html'


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


class AvailabilityInline(admin.StackedInline):
    model = Availability
    extra = 2


class WorkLocationInline(admin.StackedInline):
    model = WorkLocation
    extra = 2
    fields = ('zipcode', 'city', 'department_name',
              'region', ('longitude', 'latitude'), )
    readonly_fields = ('city', 'department_name',
                       'region', 'longitude', 'latitude', )


class FilesInline(admin.StackedInline):
    model = Files
    extra = 2


@admin.register(User)
class UserAdmin(UserAdmin, admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'type',
                    'is_complete', 'is_superuser', 'is_staff', 'last_login',)
    filter_horizontal = ('features', )
    readonly_fields = ('is_complete',)

    def is_complete(self, obj):
        text = ""
        try:
            if obj.is_complete:
                bg = "green"
                status = "Complete"
            else:
                bg = "red"
                status = "Not complete"

            text = f'<span style=\"background-color: {bg}; color: white; padding: 5px; border-radius: 5px;\">{status}</span>'
        except ValueError:
            text = "<i>n/a</i>"

        return mark_safe(text)

    fieldsets = (
        (None, {
            'fields': (('email', 'is_complete'),
                       ('first_name', 'last_name',),
                       'phone', 'siret',
                       'password', ('driving_license', 'year_experience'),
                       ('type', 'company'),),
        }),
        ('Permissions', {
            'classes': ('collapse', ),
            'fields': (
                'is_active',
                'is_staff', 'is_superuser',),
        }),
        ('Dates', {
            'classes': ('collapse', ),
            'fields': ('last_login', 'date_joined')
        }),
        ('Features', {
            'classes': ('wide',),
            'fields': ('features', )
        }),
        ('Description', {
            'classes': ('wide',),
            'fields': ('description', )
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone', 'password1', 'password2'),
        }),
    )

    ordering = ('email',)
    inlines = [AvailabilityInline, WorkLocationInline, FilesInline]
    change_form_template = "admin/user/user_change.html"


class FeatureInline(admin.TabularInline):
    model = Feature
    extra = 3
    fields = ('description', 'scope',)
    # fieldsets = (
    #     (None, {
    #         'fields': (('from_dt', 'to_dt',), ),
    #     }),
    # )


@admin.register(FeatureCategory)
class FeatureCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'scope', 'multiple_choices', 'rank',)
    fieldsets = (
        (None, {
            'fields': ('name', ('scope', 'rank', 'multiple_choices', ), )
        })),

    ordering = ('rank', 'name',)
    inlines = [FeatureInline, ]


admin.site.site_header = 'Nomad-Social Dashboard'
# we don't use Django groups
admin.site.unregister(Group)
