import os
import xml.etree.ElementTree as ET
import logging
import re

from django.core.management.base import BaseCommand, CommandError


# Based on https://gist.githubusercontent.com/tgsoverly/ef975d5b430fbce1eb33/raw/a4836655814bf09ac34bd42a6dd99f37aea7265d/merge-xml-coverage.py on 01/12/2015
# constants
PACKAGES_LIST = 'packages/package'
PACKAGES_ROOT = 'packages'
CLASSES_LIST = 'classes/class'
CLASSES_ROOT = 'classes'
METHODS_LIST = 'methods/method'
METHODS_ROOT = 'methods'
LINES_LIST = 'lines/line'
LINES_ROOT = 'lines'


def get_attributes_chain(obj, attrs):
    """Return a joined arguments of object based on given arguments"""

    if type(attrs) is list:
        result = ''
        for attr in attrs:
            result += obj.attrib[attr]
        return result
    else:
        return obj.attrib[attrs]


def merge(root, list1, list2, attr, merge_function):
    """ Groups given lists based on group attributes. Process of
    merging items with same key is handled by passed merge_function.
    Returns list1. """
    for item2 in list2:
        found = False
        for item1 in list1:
            if get_attributes_chain(item1, attr) == get_attributes_chain(item2, attr):
                item1 = merge_function(item1, item2)
                found = True
                break
        if found:
            continue
        else:
            root.append(item2)


def merge_packages(package1, package2):
    """Merges two packages. Returns package1."""
    classes1 = package1.findall(CLASSES_LIST)
    classes2 = package2.findall(CLASSES_LIST)
    if classes1 or classes2:
        merge(package1.find(CLASSES_ROOT), classes1, classes2, ['filename', 'name'], merge_classes)

    return package1


def merge_classes(class1, class2):
    """Merges two classes. Returns class1."""

    lines1 = class1.findall(LINES_LIST)
    lines2 = class2.findall(LINES_LIST)
    if lines1 or lines2:
        merge(class1.find(LINES_ROOT), lines1, lines2, 'number', merge_lines)

    methods1 = class1.findall(METHODS_LIST)
    methods2 = class2.findall(METHODS_LIST)
    if methods1 or methods2:
        merge(class1.find(METHODS_ROOT), methods1, methods2, 'name', merge_methods)

    return class1


def merge_methods(method1, method2):
    """Merges two methods. Returns method1."""

    lines1 = method1.findall(LINES_LIST)
    lines2 = method2.findall(LINES_LIST)
    merge(method1.find(LINES_ROOT), lines1, lines2, 'number', merge_lines)

    return method1


def merge_lines(line1, line2):
    """Merges two lines by summing their hits. Returns line1."""

    # merge hits
    value = int(line1.get('hits')) + int(line2.get('hits'))
    line1.set('hits', str(value))

    # merge conditionals
    con1 = line1.get('condition-coverage')
    con2 = line2.get('condition-coverage')
    if (con1 is not None and con2 is not None):
        con1value = int(con1.split('%')[0])
        con2value = int(con2.split('%')[0])
        # bigger coverage on second line, swap their conditionals
        if (con2value > con1value):
            line1.set('condition-coverage', str(con2))
            line1[0] = line2[0]

    return line1


