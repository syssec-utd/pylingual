"""
Created on Thu Nov 28 14:44:31 2019

#originally made for Cantera 2.4.  Not upgraded to work with later versions of Cantera, as of Oct 2021
"""
import xmltodict
import numpy as np
import cantera as ct
import copy

def stackListsAndArrays(listOfItemsToStack):
    stackableItemsList = copy.deepcopy(listOfItemsToStack)
    for itemIndex in range(len(listOfItemsToStack)):
        if str(type(listOfItemsToStack[itemIndex])) == "<class 'list'>":
            stackableItemsList[itemIndex] = np.atleast_2d(stackableItemsList[itemIndex]).transpose()
        else:
            pass
    return np.hstack(tuple(stackableItemsList))

def descendingLinearEWithPiecewiseOffsetCheckOneReactionAllReactions(reactions_parameters_array, piecewise_coverage_intervals_all_reactions, E_offsets_array_all_reactions, verbose=False):
    passedArray = np.zeros(len(reactions_parameters_array), dtype='bool')
    for reactionIndex in range(len(reactions_parameters_array)):
        individualreactions_parameters_array = reactions_parameters_array[reactionIndex]
        if len(np.shape(reactions_parameters_array)) == 1:
            piecewise_coverage_intervals = piecewise_coverage_intervals_all_reactions
        else:
            piecewise_coverage_intervals = piecewise_coverage_intervals_all_reactions[reactionIndex]
        E_offsets_array = E_offsets_array_all_reactions[reactionIndex]
        reactionID = str(int(individualreactions_parameters_array[0]) - 1)
        individualReactionTypeReceived = str(individualreactions_parameters_array[1])
        reactionEquation = str(individualreactions_parameters_array[2])
        E = str(individualreactions_parameters_array[5])
        e = str(individualreactions_parameters_array[8])
        concentrationDependenceSpecies = str(individualreactions_parameters_array[9])
        E_0 = float(E)
        if np.isnan(float(e)):
            e = 0.0
        g_slope = -1.0 * float(e)
        if '(S)' in reactionEquation:
            passedArray[reactionIndex] = descendingLinearEWithPiecewiseOffsetCheckOneReaction(E_0, g_slope, piecewise_coverage_intervals, E_offsets_array)
            if verbose == True:
                if passedArray[reactionIndex] == False:
                    print('The reaction with ID of' + reactionID + 'and equation of' + reactionEquation + 'did not pass descendingLinearEWithPiecewiseOffsetCheckOneReaction')
    if sum(passedArray) < len(passedArray):
        return False
    elif sum(passedArray) == len(passedArray):
        return True

def descendingLinearEWithPiecewiseOffsetCheckOneReaction(E_0, g_slope, piecewise_coverage_intervals, E_offsets_array):
    E_array = E_0 + g_slope * piecewise_coverage_intervals + E_offsets_array
    delta_E_array = np.diff(E_array)
    if np.any(delta_E_array > 0):
        return False
    else:
        return True

def makeCanteraReactionObjectsListFromFile(FileName):
    canteraReactionObjectsList = ct.Reaction.listFromFile(FileName)
    return canteraReactionObjectsList

def extractReactionParametersFromFile(InputFileName, OutputFilename=''):
    canteraReactionObjectsList = makeCanteraReactionObjectsListFromFile(InputFileName)
    reactionIDsList, reactionTypesList, reactionEquationsList, ArrheniusParametersArray, concentrationDependencesArray, concentrationDependencesSpeciesList, is_sticking_coefficientList = getReactionParametersFromCanteraReactionObjectsList(canteraReactionObjectsList)
    outputAsNumpyArray = stackListsAndArrays([reactionIDsList, reactionTypesList, reactionEquationsList, ArrheniusParametersArray, concentrationDependencesArray, concentrationDependencesSpeciesList, is_sticking_coefficientList])
    if OutputFilename != '':
        headerString = 'reactionID,canteraReactionType,reactionEquation,A,b,E,a,m,e,concentrationDependenceSpecies, is_sticking_coefficient'
        np.savetxt(OutputFilename, outputAsNumpyArray, fmt='%s', delimiter=',', comments='', header=headerString)
    return (reactionIDsList, reactionTypesList, reactionEquationsList, ArrheniusParametersArray, concentrationDependencesArray, concentrationDependencesSpeciesList, is_sticking_coefficientList)

