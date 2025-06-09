import os
import numpy as np
from QuICT.core import Circuit
from QuICT.tools.interface import OPENQASMInterface

def check_template():
    for qasm in filter(lambda x: x.startswith('template') and x.endswith('.qasm'), os.listdir('./')):
        circ: Circuit = OPENQASMInterface.load_file(qasm).circuit
        if circ.width() > 12:
            print(f'WARNING: {qasm} too large, skipped.')
        assert np.allclose(circ.matrix(), np.identity(1 << circ.width())), f'ERROR: {qasm} is not identity!'
    print('INFO: check finished.')
if __name__ == '__main__':
    check_template()