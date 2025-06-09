from ..model.base import *

def modify_parameters(parameters):
    parameters.marche_travail.salaire_minimum.smic.smic_b_horaire.update(period=period(2013), value=9)
    return parameters

class smic_h_b_9_euros(Reform):
    name = 'Réforme pour simulation ACOSS SMIC horaire brut fixe à 9 euros'

    def apply(self):
        self.modify_parameters(modifier_function=modify_parameters)