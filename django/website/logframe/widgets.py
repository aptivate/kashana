from django.forms import widgets
from django.utils.html import format_html


class ColorChoiceInput(widgets.RadioChoiceInput):
    def render(self, name=None, value=None, attrs=None, choices=()):
        name = name or self.name
        value = value or self.value
        attrs = attrs or self.attrs
        if 'id' in self.attrs:
            label_for = format_html(' for="{0}_{1}"', self.attrs['id'], self.index)
        else:
            label_for = ''
        label_cls = format_html(' class="color-tag {0}"', self.choice_value)
        return format_html('{2} <label{0}{1}>{3}</label>',
                           label_for, label_cls, self.tag(), self.choice_label)


class ColorFieldRenderer(widgets.ChoiceFieldRenderer):
    choice_input_class = ColorChoiceInput


class ColorSelect(widgets.RadioSelect):
    renderer = ColorFieldRenderer
