from mock import Mock
from django.contrib.auth import get_user_model

from ..organization_backends.invitation_backend import InvitationBackend


def test_sending_invite_works_with_business_email_as_username():
    view = InvitationBackend()
    view.user_model = Mock(spec=get_user_model(), objects=Mock(return_value=Mock(get=Mock())))

    view.invite_by_email('test@example.com')

    view.user_model.objects.get.assert_called_with(business_email='test@example.com')
