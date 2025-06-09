import numpy as np
from PyMPDATA import ScalarField, VectorField, Solver, Stepper
from PyMPDATA.boundary_conditions import Constant

class Simulation:

    def __init__(self, settings, options, static=True, n_threads=None):
        bcs = tuple((Constant(0) for _ in settings.grid))
        advector = VectorField(data=tuple((comp.astype(options.dtype) for comp in settings.advector)), halo=options.n_halo, boundary_conditions=bcs)
        advectee = ScalarField(data=np.asarray(settings.advectee, dtype=options.dtype), halo=options.n_halo, boundary_conditions=bcs)
        args = {'grid': settings.grid} if static else {'n_dims': len(settings.grid)}
        if n_threads is not None:
            args['n_threads'] = n_threads
        stepper = Stepper(options=options, **args)
        self.solver = Solver(stepper=stepper, advectee=advectee, advector=advector)

    def run(self, nt):
        return self.solver.advance(nt)

    @property
    def advectee(self):
        return self.solver.advectee