def getReactionParametersFromCanteraReactionObjectsList(reactionObjectList):
    reactionIDsList = []
    reactionTypesList = []
    reactionEquationsList = []
    ArrheniusParametersList = []
    concentrationDependencesList = []
    concentrationDependencesSpeciesList = []
    is_sticking_coefficientList = []
    for reactionObject in reactionObjectList:
        reactionIDsList.append(reactionObject.ID)
        try:
            if int(reactionObject.reaction_type) == int(20):
                reactionTypesList.append('surface_reaction')
            if int(reactionObject.reaction_type) == int(1):
                reactionTypesList.append('reaction')
            if int(reactionObject.reaction_type) == int(2):
                reactionTypesList.append('three_body_reaction')
            if int(reactionObject.reaction_type) == int(4):
                reactionTypesList.append('falloff_reaction')
        except:
            reactionTypesList.append('None')
        reactionEquationsList.append(reactionObject.equation)
        A = float(reactionObject.rate.pre_exponential_factor)
        b = float(reactionObject.rate.temperature_exponent)
        E = float(reactionObject.rate.activation_energy) / 1000
        singleReactionArrheniusParametersArray = np.array([A, b, E])
        ArrheniusParametersList.append(singleReactionArrheniusParametersArray)
        try:
            if len(reactionObject.concentration_deps) > 0:
                concentration_deps = True
            else:
                concentration_deps = False
        except:
            concentration_deps = False
        if concentration_deps == True:
            singleReactionconcentrationDependencesDict = reactionObject.concentration_deps
            temporaryconcentrationDependenceSpeciesList = list(reactionObject.concentration_deps.keys())
            if len(temporaryconcentrationDependenceSpeciesList) > 0:
                concentrationDependenceExists = True
                concentrationDependenceSpecies = temporaryconcentrationDependenceSpeciesList[0]
                a = reactionObject.concentration_deps[concentrationDependenceSpecies][0]
                m = reactionObject.concentration_deps[concentrationDependenceSpecies][1]
                e = float(reactionObject.concentration_deps[concentrationDependenceSpecies][2]) / 1000
        else:
            a = float('nan')
            m = float('nan')
            e = float('nan')
            concentrationDependenceSpecies = 'None'
        concentrationDependencesList.append(np.array([a, m, e]))
        concentrationDependencesSpeciesList.append(concentrationDependenceSpecies)
        is_sticking_coefficientList.append(reactionObject.is_sticking_coefficient)
    reactionIDsList = reactionIDsList
    reactionTypesList = reactionTypesList
    ArrheniusParametersArray = np.array(ArrheniusParametersList)
    concentrationDependencesArray = np.array(concentrationDependencesList)
    concentrationDependencesSpeciesList = concentrationDependencesSpeciesList
    is_sticking_coefficientList = is_sticking_coefficientList
    return (reactionIDsList, reactionTypesList, reactionEquationsList, ArrheniusParametersArray, concentrationDependencesArray, concentrationDependencesSpeciesList, is_sticking_coefficientList)

def make_reaction_yaml_string(individualreactions_parameters_array, for_full_yaml=False, input_Ea_units='J/kmol'):
    reaction_yaml_string = None
    reactionID = str(int(individualreactions_parameters_array[0]) - 1)
    individualReactionTypeReceived = str(individualreactions_parameters_array[1])
    reactionEquation = str(individualreactions_parameters_array[2])
    if input_Ea_units.lower() == 'j/mol':
        individualreactions_parameters_array[5] = float(individualreactions_parameters_array[5]) * 1000.0
    A = str(individualreactions_parameters_array[3])
    b = str(individualreactions_parameters_array[4])
    E = str(individualreactions_parameters_array[5])
    a = str(individualreactions_parameters_array[6])
    m = str(individualreactions_parameters_array[7])
    e = str(individualreactions_parameters_array[8])
    concentrationDependenceSpecies = str(individualreactions_parameters_array[9])
    is_sticking = str(individualreactions_parameters_array[10])
    if is_sticking.capitalize() == 'False':
        ArrheniusString = 'Arrhenius'
    if is_sticking.capitalize() == 'True':
        ArrheniusString = 'stick'
    if is_sticking.capitalize() == 'True':
        rate_constant_type = 'sticking-coefficient'
    if is_sticking.capitalize() == 'False':
        rate_constant_type = 'rate-constant'
    if individualReactionTypeReceived == 'surface_reaction':
        individualReactionTypeReceived = 'reaction'
    if individualReactionTypeReceived.lower() == 'reaction':
        rxnStringTemplate = '  equation: Eqn_string\n  rate_constant_type: {A: A_value, b: b_value, Ea: Ea_value}'
        reaction_yaml_string = rxnStringTemplate
        reaction_yaml_string = reaction_yaml_string.replace('Eqn_string', str(reactionEquation))
        reaction_yaml_string = reaction_yaml_string.replace('A_value', str(A))
        reaction_yaml_string = reaction_yaml_string.replace('b_value', str(b))
        reaction_yaml_string = reaction_yaml_string.replace('Ea_value', str(E))
        reaction_yaml_string = reaction_yaml_string.replace('rate_constant_type', str(rate_constant_type))
        if str(concentrationDependenceSpecies).lower() != 'none':
            coverageDependenceStringTemplate = '\n  coverage-dependencies:\n    speciesName: {a: a_value, m: m_value, E: e_value}'
            coverageDependenceString = coverageDependenceStringTemplate
            coverageDependenceString = coverageDependenceString.replace('speciesName', str(concentrationDependenceSpecies))
            coverageDependenceString = coverageDependenceString.replace('a_value', str(a))
            coverageDependenceString = coverageDependenceString.replace('m_value', str(m))
            coverageDependenceString = coverageDependenceString.replace('e_value', str(e))
        else:
            coverageDependenceString = ''
        reaction_yaml_string = reaction_yaml_string + coverageDependenceString
    if for_full_yaml == True:
        reaction_yaml_string = '-' + reaction_yaml_string[1:]
    return reaction_yaml_string

