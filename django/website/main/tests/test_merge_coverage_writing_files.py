import os

from django.core.files.base import ContentFile

from mock import Mock

from main.management.commands.merge_coverage_files import Command
from main.tests.helper_methods import get_package_tree


def test_writing_filtered_data_calls_filter_xml_once_per_file():
    merge_coverage_files_command = Command()

    merge_coverage_files_command.filter_xml = Mock(return_value=[get_package_tree(), get_package_tree()])

    coverage_path = os.path.join(os.path.dirname(__file__), 'sample_coverage_reports')

    merge_coverage_files_command.path = coverage_path
    report1_path = os.path.join(coverage_path, 'cobertura-coverage.xml')
    report2_path = os.path.join(coverage_path, 'coverage.xml')

    merge_coverage_files_command.xmlfiles = [report1_path, report2_path]
    merge_coverage_files_command.write_filtered_data()

    assert 2 == merge_coverage_files_command.filter_xml.call_count


def test_writing_merged_data_calls_filter_xml_once_with_one_file():
    merge_coverage_files_command = Command()
    merge_coverage_files_command.filter_xml = Mock(return_value=[get_package_tree(), get_package_tree()])

    coverage_path = os.path.join(os.path.dirname(__file__), 'sample_coverage_reports')

    merge_coverage_files_command.path = coverage_path
    report1_path = os.path.join(coverage_path, 'cobertura-coverage.xml')
    merge_coverage_files_command.finalxml = ContentFile('')

    merge_coverage_files_command.xmlfiles = [report1_path]

    merge_coverage_files_command.write_merged_data()

    assert 1 == merge_coverage_files_command.filter_xml.call_count


def test_writing_merged_data_calls_merge_xml_once_with_two_files():
    merge_coverage_files_command = Command()
    merge_coverage_files_command.merge_xml = Mock()

    coverage_path = os.path.join(os.path.dirname(__file__), 'sample_coverage_reports')

    merge_coverage_files_command.path = coverage_path
    report1_path = os.path.join(coverage_path, 'cobertura-coverage.xml')
    report2_path = os.path.join(coverage_path, 'coverage.xml')

    merge_coverage_files_command.xmlfiles = [report1_path, report2_path]
    merge_coverage_files_command.write_merged_data()

    assert 1 == merge_coverage_files_command.merge_xml.call_count


def test_writing_merged_data_calls_merge_xml_an_additonal_time_for_ervey_file_after_the_second():
    merge_coverage_files_command = Command()
    merge_coverage_files_command.merge_xml = Mock()

    coverage_path = os.path.join(os.path.dirname(__file__), 'sample_coverage_reports')

    merge_coverage_files_command.path = coverage_path
    report1_path = os.path.join(coverage_path, 'cobertura-coverage.xml')
    report2_path = os.path.join(coverage_path, 'coverage.xml')

    merge_coverage_files_command.xmlfiles = [report1_path, report2_path, report1_path, report2_path]
    merge_coverage_files_command.write_merged_data()

    assert 3 == merge_coverage_files_command.merge_xml.call_count
