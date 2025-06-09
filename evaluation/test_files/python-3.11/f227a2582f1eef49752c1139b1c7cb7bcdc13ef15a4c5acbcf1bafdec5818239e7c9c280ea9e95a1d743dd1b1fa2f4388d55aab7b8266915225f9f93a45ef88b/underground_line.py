from GridCal.Engine.Devices.enumerations import BranchType
from GridCal.Engine.Devices.editable_device import EditableDevice, DeviceType, GCProp

class UndergroundLineType(EditableDevice):

    def __init__(self, name='UndergroundLine', idtag=None, rating=1, R=0, X=0, G=0, B=0, R0=0, X0=0, G0=0, B0=0):
        """
        Constructor
        :param name: name of the device
        :param rating: rating in kA
        :param R: Resistance of positive sequence in Ohm/km
        :param X: Reactance of positive sequence in Ohm/km
        :param G: Conductance of positive sequence in Ohm/km
        :param B: Susceptance of positive sequence in Ohm/km
        :param R0: Resistance of zero sequence in Ohm/km
        :param X0: Reactance of zero sequence in Ohm/km
        :param G0: Conductance of zero sequence in Ohm/km
        :param B0: Susceptance of zero sequence in Ohm/km
        :param tpe:
        """
        EditableDevice.__init__(self, name=name, idtag=idtag, active=True, device_type=DeviceType.UnderGroundLineDevice, editable_headers={'name': GCProp('', str, 'Name of the line template'), 'idtag': GCProp('', str, 'Unique ID'), 'rating': GCProp('kA', float, 'Current rating of the cable'), 'R': GCProp('Ohm/km', float, 'Positive-sequence resistance per km'), 'X': GCProp('Ohm/km', float, 'Positive-sequence reactance per km'), 'G': GCProp('S/km', float, 'Positive-sequence shunt conductance per km'), 'B': GCProp('S/km', float, 'Positive-sequence shunt susceptance per km'), 'R0': GCProp('Ohm/km', float, 'Zero-sequence resistance per km'), 'X0': GCProp('Ohm/km', float, 'Zero-sequence reactance per km'), 'G0': GCProp('S/km', float, 'Zero-sequence shunt conductance per km'), 'B0': GCProp('S/km', float, 'Zero-sequence shunt susceptance per km')}, non_editable_attributes=list(), properties_with_profile={})
        self.tpe = BranchType.Line
        self.rating = rating
        self.R = R
        self.X = X
        self.G = G
        self.B = B
        self.R0 = R0
        self.X0 = X0
        self.G0 = G0
        self.B0 = B0

    def z_series(self):
        """
        positive sequence series impedance in Ohm per unit of length
        """
        return self.R + 1j * self.X

    def y_shunt(self):
        """
        positive sequence shunt admittance in S per unit of length
        """
        return self.G + 1j * self.B

    def change_base(self, Sbase_old, Sbase_new):
        b = Sbase_new / Sbase_old
        self.R *= b
        self.X *= b
        self.G *= b
        self.B *= b
        self.R0 *= b
        self.X0 *= b
        self.G0 *= b
        self.B0 *= b