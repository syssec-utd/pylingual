__author__ = 'Lei Cai'
__copyright__ = 'Copyright 2021, GeospaceLab'
__license__ = 'BSD-3-Clause License'
__email__ = 'lei.cai@oulu.fi'
__docformat__ = 'reStructureText'
import geospacelab.toolbox.utilities.pyclass as pyclass

class StrAttrBase(str):

    def __new__(cls, str_in):
        if issubclass(str_in.__class__, StrAttrBase):
            obj = str_in
        else:
            obj = str.__new__(cls, str_in)
        return obj

    def config(self, logging=True, **kwargs):
        pyclass.set_object_attributes(self, append=False, logging=logging, **kwargs)

class DatabaseModel(StrAttrBase):

    def __new__(cls, str_in, **kwargs):
        obj = super().__new__(cls, str_in)
        obj.category = kwargs.pop('category', '')
        obj.url = kwargs.pop('url', None)
        obj.description = kwargs.pop('description', '')
        obj.notes = kwargs.pop('notes', '')
        return obj

class FacilityModel(StrAttrBase):

    def __new__(cls, str_in, **kwargs):
        obj = super().__new__(cls, str_in)
        obj.category = kwargs.pop('category', '')
        obj.url = kwargs.pop('url', None)
        obj.description = kwargs.pop('description', '')
        obj.notes = kwargs.pop('notes', '')
        return obj

class ProductModel(StrAttrBase):

    def __new__(cls, str_in, **kwargs):
        obj = super().__new__(cls, str_in)
        obj.category = kwargs.pop('category', '')
        obj.url = kwargs.pop('url', None)
        obj.description = kwargs.pop('description', '')
        obj.notes = kwargs.pop('notes', '')
        return obj

class InstrumentModel(StrAttrBase):

    def __new__(cls, str_in, **kwargs):
        obj = super().__new__(cls, str_in)
        obj.category = kwargs.pop('category', '')
        obj.description = kwargs.pop('description', '')
        obj.notes = kwargs.pop('notes', '')
        return obj

class SiteModel(StrAttrBase):

    def __new__(cls, str_in, **kwargs):
        obj = super().__new__(cls, str_in)
        obj.category = kwargs.pop('category', '')
        obj.name = kwargs.pop('name', '')
        obj.code = str_in
        obj.location = kwargs.pop('location', {'GEO_LAT': None, 'GEO_LON': None, 'GEO_ALT': None})
        obj.description = kwargs.pop('description', '')
        obj.notes = kwargs.pop('notes', '')
        return obj

class MetadataModel(object):

    def __init__(self):
        self.database = ''

    @property
    def database(self):
        return self._database

    @database.setter
    def database(self, value):
        self._database = value

    def config(self, logging=True, **kwargs):
        pyclass.set_object_attributes(self, append=False, logging=logging, **kwargs)