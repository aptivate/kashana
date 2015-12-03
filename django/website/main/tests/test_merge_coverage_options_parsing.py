import os

from django.core.management.base import CommandError

import pytest

from main.tests.helper_methods import get_command_with_parsed_options
from main.management.commands.merge_coverage_files import Command


def test_parse_options_sets_path_from_path_option():
    merge_coverage_files_command = get_command_with_parsed_options({'path': '/1/2/3/'})

    assert '/1/2/3/' == merge_coverage_files_command.path


def test_finalxml_setting_is_path_plus_filename():
    merge_coverage_files_command = get_command_with_parsed_options({
        'path': '/1/2/3/',
        'filename': 'a_test.xml'
    })

    assert '/1/2/3/a_test.xml' == merge_coverage_files_command.finalxml


def test_xml_files_location_set_from_path():
    merge_coverage_files_command = get_command_with_parsed_options({
        'path': '/1/2/3/',
        'xmlfiles': ['test1.xml', 'test2.xml']
    })

    assert ['/1/2/3/test1.xml', '/1/2/3/test2.xml'] == merge_coverage_files_command.xmlfiles


def test_merge_coverage_files_with_no_xmlfiles_reads_in_from_disk():
    test_dir = os.path.dirname(__file__)
    coverage_dir = os.path.join(test_dir, 'sample_coverage_reports')

    merge_coverage_files_command = get_command_with_parsed_options({
        'path': coverage_dir,
        'xmlfiles': []
    })

    expected_files = [os.path.join(coverage_dir, the_file) for the_file in ['cobertura-coverage.xml', 'coverage.xml']]
    assert expected_files == merge_coverage_files_command.xmlfiles


def test_debug_levels_set_from_corresponding_name_in_logger():
    import logging
    logging_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    expected_levels = [
        getattr(logging, level) for level in logging_levels
    ]

    actual_levels = []
    for level in logging_levels:
        merge_coverage_files_command = get_command_with_parsed_options({
            'loglevel': level,
        })
        actual_levels.append(merge_coverage_files_command.loglevel)

    assert expected_levels == actual_levels


def test_lowercase_debug_levels_still_set_from_name_in_logger():
    import logging
    logging_levels = ['debug', 'info', 'warning', 'error', 'critical']
    expected_levels = [
        getattr(logging, level.upper()) for level in logging_levels
    ]

    actual_levels = []
    for level in logging_levels:
        merge_coverage_files_command = get_command_with_parsed_options({
            'loglevel': level,
        })
        actual_levels.append(merge_coverage_files_command.loglevel)

    assert expected_levels == actual_levels


def test_filter_only_setting_set_from_filter_only_option():
    merge_coverage_files_command = get_command_with_parsed_options({
        'filteronly': True,
    })
    assert merge_coverage_files_command.filteronly is True


def test_filter_suffix_setting_set_from_suffix_option():
    merge_coverage_files_command = get_command_with_parsed_options({
        'suffix': '.filter',
    })
    assert '.filter' == merge_coverage_files_command.filtersuffix


def test_package_filters_setting_set_from_package_filters_option():
    merge_coverage_files_command = get_command_with_parsed_options({
        'packagefilters': ['packagefilters'],
    })
    assert ['packagefilters'] == merge_coverage_files_command.packagefilters


def test_get_file_names_with_no_xml_files_raises_error():
    merge_coverage_files_command = Command()
    merge_coverage_files_command.path = os.path.join(os.path.dirname(__file__), '..', 'templates')
    with pytest.raises(CommandError):
        merge_coverage_files_command.get_xml_filenames()


def test_get_file_names_doesnt_include_output_file():
    merge_coverage_files_command = Command()

    coverage_path = os.path.join(os.path.dirname(__file__), 'sample_coverage_reports')
    merge_coverage_files_command.path = coverage_path
    merge_coverage_files_command.finalxml = os.path.join(coverage_path, 'coverage.xml')

    expected_files = [os.path.join(coverage_path, 'cobertura-coverage.xml')]
    actual_files = merge_coverage_files_command.get_xml_filenames()

    assert expected_files == actual_files
