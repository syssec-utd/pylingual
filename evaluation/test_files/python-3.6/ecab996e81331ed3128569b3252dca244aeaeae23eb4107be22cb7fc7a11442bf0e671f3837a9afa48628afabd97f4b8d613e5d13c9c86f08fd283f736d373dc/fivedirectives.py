"""Five ZCML directive schemas
"""
from zope.browserresource.metadirectives import IBasicResourceInformation
from zope.configuration.fields import GlobalObject
from zope.interface import Interface
from zope.schema import TextLine

class ISizableDirective(Interface):
    """Attach sizable adapters to classes.
    """
    class_ = GlobalObject(title='Class', required=True)

class IPagesFromDirectoryDirective(IBasicResourceInformation):
    """Register each file in a skin directory as a page resource
    """
    for_ = GlobalObject(title='The interface this view is for.', required=False)
    module = GlobalObject(title='Module', required=True)
    directory = TextLine(title='Directory', description='The directory containing the resource data.', required=True)