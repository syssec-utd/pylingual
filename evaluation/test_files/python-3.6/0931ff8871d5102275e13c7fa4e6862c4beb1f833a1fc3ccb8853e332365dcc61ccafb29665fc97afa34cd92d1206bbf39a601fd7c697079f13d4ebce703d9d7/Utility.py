"""
Utility.py

Package for IBM Molecule Generation Experience

MIT License

Copyright (c) 2022 International Business Machines Corporation

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit.Chem.Draw import rdMolDraw2D
from IPython.display import SVG
from PIL import Image
from matplotlib.colors import ColorConverter
from io import BytesIO
import os
import re
from collections import Counter
import copy
import logging
logger = logging.getLogger(__name__)

def fetch_QM9(directory, num_data=1000, offset=0, file_type='mol', smiles_pos=1, selection=None, index_list=None):
    """extract molecules and properties from QM9 data directory.

    Args:
        directory (str): path of the QM9 data directory
        num_data (int, optional): the number of data to fetch from the QM9 data. Defaults to 1000.
        offset (int, optional): the offset of data index in selecting num_data. Defaults to 0.
        file_type(str, optional): file type of molecule data (mol|xyz). Defaults to 'xyz'
        smiles_pos (int, optional): smiles position in xyz file (1 or 2). Defaults to 1
        selection (str, optional): how to select data ('head' or 'tail'). Defaults to None.
        index_list(str, optional): a list of specific mol file indices (dsgdb9nsd_[index].mol) to get. Defaults to None
    Returns:
        list, PropertySet: a list of SimpleMolecule objects, a set of properties

    format of properties in QM9 mol file

    == ========== =========== ======================================================
    id Property   Unit        Description
    == ========== =========== ======================================================
     1 tag        N/A         "gdb9"; string constant to ease extraction via grep
     2 index      N/A         Consecutive, 1 - based integer identifier of molecule
     3 A          GHz         Rotational constant A
     4 B          GHz         Rotational constant B
     5 C          GHz         Rotational constant C
     6 mu         Debye       Dipole moment
     7 alpha      Bohr^3      Isotropic polarizability
     8 homo       Hartree     Energy of Highest occupied molecular orbital(HOMO)
     9 lumo       Hartree     Energy of Lowest occupied molecular orbital(LUMO)
    10 gap        Hartree     Gap, difference between LUMO and HOMO
    11 r2         Bohr^2      Electronic spatial extent
    12 zpve       Hartree     Zero point vibrational energy
    13 U0         Hartree     Internal energy at 0 K
    14 U          Hartree     Internal energy at 298.15 K
    15 H          Hartree     Enthalpy at 298.15 K
    16 G          Hartree     Free energy at 298.15 K
    17 Cv         cal/(mol K) Heat capacity at 298.15 K
    == ========== =========== ======================================================
    """
    from .Molecule import Property, PropertySet
    if not os.path.exists(directory):
        logger.error('directory does not exist')
        return
    if not os.path.isdir(directory):
        logger.error('%s is not a directory', directory)
        return
    prop_map = {Property('mu'): 0, Property('alpha'): 1, Property('homo'): 2, Property('lumo'): 3, Property('gap'): 4, Property('r2'): 5, Property('zpve'): 6, Property('U0'): 7, Property('U'): 8, Property('H'): 9, Property('G'): 10, Property('Cv'): 11}
    files = os.listdir(directory)
    count = 0
    for f in files:
        index = re.search('.' + file_type, f)
        if index:
            count += 1
    smiles_set = dict()
    molecules = []
    properties = PropertySet([p for (p, pos) in sorted(prop_map.items(), key=lambda x: x[1])])
    if index_list is None:
        step = int(count / min(count, num_data))
        index_offset = min(step - 1, offset)
        select_index = range(step - index_offset, step * num_data + 1, step)
        if selection == 'head':
            select_index = range(1, min(num_data, count) + 1)
        elif selection == 'tail':
            select_index = range(max(count - num_data, 1), count + 1)
        for i in select_index:
            id = 'QM9[{0}]'.format(i)
            filename = 'dsgdb9nsd_{0:06d}.'.format(i) + file_type
            filepath = os.path.join(directory, filename)
            molecule = None
            if file_type == 'mol':
                molecule = read_mol_file(filepath, id, smiles_set, prop_map)
            elif file_type == 'xyz':
                molecule = read_xyz_file(filepath, id, smiles_pos, smiles_set, prop_map)
            if molecule is not None:
                molecules.append(molecule)
    else:
        for (i, index) in enumerate(index_list):
            id = 'QM9[{0}]'.format(index)
            filename = 'dsgdb9nsd_{0:06d}.'.format(index) + file_type
            filepath = os.path.join(directory, filename)
            molecule = None
            if file_type == 'mol':
                molecule = read_mol_file(filepath, id, smiles_set, prop_map)
            elif file_type == 'xyz':
                molecule = read_xyz_file(filepath, id, smiles_pos, smiles_set, prop_map)
            if molecule is not None:
                molecules.append(molecule)
    logger.info('extract {0} molecule data'.format(len(molecules)))
    return (molecules, properties)

def read_mol_file(filepath, id, smiles_set, prop_map):
    from .Molecule import SimpleMolecule
    if os.path.exists(filepath):
        mol = Chem.MolFromMolFile(filepath)
        if mol is not None:
            molecule = SimpleMolecule(id, mol=mol)
            smiles = Chem.MolToSmiles(mol)
            if smiles in smiles_set:
                logger.warning('duplicated molecule? %s=%s %s', id, smiles_set[smiles], smiles)
            else:
                smiles_set[smiles] = id
            with open(filepath, 'r') as file:
                moldata = file.readline().strip()
                propdata = list(map(float, moldata.split('\t')[4:]))
                for (prop, pos) in prop_map.items():
                    molecule.set_property(prop, propdata[pos])
                return molecule
    logger.error('failed to read mol file:%s', filepath)
    return None

def read_xyz_file(filepath, id, smiles_pos, smiles_set, prop_map):
    from .Molecule import SimpleMolecule
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            num_atom = int(file.readline().strip())
            moldata = file.readline().strip()
            propdata = list(map(float, moldata.split('\t')[4:]))
            for atoms in range(0, num_atom + 1):
                file.readline()
            smiles_line = file.readline()
            m = re.match('(\\S+)\\s+(\\S+)', smiles_line)
            if m is not None:
                smiles = m.group(smiles_pos)
                mol = Chem.MolFromSmiles(smiles)
                if mol is not None:
                    if smiles in smiles_set:
                        logger.warning('duplicated molecule? %s=%s %s', id, smiles_set[smiles], smiles)
                    else:
                        smiles_set[smiles] = id
                    molecule = SimpleMolecule(id, mol=mol)
                    for (prop, pos) in prop_map.items():
                        molecule.set_property(prop, propdata[pos])
                    return molecule
                else:
                    logger.error('rdkit failed to read smiles:%s', smiles)
    logger.error('failed to read xyz file:%s', filepath)
    return None

def make_ring_replacement(molecules):
    """Get the number of atoms in rings of molecules for ring replacement

    Returns:
        dict: mapping of atom and the number
    """
    from .ChemGenerator.ChemGraph import ChemVertex
    atom_count = Counter()
    for molecule in molecules:
        ring_vertices = molecule.get_graph().get_connected_ring_vertices()
        for ring_vertex in ring_vertices:
            ring_atom_count = Counter()
            for vertex in ring_vertex:
                if vertex.ring_atom():
                    ring_atom_count[vertex.atom] += 1
            for (atom, count) in ring_atom_count.items():
                if atom != 'C' and atom != ChemVertex.wild_card_atom:
                    atom_count[atom] = max(atom_count[atom], count)
    return atom_count

def draw_molecule_with_atom_index(mol, atom_labels={}, highlight_atoms=[], highlight_bonds=[], image_size=(400, 400), legend='', use_svg=False):
    """Draw molecule with atom indices and highlights

        Args:
            mol (Mol): rdkit mol object
            atom_labels (dict): a map of atom index and atom label
            highlight_atoms (list, optional): a list of highlight atom indices. Defaults to []
            highlight_bonds (list, optional): a list of highlight bond indices. Defaults to []
            image_size (tuple, optional): a tuple of image size (width, height). Defaults to (500,500)
            legend (str, optional): legend of drawing. Defaults to ''
            use_svg (bool, optional): flag to use SVG for drawing. Defaults to False

        Returns:
            PIL.Image: an image
    """
    atom_color = {}
    radius = {}
    for atom_index in highlight_atoms:
        atom_color[atom_index] = ColorConverter().to_rgb('lightgreen')
        radius[atom_index] = 0.25
    bond_color = {}
    for bond_index in highlight_bonds:
        bond_color[bond_index] = ColorConverter().to_rgb('lightpink')
    tm = rdMolDraw2D.PrepareMolForDrawing(mol, kekulize=False, wedgeBonds=False)
    if use_svg:
        view = rdMolDraw2D.MolDraw2DSVG(image_size[0], image_size[1], image_size[0], image_size[1])
    else:
        view = rdMolDraw2D.MolDraw2DCairo(image_size[0], image_size[1], image_size[0], image_size[1])
    view.SetFontSize(1.1 * view.FontSize())
    option = view.drawOptions()
    option.circleAtoms = True
    option.continuousHighlight = True
    option.dummiesAreAttachments = False
    option.fillHighlights = True
    option.includeAtomTags = False
    for atom in mol.GetAtoms():
        if atom.GetIdx() in atom_labels:
            option.atomLabels[atom.GetIdx()] = '{} [{}]'.format(atom.GetIdx(), atom_labels[atom.GetIdx()])
        elif atom.GetSymbol() == 'C':
            option.atomLabels[atom.GetIdx()] = '{}'.format(atom.GetIdx())
        elif atom.GetFormalCharge() == 0:
            option.atomLabels[atom.GetIdx()] = '{}({})'.format(atom.GetIdx(), atom.GetSymbol())
        elif atom.GetFormalCharge() == 1:
            option.atomLabels[atom.GetIdx()] = '{}({}+)'.format(atom.GetIdx(), atom.GetSymbol())
        elif atom.GetFormalCharge() == -1:
            option.atomLabels[atom.GetIdx()] = '{}({}-)'.format(atom.GetIdx(), atom.GetSymbol())
        else:
            option.atomLabels[atom.GetIdx()] = '{}({}{:+})'.format(atom.GetIdx(), atom.GetSymbol(), atom.GetFormalCharge())
    view.DrawMolecule(tm, highlightAtoms=highlight_atoms, highlightAtomColors=atom_color, highlightAtomRadii=radius, highlightBonds=highlight_bonds, highlightBondColors=bond_color, legend=legend)
    view.FinishDrawing()
    drawing = view.GetDrawingText()
    if use_svg:
        img = SVG(drawing.replace('svg:', ''))
    else:
        sio = BytesIO(drawing)
        img = Image.open(sio)
    return img

def print_rdkit_mol_info(mol):
    """Print RDKit Mol information

    Args:
        mol: RDKit mol object
    """
    print('mol:{0}'.format(Chem.MolToSmiles(mol)))
    print('smilesAtomOutputOrder:{0}'.format(mol.GetProp('_smilesAtomOutputOrder')))
    print('** atom properties **')
    for atom in mol.GetAtoms():
        print('index:{0}'.format(atom.GetIdx()))
        print('symbol:{0}'.format(atom.GetSymbol()))
        print('atomic num:{0}'.format(atom.GetAtomicNum()))
        print('chiral tag:{0}'.format(atom.GetChiralTag()))
        print('degree:{0}'.format(atom.GetDegree()))
        print('total degree:{0}'.format(atom.GetTotalDegree()))
        print('explicit valence:{0}'.format(atom.GetExplicitValence()))
        print('implicit valence:{0}'.format(atom.GetImplicitValence()))
        print('total valence:{0}'.format(atom.GetTotalValence()))
        print('formal charge:{0}'.format(atom.GetFormalCharge()))
        print('hybridization:{0}'.format(atom.GetHybridization()))
        print('aromatic:{0}'.format(atom.GetIsAromatic()))
        print('isotope:{0}'.format(atom.GetIsotope()))
        print('mass:{0}'.format(atom.GetMass()))
        print('no implicit:{0}'.format(atom.GetNoImplicit()))
        print('num explicit H:{0}'.format(atom.GetNumExplicitHs()))
        print('num implicit H:{0}'.format(atom.GetNumImplicitHs()))
        print('total num H:{0}'.format(atom.GetTotalNumHs()))
        print('num radical electrons:{0}'.format(atom.GetNumRadicalElectrons()))
        print('atom map num:{0}'.format(atom.GetAtomMapNum()))
        print('props:{0}'.format(atom.GetPropsAsDict()))
        print('')
    print('** bond properties **')
    for bond in mol.GetBonds():
        print('index:{0}'.format(bond.GetIdx()))
        print('begin atom:{0}'.format(bond.GetBeginAtomIdx()))
        print('end atom:{0}'.format(bond.GetEndAtomIdx()))
        print('bond direction:{0}'.format(bond.GetBondDir()))
        print('bond type:{0}'.format(bond.GetBondType()))
        print('bond type double:{0}'.format(bond.GetBondTypeAsDouble()))
        print('aromatic?:{0}'.format(bond.GetIsAromatic()))
        print('conjugated?:{0}'.format(bond.GetIsConjugated()))
        print('stereo:{0}'.format(bond.GetStereo()))
        print('in ring:{0}'.format(bond.IsInRing()))
        print('props:{0}'.format(bond.GetPropsAsDict()))
        print('')
    print(Chem.MolToMolBlock(mol))

def draw_molecules(molecules, max_draw=None, mols_per_row=None, sub_image_size=None, legends=None, returnPNG=False, use_svg=False):
    """Draw molecules.

    Args:
        molecules (list): a list of Molecule objects
        max_draw (int, optional): a maximum number of features to draw. Defaults to None.
        mols_per_row (int, optional): number of molecules to draw in a line. Defaults to None.
        sub_image_size (tuple, optional): image size of each molecule. Defaults to None.
        legends (list): title of each sub-structure
        returnPNG (bool, optional): return PNG format. Default to False.
        use_svg (bool, optional): use SVG drawing. Default to False.

    Returns:
        PIL: an image of molecules
    """
    mols = [m.get_mol() for m in molecules]
    if legends is None:
        legends = ['{0}'.format(m.get_id()) for m in molecules]
    return draw_rdkit_mols(mols, max_draw=max_draw, mols_per_row=mols_per_row, sub_image_size=sub_image_size, legends=legends, returnPNG=returnPNG, use_svg=use_svg)

def draw_rdkit_mols(mols, max_draw=None, mols_per_row=None, sub_image_size=None, legends=None, returnPNG=False, use_svg=False):
    """Draw molecules of RDKit Mol object(a wrapper of rdkit Chem.Draw.MolsToGridImage).

    Args:
        mols (list): a list of RDKit Mol objects
        max_draw (int, optional): a maximum number of features to draw. Defaults to None.
        mols_per_row (int, optional): number of molecules to draw in a line. Defaults to None.
        sub_image_size (tuple, optional): image size of each molecule. Defaults to None.
        legends (list, optional): title of each molecule. Defaults to None.
        returnPNG (bool, optional): return PNG format. Default to False.
        use_svg (bool, optional): use SVG drawing. Default to False.

    Returns:
        PIL: an image of molecules
    """
    if max_draw is None:
        max_draw = len(mols)
    if mols_per_row is None:
        mols_per_row = 10
        if sub_image_size is None:
            sub_image_size = (100, 100)
    elif sub_image_size is None:
        sub_image_size = (int(100 * 10 / mols_per_row), int(100 * 10 / mols_per_row))
    mols_show = []
    for i in range(min(len(mols), max_draw)):
        if mols[i] is None:
            mol = Chem.MolFromSmiles('*')
        elif mols[i].GetNumAtoms() == 0:
            mol = Chem.MolFromSmiles('*')
        else:
            mol = copy.deepcopy(mols[i])
        try:
            for atom in mol.GetAtoms():
                if not atom.IsInRing() and atom.GetIsAromatic():
                    atom.SetIsAromatic(False)
            Chem.SanitizeMol(mol)
            mols_show.append(mol)
        except ValueError as verr:
            if legends is not None:
                lgd = legends[i]
            else:
                lgd = ''
            logger.error('cannot draw mol[%d]:%s %s by %s', i, lgd, Chem.MolToSmiles(mol), verr)
            mols_show.append(Chem.MolFromSmiles('*'))
        except AttributeError as verr:
            if legends is not None:
                lgd = legends[i]
            else:
                lgd = ''
            logger.error('cannot draw mol[%d]:%s by %s', i, lgd, verr)
            mols_show.append(Chem.MolFromSmiles('*'))
    if len(mols_show) > 0:
        try:
            image = Chem.Draw.MolsToGridImage(mols_show[0:max_draw], maxMols=max_draw, molsPerRow=mols_per_row, subImgSize=sub_image_size, legends=legends, returnPNG=returnPNG, useSVG=use_svg)
        except OSError as verr:
            logger.error('failed to make an image: %s', verr)
            image = Chem.Draw.MolsToGridImage([Chem.MolFromSmiles('')], useSVG=use_svg)
    else:
        logger.error('no valid rdkit mol object to draw')
        image = None
    return image

def draw_all_molecule(molecules, filename, mols_per_row, mols_per_file, legends=None):
    """Draw all the molecules in a separated files

    Args:
        molecules (list): a list of molecules
        filename (str): file name to save images
        mols_per_row (int): the number of moles per row
        mols_per_file (int): the number of moles per file
        legends (list, optional): title of each molecule. Defaults to None.
    """
    for index in range(0, len(molecules), mols_per_file):
        mols = molecules[index:index + mols_per_file]
        if legends is None:
            legends = ['{0}'.format(mols[idx].get_id()) for idx in range(len(mols))]
        img = draw_molecules(mols, mols_per_row=mols_per_row, legends=legends, returnPNG=False)
        if img is not None:
            img.save('{0}{1}.png'.format(filename, int(index / mols_per_file) + 1))
        else:
            logger.error('failed to generate molecule image')

def draw_all_smiles(smiles, filename, mols_per_row, mols_per_file, legends=None):
    """Draw all the smiles in separated files

    Args:
        smiles (list): a list of smiles
        filename (str): file name to save images
        mols_per_row (int): the number of moles per row
        mols_per_file (int): the number of moles per file
        legends (list, optional): title of each molecule. Defaults to None.
    """
    for index in range(0, len(smiles), mols_per_file):
        sms = smiles[index:index + mols_per_file]
        rmols = [Chem.MolFromSmiles(sm) for sm in sms]
        if legends is None:
            legends = ['{0}'.format(sms[idx]) for idx in range(len(sms))]
        img = draw_rdkit_mols(rmols, mols_per_row=mols_per_row, legends=legends, returnPNG=False)
        if img is not None:
            img.save('{0}{1}.png'.format(filename, int(index / mols_per_file) + 1))
        else:
            logger.error('failed to generate molecule image')

def get_subclasses(cls):
    """Get a dictionary of available subclasses of given class.

    Args:
        cls (object): class object

    Returns:
        list: a list of subclasses
    """
    classes = [cls]
    all_leaf = False
    while not all_leaf:
        new_classes = []
        all_leaf = True
        for cls in classes:
            sub_classes = cls.__subclasses__()
            if len(sub_classes) == 0:
                new_classes.append(cls)
            else:
                new_classes.extend(sub_classes)
                all_leaf = False
        classes = new_classes
    return classes

def update_data_mask(current_mask, new_mask):
    """Update data mask (a list of True/False). None means all True list.

    Args:
        current_mask (list): a list of True/False, or None
        new_mask (list): a list of True/False, or None

    Returns:
        list: updated data mask by AND operation
    """
    if new_mask is None:
        return current_mask
    elif current_mask is None:
        return new_mask
    else:
        return [c and n for (c, n) in zip(current_mask, new_mask)]