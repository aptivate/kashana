import os
import xml.etree.ElementTree as ET

from django.core.files.base import ContentFile

from mock import patch, call, Mock

from main.management.commands.merge_coverage_files import (
    CLASSES_LIST, CLASSES_ROOT, LINES_LIST, LINES_ROOT, METHODS_LIST,
    METHODS_ROOT, Command, merge, merge_classes, merge_lines, merge_methods,
    merge_packages,
)
from main.tests.helper_methods import (
    get_method_tree, get_class_tree, get_package_tree
)


def test_merging_lines_combines_hits_for_equivalent_lines():
    line1 = ET.Element('line', {'hits':'1', 'number':'1'})
    line2 = ET.Element('line', {'hits':'3', 'number':'1'})

    merged_line = merge_lines(line1, line2)

    assert '4' == merged_line.attrib['hits']


def test_merging_lines_takes_largest_condition_coverage_for_equivalent_lines():
    line1 = ET.Element('line', {'hits': '1', 'condition-coverage': '25% 1/4', 'number': '1'})
    line2 = ET.Element('line', {'hits': '3', 'condition-coverage': '50% 1/2', 'number': '1'})

    # The line merge method needs both lines to have children in order to work
    line1.append(ET.Element('line1child'))
    line2.append(ET.Element('line2child'))

    merged_line = merge_lines(line1, line2)

    assert '50% 1/2' == merged_line.attrib['condition-coverage']


def test_merging_lines_takes_children_of_line_with_largest_condition_coverage_for_equivalent_lines():
    line1 = ET.Element('line', {'hits': '1', 'condition-coverage': '25% 1/4', 'number': '1'})
    line2 = ET.Element('line', {'hits': '3', 'condition-coverage': '50% 1/2', 'number': '1'})

    line1.append(ET.Element('line1child'))
    line2.append(ET.Element('line2child'))

    merged_line = merge_lines(line1, line2)

    assert line2[0].tag == merged_line[0].tag


@patch('main.management.commands.merge_coverage_files.merge')
def test_merge_method_merges_lines_from_methods(merge_command):
    method1 = get_method_tree('method1')
    method2 = get_method_tree('method2')

    merge_methods(method1, method2)

    merge_command.assert_called_with(method1.find(LINES_ROOT), method1.findall(LINES_LIST), method2.findall(LINES_LIST), 'number', merge_lines)


@patch('main.management.commands.merge_coverage_files.merge')
def test_merge_classes_merges_methods_and_lines_from_classes(merge_command):
    class1 = get_class_tree('test/classname1.py', 'classname1')
    class2 = get_class_tree('test/classname2.py', 'classname2')

    merge_classes(class1, class2)

    merge_calls = [
        call(class1.find(LINES_ROOT), class1.findall(LINES_LIST), class2.findall(LINES_LIST), 'number', merge_lines),
        call(class1.find(METHODS_ROOT), class1.findall(METHODS_LIST), class2.findall(METHODS_LIST), 'name', merge_methods),
    ]

    merge_command.assert_has_calls(merge_calls)


@patch('main.management.commands.merge_coverage_files.merge')
def test_merge_packages_merges_packages(merge_command):
    package1 = get_package_tree()
    package2 = get_package_tree()

    merge_packages(package1, package2)

    merge_command.assert_called_with(
        package1.find(CLASSES_ROOT), package1.findall(CLASSES_LIST), package2.findall(CLASSES_LIST), ['filename', 'name'], merge_classes
    )


def test_merge_method_calls_provided_function_for_merging_identical_items():
    package1 = get_package_tree()
    package2 = get_package_tree()

    package_1_classes_list = package1.findall(CLASSES_LIST)
    package_2_classes_list = package2.findall(CLASSES_LIST)

    mock_merge_function = Mock()

    expected_calls = [
        call(package_1_classes_list[0], package_2_classes_list[0]),
        call(package_1_classes_list[1], package_2_classes_list[1])
    ]

    merge([], package_1_classes_list, package_2_classes_list, ['filename', 'name'], mock_merge_function)

    mock_merge_function.assert_has_calls(expected_calls)


def test_merge_appends_missing_items_to_bottom_of_file():
    package1 = get_package_tree()
    package2 = get_package_tree()

    extra_class = get_class_tree('tests/class3.py', 'class3')

    # The root for the package tree is element 0
    package2_root = package2[0]
    package2_root.append(extra_class)

    package_1_classes_list = package1.findall(CLASSES_LIST)
    package_2_classes_list = package2.findall(CLASSES_LIST)

    dummy_root_node = []
    merge(dummy_root_node, package_1_classes_list, package_2_classes_list, ['filename', 'name'], Mock())

    assert [extra_class] == dummy_root_node


def test_merge_xml_calls_filter_xml_twice():
    merge_coverage_files_command = Command()

    merge_coverage_files_command.filter_xml = Mock(return_value=[get_package_tree(), get_package_tree()])

    coverage_path = os.path.join(os.path.dirname(__file__), 'sample_coverage_reports')

    merge_coverage_files_command.path = coverage_path
    report1_path = os.path.join(coverage_path, 'cobertura-coverage.xml')
    report2_path = os.path.join(coverage_path, 'coverage.xml')

    merge_coverage_files_command.merge_xml(report1_path, report2_path, ContentFile(''))
    assert 2 == merge_coverage_files_command.filter_xml.call_count


@patch('main.management.commands.merge_coverage_files.merge')
def test_merge_xml_calls_merge_once(merge_command):
    merge_coverage_files_command = Command()

    coverage_path = os.path.join(os.path.dirname(__file__), 'sample_coverage_reports')

    merge_coverage_files_command.path = coverage_path
    report1_path = os.path.join(coverage_path, 'cobertura-coverage.xml')
    report2_path = os.path.join(coverage_path, 'coverage.xml')

    merge_coverage_files_command.merge_xml(report1_path, report2_path, ContentFile(''))
    assert 1 == merge_command.call_count