class Command(BaseCommand):
    help = 'Merges the specified xml coverage reports'
    xmlfiles = ''
    path = ''
    loglevel = ''
    finalxml = ''
    filteronly = False
    filtersuffix = ''
    packagefilters = ''

    def add_arguments(self, parser):
        parser.add_argument(
            'xmlfiles', nargs='+', help="output file xml name"
        )

        parser.add_argument(
            '-p', '--path', dest='path', default='./',
            help="xml location, default current directory"
        )

        parser.add_argument(
            '-o', '--output', dest='filename',
            default='coverage-merged.xml', help="output file xml name",
        )

        parser.add_argument(
            '-l', '--log', dest='loglevel', default='DEBUG',
            choices=[
                'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL',
                'debug', 'info', 'warning', 'error', 'critical'
            ],
            help="Log level DEBUG, INFO, WARNING, ERROR, CRITICAL"
        )

        parser.add_argument(
            '-f', '--filteronly', dest='filteronly',
            default=False, action='store_true', help=(
                'If set all files will be filtered by keep rules otherwise '
                'all given files will be merged and filtered.'
            ),
        )

        parser.add_argument(
            '-s', '--suffix', dest='suffix', default='',
            help="Additional suffix which will be added to filtered files so they original files can be preserved",
        )

        newline = 10 * '\t'
        parser.add_argument(
            "-k", "--keep", dest="packagefilters", default=None,
            action="append", help=(
                "preserves only specific packages. e.g.: " + newline +
                "'python merge.py -k src.la.*'" + newline +
                "will keep all packgages in folder " +
                "src/la/ and all subfolders of this folders. " + newline +
                "There can be mutiple rules e.g.:" + newline +
                "'python merge.py -k src.la.* -k unit_tests.la.'" + newline +
                "Format of the rule is simple dot (.) separated names with "
                "wildcard (*) allowed, e.g: " + newline +
                "package.subpackage.*"
            )
        )

    def usage(self, _):
        usage = '%%prog [options] [file1 file2 ... filen]'
        epilog = (
            'If no files are specified all xml files in current directory '
            'will be selected. \nUseful when there is not known precise file '
            'name only location'
        )

        return '%s\n\n%s\n\n%s' % (usage, self.help, epilog)

    def prepare_packagefilters(self):
        if not self.packagefilters:
            return None

        # create simple regexp from given filter
        for i in range(len(self.packagefilters)):
            self.packagefilters[i] = '^' + self.packagefilters[i].replace('.', '\.').replace ('*', '.*') + '$'

        return self.packagefilters

    def get_xml_filenames(self):
        xmlfiles = []
        for filename in os.listdir(self.path):
            if not filename.endswith('.xml'):
                continue
            fullname = os.path.join(self.path, filename)
            if fullname == self.finalxml:
                continue
            xmlfiles.append(fullname)

        if not xmlfiles:
            raise CommandError('No xml files found!')

        return xmlfiles

    def parse_options(self, **options):
        xmlfiles = options['xmlfiles']
        self.path = options['path']

        if not xmlfiles:
            self.xmlfiles = self.get_xml_filenames()
        else:
            self.xmlfiles = [os.path.join(self.path, filename) for filename in xmlfiles]

        self.loglevel = getattr(logging, options['loglevel'].upper())
        self.finalxml = os.path.join(self.path, options['filename'])
        self.filteronly = options['filteronly']
        self.filtersuffix = options['suffix']
        self.packagefilters = options['packagefilters']

    def include_package(self, name):
        if not self.packagefilters:
            return True

        for packagefilter in self.packagefilters:
            if re.search(packagefilter, name):
                return True
        return False

    def filter_xml(self, xmlfile):
        xmlroot = xmlfile.getroot()
        packageroot = xmlfile.find(PACKAGES_ROOT)
        packages = xmlroot.findall(PACKAGES_LIST)

        # delete nodes from tree AND from list
        included = []
        if self.packagefilters:
            logging.debug('excluding packages:')
        for pckg in packages:
            name = pckg.get('name')
            if not self.include_package(name):
                logging.debug('excluding package "{0}"'.format(name))
                packageroot.remove(pckg)
            else:
                included.append(pckg)
        return included

    def merge_xml(self, xmlfile1, xmlfile2, outputfile):
        # parse
        xml1 = ET.parse(xmlfile1)
        xml2 = ET.parse(xmlfile2)

        # get packages
        packages1 = self.filter_xml(xml1)
        packages2 = self.filter_xml(xml2)

        # find root
        packages1root = xml1.find(PACKAGES_ROOT)

        # merge packages
        merge(packages1root, packages1, packages2, 'name', merge_packages)

        # write result to output file
        xml1.write(outputfile, encoding='UTF-8', xml_declaration=True)

    def write_filtered_data(self):
        # filter all given files
        currfile = 1
        totalfiles = len(self.xmlfiles)

        for xmlfile in self.xmlfiles:
            xml = ET.parse(xmlfile)
            self.filter_xml(xml)
            logging.debug('{1}/{2} filtering: {0}'.format(xmlfile, currfile, totalfiles))
            xml.write(xmlfile + self.filtersuffix, encoding="UTF-8", xml_declaration=True)
            currfile += 1

    def write_merged_data(self):
        # merge all given files
        totalfiles = len(self.xmlfiles)

        # special case if only one file was given
        # filter given file and save it
        if totalfiles == 1:
            logging.warning('Only one file given!')
            xmlfile = self.xmlfiles.pop(0)
            xml = ET.parse(xmlfile)
            self.filter_xml(xml)
            xml.write(self.finalxml, encoding="UTF-8", xml_declaration=True)
            return

        currfile = 1
        logging.debug('{2}/{3} merging: {0} & {1}'.format(
            self.xmlfiles[0], self.xmlfiles[1], currfile, totalfiles - 1)
        )

        self.merge_xml(self.xmlfiles[0], self.xmlfiles[1], self.finalxml)

        currfile = 2
        for i in range(2, totalfiles):
            xmlfile = self.xmlfiles[i]
            logging.debug('{2}/{3} merging: {0} & {1}'.format(
                self.finalxml, xmlfile, currfile, totalfiles - 1)
            )

            self.merge_xml(self.finalxml, xmlfile, self.finalxml)
            currfile += 1

    def handle(self, *args, **options):
        self.parse_options(**options)

        logging.basicConfig(
            level=self.loglevel,
            format='%(levelname)s %(asctime)s: %(message)s',
            datefmt='%x %X',
            stream=self.stderr
        )

        # prepare filters
        self.prepare_packagefilters()

        if self.filteronly:
            self.write_filtered_data()
        else:
            self.write_merged_data()
