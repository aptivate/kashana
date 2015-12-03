from mock import Mock

from main.management.commands.merge_coverage_files import Command
from main.tests.helper_methods import mock_out_unwanted_methods


def test_merge_coverage_handle_calls_parse_options():
    merge_coverage_files_command = Command()

    # We don't want these methods to run
    mock_out_unwanted_methods(merge_coverage_files_command, ['prepare_packagefilters', 'write_filtered_data', 'write_merged_data'])

    merge_coverage_files_command.parse_options = Mock()

    merge_coverage_files_command.handle()

    assert merge_coverage_files_command.parse_options.called


def test_merge_coverage_handle_calls_prepare_packagefilters():
    merge_coverage_files_command = Command()

    # We don't want these methods to run
    mock_out_unwanted_methods(merge_coverage_files_command, ['parse_options', 'write_filtered_data', 'write_merged_data'])

    merge_coverage_files_command.prepare_packagefilters = Mock()

    merge_coverage_files_command.handle()

    assert merge_coverage_files_command.prepare_packagefilters.called


def test_write_filtered_data_called_when_filteronly_is_true():
    merge_coverage_files_command = Command()
    merge_coverage_files_command.filteronly = True

    # We don't want these methods to run
    mock_out_unwanted_methods(merge_coverage_files_command, ['parse_options', 'prepare_packagefilters', 'write_merged_data'])

    merge_coverage_files_command.write_filtered_data = Mock()

    merge_coverage_files_command.handle()

    assert merge_coverage_files_command.write_filtered_data.called


def test_write_merged_data_called_when_filteronly_is_false():
    merge_coverage_files_command = Command()
    merge_coverage_files_command.filteronly = False

    # We don't want these methods to run
    mock_out_unwanted_methods(merge_coverage_files_command, ['parse_options', 'prepare_packagefilters', 'write_filtered_data'])

    merge_coverage_files_command.write_merged_data = Mock()

    merge_coverage_files_command.handle()

    assert merge_coverage_files_command.write_merged_data.called
