import numpy as np
import os
from ase.units import J

def write_vampire(cls, path='TB2J_results/Vampire'):
    if not os.path.exists(path):
        os.makedirs(path)
    write_vampire_unitcell_file(cls, os.path.join(path, 'vampire.UCF'))
    write_vampire_mat_file(cls, os.path.join(path, 'vampire.mat'))
    write_vampire_inp_file(cls, os.path.join(path, 'input'))

def write_vampire_unitcell_file(cls, fname):
    with open(fname, 'w') as myfile:
        cell = cls.atoms.get_cell().array
        lattice_parameters = np.linalg.norm(cell, axis=-1)
        myfile.write('# Unit cell size (Angstrom):\n')
        np.savetxt(myfile, [lattice_parameters], fmt='%f')
        myfile.write('# Unit cell lattice vectors:\n')
        np.savetxt(myfile, cell / lattice_parameters, fmt='%f')
        myfile.write('# Atoms\n')
        nspins = sum([1 if i > -1 else 0 for i in cls.index_spin])
        myfile.write('%s %s\n' % (nspins, nspins))
        natom = len(cls.atoms)
        for i in range(natom):
            text = ''
            id_spin = cls.index_spin[i]
            if id_spin > -1:
                pos = cls.atoms.get_scaled_positions()[i]
                text = '{id_spin} {pos_x} {pos_y} {pos_z} {mat_id}\n'.format(id_spin=id_spin, pos_x=pos[0], pos_y=pos[1], pos_z=pos[2], mat_id=id_spin)
                myfile.write(text)
        myfile.write('# Interactions\n')
        nexch = len(cls.exchange_Jdict.items())
        myfile.write('{num_interactions} {type_exchange}\n'.format(num_interactions=nexch, type_exchange='tensorial'))
        counter = -1
        for key in cls.exchange_Jdict:
            (R, ispin, jspin) = key
            Jtensor = cls.get_J_tensor(ispin, jspin, R)
            counter += 1
            myfile.write(f'{counter} {ispin} {jspin} {R[0]} {R[1]} {R[2]} ')
            for i in range(3):
                for j in range(3):
                    myfile.write(f'{Jtensor[i, j] * 2.0 / J} ')
            myfile.write('\n')

def write_vampire_mat_file(cls, fname):
    mat_tmpl = '#---------------------------------------------------\n# Material {id} \n#---------------------------------------------------\nmaterial[{id}]:material-name={name}\nmaterial[{id}]:damping-constant={damping}\nmaterial[{id}]:atomic-spin-moment={ms} !muB\nmaterial[{id}]:uniaxial-anisotropy-constant={k1}\nmaterial[{id}]:material-element={name}\nmaterial[{id}]:initial-spin-direction = {spinat}\nmaterial[{id}]:uniaxial-anisotropy-direction = {k1dir}\n#---------------------------------------------------\n'
    with open(fname, 'w') as myfile:
        nspins = sum([1 if i > -1 else 0 for i in cls.index_spin])
        myfile.write('material:num-materials = %s\n' % nspins)
        nspins = sum([1 if i > -1 else 0 for i in cls.index_spin])
        natom = len(cls.atoms)
        for i in range(natom):
            text = ''
            id_spin = cls.index_spin[i]
            if id_spin > -1:
                name = cls.atoms.get_chemical_symbols()[i]
                damping = 1.0
                ms = np.sqrt(np.sum(np.array(cls.spinat[i]) ** 2))
                spin = np.array(cls.spinat[i]) / ms
                spin_text = ','.join(map(str, spin))
                if cls.k1 is not None:
                    k1 = cls.k1[id_spin - 1]
                    k1dir = ', '.join(map(str, cls.k1dir[id_spin - 1]))
                else:
                    k1 = 0.0
                    k1dir = '0.0 , 0.0, 1.0'
                text = mat_tmpl.format(id=id_spin + 1, damping=damping, name=name, ms=ms, k1=k1 / J, k1dir=k1dir, spinat=spin_text)
                myfile.write(text)
        myfile.write('# Interactions\n')

def write_vampire_inp_file(cls, fname):
    text = '#------------------------------------------ \n# Creation attributes: \n#------------------------------------------ \ncreate:full\ncreate:periodic-boundaries-x \ncreate:periodic-boundaries-y \ncreate:periodic-boundaries-z \n#------------------------------------------\nmaterial:file=vampire.mat\nmaterial:unit-cell-file = "vampire.UCF"\n#------------------------------------------ \n# System Dimensions: \n#------------------------------------------ \ndimensions:unit-cell-size-x = {a}\ndimensions:unit-cell-size-y = {b}\ndimensions:unit-cell-size-z = {c}\n\ndimensions:system-size-x = 15.0 !nm \ndimensions:system-size-y = 15.0 !nm \ndimensions:system-size-z = 15.0 !nm \n#------------------------------------------ \n# Simulation attributes: \n#------------------------------------------ \nsim:temperature=300 \nsim:minimum-temperature=0 \nsim:maximum-temperature=1000\nsim:temperature-increment=25\nsim:time-steps-increment=1 \nsim:equilibration-time-steps=2500 \nsim:loop-time-steps=3000 \n#------------------------------------------ \n# Program and integrator details \n#------------------------------------------ \nsim:program=curie-temperature\nsim:integrator=llg-heun\n#------------------------------------------\n# Data output \n#------------------------------------------ \n#output:real-time\noutput:temperature\noutput:material-magnetisation \n#output:magnetisation-length \n'
    with open(fname, 'w') as myfile:
        cellpar = cls.atoms.cell.cellpar()
        myfile.write(text.format(a=cellpar[0], b=cellpar[1], c=cellpar[2]))