from pyunitx._api import make_compound_dimension, make_compound_unit, si_unit
from pyunitx.current import Current, amperes
from pyunitx.time import Time, seconds
Charge = make_compound_dimension(name='Charge', exponents={Current: 1, Time: 1})
coulombs = make_compound_unit(name='coulombs', abbrev='C', exponents={amperes: 1, seconds: 1}, scale=1, doc='    A coulomb is formally defined as the amount of charge that travels past a\n    point in a 1-Ampere current over the course of one second. Current is the\n    defined fundamental quantity in the SI system, and is certainly easier to\n    measure directly, but charge cannot be decomposed.\n    ')
generated = si_unit(base_unit=coulombs)
globals().update(generated)
fundamental_charge = make_compound_unit(name='fundamental_charge', abbrev='e', exponents={amperes: 1, seconds: 1}, scale='1.602176634e-19', doc='    This is the charge of a single proton or electron.\n    ')
__all__ = ['Charge', 'coulombs', 'fundamental_charge'] + list(generated.keys())