""" 
Module to set up run time parameters for Clawpack -- classic code.

The values set in the function setrun are then written out to data files
that will be read in by the Fortran code.
    
"""
import os
import numpy as np

def setrun(claw_pkg='amrclaw'):
    """ 
    Define the parameters used for running Clawpack.

    INPUT:
        claw_pkg expected to be "amrclaw" for this setrun.

    OUTPUT:
        rundata - object of class ClawRunData 
    
    """
    from clawpack.clawutil import data
    assert claw_pkg.lower() == 'amrclaw', "Expected claw_pkg = 'amrclaw'"
    num_dim = 1
    rundata = data.ClawRunData(claw_pkg, num_dim)
    clawdata = rundata.clawdata
    clawdata.num_dim = num_dim
    clawdata.lower[0] = 0.0
    clawdata.upper[0] = 1.0
    clawdata.num_cells[0] = 50
    clawdata.num_eqn = 3
    clawdata.num_aux = 0
    clawdata.capa_index = 0
    clawdata.t0 = 0.0
    clawdata.restart = False
    clawdata.restart_file = 'fort.q0006'
    clawdata.output_style = 1
    if clawdata.output_style == 1:
        clawdata.num_output_times = 10
        clawdata.tfinal = 0.038
        clawdata.output_t0 = True
    elif clawdata.output_style == 2:
        clawdata.output_times = [0.0, 0.1]
    elif clawdata.output_style == 3:
        clawdata.output_step_interval = 1
        clawdata.total_steps = 50
        clawdata.output_t0 = True
    clawdata.output_format = 'ascii'
    clawdata.output_q_components = 'all'
    clawdata.output_aux_components = 'none'
    clawdata.output_aux_onlyonce = True
    clawdata.verbosity = 0
    clawdata.dt_variable = True
    clawdata.dt_initial = 1e-06
    clawdata.dt_max = 1e+99
    clawdata.cfl_desired = 0.9
    clawdata.cfl_max = 1.0
    clawdata.steps_max = 5000
    clawdata.order = 2
    clawdata.num_waves = 3
    clawdata.limiter = clawdata.num_waves * ['minmod']
    clawdata.use_fwaves = False
    clawdata.source_split = 0
    clawdata.num_ghost = 2
    clawdata.bc_lower[0] = 'wall'
    clawdata.bc_upper[0] = 'wall'
    rundata.gaugedata.gauges = []
    rundata.gaugedata.gauges.append([4, 0.4, 0, 1000000000.0])
    rundata.gaugedata.gauges.append([7, 0.7, 0, 1000000000.0])
    rundata.gaugedata.gauges.append([8, 0.8, 0, 1000000000.0])
    clawdata.checkpt_style = 0
    if clawdata.checkpt_style == 0:
        pass
    elif clawdata.checkpt_style == 1:
        pass
    elif clawdata.checkpt_style == 2:
        clawdata.checkpt_times = [0.1, 0.15]
    elif clawdata.checkpt_style == 3:
        clawdata.checkpt_interval = 5
    amrdata = rundata.amrdata
    amrdata.max1d = 500
    amrdata.amr_levels_max = 4
    amrdata.refinement_ratios_x = [2, 6, 10]
    amrdata.refinement_ratios_t = [2, 6, 10]
    amrdata.aux_type = []
    amrdata.flag_richardson = False
    amrdata.flag_richardson_tol = 1e-06
    amrdata.flag2refine = True
    amrdata.flag2refine_tol = 0.1
    amrdata.regrid_interval = 2
    amrdata.regrid_buffer_width = 3
    amrdata.clustering_cutoff = 0.7
    amrdata.verbosity_regrid = 0
    regions = rundata.regiondata.regions
    regions.append([1, 4, 0, 1000000000.0, 0, 1.0])
    regions.append([4, 4, 0, 0.002, 0.05, 0.15])
    regions.append([4, 4, 0, 0.002, 0.85, 0.95])
    amrdata.dprint = False
    amrdata.eprint = False
    amrdata.edebug = False
    amrdata.gprint = False
    amrdata.nprint = False
    amrdata.pprint = False
    amrdata.rprint = False
    amrdata.sprint = False
    amrdata.tprint = False
    amrdata.uprint = False
    return rundata
if __name__ == '__main__':
    import sys
    rundata = setrun(*sys.argv[1:])
    rundata.write()