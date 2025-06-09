from oelint_adv.cls_rule import Rule
from oelint_parser.cls_item import Variable
from oelint_parser.constants import CONSTANTS
from oelint_parser.helper_files import is_image
from oelint_parser.helper_files import is_packagegroup

class VarMandatoryExists(Rule):

    def __init__(self):
        super().__init__(id='oelint.var.mandatoryvar', severity='error', message='<FOO>', onappend=False, appendix=CONSTANTS.VariablesMandatory)
    IMAGE_EXCLUDES = ['CVE_PRODUCT', 'HOMEPAGE', 'SRC_URI']
    PACKAGEGRP_EXCLUDES = ['CVE_PRODUCT', 'HOMEPAGE', 'LICENSE', 'SRC_URI']

    def check(self, _file, stash):
        res = []
        _is_pkg_group = is_packagegroup(stash, _file)
        _is_image = is_image(stash, _file)
        for var in CONSTANTS.VariablesMandatory:
            if _is_pkg_group and var in VarMandatoryExists.PACKAGEGRP_EXCLUDES:
                continue
            if _is_image and var in VarMandatoryExists.IMAGE_EXCLUDES:
                continue
            items = stash.GetItemsFor(filename=_file, classifier=Variable.CLASSIFIER, attribute=Variable.ATTR_VAR, attributeValue=var)
            if not any(items):
                res += self.finding(_file, 0, "Variable '{a}' should be set".format(a=var), appendix=var)
        return res