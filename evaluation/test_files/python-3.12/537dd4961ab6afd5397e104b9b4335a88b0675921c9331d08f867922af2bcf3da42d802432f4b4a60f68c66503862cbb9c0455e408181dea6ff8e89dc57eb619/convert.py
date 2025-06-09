import os
from osm_fieldwork.yamlfile import YamlFile
from osm_fieldwork.xlsforms import xlsforms_path
import logging
import argparse
import sys
log = logging.getLogger(__name__)

class Convert(YamlFile):
    """A class to apply a YAML config file and convert ODK to OSM"""

    def __init__(self, xform: str):
        path = xlsforms_path.replace('xlsforms', '')
        if type(xform) == str:
            file = f'{path}{xform}'
            xform = file
        else:
            file = f'{path}/xforms.yaml'
        self.yaml = YamlFile(file)
        self.filespec = file
        self.convert = dict()
        self.ignore = list()
        self.private = list()
        for item in self.yaml.yaml['convert']:
            key = list(item.keys())[0]
            value = item[key]
            if type(value) is str:
                self.convert[key] = value
            elif type(value) is list:
                vals = dict()
                for entry in value:
                    if type(entry) is str:
                        tag = entry
                    else:
                        tag = list(entry.keys())[0]
                        vals[tag] = entry[tag]
                self.convert[key] = vals
        self.ignore = self.yaml.yaml['ignore']
        self.private = self.yaml.yaml['private']
        self.multiple = self.yaml.yaml['multiple']

    def privateData(self, keyword):
        """See is a keyword is in the private data category"""
        return keyword in self.private

    def convertData(self, keyword):
        """See is a keyword is in the convert data category"""
        return keyword in self.convert

    def ignoreData(self, keyword):
        """See is a keyword is in the convert data category"""
        return keyword in self.ignore

    def escape(self, value):
        """Escape characters like embedded quotes in text fields"""
        tmp = value.replace(' ', '_')
        return tmp.replace("'", '&apos;')

    def getKeyword(self, value):
        """Get the value for a keyword from the yaml file"""
        key = self.yaml.yaml(value)
        if type(key) == bool:
            return value
        if len(key) == 0:
            key = self.yaml.getKeyword(value)
        return key

    def getValues(self, tag=None):
        """Get the values for a primary key"""
        if tag is not None:
            if tag in self.convert:
                return self.convert[tag]
        else:
            return None

    def convertEntry(self, tag=None, value=None):
        """Convert a tag and value from the ODK represention to an OSM one"""
        all = list()
        if tag not in self.convert and tag not in self.ignore and (tag not in self.private):
            return (tag, value)
        newtag = None
        newval = None
        if self.convertData(tag):
            newtag = self.convertTag(tag)
            if newtag != tag:
                logging.debug("Converted Tag for entry '%s' to '%s'" % (tag, newtag))
        if newtag is None:
            newtag = tag
        if newtag == 'ele':
            value = value[:7]
        newval = self.convertValue(newtag, value)
        if newval != value:
            logging.debug("Converted Value for entry '%s' to '%s'" % (value, newval))
            for i in newval:
                key = list(i.keys())[0]
                newtag = key
                newval = i[key]
                all.append({newtag: newval})
        else:
            all.append({newtag: newval})
        return all

    def convertValue(self, tag=None, value=None):
        """Convert a single tag value"""
        all = list()
        vals = self.getValues(tag)
        if vals is None:
            return value
        if type(vals) is dict:
            if value not in vals:
                all.append({tag: value})
                return all
            if type(vals[value]) is bool:
                entry = dict()
                if vals[value]:
                    entry[tag] = 'yes'
                else:
                    entry[tag] = 'no'
                all.append(entry)
                return all
            for item in vals[value].split(','):
                entry = dict()
                tmp = item.split('=')
                if len(tmp) == 1:
                    entry[tag] = vals[value]
                else:
                    entry[tmp[0]] = tmp[1]
                    logging.debug('\tValue %s converted to %s' % (value, entry))
                all.append(entry)
        return all

    def convertTag(self, tag=None):
        """Convert a single tag"""
        if tag in self.convert:
            newtag = self.convert[tag]
            if type(newtag) is str:
                logging.debug("\tTag '%s' converted to '%s'" % (tag, newtag))
                tmp = newtag.split('=')
                if len(tmp) > 1:
                    newtag = tmp[0]
            elif type(newtag) is list:
                logging.error('FIXME: list()')
                return tag
            elif type(newtag) is dict:
                return tag
            return newtag
        else:
            return tag

    def dump(self):
        """Dump the contents of the yaml file"""
        print('YAML file: %s' % self.filespec)
        for key, val in self.convert.items():
            if type(val) is list:
                print('Tag %s is' % key)
                for data in val:
                    print('\t%r' % data)
            else:
                print('Tag %s is %s' % (key, val))
if __name__ == '__main__':
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    parser = argparse.ArgumentParser(description='Read and parse a YAML file')
    parser.add_argument('-x', '--xform', default='xform.yaml', help='Default Yaml file')
    parser.add_argument('-i', '--infile', help='The CSV input file')
    args = parser.parse_args()
    convert = Convert('xforms.yaml')
    print('-----')
    entry = convert.convertEntry('waterpoint', 'faucet')
    for i in entry:
        print('XX: %r' % i)
    entry = convert.convertEntry('operational_status', 'closed')
    for i in entry:
        print('XX: %r' % i)
    entry = convert.convertEntry('seasonal', 'wet')
    for i in entry:
        print('XX: %r' % i)
    entry = convert.convertEntry('seasonal', 'rainy')
    for i in entry:
        print('XX: %r' % i)
    entry = convert.convertEntry('power', 'solar')
    for i in entry:
        print('XX: %r' % i)