from django.contrib import admin
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from .models import Settings


class SettingsAdmin(admin.ModelAdmin):
    actions_on_top = False

    def delete_view(self, request, object_id, extra_context=None):
        return HttpResponseRedirect(reverse("admin:index"))

    def add_view(self, request, form_url="", extra_context=None):
        return HttpResponseRedirect(reverse("admin:index"))

    def change_view(self, request, obj_id, form_url="", extra_ctx=None):
        changelist_url = reverse("admin:appconf_settings_changelist")
        response = super(SettingsAdmin, self).change_view(
            request, obj_id, form_url, extra_ctx)
        if request.method == "POST" and response.url == changelist_url:
            return HttpResponseRedirect(reverse("admin:index"))
        return response

    def changelist_view(self, request, extra_ctx=None):
        conf = Settings.objects.get()
        return HttpResponseRedirect(reverse("admin:appconf_settings_change", args=[conf.id]))


admin.site.register(Settings, SettingsAdmin)
