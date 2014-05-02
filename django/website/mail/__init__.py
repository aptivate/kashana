# coding=utf-8
from __future__ import unicode_literals

from django.conf import settings
from django.core.mail import EmailMessage
from django.template import loader, Template, Context, TemplateDoesNotExist


DEFAULT_FROM = settings.EMAIL_BOT_ADDRESS


def notify(params, fail_silently=False, connection=None):
    fail_silently = bool(params.get('fail_silently', fail_silently))
    valid_parameters = ['subject', 'body', 'from_email', 'to', 'bcc',
                        'attachments', 'headers', 'cc', 'template_name',
                        'context', 'fail_silently']

    options = params.copy()
    bad_keys = [key for key in options if key not in valid_parameters]
    for key in bad_keys:
        del options[key]

    if 'template_name' in options and 'context' in options:
        # Build email body from template and use it instead
        template_name = options['template_name']
        try:
            template = loader.get_template(template_name)
        except TemplateDoesNotExist:
            template = Template(template_name)
        if type(options['context']) == dict:
            context = Context(options['context'])
        else:
            context = options['context']
        email_body = template.render(context)
        options['body'] = email_body
        del options['template_name']
        del options['context']

    options['from_email'] = params.get('from_email', DEFAULT_FROM)

    email = EmailMessage(connection=connection, **options)
    email.send(fail_silently)
    return email
