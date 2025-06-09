from datetime import datetime, timezone
from decimal import Decimal
from typing import Any, Dict
import pytest
from pydantic import ValidationError
from bo4e.com.tagesvektor import Tagesvektor
from bo4e.com.zeitreihenwertkompakt import Zeitreihenwertkompakt
from tests.serialization_helper import assert_serialization_roundtrip
from tests.test_sigmoidparameter import example_sigmoidparameter
example_tagesvektor: Tagesvektor = Tagesvektor(tag=datetime(2021, 12, 15, 5, 0, tzinfo=timezone.utc), werte=[Zeitreihenwertkompakt(wert=Decimal(40)), Zeitreihenwertkompakt(wert=Decimal(50))])
example_tagesvektor_json = {'tag': datetime(2021, 12, 15, 5, 0, tzinfo=timezone.utc), 'werte': [{'wert': Decimal('40'), 'statuszusatz': None, 'status': None}, {'wert': Decimal('50'), 'statuszusatz': None, 'status': None}]}

class TestTagesvektor:

    @pytest.mark.parametrize('tagesvektor, expected_json_dict', [pytest.param(example_tagesvektor, example_tagesvektor_json)])
    def test_serialization_roundtrip(self, tagesvektor: Tagesvektor, expected_json_dict: Dict[str, Any]) -> None:
        """
        Test de-/serialisation of Preisstaffel.
        """
        assert_serialization_roundtrip(tagesvektor, expected_json_dict)

    def test_missing_required_attribute(self) -> None:
        with pytest.raises(ValidationError) as excinfo:
            _ = Tagesvektor()
        assert '2 validation errors' in str(excinfo.value)

    def test_list_not_long_enough_attribute(self) -> None:
        with pytest.raises(ValidationError) as excinfo:
            _ = Tagesvektor(tag=datetime(2021, 12, 15, 5, 0, tzinfo=timezone.utc), werte=[])
        assert '1 validation error' in str(excinfo.value)
        assert 'ensure this value has at least 1 item' in str(excinfo.value)