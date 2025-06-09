from .model import Model
"\nopentiva.alfentanil\n===================\n\nThis module contains the classes for alfentanil models.\n\nAll Classes have the same parameters and attributes.\n\nParameters\n----------\nsex\n    0 for male or 1 for female\nage\n    in years\nweight\n    in kg\nheight\n   in cm\n\nAttributes\n----------\ncompartments : int\n    number of compartments to model; 1, 2 or 3\nconcentration_unit : str\n    drug concentration unit\ntarget_unit : str\n    target concentration unit\nage_lower : float\n    lower age limit of model; -1 if no limit\nage_upper : float\n    upper age limit of model; -1 if no limit\nweight_lower : float\n    lower weight limit of model; -1 if no limit\nweight_upper : float\n    upper weight limit of model; -1 if no limit\npmid : str\n    Pubmed ID of model's reference\ndoi : str\n    Digital Object Identifier (DOI) of model's reference\nwarning : str\n    Warnings relating to non-validated anthropometric values\nv1 : float\n    volume of central compartment\nk10 : float\n    equilibrium rate constant from compartment 1 to 0\nk12 : float\n    equilibrium rate constant from compartment 1 to 2\nk13 : float\n    equilibrium rate constant from compartment 1 to 3\nk21 : float\n    equilibrium rate constant from compartment 2 to 1\nk31 : float\n    equilibrium rate constant from compartment 3 to 1\nke0 : float\n    effect compartment equilibrium rate constant\n"

class Maitre(Model):
    """Maitre class holds pharmacokinetic parameters for the Maitre alfentanil
    model.

    Reference: PMID: 3099604

    Keo PMID: 1824743 DOI: 10.1097/00000542-199101000-00010
    """

    def __init__(self, sex: int, age: float, weight: float, height: float):
        super().__init__(sex, age, weight, height)
        self.compartments = 3
        self.concentration_unit = 'mcg/ml'
        self.target_unit = 'ng/ml'
        self.age_lower = 25
        self.age_upper = 53
        self.weight_lower = 41
        self.weight_upper = 95
        self.pmid = '3099604'
        self.doi = ''
        self.validate_anthropometric_values()
        if sex == 0:
            self.v1 = 0.11 * weight
        elif sex == 1:
            self.v1 = 0.11 * 1.15 * weight
        if age < 40:
            self.k10 = 0.356 / self.v1
        elif age >= 40:
            self.k10 = (0.356 - 0.00269 * (age - 40)) / self.v1
        self.k12 = 0.104
        self.k13 = 0.017
        self.k21 = 0.0673
        if age < 40:
            self.k31 = 0.0126
        elif age >= 40:
            self.k31 = 0.0126 - 0.000113 * (age - 40)
        self.ke0 = 0.77

class Goresky(Model):
    """Goresky class holds pharmacokinetic parameters for the Goresky
    alfentanil model.

    Reference: PMID: 3118743 DOI: 10.1097/00000542-198711000-00007

    Keo PMID: 1824743 DOI: 10.1097/00000542-199101000-00010
    """

    def __init__(self, sex: int, age: float, weight: float, height: float):
        super().__init__(sex, age, weight, height)
        self.compartments = 2
        self.concentration_unit = 'mcg/ml'
        self.target_unit = 'ng/ml'
        self.age_lower = 1
        self.age_upper = 14
        self.weight_lower = -1
        self.weight_upper = -1
        self.pmid = '3118743'
        self.doi = '10.1097/00000542-198711000-00007'
        self.validate_anthropometric_values()
        self.v1 = 0.206 * weight
        self.k10 = 0.038
        self.k12 = 0.018
        self.k21 = 0.018
        self.ke0 = 0.77

class Scott(Model):
    """Scott class holds pharmacokinetic parameters for the Scott alfentanil
    model.

    Reference: PMID: 3100765

    Keo PMID: 1824743 DOI: 10.1097/00000542-199101000-00010
    """

    def __init__(self, sex: int, age: float, weight: float, height: float):
        super().__init__(sex, age, weight, height)
        self.compartments = 3
        self.concentration_unit = 'mcg/ml'
        self.target_unit = 'ng/ml'
        self.age_lower = -1
        self.age_upper = -1
        self.weight_lower = -1
        self.weight_upper = -1
        self.pmid = '3100765'
        self.doi = ''
        self.validate_anthropometric_values()
        self.v1 = 2.185 / 70 * weight
        self.cl1 = 0.195
        self.k10 = self.cl1 / self.v1
        self.k12 = 0.656
        self.k13 = 0.113
        self.k21 = 0.214
        self.k31 = 0.017
        self.ke0 = 0.77