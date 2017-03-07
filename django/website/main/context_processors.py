import os

from django.conf import settings


def deploy_env(request):
    """
    Add the deploy environment and debug mode so we can show it when useful
    """
    import local_settings
    if hasattr(local_settings, 'DEPLOY_ENV'):
        deploy_env = local_settings.DEPLOY_ENV
    else:
        local_settings_file = os.path.join(os.path.dirname(__file__), os.pardir, 'local_settings.py')
        if os.path.exists(local_settings_file):
            deploy_env = os.readlink(local_settings_file).split('.')[-1]
        else:
            deploy_env = "Unknown deploy environment"
    extra_context = {'deploy_env': deploy_env,
                     'DEBUG_MODE': getattr(settings, "DEBUG", False)}
    return extra_context


def logframe_list(request):
    from logframe.models import LogFrame
    if request.user.is_authenticated():
        extra_context = {'logframe_list': LogFrame.objects.filter(organization__in=request.user.organizations_organization.all())}
    else:
        extra_context = {'logframe_list': []}
    return extra_context


def organization_list(request):
    if request.user.is_authenticated():
        extra_context = {'organization_list': request.user.organizations_organization.all()}
    else:
        extra_context = {'organization_list': []}
    return extra_context
