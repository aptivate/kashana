from django.core.exceptions import ValidationError
from floppyforms.__future__.models import ModelForm
from logframe.models import LogFrame


class CreateLogFrameForm(ModelForm):
    class Meta(object):
        model = LogFrame
        fields = ('name',)

    def clean_name(self):
        if LogFrame.objects.filter(name=self.cleaned_data['name']).exists():
            raise ValidationError("A Logframe with this name already exists")
        if not self.cleaned_data['name'].strip():
            raise ValidationError("The Logframe name must contain non-whitespace characters")
        return self.cleaned_data['name']
