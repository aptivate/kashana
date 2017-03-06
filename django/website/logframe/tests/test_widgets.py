from ..widgets import ColorChoiceInput, ColorSelect
import re


def test_color_choice_input_widget_rendering():
    color_choice_input = ColorChoiceInput('color_widget', 1, {'id': '1'}, ('blue', 'Blue'), 1)
    expected_output = '<input id="1_1" name="color_widget" type="radio" value="blue" /> <label for="1_1" class="color-tag blue">Blue</label>'
    actual_output = color_choice_input.render()
    assert expected_output == actual_output


def test_color_choice_input_widget_not_escaped_when_rendering_color_select():
    color_choices = (('blue', 'Blue',), ('green', 'Green'))
    color_select = ColorSelect(choices=color_choices)
    output = color_select.render('color', None, {}, [])
    escaped_html = re.search('(&lt;|&gt;|&quot;)', output)
    assert escaped_html is None
