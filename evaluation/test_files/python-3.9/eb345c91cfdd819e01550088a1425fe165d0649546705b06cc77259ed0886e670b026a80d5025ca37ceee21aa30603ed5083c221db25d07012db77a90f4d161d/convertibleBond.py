from RiskQuantLib.Set.Security.Bond.convertibleBond import setConvertibleBond
from RiskQuantLib.Security.Bond.bond import bond

class convertibleBond(bond, setConvertibleBond):

    def __init__(self, codeString, nameString, securityTypeString='Convertible Bond'):
        super(convertibleBond, self).__init__(codeString, nameString, securityTypeString)