def make_reaction_cti_string(individualreactions_parameters_array):
    reaction_cti_string = None
    reactionID = str(int(individualreactions_parameters_array[0]) - 1)
    individualReactionTypeReceived = str(individualreactions_parameters_array[1])
    reactionEquation = str(individualreactions_parameters_array[2])
    A = str(individualreactions_parameters_array[3])
    b = str(individualreactions_parameters_array[4])
    E = str(individualreactions_parameters_array[5])
    a = str(individualreactions_parameters_array[6])
    m = str(individualreactions_parameters_array[7])
    e = str(individualreactions_parameters_array[8])
    concentrationDependenceSpecies = str(individualreactions_parameters_array[9])
    is_sticking = str(individualreactions_parameters_array[10])
    if is_sticking.capitalize() == 'False':
        ArrheniusString = 'Arrhenius'
    if is_sticking.capitalize() == 'True':
        ArrheniusString = 'stick'
    if individualReactionTypeReceived.lower() == 'reaction':
        reaction_cti_string = "reaction('{0}',\n        {1}({2}, {3}, {4}])".format(reactionEquation, ArrheniusString, A, b, E)
    if individualReactionTypeReceived.lower() == 'surface_reaction':
        if concentrationDependenceSpecies.capitalize() == 'None':
            reaction_cti_string = 'surface_reaction("{0}",\n            {1}({2}, {3}, {4}))'.format(reactionEquation, ArrheniusString, A, b, E)
        if concentrationDependenceSpecies.capitalize() != 'None':
            reaction_cti_string = 'surface_reaction("{0}",\n            {1}({2}, {3}, {4},\n            coverage = [\'{5}\', {6}, {7}, {8}]))'.format(reactionEquation, ArrheniusString, A, b, E, concentrationDependenceSpecies, a, m, e)
    return reaction_cti_string

def create_full_cti(model_name, reactions_parameters_array=[], cti_top_info_string=None, write_cti_to_file=False):
    if cti_top_info_string == None:
        cti_top_info_filename = model_name + '_cti_top_info.cti'
        with open(cti_top_info_filename, 'r') as cti_top_info_file:
            cti_top_info_string = cti_top_info_file.read()
    if len(reactions_parameters_array) == len([]):
        reaction_parameters_filename = model_name + '_input_reactions_parameters.csv'
        reactions_parameters_array = np.genfromtxt(reaction_parameters_filename, delimiter=',', skip_header=1, dtype='str')
    reactionsDataHeader = '\n\n#------------------------------------------------------------------------------- \n#  Reaction data \n#------------------------------------------------------------------------------- \n                           \n'
    cti_reactions_string = '\n'
    for element in reactions_parameters_array:
        cti_reactions_string += make_reaction_cti_string(element) + '\n'
    cti_string = cti_top_info_string + reactionsDataHeader + cti_reactions_string
    if write_cti_to_file == True:
        cti_filename = model_name + '_cti_full.cti'
        with open(cti_filename, 'w') as cti_file:
            cti_file.write(cti_string)
    return cti_string

