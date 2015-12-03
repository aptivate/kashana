import xml.etree.ElementTree as ET

from main.management.commands.merge_coverage_files import get_attributes_chain


def test_get_attributes_chain_merges_attributes_into_string_when_list_given():
    element = ET.Element('lines', {'name': 'test', 'description': ' data'})

    attributes_chain = get_attributes_chain(element, ['name', 'description'])

    assert 'test data' == attributes_chain


def test_get_attributes_chain_returns_attribute_when_given_single_name():
    element = ET.Element('lines', {'name': 'test', 'description': ' data'})

    attributes_chain = get_attributes_chain(element, 'name')

    assert 'test' == attributes_chain
