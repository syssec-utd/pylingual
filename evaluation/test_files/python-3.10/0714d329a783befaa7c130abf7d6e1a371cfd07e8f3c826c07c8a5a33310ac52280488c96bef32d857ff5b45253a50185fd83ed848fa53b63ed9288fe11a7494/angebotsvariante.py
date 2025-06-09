"""
Contains Angebotsvariante and corresponding marshmallow schema for de-/serialization
"""
from datetime import datetime
from typing import Optional
from pydantic import conlist
from bo4e.com.angebotsteil import Angebotsteil
from bo4e.com.betrag import Betrag
from bo4e.com.com import COM
from bo4e.com.menge import Menge
from bo4e.enum.angebotsstatus import Angebotsstatus

class Angebotsvariante(COM):
    """
    Führt die verschiedenen Ausprägungen der Angebotsberechnung auf

    .. raw:: html

        <object data="../_static/images/bo4e/com/Angebotsvariante.svg" type="image/svg+xml"></object>

    .. HINT::
        `Angebotsvariante JSON Schema <https://json-schema.app/view/%23?url=https://raw.githubusercontent.com/Hochfrequenz/BO4E-python/main/json_schemas/com/Angebotsvariante.json>`_

    """
    angebotsstatus: Angebotsstatus
    erstellungsdatum: datetime
    bindefrist: datetime
    teile: conlist(Angebotsteil, min_items=1)
    '\n    Angebotsteile werden im einfachsten Fall für eine Marktlokation oder Lieferstellenadresse erzeugt.\n    Hier werden die Mengen und Gesamtkosten aller Angebotspositionen zusammengefasst.\n    Eine Variante besteht mindestens aus einem Angebotsteil.\n    '
    gesamtmenge: Optional[Menge] = None
    gesamtkosten: Optional[Betrag] = None