"""
Tipo `Colore` e funzioni per produrre colori.
"""
from __future__ import annotations
from pytamaro.color import Color, rgb_color, rgba_color
Colore = Color
'\nRappresenta un colore nello spazio colore RGBA (usando interi tra 0 e 255).\n'

def colore_rgb(rosso: int, verde: int, blu: int) -> Colore:
    """
    Ritorna un colore completamente opaco con le componenti indicate per il
    rosso, verde e blu.

    :param rosso: componente rosso (0 -- 255)
    :param verde: componente verde (0 -- 255)
    :param blu: componente blu (0 -- 255)
    :returns: un colore con le componenti RGB indicate
    """
    return rgb_color(rosso, verde, blu)

def colore_rgba(rosso: int, verde: int, blu: int, alpha: int) -> Colore:
    """
    Ritorna un colore con le componenti indicate per rosso, verde e blu e un
    certo grado di trasparenza determinato da `alpha`.

    :param rosso: componente rosso (0 -- 255)
    :param verde: componente verde (0 -- 255)
    :param blu: componente blu (0 -- 255)
    :param alpha: componente alpha (trasparenza), dove 0 è completamente
                  trasparente e 255 completamente opaco
    :returns: un colore con le componenti RGBA indicate
    """
    return rgba_color(rosso, verde, blu, alpha)