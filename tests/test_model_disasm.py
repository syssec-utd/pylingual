import pytest

from pylingual.masking.global_masker import Masker
from pylingual.masking.model_disasm import restore_masked_source_text


@pytest.mark.parametrize("mask", ["<mask_0>", "'<mask_0>'", '"<mask_0>"'])
def test_container_masks_restore_without_wrapper_quotes(mask):
    masker = Masker()
    masker.global_tab[{"size": (32, 32), "crop": True}] = "<mask_0>"

    assert restore_masked_source_text([f"value = {mask}"], masker) == ["value = {'size': (32, 32), 'crop': True}"]


def test_quoted_string_mask_keeps_literal_quotes():
    masker = Masker()
    masker.global_tab["it's"] = "<mask_0>"

    assert restore_masked_source_text(["value = '<mask_0>'"], masker) == ["value = 'it\\'s'"]
