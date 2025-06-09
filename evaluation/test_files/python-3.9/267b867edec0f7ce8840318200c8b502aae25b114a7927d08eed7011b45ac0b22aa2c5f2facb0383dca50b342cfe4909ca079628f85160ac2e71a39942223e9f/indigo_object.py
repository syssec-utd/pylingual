from ctypes import CDLL, POINTER, byref, c_float, c_int, c_ubyte, pointer
from typing import TYPE_CHECKING, Any, Tuple
from .hybridization import Hybridization
from .indigo_exception import IndigoException
from .indigo_lib import IndigoLib
from .salts import SALTS
if TYPE_CHECKING:
    from .indigo import Indigo

class IndigoObject:
    """Wraps all Indigo model objects"""

    def __init__(self, session: 'Indigo', id_: int, parent: Any=None):
        self.session: Indigo = session
        self.id: int = id_
        self.parent: Any = parent

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._lib().indigoClose(self.id)

    def __del__(self):
        self.dispose()

    def __str__(self):
        internal_type = self.dbgInternalType()
        if internal_type == '#02: <molecule>':
            return 'molecule ({})'.format(self.smiles())
        elif internal_type == '#03: <query molecule>':
            return 'query_molecule ({})'.format(self.smarts())
        return object.__str__(self)

    def __iter__(self):
        return self

    def _next(self):
        new_obj = IndigoLib.checkResult(self._lib().indigoNext(self.id))
        if new_obj == 0:
            return None
        else:
            return IndigoObject(self.session, new_obj, self)

    def __next__(self):
        obj = self._next()
        if obj is None:
            raise StopIteration
        return obj

    def _lib(self) -> CDLL:
        return self.session._lib()

    def dispose(self) -> None:
        if self.id >= 0 and self.session.getSessionId() >= 0:
            self._lib().indigoFree(self.id)
            self.id = -1

    def next(self):
        """Generic iterator method

        Returns:
            IndigoObject: next item in the collection
        """
        return self.__next__()

    def oneBitsList(self):
        """Returns string representation of fingerprint

        Returns:
            str: ones bits string for the fingerprint
        """
        return IndigoLib.checkResultString(self._lib().indigoOneBitsList(self.id))

    def mdlct(self):
        """Gets MDL CT as a buffer

        Returns:
            IndigoObject: buffer containing the MDLCT
        """
        buf = self.session.writeBuffer()
        IndigoLib.checkResult(self._lib().indigoSaveMDLCT(self.id, buf.id))
        return buf.toBuffer()

    def xyz(self):
        """Atom method gets coordinates of atom

        Raises:
            IndigoException: if no XYZ coordinates for the object

        Returns:
            list: 3-element array with coordinates
        """
        xyz = self._lib().indigoXYZ(self.id)
        if xyz is None:
            raise IndigoException(self._lib().indigoGetLastError())
        return [xyz[0], xyz[1], xyz[2]]

    def alignAtoms(self, atom_ids, desired_xyz):
        """
        Atom method determines and applies the best transformation
        for the given molecule so that the specified atoms move as close as
        possible to the desired positions

        Args:
            atom_ids (list): atom indexes
            desired_xyz (list): desired coordinates for atoms
                                (size atom_ids * 3)

        Raises:
            IndigoException: if input array size does not match

        Returns:
            float: root-mean-square measure of the difference between the
                   desired and obtained positions
        """
        if len(atom_ids) * 3 != len(desired_xyz):
            raise IndigoException('alignAtoms(): desired_xyz[] must be exactly 3 times bigger than atom_ids[]')
        atoms = (c_int * len(atom_ids))()
        for i in range(len(atoms)):
            atoms[i] = atom_ids[i]
        xyz = (c_float * len(desired_xyz))()
        for i in range(len(desired_xyz)):
            xyz[i] = desired_xyz[i]
        return IndigoLib.checkResultFloat(self._lib().indigoAlignAtoms(self.id, len(atoms), atoms, xyz))

    def addStereocenter(self, type_, v1, v2, v3, v4=-1):
        """Atom method adds stereo information for atom

        Args:
            type_ (int): Stereocenter type. Use Indigo constants ABS, OR,
                         AND, EITHER
            v1 (int): pyramid info
            v2 (int): pyramid info
            v3 (int): pyramid info
            v4 (int): pyramid info. Optional, defaults to -1.

        Returns:
            int: 1 if stereocenter is added successfully
        """
        return IndigoLib.checkResult(self._lib().indigoAddStereocenter(self.id, type_, v1, v2, v3, v4))

    def clone(self):
        """Clones IndigoObject

        Returns:
            IndigoObject: cloned object
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoClone(self.id)))

    def check(self, check_flags=''):
        """Molecule method verifies the structure

        Args:
            check_flags (str): Flags to verify. Optional, defaults to "".

        Returns:
            str: verification result as a JSON string
        """
        if check_flags is None:
            check_flags = ''
        return IndigoLib.checkResultString(self._lib().indigoCheckObj(self.id, check_flags.encode()))

    def close(self):
        """FileOutput method closes file descriptor

        Returns:
            int: 1 if file is closed successfully. -1 otherwise
        """
        return IndigoLib.checkResult(self._lib().indigoClose(self.id))

    def hasNext(self):
        """Iterator method checks presence of a next element

        Returns:
            bool: true if collection has a next element, false otherwise
        """
        return bool(IndigoLib.checkResult(self._lib().indigoHasNext(self.id)))

    def index(self):
        """Atom method returns index of the element

        Returns:
            int: element index
        """
        return IndigoLib.checkResult(self._lib().indigoIndex(self.id))

    def remove(self):
        """Container method removes the element from its container

        Returns:
            int: 1 if element was removed
        """
        return IndigoLib.checkResult(self._lib().indigoRemove(self.id))

    def saveMolfile(self, filename):
        """Molecule method saves the structure into a Molfile

        Args:
            filename (str): full file path to the output file

        Returns:
            int: 1 if file is saved successfully
        """
        return IndigoLib.checkResult(self._lib().indigoSaveMolfileToFile(self.id, filename.encode()))

    def molfile(self):
        """Molecule method returns the structure as a string in Molfile format

        Returns:
            str: Molfile string
        """
        return IndigoLib.checkResultString(self._lib().indigoMolfile(self.id))

    def saveCml(self, filename):
        """Molecule method saves the structure into a CML file

        Args:
            filename (str): full path to the output file

        Returns:
            int: 1 if the file is saved successfully
        """
        return IndigoLib.checkResult(self._lib().indigoSaveCmlToFile(self.id, filename.encode()))

    def cml(self):
        """Molecule method returns the structure as a string in CML format

        Returns:
            str: CML string
        """
        return IndigoLib.checkResultString(self._lib().indigoCml(self.id))

    def saveCdxml(self, filename):
        """Molecule method saves the structure into a CDXML file

        Args:
            filename (str): full path to the output file

        Returns:
            int: 1 if the file is saved successfully
        """
        return IndigoLib.checkResult(self._lib().indigoSaveCdxmlToFile(self.id, filename.encode()))

    def cdxml(self):
        """Molecule method returns the structure as a string in CDXML format

        Returns:
            str: CDXML string
        """
        return IndigoLib.checkResultString(self._lib().indigoCdxml(self.id))

    def json(self):
        """Structure method returns the structure as a string in KET format

        Returns:
            str: KET format for the structure
        """
        return IndigoLib.checkResultString(self._lib().indigoJson(self.id))

    def saveMDLCT(self, output):
        """Structure method saves the structure in MDLCT format into a buffer

        Args:
            output (IndigoObject): buffer to be updated

        Returns:
            int: 1 if the structure is saved
        """
        return IndigoLib.checkResult(self._lib().indigoSaveMDLCT(self.id, output.id))

    def addReactant(self, molecule):
        """Reaction method adds the given molecule copy to reactants

        Args:
            molecule (IndigoObject): molecule to be added

        Returns:
            int: 1 if the molecule was added correctly
        """
        return IndigoLib.checkResult(self._lib().indigoAddReactant(self.id, molecule.id))

    def addProduct(self, molecule):
        """Reaction method adds the given molecule copy to products

        Args:
            molecule (IndigoObject): molecule to be added

        Returns:
            int: 1 if the molecule was added correctly
        """
        return IndigoLib.checkResult(self._lib().indigoAddProduct(self.id, molecule.id))

    def addCatalyst(self, molecule):
        """Reaction method adds the given molecule copy to catalysts

        Args:
            molecule (IndigoObject): molecule to be added

        Returns:
            int: 1 if the molecule was added correctly
        """
        return IndigoLib.checkResult(self._lib().indigoAddCatalyst(self.id, molecule.id))

    def countReactants(self):
        """Reaction method returns the number of reactants

        Returns:
            int: number of reactants
        """
        return IndigoLib.checkResult(self._lib().indigoCountReactants(self.id))

    def countProducts(self):
        """Reaction method returns rge number of products

        Returns:
            int: number of products
        """
        return IndigoLib.checkResult(self._lib().indigoCountProducts(self.id))

    def countCatalysts(self):
        """Reaction method returns the number of catalysts

        Returns:
            int: number of catalysts
        """
        return IndigoLib.checkResult(self._lib().indigoCountCatalysts(self.id))

    def countMolecules(self):
        """Reaction method returns the number of reactants, products, and
           catalysts

        Returns:
            int: number of reactants, products, and catalysts
        """
        return IndigoLib.checkResult(self._lib().indigoCountMolecules(self.id))

    def getMolecule(self, index):
        """Reaction method returns a molecule by index

        Args:
            index (int): molecule index

        Returns:
            IndigoObject: molecule object
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoGetMolecule(self.id, index)))

    def iterateReactants(self):
        """Reaction method iterates reactants

        Returns:
            IndigoObject: reactant iterator
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoIterateReactants(self.id)))

    def iterateProducts(self):
        """Reaction method iterates products

        Returns:
            IndigoObject: product iterator
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoIterateProducts(self.id)))

    def iterateCatalysts(self):
        """Reaction method iterates catalysts

        Returns:
            IndigoObject: catalyst iterator
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoIterateCatalysts(self.id)))

    def iterateMolecules(self):
        """Reaction method iterates molecules

        Returns:
            IndigoObject: reactant, products, and catalysts iterator
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoIterateMolecules(self.id)))

    def saveRxnfile(self, filename):
        """Reaction method saves the reaction into an RXN file

        Args:
            filename (str): output file path for the reaction

        Returns:
            int: 1 if everything is saved without issues
        """
        return IndigoLib.checkResult(self._lib().indigoSaveRxnfileToFile(self.id, filename.encode()))

    def rxnfile(self):
        """Reaction method returns the reaction as a string in RXN format

        Returns:
            str: RXN string
        """
        return IndigoLib.checkResultString(self._lib().indigoRxnfile(self.id))

    def optimize(self, options=''):
        """
        QueryReaction or QueryMolecule method for query optimizations for
        faster substructure search

        Args:
            options (str): Options for optimization. Optional, defaults to "".

        Returns:
            int: 1 if optimization is performed without issues
        """
        if options is None:
            options = ''
        return IndigoLib.checkResult(self._lib().indigoOptimize(self.id, options.encode()))

    def normalize(self, options=''):
        """Molecule method for structure normalization.
        It neutralizes charges, resolves 5-valence Nitrogen, removes hydrogens,
        etc.

        Args:
            options (str): Normalization options. Optional, defaults to "".

        Returns:
            int: 1 if normalization is performed without issues
        """
        if options is None:
            options = ''
        return bool(IndigoLib.checkResult(self._lib().indigoNormalize(self.id, options.encode())))

    def standardize(self):
        """Molecule method for structure standardization.
        It standardizes charges, stereo, etc.

        Returns:
            int: 1 if standardization is performed without issues
        """
        return IndigoLib.checkResult(self._lib().indigoStandardize(self.id))

    def ionize(self, ph, ph_toll):
        """Method for structure ionization at specified pH and pH tolerance

        Args:
            ph (float): pH value
            ph_toll (float): pH tolerance

        Returns:
            int: 1 if ionization is performed without issues
        """
        return IndigoLib.checkResult(self._lib().indigoIonize(self.id, ph, ph_toll))

    def getAcidPkaValue(self, atom: 'IndigoObject', level, min_level):
        """Molecule method calculates acid pKa value

        Args:
            atom (int): input atom index
            level (int): pka level
            min_level (int): pka min level

        Returns:
            float: pka result
        """
        result = IndigoLib.checkResultPtr(self._lib().indigoGetAcidPkaValue(self.id, atom.id, level, min_level))
        return result[0]

    def getBasicPkaValue(self, atom, level, min_level):
        """Molecule method calculates basic pKa value

        Args:
            atom (IndigoObject): input atom index
            level (int): pka level
            min_level (int): pka min level

        Returns:
            float: pka result
        """
        result = IndigoLib.checkResultPtr(self._lib().indigoGetBasicPkaValue(self.id, atom.id, level, min_level))
        return result[0]

    def automap(self, mode=''):
        """Automatic reaction atom-to-atom mapping

        Args:
            mode (str): mode is one of the following (separated by a space):
            "discard" : discards the existing mapping entirely and considers
                        only the existing reaction centers (the default)
            "keep"    : keeps the existing mapping and maps unmapped atoms
            "alter"   : alters the existing mapping, and maps the rest of the
                        reaction but may change the existing mapping
            "clear"   : removes the mapping from the reaction.

            "ignore_charges" : do not consider atom charges while searching
            "ignore_isotopes" : do not consider atom isotopes while searching
            "ignore_valence" : do not consider atom valence while searching
            "ignore_radicals" : do not consider atom radicals while searching

        Returns:
            int: 1 if atom mapping is done without errors
        """
        if mode is None:
            mode = ''
        return IndigoLib.checkResult(self._lib().indigoAutomap(self.id, mode.encode()))

    def atomMappingNumber(self, reaction_atom):
        """Reaction atom method returns assigned mapping

        Args:
            reaction_atom (IndigoObject): reaction molecule atom

        Returns:
            int: atom mapping value
        """
        return IndigoLib.checkResult(self._lib().indigoGetAtomMappingNumber(self.id, reaction_atom.id))

    def setAtomMappingNumber(self, reaction_atom, number):
        """Reaction atom method sets atom mapping

        Args:
            reaction_atom (IndigoObject): reaction molecule atom
            number (int): atom mapping

        Returns:
            int: 1 if atom mapping is set
        """
        return IndigoLib.checkResult(self._lib().indigoSetAtomMappingNumber(self.id, reaction_atom.id, number))

    def reactingCenter(self, reaction_bond):
        """Reaction bond method returns reacting center

        Args:
            reaction_bond (IndigoObject): reaction molecule bond

        Returns:
            int: reacting center enum. One of values
                * RC_NOT_CENTER = -1
                * RC_UNMARKED = 0
                * RC_CENTER = 1
                * RC_UNCHANGED = 2
                * RC_MADE_OR_BROKEN = 4
                * RC_ORDER_CHANGED = 8
        """
        value = c_int()
        res = IndigoLib.checkResult(self._lib().indigoGetReactingCenter(self.id, reaction_bond.id, pointer(value)))
        if res == 0:
            return None
        return value.value

    def setReactingCenter(self, reaction_bond, rc):
        """Reaction bond method sets reacting center

        Args:
            reaction_bond (IndigoObject): reaction molecule bond
            rc (int): reacting center, one of the following
                * RC_NOT_CENTER = -1
                * RC_UNMARKED = 0
                * RC_CENTER = 1
                * RC_UNCHANGED = 2
                * RC_MADE_OR_BROKEN = 4
                * RC_ORDER_CHANGED = 8

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetReactingCenter(self.id, reaction_bond.id, rc))

    def clearAAM(self):
        """Reaction method clears atom mapping for atoms

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoClearAAM(self.id))

    def correctReactingCenters(self):
        """Reaction method corrects reacting centers according to AAM

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoCorrectReactingCenters(self.id))

    def iterateAtoms(self):
        """Molecule method returns an iterator for all atoms
        including r-sites and pseudoatoms

        Returns:
            IndigoObject: atom iterator
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoIterateAtoms(self.id)))

    def iteratePseudoatoms(self):
        """Molecule method returns an iterator for all pseudoatoms

        Returns:
            IndigoObject: atom iterator
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoIteratePseudoatoms(self.id)))

    def iterateRSites(self):
        """Molecule method returns an iterator for all r-sites

        Returns:
            IndigoObject: atom iterator
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoIterateRSites(self.id)))

    def iterateStereocenters(self):
        """Molecule method returns an iterator for all atoms with stereocenters

        Returns:
            IndigoObject: atom iterator
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoIterateStereocenters(self.id)))

    def iterateAlleneCenters(self):
        """Molecule method returns an iterator for all atoms with allene
           centers

        Returns:
            IndigoObject: atom iterator
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoIterateAlleneCenters(self.id)))

    def iterateRGroups(self):
        """Molecule method returns an iterator for all r-group

        Returns:
            IndigoObject: r-group iterator
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoIterateRGroups(self.id)))

    def countRGroups(self):
        """Molecule method returns the number of r-groups

        Returns:
            int: number of r-groups
        """
        return IndigoLib.checkResult(self._lib().indigoCountRGroups(self.id))

    def isPseudoatom(self):
        """Atom method returns true if atom is pseudoatom

        Returns:
            bool: True if pseudoatom
        """
        return bool(IndigoLib.checkResult(self._lib().indigoIsPseudoatom(self.id)))

    def isRSite(self):
        """Atom method returns true if atom is R-site

        Returns:
            bool: True if R-site
        """
        return bool(IndigoLib.checkResult(self._lib().indigoIsRSite(self.id)))

    def isTemplateAtom(self):
        """Atom method returns true if atom is a template atom

        Returns:
            bool: True if template
        """
        return bool(IndigoLib.checkResult(self._lib().indigoIsTemplateAtom(self.id)))

    def stereocenterType(self):
        """Atom method returns stereo center type

        Returns:
            int: type of stereocenter
                * ABS = 1
                * OR = 2
                * AND = 3
                * EITHER = 4
        """
        return IndigoLib.checkResult(self._lib().indigoStereocenterType(self.id))

    def stereocenterGroup(self):
        """Atom method returns stereocenter group

        Returns:
            int: group index
        """
        return IndigoLib.checkResult(self._lib().indigoStereocenterGroup(self.id))

    def setStereocenterGroup(self, group):
        """Atom method sets stereocenter group

        Args:
            group (int): group index
        """
        IndigoLib.checkResult(self._lib().indigoSetStereocenterGroup(self.id, group))

    def changeStereocenterType(self, type_):
        """Atom method changes stereocenter type

        Args:
            type_ (int): stereo type.
                * ABS = 1
                * OR = 2
                * AND = 3
                * EITHER = 4

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoChangeStereocenterType(self.id, type_))

    def validateChirality(self):
        """Molecule or reaction method validates chirality"""
        IndigoLib.checkResult(self._lib().indigoValidateChirality(self.id))

    def singleAllowedRGroup(self):
        """Atom method returns single allowed r-group

        Returns:
            int: single allowed r-group
        """
        return IndigoLib.checkResult(self._lib().indigoSingleAllowedRGroup(self.id))

    def iterateRGroupFragments(self):
        """RGroup method iterates r-group fragments

        Returns:
            IndigoObject: r-group fragment iterator
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoIterateRGroupFragments(self.id)))

    def countAttachmentPoints(self):
        """Molecule or RGroup method returns the number of attachment points

        Returns:
            int: number of attachment points
        """
        return IndigoLib.checkResult(self._lib().indigoCountAttachmentPoints(self.id))

    def iterateAttachmentPoints(self, order):
        """Molecule method iterates attachment points

        Args:
            order (int): attachment points order

        Returns:
            IndigoObject: attachment points iterator
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoIterateAttachmentPoints(self.id, order)))

    def symbol(self):
        """Atom method returns string symbol

        Returns:
            str: atom symbol
        """
        return IndigoLib.checkResultString(self._lib().indigoSymbol(self.id))

    def degree(self):
        """Atom method returns the atom number of neighbors

        Returns:
            int: number of atom neighbors
        """
        return IndigoLib.checkResult(self._lib().indigoDegree(self.id))

    def charge(self):
        """Atom method returns the charge of the atom

        Returns:
            int: charge
        """
        value = c_int()
        res = IndigoLib.checkResult(self._lib().indigoGetCharge(self.id, pointer(value)))
        if res == 0:
            return None
        return value.value

    def getHybridization(self):
        """Atom method returns HybridizationType

        Returns:
            Hybridization: atom hybridization
        """
        return Hybridization(IndigoLib.checkResult(self._lib().indigoGetHybridization(self.id)))

    def getHybridizationStr(self):
        """Atom method returns hybridization type string

        Returns:
            str: atom hybridization
        """
        return self.getHybridization().name

    def getExplicitValence(self):
        """Atom method returns the explicit valence

        Returns:
            int: valence
        """
        value = c_int()
        res = IndigoLib.checkResult(self._lib().indigoGetExplicitValence(self.id, pointer(value)))
        if res == 0:
            return None
        return value.value

    def setExplicitValence(self, valence):
        """Atom method sets the explicit valence

        Args:
            valence (int): valence

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetExplicitValence(self.id, valence))

    def radicalElectrons(self):
        """Atom method returns the number of radical electrons

        Returns:
            int: radical electrons number
        """
        value = c_int()
        res = IndigoLib.checkResult(self._lib().indigoGetRadicalElectrons(self.id, pointer(value)))
        if res == 0:
            return None
        return value.value

    def radical(self):
        """Atom method returns the radical value

        Returns:
            int: radical value
        """
        value = c_int()
        res = IndigoLib.checkResult(self._lib().indigoGetRadical(self.id, pointer(value)))
        if res == 0:
            return None
        return value.value

    def setRadical(self, radical):
        """Atom method sets the radical value

        Args:
            radical (int): radical value

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetRadical(self.id, radical))

    def atomicNumber(self):
        """Atom method returns the atomic number

        Returns:
            int: atomic number
        """
        return IndigoLib.checkResult(self._lib().indigoAtomicNumber(self.id))

    def isotope(self):
        """Atom method returns the isotope number

        Returns:
            int: isotope number
        """
        return IndigoLib.checkResult(self._lib().indigoIsotope(self.id))

    def valence(self):
        """Atom method returns the valence

        Returns:
            int: atom valence
        """
        return IndigoLib.checkResult(self._lib().indigoValence(self.id))

    def checkValence(self):
        """Atom method validates the valence

        Returns:
            int: 1 if valence has no errors, 0 otherwise
        """
        return IndigoLib.checkResult(self._lib().indigoCheckValence(self.id))

    def checkQuery(self):
        """Atom, Bond, Molecule, Reaction method verifies if object is query

        Returns:
            int: 1 if object is query, 0 otherwise
        """
        return IndigoLib.checkResult(self._lib().indigoCheckQuery(self.id))

    def checkRGroups(self):
        """Molecule method verifies if the structure contains r-groups

        Returns:
            int: 1 if molecule contains r-groups, 0 otherwise
        """
        return IndigoLib.checkResult(self._lib().indigoCheckRGroups(self.id))

    def checkChirality(self):
        """Molecule method verifies if the structure has a chiral flag

        Returns:
            int: 1 if there is chiral flag, 0 otherwise
        """
        return IndigoLib.checkResult(self._lib().indigoCheckChirality(self.id))

    def check3DStereo(self):
        """Molecule method verifies if the structure contains 3d stereo

        Returns:
            int: 1 if structure contains 3d stereo, 0 otherwise
        """
        return IndigoLib.checkResult(self._lib().indigoCheck3DStereo(self.id))

    def checkStereo(self):
        """Molecule method verifies if the structure contains stereocenters

        Returns:
            int: 1 if molecule contains stereo, 0 otherwise
        """
        return IndigoLib.checkResult(self._lib().indigoCheckStereo(self.id))

    def checkSalt(self):
        """Molecule method verifies if the structure contains salt.

        Returns:
            bool: True if structure contains salt
        """
        for target_fragment in self.iterateComponents():
            target_fragment = target_fragment.clone()
            for salt in SALTS:
                query_salt = self.session.loadQueryMolecule(salt)
                matcher = self.session.substructureMatcher(target_fragment)
                if matcher.match(query_salt):
                    return True
        return False

    def stripSalt(self, inplace=False):
        """Molecule method strips all inorganic components.

        Args:
            inplace(bool): if False - returns the copy of the molecule,
                           without inorganic components, if True - strips
                           inorganic components from the molecule itself.

        Returns:
            IndigoObject: if inplace=False - new molecule without inorganic
                          components,
                          if inplace=True - initial molecule without inorganic
                          components.
        """
        salts_atoms = []
        idx = 0
        for target_fragment in self.iterateComponents():
            target_fragment = target_fragment.clone()
            n_atoms = target_fragment.countAtoms()
            for salt in SALTS:
                query_salt = self.session.loadQueryMolecule(salt)
                matcher = self.session.substructureMatcher(target_fragment)
                if matcher.match(query_salt):
                    salt_position = [i for i in range(idx, idx + n_atoms)]
                    salts_atoms.extend(salt_position)
            idx += n_atoms
        if not inplace:
            saltless_fragment = self.clone()
            saltless_fragment.removeAtoms(salts_atoms)
            return saltless_fragment
        else:
            self.removeAtoms(salts_atoms)
            return self

    def countHydrogens(self):
        """Atom or Molecule method returns the number of hydrogens

        Returns:
            int: number of hydrogens
        """
        value = c_int()
        res = IndigoLib.checkResult(self._lib().indigoCountHydrogens(self.id, pointer(value)))
        if res == 0:
            return None
        return value.value

    def countImplicitHydrogens(self):
        """Atom or Molecule method returns the number of implicit hydrogens

        Returns:
            int: number of hydrogens
        """
        return IndigoLib.checkResult(self._lib().indigoCountImplicitHydrogens(self.id))

    def setXYZ(self, x, y, z):
        """Atom methods sets the given coordinates

        Args:
            x (float): X coordinate
            y (float): Y coordinate
            z (float): Z coordinate

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetXYZ(self.id, x, y, z))

    def countSuperatoms(self):
        """Molecule method calculates the number of super atoms

        Returns:
            int: number of super atoms
        """
        return IndigoLib.checkResult(self._lib().indigoCountSuperatoms(self.id))

    def countDataSGroups(self):
        """Molecule method returns the number of data s-groups

        Returns:
            int: number of s-groups
        """
        return IndigoLib.checkResult(self._lib().indigoCountDataSGroups(self.id))

    def countRepeatingUnits(self):
        """Molecule method returns the number of repeating units

        Returns:
            int: number of repeating units
        """
        return IndigoLib.checkResult(self._lib().indigoCountRepeatingUnits(self.id))

    def countMultipleGroups(self):
        """Molecule method returns the number of multiple s-groups

        Returns:
            int: number of multiple s-groups
        """
        return IndigoLib.checkResult(self._lib().indigoCountMultipleGroups(self.id))

    def countGenericSGroups(self):
        """Molecule method returns the number of generic s-groups

        Returns:
            int: number of generic s-groups
        """
        return IndigoLib.checkResult(self._lib().indigoCountGenericSGroups(self.id))

    def iterateDataSGroups(self):
        """Molecule method iterates data s-groups

        Returns:
            IndigoObject: s-groups iterator
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoIterateDataSGroups(self.id)))

    def iterateSuperatoms(self):
        """Molecule method iterates superatoms

        Returns:
            IndigoObject: superatoms iterator
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoIterateSuperatoms(self.id)))

    def iterateGenericSGroups(self):
        """Molecule method iterates generic s-groups

        Returns:
            IndigoObject: generic s-groups iterator
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoIterateGenericSGroups(self.id)))

    def iterateRepeatingUnits(self):
        """Molecule method iterates repeating units

        Returns:
            IndigoObject: repeating units iterator
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoIterateRepeatingUnits(self.id)))

    def iterateMultipleGroups(self):
        """Molecule method iterates Multiple s-groups

        Returns:
            IndigoObject: Mul s-groups iterator
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoIterateMultipleGroups(self.id)))

    def iterateSGroups(self):
        """Molecule method iterates s-groups

        Returns:
            IndigoObject: s-groups iterator
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoIterateSGroups(self.id)))

    def iterateTGroups(self):
        """Molecule method iterates t-groups

        Returns:
            IndigoObject: t-groups iterator
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoIterateTGroups(self.id)))

    def getSuperatom(self, index):
        """Molecule method returns a superatom by index

        Args:
            index (int): super atom index

        Returns:
            IndigoObject: super atom
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoGetSuperatom(self.id, index)))

    def getDataSGroup(self, index):
        """Molecule method returns a data s-group by index

        Args:
            index (int): sgroup index

        Returns:
            IndigoObject: data sgroup
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoGetDataSGroup(self.id, index)))

    def getGenericSGroup(self, index):
        """Molecule method returns a generic s-group by index

        Args:
            index (int): s-group index

        Returns:
            IndigoObject: generic s-group
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoGetGenericSGroup(self.id, index)))

    def getMultipleGroup(self, index):
        """Molecule method returns a Multiple s-group by index

        Args:
            index (int): mul s-group index

        Returns:
            IndigoObject: mul s-group
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoGetMultipleGroup(self.id, index)))

    def getRepeatingUnit(self, index):
        """Molecule method returns a repeating unit by index

        Args:
            index (int): repeating unit index

        Returns:
            IndigoObject: repeating unit
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoGetRepeatingUnit(self.id, index)))

    def description(self):
        """Data s-group method returns description

        Returns:
            str: s-group description
        """
        return IndigoLib.checkResultString(self._lib().indigoDescription(self.id))

    def data(self):
        """Data s-group method returns data

        Returns:
            str: s-group data
        """
        return IndigoLib.checkResultString(self._lib().indigoData(self.id))

    def addDataSGroup(self, atoms, bonds, description, data):
        """Molecule method adds a data s-group

        Args:
            atoms (list): atom indexes list
            bonds (list): bond indexes list
            description (str): data s-group description
            data (str): data s-group data

        Returns:
            IndigoObject: SGroup object
        """
        arr2 = (c_int * len(atoms))()
        for i in range(len(atoms)):
            arr2[i] = atoms[i]
        arr4 = (c_int * len(bonds))()
        for i in range(len(bonds)):
            arr4[i] = bonds[i]
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoAddDataSGroup(self.id, len(arr2), arr2, len(arr4), arr4, description.encode(), data.encode())))

    def addSuperatom(self, atoms, name):
        """Molecule method adds superatom

        Args:
            atoms (list): atom indexes list
            name (str): superatom name

        Returns:
            IndigoObject: superatom object
        """
        arr2 = (c_int * len(atoms))()
        for i in range(len(atoms)):
            arr2[i] = atoms[i]
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoAddSuperatom(self.id, len(arr2), arr2, name.encode())))

    def setDataSGroupXY(self, x, y, options=''):
        """SGroup method sets coordinates

        Args:
            x (float): X coordinate
            y (float): Y coordinate
            options (str): options. Optional, defaults to "".

        Returns:
            int: 1 if there are no errors
        """
        if options is None:
            options = ''
        return IndigoLib.checkResult(self._lib().indigoSetDataSGroupXY(self.id, x, y, options.encode()))

    def setSGroupData(self, data):
        """SGroup method adds data

        Args:
            data (str): data string

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetSGroupData(self.id, data.encode()))

    def setSGroupCoords(self, x, y):
        """SGroup method sets coordinates

        Args:
            x (float): X coordinate
            y (float): Y coordinate

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetSGroupCoords(self.id, x, y))

    def setSGroupDescription(self, description):
        """SGroup method sets description

        Args:
            description (str): description string

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetSGroupDescription(self.id, description.encode()))

    def setSGroupFieldName(self, name):
        """SGroup method sets field name

        Args:
            name (str): name string

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetSGroupFieldName(self.id, name.encode()))

    def setSGroupQueryCode(self, code):
        """SGroup methods sets query code

        Args:
            code (str): code string

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetSGroupQueryCode(self.id, code.encode()))

    def setSGroupQueryOper(self, oper):
        """SGroup method sets query oper

        Args:
            oper (str): query oper string

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetSGroupQueryOper(self.id, oper.encode()))

    def setSGroupDisplay(self, option):
        """SGroup method sets display

        Args:
            option (str): display string

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetSGroupDisplay(self.id, option.encode()))

    def setSGroupLocation(self, option):
        """SGroup method sets location

        Args:
            option (str): location string

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetSGroupLocation(self.id, option.encode()))

    def setSGroupTag(self, tag):
        """SGroup method sets tag

        Args:
            tag (str): tag string

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetSGroupTag(self.id, tag.encode()))

    def setSGroupTagAlign(self, tag_align):
        """SGroup method sets tag align

        Args:
            tag_align (int): tag align value

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetSGroupTagAlign(self.id, tag_align))

    def setSGroupDataType(self, data_type):
        """SGroup method sets data type

        Args:
            data_type (str): data type string

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetSGroupDataType(self.id, data_type.encode()))

    def setSGroupXCoord(self, x):
        """Sgroup method sets X coordinate

        Args:
            x (float): X coordinate

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetSGroupXCoord(self.id, x))

    def setSGroupYCoord(self, y):
        """Sgroup method sets Y coordinate

        Args:
            y (float): Y coordinate

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetSGroupYCoord(self.id, y))

    def createSGroup(self, sgtype, mapping, name):
        """Molecule method creates an SGroup

        Args:
            sgtype (str): sgroup type
            mapping (IndigoObject): mapping object
            name (str): sgroup name

        Returns:
            IndigoObject: sgroup object
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoCreateSGroup(sgtype.encode(), mapping.id, name.encode())))

    def setSGroupClass(self, sgclass):
        """SGroup method sets class

        Args:
            sgclass (str): sgroup class

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetSGroupClass(self.id, sgclass.encode()))

    def setSGroupName(self, sgname):
        """SGroup method sets group name

        Args:
            sgname (str): sgroup name string

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetSGroupName(self.id, sgname.encode()))

    def getSGroupClass(self):
        """SGroup method returns sgroup class

        Returns:
            str: sgroup class string
        """
        return IndigoLib.checkResultString(self._lib().indigoGetSGroupClass(self.id))

    def getSGroupName(self):
        """SGroup method returns sgroup name

        Returns:
            str: sgroup name string
        """
        return IndigoLib.checkResultString(self._lib().indigoGetSGroupName(self.id))

    def getSGroupNumCrossBonds(self):
        """SGroup method returns the number of cross bonds

        Returns:
            int: number of cross bonds
        """
        return IndigoLib.checkResult(self._lib().indigoGetSGroupNumCrossBonds(self.id))

    def addSGroupAttachmentPoint(self, aidx, lvidx, apid):
        """SGroup method sets attachment point info

        Args:
            aidx (int): index
            lvidx (int): index
            apid (str): id string

        Returns:
            int: attachment point index
        """
        return IndigoLib.checkResult(self._lib().indigoAddSGroupAttachmentPoint(self.id, aidx, lvidx, apid.encode()))

    def deleteSGroupAttachmentPoint(self, apidx):
        """SGroup method removes the attachment point

        Args:
            apidx (int): attachment point index

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoDeleteSGroupAttachmentPoint(self.id, apidx))

    def getSGroupDisplayOption(self):
        """SGroup method returns display option

        Returns:
            int: display option
        """
        return IndigoLib.checkResult(self._lib().indigoGetSGroupDisplayOption(self.id))

    def setSGroupDisplayOption(self, option):
        """SGroup method sets display option

        Args:
            option (int): display option

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetSGroupDisplayOption(self.id, option))

    def getSGroupSeqId(self):
        """SGroup method returns SEQID

        Returns:
            int: SEQID value
        """
        return IndigoLib.checkResult(self._lib().indigoGetSGroupSeqId(self.id))

    def getSGroupCoords(self):
        """Sgroup method returns coordinates

        Raises:
            IndigoException: if no coordinates exist for the sgroup

        Returns:
            list: [x, y] coordinates
        """
        xyz = self._lib().indigoGetSGroupCoords(self.id)
        if xyz is None:
            raise IndigoException(self._lib().indigoGetLastError())
        return [xyz[0], xyz[1]]

    def getRepeatingUnitSubscript(self):
        """Repeating unit method returns subscript

        Returns:
            str: subscript value
        """
        return IndigoLib.checkResultString(self._lib().indigoGetRepeatingUnitSubscript(self.id))

    def getRepeatingUnitConnectivity(self):
        """Repeating unit method returns connectivity

        Returns:
            int: connectivity value
        """
        return IndigoLib.checkResult(self._lib().indigoGetRepeatingUnitConnectivity(self.id))

    def getSGroupMultiplier(self):
        """Multiple group method returns multiplier

        Returns:
            int: multiplier value
        """
        return IndigoLib.checkResult(self._lib().indigoGetSGroupMultiplier(self.id))

    def setSGroupMultiplier(self, mult):
        """Multiple group sets multiplier value

        Args:
            mult (int): multiplier value

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetSGroupMultiplier(self.id, mult))

    def setSGroupBrackets(self, style, x1, y1, x2, y2, x3, y3, x4, y4):
        """SGroup method sets brackets

        Args:
            style (int): bracket style
            x1 (float): X1 coordinate
            y1 (float): Y1 coordinate
            x2 (float): X2 coordinate
            y2 (float): Y2 coordinate
            x3 (float): X3 coordinate
            y3 (float): Y3 coordinate
            x4 (float): X4 coordinate
            y4 (float): Y4 coordinate

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetSGroupBrackets(self.id, style, x1, y1, x2, y2, x3, y3, x4, y4))

    def findSGroups(self, prop, val):
        """Molecule method finds SGroup by property and value

        Args:
            prop (str): property string
            val (str): value string

        Returns:
            IndigoObject: SGroup iterator
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoFindSGroups(self.id, prop.encode(), val.encode())))

    def getSGroupType(self):
        """SGroup method returns type

        Returns:
            int: sgroup type
        """
        return IndigoLib.checkResult(self._lib().indigoGetSGroupType(self.id))

    def getSGroupIndex(self):
        """SGroup method returns index

        Returns:
            int: sgroup index
        """
        return IndigoLib.checkResult(self._lib().indigoGetSGroupIndex(self.id))

    def getSGroupOriginalId(self):
        """SGroup method returns original id

        Returns:
            int: original id
        """
        return IndigoLib.checkResult(self._lib().indigoGetSGroupOriginalId(self.id))

    def setSGroupOriginalId(self, original):
        """SGroup method sets original id

        Args:
            original (int): original id value

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetSGroupOriginalId(self.id, original))

    def getSGroupParentId(self):
        """SGroup method returns parent id

        Returns:
            int: parent id
        """
        return IndigoLib.checkResult(self._lib().indigoGetSGroupParentId(self.id))

    def setSGroupParentId(self, parent):
        """SGroup method sets parent id

        Args:
            parent (int): parent id

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetSGroupParentId(self.id, parent))

    def addTemplate(self, templates, name):
        """Molecule method adds template TGroup

        Args:
            templates (IndigoObject): molecule template
            name (str): template name

        Returns:
            int: template index
        """
        return IndigoLib.checkResult(self._lib().indigoAddTemplate(self.id, templates.id, name.encode()))

    def removeTemplate(self, name):
        """Molecule method removes template TGroup by name

        Args:
            name (str): template name

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoRemoveTemplate(self.id, name.encode()))

    def findTemplate(self, name):
        """Molecule method finds template by name

        Args:
            name (str): template name

        Returns:
            int: template index
        """
        return IndigoLib.checkResult(self._lib().indigoFindTemplate(self.id, name.encode()))

    def getTGroupClass(self):
        """TGroup method returns class

        Returns:
            str: class value
        """
        return IndigoLib.checkResultString(self._lib().indigoGetTGroupClass(self.id))

    def getTGroupName(self):
        """TGroup method returns name

        Returns:
            str: name value
        """
        return IndigoLib.checkResultString(self._lib().indigoGetTGroupName(self.id))

    def getTGroupAlias(self):
        """TGroup method returns alias

        Returns:
            str: alias value
        """
        return IndigoLib.checkResultString(self._lib().indigoGetTGroupAlias(self.id))

    def transformSCSRtoCTAB(self):
        """Molecule method transforms SCSR to full CTAB

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoTransformSCSRtoCTAB(self.id))

    def transformCTABtoSCSR(self, templates):
        """Molecule method transforms CTAB to SCSR using templates

        Args:
            templates (IndigoObject): Molecule object with templates

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoTransformCTABtoSCSR(self.id, templates.id))

    def getTemplateAtomClass(self):
        """Atom method returns template class

        Returns:
            str: template class
        """
        return IndigoLib.checkResult(self._lib().indigoGetTemplateAtomClass(self.id))

    def setTemplateAtomClass(self, name):
        """Atom method sets template class

        Args:
            name (str): class name

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetTemplateAtomClass(self.id, name.encode()))

    def clean2d(self):
        """Molecule or reaction method recalculates coordinates

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoClean2d(self.id))

    def resetCharge(self):
        """Atom method resets charge

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoResetCharge(self.id))

    def resetExplicitValence(self):
        """Atom method resets explicit valence

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoResetExplicitValence(self.id))

    def resetRadical(self):
        """Atom method resets radical

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoResetRadical(self.id))

    def resetIsotope(self):
        """Atom method resets isotope

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoResetIsotope(self.id))

    def setAttachmentPoint(self, order):
        """Atom method sets attachment point

        Args:
            order (int): attachment point order

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetAttachmentPoint(self.id, order))

    def clearAttachmentPoints(self):
        """Atom method clears attachment points

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoClearAttachmentPoints(self.id))

    def removeConstraints(self, type_):
        """Atom method removes constraints

        Args:
            type_ (str): constraint type

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoRemoveConstraints(self.id, type_.encode()))

    def addConstraint(self, type_, value):
        """Atom method adds a constraint

        Args:
            type_ (str): constraint type
            value (str): constraint value

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoAddConstraint(self.id, type_.encode(), value.encode()))

    def addConstraintNot(self, type_, value):
        """Atom method adds a NOT constraint

        Args:
            type_ (str): constraint type
            value (str): constraint value

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoAddConstraintNot(self.id, type_.encode(), value.encode()))

    def addConstraintOr(self, type_, value):
        """Atom method adds an OR constraint

        Args:
            type_ (str): constraint type
            value (str): constraint value

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoAddConstraintOr(self.id, type_.encode(), value.encode()))

    def resetStereo(self):
        """Atom or bond method resets stereo

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoResetStereo(self.id))

    def invertStereo(self):
        """Atom or bond method inverts stereo

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoInvertStereo(self.id))

    def countAtoms(self):
        """Molecule or SGroup method returns the number of atoms

        Returns:
            int: number of atoms
        """
        return IndigoLib.checkResult(self._lib().indigoCountAtoms(self.id))

    def countBonds(self):
        """Molecule or SGroup method returns the number of bonds

        Returns:
            int: number of bonds
        """
        return IndigoLib.checkResult(self._lib().indigoCountBonds(self.id))

    def countPseudoatoms(self):
        """Molecule method returns the number of pseudoatoms

        Returns:
            int: number of pseudoatoms
        """
        return IndigoLib.checkResult(self._lib().indigoCountPseudoatoms(self.id))

    def countRSites(self):
        """Molecule method returns the number of r-sites

        Returns:
            int: number of r-sites
        """
        return IndigoLib.checkResult(self._lib().indigoCountRSites(self.id))

    def iterateBonds(self):
        """Molecule or SGroup method returns bonds iterator

        Returns:
            IndigoObject: bonds iterator
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoIterateBonds(self.id)))

    def logP(self):
        """Molecule method returns calculated Crippen logP value

        Returns:
            float: calculated logP value of the molecule
        """
        return IndigoLib.checkResultFloat(self._lib().indigoLogP(self.id))

    def molarRefractivity(self):
        """Molecule method returns calculated Crippen molar refractivity

        Returns:
            float: calculated value of molar refractivity
        """
        return IndigoLib.checkResultFloat(self._lib().indigoMolarRefractivity(self.id))

    def pKa(self):
        """Molecule method returns calculated Lee-Crippen SMARTS pKa value

        Returns:
            float: calculated pKa value of the molecule
        """
        return IndigoLib.checkResultFloat(self._lib().indigoPka(self.id))

    def bondOrder(self):
        """Bond method returns bond order

        Returns:
            int: bond order
        """
        return IndigoLib.checkResult(self._lib().indigoBondOrder(self.id))

    def bondStereo(self):
        """Bond method returns bond stereo

        Returns:
            int: bond stereo
        """
        return IndigoLib.checkResult(self._lib().indigoBondStereo(self.id))

    def topology(self):
        """Bond method returns bond topology

        Returns:
            int: bond topology
        """
        return IndigoLib.checkResult(self._lib().indigoTopology(self.id))

    def iterateNeighbors(self):
        """Atom method returns neighbors iterator

        Returns:
            IndigoObject: atom neighbor iterator
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoIterateNeighbors(self.id)))

    def bond(self):
        """Atom neighbor method returns bond

        Returns:
            IndigoObject: bond object
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoBond(self.id)))

    def getAtom(self, idx):
        """Molecule method returns atom by index

        Args:
            idx (int): atom index

        Returns:
            IndigoObject: atom object
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoGetAtom(self.id, idx)))

    def getBond(self, idx):
        """Molecule method returns bond by index

        Args:
            idx (int): bond index

        Returns:
            IndigoObject: bond object
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoGetBond(self.id, idx)))

    def source(self):
        """Bond method returns source atom

        Returns:
            IndigoObject: atom object
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoSource(self.id)))

    def destination(self):
        """Bond method returns destination atom

        Returns:
            IndigoObject: atom object
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoDestination(self.id)))

    def clearCisTrans(self):
        """Molecule or reaction method clears cis-trans stereo

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoClearCisTrans(self.id))

    def clearStereocenters(self):
        """Molecule or reaction method clears stereo centers

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoClearStereocenters(self.id))

    def countStereocenters(self):
        """Molecule method returns the number of stereocenters

        Returns:
            int: number of stereocenters
        """
        return IndigoLib.checkResult(self._lib().indigoCountStereocenters(self.id))

    def clearAlleneCenters(self):
        """Molecule method clears allene centers

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoClearAlleneCenters(self.id))

    def countAlleneCenters(self):
        """Molecule method returns the number of allene centers

        Returns:
            int: number of allene centers
        """
        return IndigoLib.checkResult(self._lib().indigoCountAlleneCenters(self.id))

    def resetSymmetricCisTrans(self):
        """Molecule or reaction method clears symmetric stereo cis-trans

        Returns:
            int: number of reset centers
        """
        return IndigoLib.checkResult(self._lib().indigoResetSymmetricCisTrans(self.id))

    def resetSymmetricStereocenters(self):
        """Molecule or reaction method clears symmetric stereocenters

        Returns:
            int: number of reset centers
        """
        return IndigoLib.checkResult(self._lib().indigoResetSymmetricStereocenters(self.id))

    def markEitherCisTrans(self):
        """Molecule or reaction method marks cis-trans stereo

        Returns:
            int: number of marked stereo
        """
        return IndigoLib.checkResult(self._lib().indigoMarkEitherCisTrans(self.id))

    def markStereobonds(self):
        """Molecule or reaction method marks stereo bonds

        Returns:
            int: 0 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoMarkStereobonds(self.id))

    def addAtom(self, symbol):
        """Molecule method adds an atom

        Args:
            symbol (str): atom symbol

        Returns:
            IndigoObject: atom object
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoAddAtom(self.id, symbol.encode())))

    def resetAtom(self, symbol):
        """Atom method resets atom to the new symbol

        Args:
            symbol (str): atom symbol
        """
        IndigoLib.checkResult(self._lib().indigoResetAtom(self.id, symbol.encode()))

    def addRSite(self, name):
        """Molecule method adds r-site

        Args:
            name (str): r-site name

        Returns:
            IndigoObject: atom object
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoAddRSite(self.id, name.encode())))

    def setRSite(self, name):
        """Atom method sets r-site

        Args:
            name (str): r-site name

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetRSite(self.id, name.encode()))

    def setCharge(self, charge):
        """Atom method sets charge

        Args:
            charge (int): charge value

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetCharge(self.id, charge))

    def setIsotope(self, isotope):
        """Atom method sets isotope

        Args:
            isotope (int): isotope value

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetIsotope(self.id, isotope))

    def setImplicitHCount(self, impl_h):
        """Atom method sets implicit hydrogen count

        Args:
            impl_h (int): implicit hydrogen count

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetImplicitHCount(self.id, impl_h))

    def addBond(self, destination, order):
        """Atom method adds bond

        Args:
            destination (IndigoObject): atom object destination
            order (int): bond order

        Returns:
            IndigoObject: bond object
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoAddBond(self.id, destination.id, order)))

    def setBondOrder(self, order):
        """Bond method sets order

        Args:
            order (int): order value

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetBondOrder(self.id, order))

    def merge(self, what):
        """Molecule method merges molecule with the given structure

        Args:
            what (IndigoObject): molecule object to merge with

        Returns:
            IndigoObject: mapping object for merged structure
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoMerge(self.id, what.id)))

    def highlight(self):
        """Atom or bond method to add highlighting

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoHighlight(self.id))

    def unhighlight(self):
        """Atom or bond method to remove highlighting

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoUnhighlight(self.id))

    def isHighlighted(self):
        """Atom or bond method returns True if highlighted

        Returns:
            bool: True if highlighted, False otherwise
        """
        return bool(IndigoLib.checkResult(self._lib().indigoIsHighlighted(self.id)))

    def countComponents(self):
        """Molecule method returns the number of components

        Returns:
            int: number of components
        """
        return IndigoLib.checkResult(self._lib().indigoCountComponents(self.id))

    def componentIndex(self):
        """Atom method returns component index

        Returns:
            int: component index
        """
        return IndigoLib.checkResult(self._lib().indigoComponentIndex(self.id))

    def iterateComponents(self):
        """Molecule method returns components iterator

        Returns:
            IndigoObject: molecule components iterator
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoIterateComponents(self.id)))

    def component(self, index):
        """Molecule method returns component by index

        Args:
            index (int): component index

        Returns:
            IndigoObject: molecule component object
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoComponent(self.id, index)))

    def countSSSR(self):
        """Molecule method returns the size of the smallest set of the smallest
           rings

        Returns:
            int: SSSR rings count
        """
        return IndigoLib.checkResult(self._lib().indigoCountSSSR(self.id))

    def iterateSSSR(self):
        """Molecule method returns the smallest set of the smallest rings
           iterator

        Returns:
            IndigoObject: SSSR iterator
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoIterateSSSR(self.id)))

    def iterateSubtrees(self, min_atoms, max_atoms):
        """Molecule method returns subtrees iterator

        Args:
            min_atoms (int): min atoms neighbors limit
            max_atoms (int): max atoms neighbors limit

        Returns:
            IndigoObject: subtrees iterator
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoIterateSubtrees(self.id, min_atoms, max_atoms)))

    def iterateRings(self, min_atoms, max_atoms):
        """Molecule method returns rings iterator

        Args:
            min_atoms (int): min atoms neighbors limit
            max_atoms (int): max atoms neighbors limit

        Returns:
            IndigoObject: rings iterator
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoIterateRings(self.id, min_atoms, max_atoms)))

    def iterateEdgeSubmolecules(self, min_bonds, max_bonds):
        """Molecule method returns edge submolecules iterator

        Args:
            min_bonds (int): min bonds neighbors limit
            max_bonds (int): max bonds neighbors limit

        Returns:
            IndigoObject: submolecules iterator
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoIterateEdgeSubmolecules(self.id, min_bonds, max_bonds)))

    def countHeavyAtoms(self):
        """Molecule method returns the number of heavy atoms

        Returns:
            int: heavy atom count
        """
        return IndigoLib.checkResult(self._lib().indigoCountHeavyAtoms(self.id))

    def grossFormula(self):
        """Molecule method returns gross formula

        Returns:
            str: gross formula
        """
        gf_id = IndigoLib.checkResult(self._lib().indigoGrossFormula(self.id))
        gf = IndigoObject(self.session, gf_id)
        return IndigoLib.checkResultString(self._lib().indigoToString(gf.id))

    def molecularWeight(self):
        """Molecule method returns molecular weight

        Returns:
            float: molecular weight value
        """
        return IndigoLib.checkResultFloat(self._lib().indigoMolecularWeight(self.id))

    def mostAbundantMass(self):
        """Molecule method returns the most abundant mass

        Returns:
            float: most abundant mass
        """
        return IndigoLib.checkResultFloat(self._lib().indigoMostAbundantMass(self.id))

    def monoisotopicMass(self):
        """Molecule method returns the monoisotopic mass

        Returns:
            float: monoisotopic mass
        """
        return IndigoLib.checkResultFloat(self._lib().indigoMonoisotopicMass(self.id))

    def massComposition(self):
        """Molecule method returns mass composition

        Returns:
            str: mass composition string
        """
        return IndigoLib.checkResultString(self._lib().indigoMassComposition(self.id))

    def tpsa(self, include_sp=False):
        """Molecule method returns the TPSA value

        Args:
            include_sp (bool): include S and P atoms to TPSA calculation,
                              false by default

        Returns:
            float: TPSA value
        """
        return IndigoLib.checkResultFloat(self._lib().indigoTPSA(self.id, include_sp))

    def numRotatableBonds(self):
        """Molecule method returns the number of rotatable bonds

        Returns:
            int: number of rotatable bonds
        """
        return IndigoLib.checkResult(self._lib().indigoNumRotatableBonds(self.id))

    def numHydrogenBondAcceptors(self):
        """Molecule method returns the number of hydrogen bond acceptors

        Returns:
            float: number of hydrogen bond acceptors
        """
        return IndigoLib.checkResult(self._lib().indigoNumHydrogenBondAcceptors(self.id))

    def numHydrogenBondDonors(self):
        """Molecule method returns the number of hydrogen bond donors

        Returns:
            float: number of hydrogen bond donors
        """
        return IndigoLib.checkResult(self._lib().indigoNumHydrogenBondDonors(self.id))

    def canonicalSmiles(self):
        """Molecule or reaction method returns canonical smiles

        Returns:
            str: canonical smiles string
        """
        return IndigoLib.checkResultString(self._lib().indigoCanonicalSmiles(self.id))

    def canonicalSmarts(self):
        """Molecule method returns canonical smarts

        Returns:
            str: canonical smarts
        """
        return IndigoLib.checkResultString(self._lib().indigoCanonicalSmarts(self.id))

    def hash(self):
        """Molecule or Reaction method returns hash code

        Returns:
            int: hash
        """
        return IndigoLib.checkResult(self._lib().indigoHash(self.id))

    def layeredCode(self):
        """Molecule method returns layered code

        Returns:
            str: layered code string
        """
        return IndigoLib.checkResultString(self._lib().indigoLayeredCode(self.id))

    def symmetryClasses(self) -> Tuple[int, ...]:
        """Molecule method returns symmetry classes

        Returns:
            Tuple[int, ...]: symmetry classes integer sequence
        """
        c_size = c_int()
        c_buf = IndigoLib.checkResultPtr(self._lib().indigoSymmetryClasses(self.id, pointer(c_size)))
        return tuple((c_buf[i] for i in range(c_size.value)))

    def hasCoord(self):
        """Molecule method returns True if the structure contains coordinates

        Returns:
            bool: True if contains coordinates, False otherwise
        """
        return bool(IndigoLib.checkResult(self._lib().indigoHasCoord(self.id)))

    def hasZCoord(self):
        """Molecule method returns True if the structure contains Z coordinate

        Returns:
            bool: True if contains Z coordinate, False otherwise
        """
        return bool(IndigoLib.checkResult(self._lib().indigoHasZCoord(self.id)))

    def isChiral(self):
        """Molecule method returns True if the structure contains chiral flag

        Returns:
            bool: True if contains chiral flag, False otherwise
        """
        return bool(IndigoLib.checkResult(self._lib().indigoIsChiral(self.id)))

    def isPossibleFischerProjection(self, options):
        """Molecule method returns True if the structure contains possible
           Fischer projection

        Args:
            options (str): projection options

        Returns:
            bool: True if structure contains possible Fischer projection
        """
        return bool(IndigoLib.checkResult(self._lib().indigoIsPossibleFischerProjection(self.id, options.encode())))

    def createSubmolecule(self, vertices):
        """Molecule method creates a submolecule from the given atom list

        Args:
            vertices (list): list of atom indexes

        Returns:
            IndigoObject: molecule object as submolecule
        """
        arr2 = (c_int * len(vertices))()
        for i in range(len(vertices)):
            arr2[i] = vertices[i]
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoCreateSubmolecule(self.id, len(arr2), arr2)))

    def createEdgeSubmolecule(self, vertices, edges):
        """Molecule method creates a submolecule from the given vertex atom
           and bond list

        Args:
            vertices (list): list of atom indexes
            edges (list): list of bond indexes

        Returns:
            IndigoObject: molecule object as submolecule
        """
        arr2 = (c_int * len(vertices))()
        for i in range(len(vertices)):
            arr2[i] = vertices[i]
        arr4 = (c_int * len(edges))()
        for i in range(len(edges)):
            arr4[i] = edges[i]
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoCreateEdgeSubmolecule(self.id, len(arr2), arr2, len(arr4), arr4)))

    def getSubmolecule(self, vertices):
        """Molecule method returns submolecule by the given atom list

        Args:
            vertices (list): list of atom indexes

        Returns:
            IndigoObject: submolecule object
        """
        arr2 = (c_int * len(vertices))()
        for i in range(len(vertices)):
            arr2[i] = vertices[i]
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoGetSubmolecule(self.id, len(arr2), arr2)), self)

    def removeAtoms(self, vertices):
        """Molecule method removes atoms

        Args:
            vertices (list): atom indexes list

        Returns:
            int: 1 if there are no errors
        """
        arr2 = (c_int * len(vertices))()
        for i in range(len(vertices)):
            arr2[i] = vertices[i]
        return IndigoLib.checkResult(self._lib().indigoRemoveAtoms(self.id, len(arr2), arr2))

    def removeBonds(self, bonds):
        """Molecule method removes bonds

        Args:
            bonds (list): bond indexes list

        Returns:
            int: 1 if there are no errors
        """
        arr2 = (c_int * len(bonds))()
        for i in range(len(bonds)):
            arr2[i] = bonds[i]
        return IndigoLib.checkResult(self._lib().indigoRemoveBonds(self.id, len(arr2), arr2))

    def aromatize(self):
        """Molecule or reaction method aromatizes the structure

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoAromatize(self.id))

    def dearomatize(self):
        """Molecule or reaction method de-aromatizes the structure

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoDearomatize(self.id))

    def foldHydrogens(self):
        """Molecule or reaction method folds hydrogens

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoFoldHydrogens(self.id))

    def unfoldHydrogens(self):
        """Molecule or reaction method unfolds hydrogens

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoUnfoldHydrogens(self.id))

    def layout(self):
        """Molecule or reaction method calculates layout for the structure

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoLayout(self.id))

    def smiles(self):
        """Molecule or reaction method calculates SMILES for the structure

        Returns:
            str: smiles string
        """
        return IndigoLib.checkResultString(self._lib().indigoSmiles(self.id))

    def smarts(self):
        """Molecule or reaction method calculates SMARTS for the structure

        Returns:
            str: smarts string
        """
        return IndigoLib.checkResultString(self._lib().indigoSmarts(self.id))

    def name(self):
        """IndigoObject method returns name

        Returns:
            str: name string
        """
        return IndigoLib.checkResultString(self._lib().indigoName(self.id))

    def setName(self, name):
        """IndigoObject method sets name

        Args:
            name (str): name string

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetName(self.id, name.encode()))

    def serialize(self) -> bytes:
        """IndigoObject method serializes the object into byte array

        Returns:
            list: array of bytes
        """
        c_size = c_int()
        c_buf = POINTER(c_ubyte)()
        IndigoLib.checkResult(self._lib().indigoSerialize(self.id, pointer(c_buf), pointer(c_size)))
        return bytes((c_buf[i] for i in range(c_size.value)))

    def hasProperty(self, prop):
        """Object method returns True if the given property exists

        Args:
            prop (str): property name

        Returns:
            bool: flag True if property exists
        """
        return bool(IndigoLib.checkResult(self._lib().indigoHasProperty(self.id, prop)))

    def getProperty(self, prop):
        """Object method returns property by the given name

        Args:
            prop (str): property name

        Returns:
            str: property value
        """
        return IndigoLib.checkResultString(self._lib().indigoGetProperty(self.id, prop.encode()))

    def setProperty(self, prop, value):
        """Object method sets property

        Args:
            prop (str): property name
            value (str): property value

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSetProperty(self.id, prop.encode(), value.encode()))

    def removeProperty(self, prop):
        """Object method removes property

        Args:
            prop (str): property name

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoRemoveProperty(self.id, prop.encode()))

    def iterateProperties(self):
        """Object method returns properties iterator

        Returns:
            IndigoObject: properties iterator
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoIterateProperties(self.id)))

    def clearProperties(self):
        """Object method clears all properties

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoClearProperties(self.id))

    def checkBadValence(self):
        """Molecule, atom or reaction method validates bad valence

        Returns:
            str: string containing valence validation errors
        """
        return IndigoLib.checkResultString(self._lib().indigoCheckBadValence(self.id))

    def checkAmbiguousH(self):
        """Molecule or reaction method validates ambiguous hydrogens

        Returns:
            str: string containing hydrogens validation errors
        """
        return IndigoLib.checkResultString(self._lib().indigoCheckAmbiguousH(self.id))

    def fingerprint(self, type_):
        """Molecule or reaction method returns fingerprint representation

        Args:
            type_ (str): fingerprint type. One of the following: "sim", "sub",
                         "sub-res", "sub-tau", "full"

        Returns:
            IndigoObject: fingerprint object
        """
        new_obj = IndigoLib.checkResult(self._lib().indigoFingerprint(self.id, type_.encode()))
        if new_obj == 0:
            return None
        return IndigoObject(self.session, new_obj, self)

    def countBits(self):
        """Fingerprint method returns the count of 1 bits

        Returns:
            int: number of 1 bits
        """
        return IndigoLib.checkResult(self._lib().indigoCountBits(self.id))

    def rawData(self):
        """Object method returns string representation

        Returns:
            str: string for the object
        """
        return IndigoLib.checkResultString(self._lib().indigoRawData(self.id))

    def tell(self):
        """Object method returns the size of the content, e.g. SDF number of
           structures

        Returns:
            int: size of the content
        """
        return IndigoLib.checkResult(self._lib().indigoTell(self.id))

    def sdfAppend(self, item):
        """SDF method adds a new structure

        Args:
            item (IndigoObject): structure to be added

        Returns:
            int: 1 if there are errors
        """
        return IndigoLib.checkResult(self._lib().indigoSdfAppend(self.id, item.id))

    def smilesAppend(self, item):
        """Smiles builder methods adds a new structure

        Args:
            item (IndigoObject): structure to be added

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoSmilesAppend(self.id, item.id))

    def rdfHeader(self):
        """RDF builder adds header

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoRdfHeader(self.id))

    def rdfAppend(self, item):
        """RDF builder method adds a new structure

        Args:
            item (IndigoObject): new structure to be added

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoRdfAppend(self.id, item.id))

    def cmlHeader(self):
        """CML builder adds header

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoCmlHeader(self.id))

    def cmlAppend(self, item):
        """CML builder adds a new structure

        Args:
            item (IndigoObject): new structure to be added

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoCmlAppend(self.id, item.id))

    def cmlFooter(self):
        """CML builder adds footer information

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoCmlFooter(self.id))

    def append(self, object_):
        """Saver method adds a new object

        Args:
            object_ (IndigoObject): object to be added

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoAppend(self.id, object_.id))

    def arrayAdd(self, object_):
        """Array method adds a new object

        Args:
            object_ (IndigoObject): object to be added

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoArrayAdd(self.id, object_.id))

    def at(self, index):
        """Loader method returns element by index

        Args:
            index (int): element index

        Returns:
            IndigoObject: element object
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoAt(self.id, index)))

    def count(self):
        """Loader method returns the number of elements

        Returns:
            int: number of elements
        """
        return IndigoLib.checkResult(self._lib().indigoCount(self.id))

    def clear(self):
        """Array, molecule or reaction method clears the object

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoClear(self.id))

    def iterateArray(self):
        """Array method returns iterator for elements

        Returns:
            IndigoObject: elements iterator
        """
        new_obj = IndigoLib.checkResult(self._lib().indigoIterateArray(self.id))
        if new_obj == 0:
            return None
        else:
            return IndigoObject(self.session, new_obj, self)

    def ignoreAtom(self, atom_object):
        """Matcher method adds atom to ignore list

        Args:
            atom_object (IndigoObject): atom to ignore

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoIgnoreAtom(self.id, atom_object.id))

    def unignoreAtom(self, atom_object):
        """Matcher method removes atom from ignore list

        Args:
            atom_object (IndigoObject): atom to remove from ignore

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoUnignoreAtom(self.id, atom_object.id))

    def unignoreAllAtoms(self):
        """Matcher method clears ignore list

        Returns:
            int: 1 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoUnignoreAllAtoms(self.id))

    def match(self, query):
        """Matcher method executes matching

        Args:
            query (IndigoObject): query structure

        Returns:
            IndigoObject: mapping object
        """
        new_obj = IndigoLib.checkResult(self._lib().indigoMatch(self.id, query.id))
        if new_obj == 0:
            return None
        else:
            return IndigoObject(self.session, new_obj, self)

    def countMatches(self, query):
        """Matcher method returns the number of matches

        Args:
            query (IndigoObject): query structure

        Returns:
            int: number of matches
        """
        return IndigoLib.checkResult(self._lib().indigoCountMatches(self.id, query.id))

    def countMatchesWithLimit(self, query, embeddings_limit):
        """Matcher method returns the number of matches with max limit

        Args:
            query (IndigoObject): query structure
            embeddings_limit (int): max number of matches to search

        Returns:
            int: number of matches
        """
        return IndigoLib.checkResult(self._lib().indigoCountMatchesWithLimit(self.id, query.id, embeddings_limit))

    def iterateMatches(self, query):
        """Matcher method returns matches iterator

        Args:
            query (IndigoObject): query structure

        Returns:
            IndigoObject: matches iterator
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoIterateMatches(self.id, query.id)))

    def highlightedTarget(self):
        """Mapping method returns highlighted target

        Returns:
            IndigoObject: highlighted molecule structure
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoHighlightedTarget(self.id)))

    def mapAtom(self, atom):
        """Mapping method returns mapped atom for the given atom

        Args:
            atom (IndigoObject): query atom to map

        Returns:
            IndigoObject: mapped atom
        """
        new_obj = IndigoLib.checkResult(self._lib().indigoMapAtom(self.id, atom.id))
        if new_obj == 0:
            return None
        else:
            return IndigoObject(self.session, new_obj, self)

    def mapBond(self, bond):
        """Mapping method returns mapped bond for the given bond

        Args:
            bond (IndigoObject): query bond to map

        Returns:
            IndigoObject: mapped bond
        """
        new_obj = IndigoLib.checkResult(self._lib().indigoMapBond(self.id, bond.id))
        if new_obj == 0:
            return None
        else:
            return IndigoObject(self.session, new_obj, self)

    def mapMolecule(self, molecule):
        """Reaction mapping method returns mapped molecule for the given query
           molecule

        Args:
            molecule (IndigoObject): query molecule to map

        Returns:
            IndigoObject: mapped molecule
        """
        new_obj = IndigoLib.checkResult(self._lib().indigoMapMolecule(self.id, molecule.id))
        if new_obj == 0:
            return None
        else:
            return IndigoObject(self.session, new_obj, self)

    def allScaffolds(self):
        """Scaffold method returns all scaffolds

        Returns:
            IndigoObject: array of all scaffolds
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoAllScaffolds(self.id)))

    def decomposedMoleculeScaffold(self):
        """Deconvolution method starts molecule decomposition

        Returns:
            IndigoObject: decomposed molecule
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoDecomposedMoleculeScaffold(self.id)))

    def iterateDecomposedMolecules(self):
        """Deconvolution method returns decomposed molecules iterator

        Returns:
            IndigoObject: decomposed molecules iterator
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoIterateDecomposedMolecules(self.id)))

    def decomposedMoleculeHighlighted(self):
        """Deconvolution method returns decomposed highlighted molecule

        Returns:
            IndigoObject: decomposed highlighted molecule
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoDecomposedMoleculeHighlighted(self.id)))

    def decomposedMoleculeWithRGroups(self):
        """Deconvolution method returns decomposed molecule with R-groups

        Returns:
            IndigoObject: decomposed molecule with R-groups
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoDecomposedMoleculeWithRGroups(self.id)))

    def decomposeMolecule(self, mol):
        """Deconvolution method makes decomposition for the given molecule

        Args:
            mol (IndigoObject): molecule to decompose

        Returns:
            IndigoObject: deconvolution element object
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoDecomposeMolecule(self.id, mol.id)))

    def iterateDecompositions(self):
        """Deconvolution element method returns decompositions iterator

        Returns:
            IndigoObject: decompositions iterator
        """
        return IndigoObject(self.session, IndigoLib.checkResult(self._lib().indigoIterateDecompositions(self.id)))

    def addDecomposition(self, q_match):
        """Deconvolution method adds query match

        Args:
            q_match (IndigoObject): decomposition match object

        Returns:
            int: 0 if there are no errors
        """
        return IndigoLib.checkResult(self._lib().indigoAddDecomposition(self.id, q_match.id))

    def toString(self):
        """Object method returns string representation

        Returns:
            str: string representation for the object
        """
        return IndigoLib.checkResultString(self._lib().indigoToString(self.id))

    def toBuffer(self) -> bytes:
        """Object method returns binary representation

        Returns:
            list: array of bytes
        """
        c_size = c_int()
        c_buf = POINTER(c_ubyte)()
        IndigoLib.checkResult(self._lib().indigoToBuffer(self.id, byref(c_buf), byref(c_size)))
        return bytes((c_buf[i] for i in range(c_size.value)))

    def stereocenterPyramid(self):
        """Atom method returns stereopyramid information

        Returns:
            str: stereopyramid information string
        """
        ptr = IndigoLib.checkResultPtr(self._lib().indigoStereocenterPyramid(self.id))
        res = [0] * 4
        for i in range(4):
            res[i] = ptr[i]
        return res

    def expandAbbreviations(self):
        """Molecule method expands abbreviations

        Returns:
            int: count of expanded abbreviations
        """
        return IndigoLib.checkResult(self._lib().indigoExpandAbbreviations(self.id))

    def dbgInternalType(self):
        """Object method returns type

        Returns:
            str: object type string
        """
        return IndigoLib.checkResultString(self._lib().indigoDbgInternalType(self.id))