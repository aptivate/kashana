from datetime import date
from os.path import basename
from django.utils.html import conditional_escape, format_html
from django.utils.encoding import force_text
from django.utils.safestring import mark_safe
from django.forms.widgets import CheckboxInput, MultiWidget, Select
import floppyforms as forms
from form_utils.widgets import ImageWidget
from django.forms.widgets import ClearableFileInput, Textarea, Widget


class DateInput2(forms.TextInput):
    # Javascript & CSS available through assets:
    # widget_js_date_input_2 or widget_js_all
    # widget_css_date_input_2 or widget_css_all
    def get_context(self, name, value, attrs):
        ctx = super(DateInput2, self).get_context(name, value, attrs)
        ctx['attrs']['placeholder'] = 'YYYY-MM-DD'
        ctx['attrs']['class'] = 'date-picker'
        return ctx


class YearMonthDateSelectorWidget(MultiWidget):
    def __init__(self, attrs=None):
        if not attrs:
            attrs = {}
        attrs.update({'class': 'year-month-date-selector'})
        months = [(1, 'Janury'),
                  (2, 'February'),
                  (3, 'March'),
                  (4, 'April'),
                  (5, 'May'),
                  (6, 'June'),
                  (7, 'July'),
                  (8, 'August'),
                  (9, 'September'),
                  (10, 'October'),
                  (11, 'November'),
                  (12, 'December')]
        this_year = (date.today()).year
        years = [(year, year) for year in range(2010, this_year + 7)]
        months.insert(0, ('', '----'))
        years.insert(0, ('', '----'))
        widgets = (Select(attrs=attrs, choices=months),
                   Select(attrs=attrs, choices=years))
        super(YearMonthDateSelectorWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        value_list = [None, None]
        if value:
            if isinstance(value, str) or isinstance(value, unicode):
                # e.g. 2010-10-01; [::-1] reverses list
                value_list = [int(v) for v in value.split("-")[:2][::-1]]
            else:  # Date
                value_list = [value.month, value.year]
        return value_list

    def format_output(self, rendered_widgets):
        return u''.join(rendered_widgets)

    def value_from_datadict(self, data, files, name):
        month = self.widgets[0].value_from_datadict(data, files, name + '_0')
        year = self.widgets[1].value_from_datadict(data, files, name + '_1')
        try:
            value_to_store = date(day=15, month=int(month), year=int(year))
        except ValueError:
            return ''
        else:
            return str(value_to_store)


class YearDateSelectorWidget(forms.widgets.NumberInput):
    def __init__(self, attrs=None):
        wattrs = {
            'placeholder': 'YYYY',
            'size': 4,
            'maxlength': 4,
            'class': 'year-date-selector'
        }
        if attrs:
            wattrs.update(attrs)
        super(YearDateSelectorWidget, self).__init__(wattrs)

    def render(self, name, value, attrs=None):
        if type(value) in (str, unicode):
            value = value
        elif type(value) == date:
            value = value.year
        else:
            value = ""
        return super(YearDateSelectorWidget, self).render(
            name, value, attrs)

    def value_from_datadict(self, data, files, name):
        value_to_store = None
        year = data.get(name, "")  # Cause value error if we don't have it
        try:
            year = int(year)
        except ValueError:
            return super(YearDateSelectorWidget, self).value_from_datadict(
                data, files, name)
        if year:
            value_to_store = date(day=15, month=7, year=year)
        return value_to_store


class BetterSelectMultiple(forms.SelectMultiple):
    def __init__(self, attrs=None, choices=()):
        widget_attrs = {
            'size': 10,
            'class': 'widget-multi-select'
        }
        if attrs:
            widget_attrs.update(attrs)
        super(BetterSelectMultiple, self).__init__(widget_attrs, choices)


class BetterFileInput(ClearableFileInput):
    # Javascript available through assets:
    # widget_js_better_file_input or widget_js_all
    template_with_initial = u"""
        <div class="field-clear">
            <span class="field-clear-initial">%(initial)s</span>
            <script>document.write('<span class="field-clear-check-button pure-button pure-button-xsmall pure-button-error">Remove</span><span class="field-clear-cancel pure-button-xsmall pure-button pure-button-hidden">Cancel</span>')</script>
            <div class="browse-box">%(input)s</div>
            <noscript>%(clear_template)s</noscript>
            <script>document.write('<div class="field-clear-hidden-input pure-button-hidden">%(clear)s</div>')</script>
        </div>"""
    template_with_clear = u"""
        <label for="%(clear_checkbox_id)s" class="field-clear-check">
            Remove file: %(clear)s (tick and save)
        </label>"""

    def render(self, name, value, attrs=None):
        '''Same render method as ClearableFileInput has except that it wraps
        displayed file name with os.path.basename for nicer output.'''
        substitutions = {
            'initial_text': self.initial_text,
            'input_text': self.input_text,
            'clear_template': '',
            'clear_checkbox_label': self.clear_checkbox_label,
        }
        template = '%(input)s'
        substitutions['input'] = super(ClearableFileInput, self).render(name, value, attrs)

        if value and hasattr(value, "url"):
            template = self.template_with_initial
            substitutions['initial'] = format_html(u'<a href="{0}">{1}</a>',
                                                   value.url,
                                                   basename(force_text(value)))
            if not self.is_required:
                checkbox_name = self.clear_checkbox_name(name)
                checkbox_id = self.clear_checkbox_id(checkbox_name)
                substitutions['clear_checkbox_name'] = conditional_escape(checkbox_name)
                substitutions['clear_checkbox_id'] = conditional_escape(checkbox_id)
                substitutions['clear'] = CheckboxInput().render(checkbox_name, False, attrs={'id': checkbox_id})
                substitutions['clear_template'] = self.template_with_clear % substitutions

        return mark_safe(template % substitutions)

    def value_from_datadict(self, data, files, name):
        '''
        Practically same as ClearableFileInput except that when user
        contradicts themselves, we return upload (upload wins).
        '''
        upload = super(ClearableFileInput, self).value_from_datadict(data, files, name)
        if not self.is_required and CheckboxInput().value_from_datadict(
                data, files, self.clear_checkbox_name(name)) and not upload:
            # False signals to clear any existing value, as opposed to just None
            return False
        return upload


class BetterImageInput(ClearableFileInput, ImageWidget):
    template = u"""
            <span class="field-clear-initial">%(image)s</span>
            <br />
            <script>document.write('<span class="field-clear-check-button pure-button pure-button-xsmall pure-button-error">Remove</span><span class="field-clear-cancel pure-button-xsmall pure-button pure-button-hidden">Cancel</span>')</script>
            <div class="browse-box">%(input)s</div>
    """
    template_with_clear = u"""
        <label for="%(clear_checkbox_id)s" class="field-clear-check">
            Remove file: %(clear)s (tick and save)
        </label>"""
    template_with_initial = u"""
        <div class="field-clear">
            %(input)s
            <noscript>%(clear_template)s</noscript>
            <script>document.write('<span class="field-clear-hidden-input pure-button pure-button-xsmall pure-button-hidden">%(clear)s</span>')</script>
        </div>"""


class TextareaWordLimit(Textarea):
    # Javascript & CSS available through assets:
    # widget_js_all

    def __init__(self, attrs=None):
        w_attrs = {'class': "input-word-limit"}
        if attrs:
            w_attrs.update(attrs)
        super(TextareaWordLimit, self).__init__(w_attrs)


class PrintValueWidget(Widget):
    '''
    Prints value

    You can control the output by providing following attributes:
    - formatter, which should be a callable that receives a value and returns
    the formatted version of it (default: returns unchanged)
    - template, which defines HTML template that will be used (default:
        <span>{0}</span>)
    '''
    def render(self, name, value, attrs=None):
        formatter = self.attrs.get('formatter', lambda x: x)
        template = self.attrs.get('template', u"<span>{0}</span>")
        return format_html(template.format(formatter(value)))


class ReadOnlyWidget(PrintValueWidget):
    # By default PrintValueWidget behaves like read only output
    pass
