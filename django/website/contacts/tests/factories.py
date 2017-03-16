# coding=utf-8
from __future__ import unicode_literals
from datetime import datetime

from django.contrib.auth.models import Group

import factory
from organizations.models import Organization, OrganizationUser

from ..group_permissions import GroupPermissions
from ..models import User


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        abstract = False

    # must be unique so we specify and increase
    business_email = factory.Sequence(lambda n: "email%d@test.com" % n)
    first_name = factory.Sequence(lambda n: "ｆíｒѕｔ %d" % n)
    last_name = factory.Sequence(lambda n: "ｌåｓｔɭａｓｔ %d" % n)

    last_login = datetime.now()


def ContactsManagerFactory():
    group_name = 'Contacts Managers'
    try:
        group = Group.objects.get(name=group_name)
    except Group.DoesNotExist:
        # Don't run it if we don't have to (e.g. calling factory more than
        # once per test)
        GroupPermissions()._add_contacts_managers_permissions()
        group = Group.objects.get(name=group_name)
    user = UserFactory()
    user.groups.add(group)
    return user


class OrganizationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Organization
        abstract = False

    name = factory.Sequence(lambda n: u"Ộrg Ꞑame {0}".format(n))
    slug = factory.Sequence(lambda n: "org-name-{0}".format(n))


class OrganizationUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrganizationUser
        abstract = False

    user = factory.SubFactory(UserFactory)

    @classmethod
    def _generate(cls, create, attrs):
        org_slug = attrs.pop('org_slug', False)
        organization = Organization.objects.first() if Organization.objects.exists() else OrganizationFactory()
        if org_slug:
            organization.slug = org_slug
            organization.save()
        if attrs is None:
            attrs = {}
        if 'organization' not in attrs:
            attrs['organization'] = organization
        return super(OrganizationUserFactory, cls)._generate(create, attrs)
