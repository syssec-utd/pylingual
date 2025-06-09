"""
Created on 2022-08-17

@author: wf
"""
import datetime
import os
from jinja2 import Environment, select_autoescape, FileSystemLoader

class TemplateEnv:
    """
    template environment
    """

    def __init__(self):
        scriptdir = os.path.dirname(os.path.abspath(__file__))
        template_folder = scriptdir + '/../ceurws/resources/templates'
        self.env = Environment(loader=FileSystemLoader(searchpath=template_folder), autoescape=select_autoescape(['html', 'xml']))
        self.env.globals['datetime'] = datetime.datetime
        self.env.globals['enumerate'] = enumerate
        self.env.globals['len'] = len

    def getTemplate(self, templateName: str):
        """
        get the template with the given name
        
        Args:
            templateName(str): the template to get
        """
        template = self.env.get_template(templateName)
        return template