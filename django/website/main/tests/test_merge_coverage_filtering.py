import os
import xml.etree.ElementTree as ET

from main.management.commands.merge_coverage_files import Command, PACKAGES_LIST


def test_filtering_xml_when_no_package_filters_includes_all_packages_in_list():
    merge_coverage_files_command = Command()

    file_path = os.path.join(os.path.dirname(__file__), 'sample_coverage_reports', 'coverage.xml')

    xml_file = ET.parse(file_path)
    included = merge_coverage_files_command.filter_xml(xml_file)

    expected_pakages = ['django.website.example5', 'django.website.example5.tests', 'src.second']
    actual_packages = [package.attrib['name'] for package in included]

    assert expected_pakages == actual_packages


def test_filtering_xml_when_no_package_filters_includes_all_packages_in_file():
    merge_coverage_files_command = Command()

    file_path = os.path.join(os.path.dirname(__file__), 'sample_coverage_reports', 'coverage.xml')

    xml_file = ET.parse(file_path)
    merge_coverage_files_command.filter_xml(xml_file)

    packages = xml_file.getroot().findall(PACKAGES_LIST)
    expected_pakages = ['django.website.example5', 'django.website.example5.tests', 'src.second']
    actual_packages = [package.attrib['name'] for package in packages]

    assert expected_pakages == actual_packages


def test_filtering_xml_when_package_filters_excludes_unwanted_packages_from_list():
    merge_coverage_files_command = Command()
    merge_coverage_files_command.packagefilters = ['^django\.website\.example5$']

    file_path = os.path.join(os.path.dirname(__file__), 'sample_coverage_reports', 'coverage.xml')

    xml_file = ET.parse(file_path)
    included = merge_coverage_files_command.filter_xml(xml_file)

    expected_pakages = ['django.website.example5']
    actual_packages = [package.attrib['name'] for package in included]

    assert expected_pakages == actual_packages


def test_filtering_xml_when_package_filters_excludes_unwanted_packages_from_file():
    merge_coverage_files_command = Command()
    merge_coverage_files_command.packagefilters = ['^django\.website\.example5$']

    file_path = os.path.join(os.path.dirname(__file__), 'sample_coverage_reports', 'coverage.xml')

    xml_file = ET.parse(file_path)
    merge_coverage_files_command.filter_xml(xml_file)

    included = xml_file.getroot().findall(PACKAGES_LIST)

    expected_packages = ['django.website.example5']
    actual_packages = [package.attrib['name'] for package in included]

    assert expected_packages == actual_packages
