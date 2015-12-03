from main.tests.helper_methods import get_command_with_parsed_options


def test_include_package_returns_true_when_no_filters():
    merge_coverage_files_command = get_command_with_parsed_options({
        'packagefilters': [],
    })

    assert merge_coverage_files_command.include_package('test')


def test_include_package_returns_true_when_package_name_is_same_as_filter():
    merge_coverage_files_command = get_command_with_parsed_options({
        'packagefilters': ['package1.test'],
    })

    assert merge_coverage_files_command.include_package('package1.test')


def test_include_package_returns_true_when_package_subpackage_of_filter():
    merge_coverage_files_command = get_command_with_parsed_options({
        'packagefilters': ['package1.test.*'],
    })

    assert merge_coverage_files_command.include_package('package1.test.subpackage')


def test_include_package_returns_false_when_filter_exists_and_not_matched():
    merge_coverage_files_command = get_command_with_parsed_options({
        'packagefilters': ['missingletters'],
    })

    assert not merge_coverage_files_command.include_package('misingletters')