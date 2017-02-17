from django.forms import widgets
from django.forms.widgets import ChoiceFieldRenderer
from django.utils.encoding import force_text
from django.utils.html import format_html
from django.utils.safestring import mark_safe


class ColorChoiceInput(widgets.RadioChoiceInput):
    def render(self, name=None, value=None, attrs=None, choices=()):
        if 'id' in self.attrs:
            label_for = format_html(' for="{0}"', self.attrs['id'])
        else:
            label_for = ''
        label_cls = format_html(' class="color-tag {0}"', self.choice_value)
        return format_html('{2} <label{0}{1}>{3}</label>',
                           label_for, label_cls, self.tag(), self.choice_label)


class ColorFieldRenderer(widgets.ChoiceFieldRenderer):
    choice_input_class = ColorChoiceInput

    def render(self):
        """
        Outputs a <ul> for this set of choice fields.
        If an id was given to the field, it is applied to the <ul> (each
        item in the list will get an id of `$id_$i`).

        This was copied from ChoiceFieldRenderer to stop the various list items
        being escaped when rendered
        """
        id_ = self.attrs.get('id', None)
        output = []
        for i, choice in enumerate(self.choices):
            choice_value, choice_label = choice
            if isinstance(choice_label, (tuple, list)):
                attrs_plus = self.attrs.copy()
                if id_:
                    attrs_plus['id'] += '_{}'.format(i)
                sub_ul_renderer = ChoiceFieldRenderer(name=self.name,
                                                      value=self.value,
                                                      attrs=attrs_plus,
                                                      choices=choice_label)
                sub_ul_renderer.choice_input_class = self.choice_input_class
                output.append(format_html(self.inner_html, choice_value=choice_value,
                                          sub_widgets=sub_ul_renderer.render()))
            else:
                w = self.choice_input_class(self.name, self.value,
                                            self.attrs.copy(), choice, i)
                output.append(format_html(self.inner_html,
                                          choice_value=mark_safe(force_text(w)), sub_widgets=''))
        return format_html(self.outer_html,
                           id_attr=format_html(' id="{}"', id_) if id_ else '',
                           content=mark_safe('\n'.join(output)))


class ColorSelect(widgets.RadioSelect):
    renderer = ColorFieldRenderer
