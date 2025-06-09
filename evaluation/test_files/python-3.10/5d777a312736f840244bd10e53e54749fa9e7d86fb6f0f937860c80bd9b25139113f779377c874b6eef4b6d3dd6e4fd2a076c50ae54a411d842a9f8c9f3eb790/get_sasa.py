import biotite.structure.io.pdb as pdb
import biotite.structure as struc
import gzip

def get_sasa(pdb_file_path):
    """
    pdb_file_path: example  a.pdb or a.pdb.gz
    """
    if pdb_file_path[-3:] == '.gz':
        with gzip.open(pdb_file_path, 'rt') as f:
            model = pdb.PDBFile.read(f).get_structure(model=1)
    else:
        with open(pdb_file_path, 'r') as f:
            model = pdb.PDBFile.read(f).get_structure(model=1)
    atom_sasa = struc.sasa(model, vdw_radii='Single')
    res_sasa = struc.apply_residue_wise(model, atom_sasa, np.sum)
    return res_sasa