def create_full_yaml(model_name, reactions_parameters_array=[], yaml_top_info_string='', write_yaml_to_file=False):
    if yaml_top_info_string == '':
        yaml_top_info_filename = model_name + '_yaml_top_info.yaml'
        with open(yaml_top_info_filename, 'r') as yaml_top_info_file:
            yaml_top_info_string = yaml_top_info_file.read()
    if len(reactions_parameters_array) == len([]):
        reaction_parameters_filename = model_name + '_input_reactions_parameters.csv'
        reactions_parameters_array = np.genfromtxt(reaction_parameters_filename, delimiter=',', skip_header=1, dtype='str')
    reactionsDataHeader = 'reactions:\n'
    yaml_reactions_string = ''
    for element in reactions_parameters_array:
        yaml_reactions_string += make_reaction_yaml_string(element, for_full_yaml=True) + '\n'
    yaml_string = yaml_top_info_string + reactionsDataHeader + yaml_reactions_string
    if write_yaml_to_file == True:
        yaml_filename = model_name + '_yaml_full.yaml'
        with open(yaml_filename, 'w') as yaml_file:
            yaml_file.write(yaml_string)
    return yaml_string

def findModifiableParameterIndices(reactions_parameters_array):
    reactions_parameters_array = np.atleast_2d(reactions_parameters_array)
    listOfModifiableParameterIndices = []
    listOfOriginalValues = []
    for reactionIndex, individualreactions_parameters_array in enumerate(reactions_parameters_array):
        reactionID = str(int(individualreactions_parameters_array[0]) - 1)
        individualReactionTypeReceived = str(individualreactions_parameters_array[1])
        reactionEquation = str(individualreactions_parameters_array[2])
        A = str(individualreactions_parameters_array[3])
        b = str(individualreactions_parameters_array[4])
        E = str(individualreactions_parameters_array[5])
        a = str(individualreactions_parameters_array[6])
        m = str(individualreactions_parameters_array[7])
        e = str(individualreactions_parameters_array[8])
        concentrationDependenceSpecies = str(individualreactions_parameters_array[9])
        is_sticking = str(individualreactions_parameters_array[10])
        listOfModifiableParameterIndices = listOfModifiableParameterIndices + [[reactionIndex, 3], [reactionIndex, 4], [reactionIndex, 5]]
        if individualReactionTypeReceived == 'surface_reaction':
            if concentrationDependenceSpecies != 'None':
                listOfModifiableParameterIndices = listOfModifiableParameterIndices + [[reactionIndex, 6], [reactionIndex, 7], [reactionIndex, 8]]
    return listOfModifiableParameterIndices

def getAllModifiableReactionParametersValues(reactions_parameters_array, listOfModifiableParameterIndices=[]):
    if listOfModifiableParameterIndices == []:
        listOfModifiableParameterIndices = findModifiableParameterIndices(reactions_parameters_array)
    listOfOriginalValues = []
    for modifiableParameterIndex in range(len(listOfModifiableParameterIndices)):
        reactionIndex = listOfModifiableParameterIndices[modifiableParameterIndex][0]
        individualReactionParameterIndex = listOfModifiableParameterIndices[modifiableParameterIndex][1]
        originalValue = reactions_parameters_array[reactionIndex][individualReactionParameterIndex]
        listOfOriginalValues.append(originalValue)
    return listOfOriginalValues

def modifyAllAdjustableReactionParametersArrayValues(reactions_parameters_array, newParametersList):
    reactions_parameters_array = np.atleast_2d(reactions_parameters_array)
    listOfModifiableParameterIndices = findModifiableParameterIndices(reactions_parameters_array)
    if len(listOfModifiableParameterIndices) != len(newParametersList):
        print('WARNING: modifyAllAdjustablereactions_parameters_arrayValues has been called with a newParametersList that is not of matching length.')
    modified_reactions_parameters_array = copy.deepcopy(reactions_parameters_array)
    for newParameterIndex in range(len(newParametersList)):
        newValue = newParametersList[newParameterIndex]
        reactionIndex = listOfModifiableParameterIndices[newParameterIndex][0]
        individualReactionParameterIndex = listOfModifiableParameterIndices[newParameterIndex][1]
        modified_reactions_parameters_array[reactionIndex][individualReactionParameterIndex] = str(newValue)
    return modified_reactions_parameters_array
