from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from pylingual.decompiler import Decompiler


def test_purge_lets_timeouts_through():
    """A timeout while purging (an alarm, as eval harnesses set) is raised, not read as nothing left to purge."""
    d = Decompiler.__new__(Decompiler)
    d.equivalence_results = [SyntaxError("invalid syntax")]
    d.ordered_bytecodes = [SimpleNamespace(name="bad", codeobj=0)]
    d.source_context = SimpleNamespace(purged_cfts=["purged"], purge=Mock())
    d.find_comp_error_cause = Mock(return_value=0)
    d.check_reconstruction = Mock(side_effect=TimeoutError("deadline"))
    with pytest.raises(TimeoutError):
        d.purge_comp_errors()
    assert d.source_context.purged_cfts == []
