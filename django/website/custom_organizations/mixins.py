from django.shortcuts import get_object_or_404


class GetOrgBySlugMixin(object):
    slug_field = 'org_slug'

    def get_object(self):
        model = self.get_org_model()
        return get_object_or_404(model, slug=self.kwargs[self.slug_field])
    get_organization = get_object