'\n#DEPRECATED BECAUSE NOW WE USE CANTERA CODE OR CANTERA OBJECTS\ndef makeDictfromXMLFile(FileName): #Filename is a string, can include path.\n    with open("methane_pox_on_pt.xml") as xmlfile:\n        xmldict = xmltodict.parse(xmlfile.read())\n    return xmldict\n#DEPRECATED BECAUSE NOW WE USE CANTERA CODE OR CANTERA OBJECTS\ndef makeReactionObjectsListFromCTMLasDict(CTMLasDict):\n    reactionObjectsList = CTMLasDict["ctml"]["reactionData"][\'reaction\']\n    return reactionObjectsList\n\n#DEPRECATED BECAUSE NOW WE USE CANTERA CODE OR CANTERA OBJECTS  \n    #NOte: does not have is_sticking_coefficientList and would need that to be useful.\ndef getReactionParametersFromReactionObjectsList(reactionObjectList):\n    reactionIDsList = []\n    reactionTypesList = []\n    reactionEquationsList = []\n    ArrheniusParametersList =[] #List of numpy arrays with A,b,E for each reaction.\n    concentrationDependencesList =[]\n    concentrationDependencesSpeciesList = []\n    for reactionObject in reactionObjectList:\n        reactionIDsList.append(reactionObject["@id"])\n        try:\n            reactionTypesList.append(reactionObject["@type"])\n        except:\n            reactionTypesList.append("None")\n        #Now need to modify equation based on whether it\'s irreversible or not.\n        reactionEquation = reactionObject["equation"]\n        if reactionObject["@reversible"]=="no":\n            reactionEquation = reactionEquation.replace("=]","=>")\n        if reactionObject["@reversible"]=="yes":\n            reactionEquation = reactionEquation.replace("=]","<=>")\n        reactionEquationsList.append(reactionEquation)\n        A = float(reactionObject[\'rateCoeff\'][\'Arrhenius\'][\'A\'])\n        b = float(reactionObject[\'rateCoeff\'][\'Arrhenius\'][\'b\'])\n        if reactionObject[\'rateCoeff\'][\'Arrhenius\'][\'E\'][\'@units\']=="J/mol":\n            E = float(reactionObject[\'rateCoeff\'][\'Arrhenius\'][\'E\'][\'#text\']) #the xml is written in a way that this is necessary.\n        else:\n            E = 0.0\n            print("Error: Currently, ony J/mol is supported for units of E. Fix parameters for this reaction: " + reactionObject[\'equation\'])\n        singleReactionArrheniusParametersArray = np.array([A,b,E])\n        ArrheniusParametersList.append(singleReactionArrheniusParametersArray)\n        #Now check for coverage parameters.\n        if "coverage" in reactionObject[\'rateCoeff\'][\'Arrhenius\']:\n            singleReactionconcentrationDependencesDict = reactionObject[\'rateCoeff\'][\'Arrhenius\'][\'coverage\']\n            speciesDependence = singleReactionconcentrationDependencesDict[\'@species\']\n            a = float(singleReactionconcentrationDependencesDict[\'a\'])\n            m = float(singleReactionconcentrationDependencesDict[\'m\'])\n            if singleReactionconcentrationDependencesDict[\'e\'][\'@units\']=="J/mol":\n                e = float(singleReactionconcentrationDependencesDict[\'e\'][\'#text\']) #the xml is written in a way that this is necessary.\n            else:\n                e = 0.0\n                print("Error: Currently, ony J/mol is supported for units of e. Fix coverage parameters for this reaction: " + reactionObject[\'equation\'])\n        else:#There is no coverage dependence, so will put \'NaN\')\n             a = float(\'nan\')\n             m = float(\'nan\')\n             e = float(\'nan\')\n             speciesDependence = \'None\'\n        concentrationDependencesList.append(np.array([a,m,e]))\n        concentrationDependencesSpeciesList.append(speciesDependence)\n    reactionIDsList = reactionIDsList\n    reactionTypesList = reactionTypesList\n    ArrheniusParametersArray = np.array(ArrheniusParametersList)\n    concentrationDependencesArray = np.array(concentrationDependencesList)\n    concentrationDependencesSpeciesList = concentrationDependencesSpeciesList\n    return reactionIDsList, reactionTypesList, reactionEquationsList, ArrheniusParametersArray, concentrationDependencesArray, concentrationDependencesSpeciesList\n'

