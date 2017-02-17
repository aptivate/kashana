from ..widgets import ColorChoiceInput
from logframe.widgets import ColorSelect


def test_color_choice_input_widget_rendering():
    color_choice_input = ColorChoiceInput('color_widget', 1, {'id': '1'}, ('blue', 'Blue'), 1)
    expected_output = '<input id="1_1" name="color_widget" type="radio" value="blue" /> <label for="1_1" class="color-tag blue">Blue</label>'
    actual_output = color_choice_input.render()
    assert expected_output == actual_output


def test_color_choice_input_widget_not_escaped_when_rendering_color_select():
    color_choices = (('blue', 'Blue',), ('green', 'Green'))
    color_select = ColorSelect(choices=color_choices)
    expected_output = '<ul><li><input name="color" type="radio" value="blue" /> <label class="color-tag blue">Blue</label></li>\n<li><input name="color" type="radio" value="green" /> <label class="color-tag green">Green</label></li></ul>'
    actual_output = color_select.render('color', None, {}, [])
    assert expected_output == actual_output
