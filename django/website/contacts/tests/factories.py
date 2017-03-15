# coding=utf-8
from __future__ import unicode_literals
from datetime import datetime

from django.contrib.auth.models import Group

import factory
from organizations.models import Organization, OrganizationUser

from ..group_permissions import GroupPermissions
from ..models import User


class UserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = User

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
    FACTORY_FOR = Organization

    name = factory.Sequence(lambda n: u"Ộrg Ꞑame {0}".format(n))
    slug = factory.Sequence(lambda n: "org-name-{0}".format(n))


class OrganizationUserFactory(factory.django.DjangoModelFactory):
    FACTORY_FOR = OrganizationUser

    organization = Organization.objects.get() if Organization.objects.exists() else OrganizationFactory()
    user = ContactsManagerFactory()