def ArrheniusParameterAddedToInOnePhase(canteraModule, canteraPhaseObject, ArrheniusParametersOperandsArray, byProvidedReactionID=True):
    reactions_parameters_array = ArrheniusParametersOperandsArray
    ct = canteraModule
    for individualreactions_parameters_array in reactions_parameters_array:
        reactionID = str(int(individualreactions_parameters_array[0]) - 1)
        individualReactionTypeReceived = str(individualreactions_parameters_array[1])
        reactionEquation = str(individualreactions_parameters_array[2])
        A_operand = float(individualreactions_parameters_array[3])
        b_operand = float(individualreactions_parameters_array[4])
        E_operand = float(individualreactions_parameters_array[5])
        a_operand = float(individualreactions_parameters_array[6])
        m_operand = float(individualreactions_parameters_array[7])
        e_operand = float(individualreactions_parameters_array[8])
        concentrationDependenceSpecies = str(individualreactions_parameters_array[9])
        if byProvidedReactionID == False:
            reactionID = canteraPhaseObject.reaction_equations().index(reactionEquation)
        existingReactionObject = canteraPhaseObject.reactions()[int(reactionID)]
        existingA = float(existingReactionObject.rate.pre_exponential_factor)
        existingb = float(existingReactionObject.rate.temperature_exponent)
        existingE = float(existingReactionObject.rate.activation_energy)
        temporaryconcentrationDependenceSpeciesList = list(existingReactionObject.concentration_deps.keys())
        if len(temporaryconcentrationDependenceSpeciesList) > 0:
            concentrationDependenceExists = True
            concentrationDependenceSpecies = temporaryconcentrationDependenceSpeciesList[0]
            existinga = existingReactionObject.concentration_deps[concentrationDependenceSpecies][0]
            existingm = existingReactionObject.concentration_deps[concentrationDependenceSpecies][1]
            existinge = existingReactionObject.concentration_deps[concentrationDependenceSpecies][2]
        existingReactionObject.rate = ct.Arrhenius(float(existingA + A_operand), float(existingb + b_operand), float(existingE + E_operand))
        if concentrationDependenceExists == True:
            print('Warning: Coverage dependence modifiers not working yet')
            try:
                if a_operand + m_operand + e_operand != 0.0:
                    tupleForconcentrationDependence = (existinga + a_operand, existingm + m_operand, existinge + e_operand)
                    existingReactionObject.concentration_deps[concentrationDependenceSpecies] = tupleForconcentrationDependence
            except:
                pass
        canteraPhaseObject.modify_reaction(int(reactionID), existingReactionObject)

def ArrheniusParametersMultiplierInOnePhase(canteraModule, canteraPhaseObject, ArrheniusParametersMultipliersArray, byProvidedReactionID=True):
    reactions_parameters_array = ArrheniusParametersMultipliersArray
    ct = canteraModule
    for individualreactions_parameters_array in reactions_parameters_array:
        reactionID = str(int(individualreactions_parameters_array[0]) - 1)
        individualReactionTypeReceived = str(individualreactions_parameters_array[1])
        reactionEquation = str(individualreactions_parameters_array[2])
        A_multiplier = float(individualreactions_parameters_array[3])
        b_multiplier = float(individualreactions_parameters_array[4])
        E_multiplier = float(individualreactions_parameters_array[5])
        a_multiplier = float(individualreactions_parameters_array[6])
        m_multiplier = float(individualreactions_parameters_array[7])
        e_multiplier = float(individualreactions_parameters_array[8])
        concentrationDependenceSpecies = str(individualreactions_parameters_array[9])
        if byProvidedReactionID == False:
            reactionID = canteraPhaseObject.reaction_equations().index(reactionEquation)
        existingReactionObject = canteraPhaseObject.reactions()[int(reactionID)]
        existingA = float(existingReactionObject.rate.pre_exponential_factor)
        existingb = float(existingReactionObject.rate.temperature_exponent)
        existingE = float(existingReactionObject.rate.activation_energy)
        temporaryconcentrationDependenceSpeciesList = list(existingReactionObject.concentration_deps.keys())
        if len(temporaryconcentrationDependenceSpeciesList) > 0:
            concentrationDependenceExists = True
            concentrationDependenceSpecies = temporaryconcentrationDependenceSpeciesList[0]
            existinga = existingReactionObject.concentration_deps[concentrationDependenceSpecies][0]
            existingm = existingReactionObject.concentration_deps[concentrationDependenceSpecies][1]
            existinge = existingReactionObject.concentration_deps[concentrationDependenceSpecies][2]
        existingReactionObject.rate = ct.Arrhenius(float(existingA * A_multiplier), float(existingb * b_multiplier), float(existingE * E_multiplier))
        if concentrationDependenceExists == True:
            print('Warning: Coverage dependence modifiers not working yet')
            try:
                if a_multiplier * m_multiplier * e_multiplier != 1.0:
                    tupleForconcentrationDependence = (existinga * a_multiplier, existingm * m_multiplier, existinge * e_multiplier)
                    existingReactionObject.concentration_deps[concentrationDependenceSpecies] = tupleForconcentrationDependence
            except:
                pass
        canteraPhaseObject.modify_reaction(int(reactionID), existingReactionObject)

