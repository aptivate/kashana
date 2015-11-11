from ..widgets import ColorChoiceInput


def test_color_choice_input_widget_rendering():
    color_choice_input = ColorChoiceInput('color_widget', 1, {'id': '1'}, ('blue', 'Blue'), 1)
    expected_output = '<input id="1_1" name="color_widget" type="radio" value="blue" /> <label for="1_1" class="color-tag blue">Blue</label>'
    actual_output = color_choice_input.render()
    assert expected_output == actual_output
