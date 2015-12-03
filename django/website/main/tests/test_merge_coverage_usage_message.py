from main.management.commands.merge_coverage_files import Command


def test_usage_returns_help_string():
    merge_coverage_files_command = Command()

    usage_string = (
        '%%prog [options] [file1 file2 ... filen]\n\nMerges the specified '
        'xml coverage reports\n\nIf no files are '
        'specified all xml files in current directory will be selected. '
        '\nUseful when there is not known precise file name only location'
    )

    assert usage_string == merge_coverage_files_command.usage('')