def populatePiecewiseCoverageDependence(simulation_settings_module, original_reactions_parameters_array, species_name, kineticParameterName, piecewise_coverage_intervals, modifiers_array):
    try:
        len(simulation_settings_module.piecewise_coverage_dependences)
    except:
        simulation_settings_module.piecewise_coverage_dependences = {}
    try:
        len(simulation_settings_module.piecewise_coverage_dependences[species_name])
    except:
        simulation_settings_module.piecewise_coverage_dependences[species_name] = {}
        simulation_settings_module.piecewise_coverage_dependences[species_name]['piecewise_coverage_intervals'] = piecewise_coverage_intervals
        simulation_settings_module.piecewise_coverage_dependences[species_name]['piecewise_kinetic_parameter_modifier_arrays'] = {}
    simulation_settings_module.original_reactions_parameters_array = original_reactions_parameters_array
    simulation_settings_module.piecewise_coverage_dependences[species_name]['piecewise_kinetic_parameter_modifier_arrays'][kineticParameterName] = np.array(modifiers_array)
    return simulation_settings_module.piecewise_coverage_dependences

def getInterpolatedModifiersArray(existing_values, piecewise_coverage_dependences, species_name, species_coverage, kineticParameterKey, reaction_parameters_array_kinetic_parameter_index):
    all_coverages_modifiers_array = np.array(piecewise_coverage_dependences[species_name]['piecewise_kinetic_parameter_modifier_arrays'][kineticParameterKey], dtype='float')
    if len(all_coverages_modifiers_array) != len(existing_values):
        print('You have piecewise_coverage_dependence set to True in the simulation settings. However, the coverage dependence array for kinetic parameter ' + kineticParameterKey + ' has a function of the coverage of' + species_name + 'does not match the length of the kinetic parameters array. These lengths must match to use this feature.')
    all_piecewise_coverage_intervals = np.array(piecewise_coverage_dependences[species_name]['piecewise_coverage_intervals'], dtype='float')
    index_of_relevant_interval_low = np.searchsorted(all_piecewise_coverage_intervals, species_coverage, side='right') - 1
    index_of_relevant_interval_high = index_of_relevant_interval_low + 1
    if species_coverage <= min(all_piecewise_coverage_intervals):
        indexOfMin = np.where(all_piecewise_coverage_intervals == min(all_piecewise_coverage_intervals))
        interpolated_modifiers_array = np.array(all_coverages_modifiers_array[:, indexOfMin]).flatten()
    elif species_coverage >= max(all_piecewise_coverage_intervals):
        indexOfMax = np.where(all_piecewise_coverage_intervals == max(all_piecewise_coverage_intervals))
        interpolated_modifiers_array = np.array(all_coverages_modifiers_array[:, indexOfMax]).flatten()
    else:
        modifiers_array_low = np.array(all_coverages_modifiers_array[:, index_of_relevant_interval_low], dtype='float')
        modifiers_array_high = np.array(all_coverages_modifiers_array[:, index_of_relevant_interval_high], dtype='float')
        piecewise_interval_low = np.array(all_piecewise_coverage_intervals[index_of_relevant_interval_low], dtype='float')
        piecewise_interval_high = np.array(all_piecewise_coverage_intervals[index_of_relevant_interval_high], dtype='float')
        slopes_array = (modifiers_array_high - modifiers_array_low) / (piecewise_interval_high - piecewise_interval_low)
        intercepts_array = modifiers_array_high - 1.0 * slopes_array * piecewise_interval_high
        interpolated_modifiers_array = slopes_array * species_coverage + intercepts_array
    return interpolated_modifiers_array

