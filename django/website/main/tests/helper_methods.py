import xml.etree.ElementTree as ET

from mock import Mock

from main.management.commands.merge_coverage_files import Command


def get_options():
    return {
        # The xmlfiles option requires a default value present to stop attempts
        # to read the files from disk
        'xmlfiles': ['a_test.xml'],
        'path': '',
        'loglevel': 'DEBUG',
        'filename': 'test_output.xml',
        'filteronly': False,
        'suffix': '',
        'packagefilters': ''
    }


def get_command_with_parsed_options(new_options=None):
    merge_coverage_files_command = Command()

    options = get_options()
    if new_options:
        options.update(new_options)

    merge_coverage_files_command.parse_options(**options)
    return merge_coverage_files_command


def get_line_tree():
    line_root = ET.Element('lines')
    line1 = ET.Element('line', {'number': '1', 'hits': '1'})
    line2 = ET.Element('line', {'number': '2', 'hits': '2'})

    line1.append(ET.Element('linechild1'))
    line2.append(ET.Element('linechild2'))
    line_root.extend([line1, line2])

    return line_root


def get_method_tree(method_name):
    method = ET.Element('method', {'name': method_name})
    line_root = get_line_tree()
    method.append(line_root)

    return method


def get_class_tree(filename, name):
    class_element = ET.Element('class', {'filename': filename, 'name': name})
    class_element.append(get_line_tree())

    method_root = ET.Element('methods')
    method_root.append(get_method_tree('method1'))
    method_root.append(get_method_tree('method2'))
    class_element.append(method_root)

    return class_element


def get_package_tree():
    package_element = ET.Element('package', {'name': 'tests'})

    class_root = ET.Element('classes')
    class1 = get_class_tree('tests/class1.py', 'class1')
    class2 = get_class_tree('tests/class2.py', 'class2')
    class_root.extend([class1, class2])

    package_element.append(class_root)

    return package_element


def mock_out_unwanted_methods(command, method_names):
    for name in method_names:
        setattr(command, name, Mock())
