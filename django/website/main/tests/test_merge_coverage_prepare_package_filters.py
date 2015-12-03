from main.tests.helper_methods import get_command_with_parsed_options


def test_prepare_package_filters_returns_none_when_no_package_filters():
    merge_coverage_files_command = get_command_with_parsed_options({
        'packagefilters': [],
    })

    assert merge_coverage_files_command.prepare_packagefilters() is None


def test_prepare_package_filters_converts_filters_to_regex():
    merge_coverage_files_command = get_command_with_parsed_options({
        'packagefilters': ['missingletters', 'test1.class', 'test2.*'],
    })

    assert ['^missingletters$', '^test1\.class$', '^test2\..*$'] == merge_coverage_files_command.prepare_packagefilters()