def calculatePiecewiseCoverageDependentModifiedParametersArray(settingsModuleOrObject, species_names, species_coverages):
    original_reactions_parameters_array = settingsModuleOrObject.original_reactions_parameters_array
    modified_reactions_parameters_array = np.array(copy.deepcopy(original_reactions_parameters_array), dtype='str')
    piecewise_coverage_dependences = settingsModuleOrObject.piecewise_coverage_dependences
    for species_name in piecewise_coverage_dependences.keys():
        species_index = species_names.index(species_name)
        species_coverage = float(species_coverages[species_index])
        for kineticParameterKey in piecewise_coverage_dependences[species_name]['piecewise_kinetic_parameter_modifier_arrays']:
            if kineticParameterKey == 'A':
                reaction_parameters_array_kinetic_parameter_index = 3
                existing_parameter_values = np.array(modified_reactions_parameters_array[:, reaction_parameters_array_kinetic_parameter_index], dtype='float')
                modifiers_array = getInterpolatedModifiersArray(modified_reactions_parameters_array, piecewise_coverage_dependences, species_name, species_coverage, kineticParameterKey, reaction_parameters_array_kinetic_parameter_index)
                modified_values = existing_parameter_values * 10 ** modifiers_array
                modified_reactions_parameters_array[:, reaction_parameters_array_kinetic_parameter_index] = np.array(modified_values, dtype='str')
            if kineticParameterKey == 'E':
                reaction_parameters_array_kinetic_parameter_index = 5
                existing_parameter_values = np.array(modified_reactions_parameters_array[:, reaction_parameters_array_kinetic_parameter_index], dtype='float')
                modifiers_array = getInterpolatedModifiersArray(modified_reactions_parameters_array, piecewise_coverage_dependences, species_name, species_coverage, kineticParameterKey, reaction_parameters_array_kinetic_parameter_index)
                modified_values = existing_parameter_values + modifiers_array
                modified_reactions_parameters_array[:, reaction_parameters_array_kinetic_parameter_index] = np.array(modified_values, dtype='str')
    return modified_reactions_parameters_array

def multiplyReactionsInOnePhase(canteraModule, canteraPhaseObject, reactions_parameters_array, rateMultipliersArray, byProvidedReactionID=True):
    ct = canteraModule
    for inputReactionIndex, individualreactions_parameters_array in enumerate(reactions_parameters_array):
        reactionID = str(int(individualreactions_parameters_array[0]) - 1)
        reactionEquation = str(individualreactions_parameters_array[2])
        if byProvidedReactionID == False:
            reactionID = canteraPhaseObject.reaction_equations().index(reactionEquation)
        canteraPhaseObject.set_multiplier(rateMultipliersArray[inputReactionIndex], int(reactionID))

def modifyReactionsInOnePhase(canteraPhaseObject, reactions_parameters_array, ArrheniusOnly=False, byProvidedReactionID=True, input_Ea_units='J/mol'):
    import cantera as ct
    if str(type(canteraPhaseObject)) == "<class 'cantera.composite.Interface'>":
        phaseType = 'Interface'
        inputReactionTypeNeeded = 'InterfaceReaction'
    elif str(type(canteraPhaseObject)) == "<class 'cantera.composite.Solution'>":
        phaseType = 'Solution'
        inputReactionTypeNeeded = 'Reaction'
    else:
        inputReactionTypeNeeded = 'reaction'
    for individualreactions_parameters_array in reactions_parameters_array:
        individualreactions_parameters_array = np.array(individualreactions_parameters_array)
        reactionID = str(int(individualreactions_parameters_array[0]) - 1)
        reactionEquation = str(individualreactions_parameters_array[2])
        if '(S)' in reactionEquation:
            inputReactionType = 'InterfaceReaction'
        else:
            inputReactionType = 'Reaction'
        if inputReactionType == inputReactionTypeNeeded:
            if byProvidedReactionID == False:
                reactionID = canteraPhaseObject.reaction_equations().index(reactionEquation)
            if input_Ea_units.lower() == 'j/mol':
                individualreactions_parameters_array[5] = float(individualreactions_parameters_array[5]) * 1000.0
            if ArrheniusOnly == True:
                A = str(individualreactions_parameters_array[3])
                b = str(individualreactions_parameters_array[4])
                E = str(individualreactions_parameters_array[5])
                existingReactionObject = canteraPhaseObject.reactions()[int(reactionID)]
                existingReactionObject.rate = ct.Arrhenius(float(A), float(b), float(E))
                canteraPhaseObject.modify_reaction(int(reactionID), existingReactionObject)
            if ArrheniusOnly == False:
                yaml_string = make_reaction_yaml_string(individualreactions_parameters_array, for_full_yaml=False, input_Ea_units='J/kmol')
                from distutils.version import LooseVersion, StrictVersion
                if LooseVersion(ct.__version__) < LooseVersion('2.6'):
                    modifiedReactionObject = ct.Reaction.fromYaml(yaml_string, kinetics=canteraPhaseObject)
                if LooseVersion(ct.__version__) >= LooseVersion('2.6'):
                    modifiedReactionObject = ct.Reaction.from_yaml(yaml_string, kinetics=canteraPhaseObject)
                canteraPhaseObject.modify_reaction(int(reactionID), modifiedReactionObject)

def main():
    pass
if __name__ == '__main__':
    main()