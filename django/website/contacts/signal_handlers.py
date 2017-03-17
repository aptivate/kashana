from django.contrib.auth.models import Permission
from django.dispatch.dispatcher import receiver
from registration import signals


@receiver(signals.user_activated, dispatch_uid='contacts.signal_handlers.grant_create_organization_permissions')
def grant_create_organization_permissions(sender, user, request, **kwargs):
    add_org_permission = Permission.objects.get(codename='add_organization')
    add_user_permission = Permission.objects.get(codename='add_user')

    user.user_permissions.add(add_org_permission, add_user_permission)
