"""
Project-wide **mapping utility** unit tests.

This submodule unit tests the public API of the private
:mod:`beartype._util.kind.utilkinddict` submodule.
"""
from pytest import raises
THE_SONG_OF_HIAWATHA = {'By the shore': 'of Gitche Gumee', 'By the shining': 'Big-Sea-Water', 'At the': 'doorway of his wigwam', 'In the': 'pleasant Summer morning', 'Hiawatha': 'stood and waited.'}
'\nArbitrary dictionary to be merged.\n'
THE_SONG_OF_HIAWATHA_SINGING_IN_THE_SUNSHINE = {'By the shore': 'of Gitche Gumee', 'By the shining': ['Big-Sea-Water'], 'At the': 'doorway of his wigwam', 'In the': ['pleasant', 'Summer morning'], 'Hiawatha': 'stood and waited.', 'All the air': ['was', 'full of freshness,'], 'All the earth': 'was bright and joyous,', 'And': ['before him,', 'through the sunshine,'], 'Westward': 'toward the neighboring forest', 'Passed in': ['golden swarms', 'the Ahmo,'], 'Passed the': 'bees, the honey-makers,', 'Burning,': ['singing', 'in the sunshine.']}
'\nArbitrary dictionary to be merged, intentionally containing two key-value\ncollisions with the :data:`THE_SONG_OF_HIAWATHA` dictionary *and* unhashable\nvalues.\n'
FROM_THE_BROW_OF_HIAWATHA = {'From the': 'brow of Hiawatha', 'Gone was': 'every trace of sorrow,', 'As the fog': 'from off the water,', 'As the mist': 'from off the meadow.'}
'\nArbitrary dictionary to be merged, intentionally containing neither key nor\nkey-value collisions with any other global dictionary.\n'
IN_THE_LODGE_OF_HIAWATHA = {'I am': 'going, O Nokomis,', 'On a': 'long and distant journey,', 'To the portals': 'of the Sunset,', 'To the regions': 'of the home-wind,', 'Of the Northwest-Wind,': 'Keewaydin.'}
'\nArbitrary dictionary to be merged, intentionally containing:\n\n* No key-value collisions with the :data:`THE_SONG_OF_HIAWATHA` dictionary.\n* Two key collisions but *no* key-value collisions with the\n  :data:`FAREWELL_O_HIAWATHA` dictionary.\n'
FAREWELL_O_HIAWATHA = {'Thus departed': 'Hiawatha,', 'Hiawatha': 'the Beloved,', 'In the': 'glory of the sunset,', 'In the purple': 'mists of evening,', 'To the regions': 'of the home-wind,', 'Of the Northwest-Wind,': 'Keewaydin.'}
'\nArbitrary dictionary to be merged, intentionally containing two key-value\ncollisions with the :data:`THE_SONG_OF_HIAWATHA` dictionary.\n'
THE_SONG_OF_HIAWATHA_IN_THE_LODGE_OF_HIAWATHA = {'By the shore': 'of Gitche Gumee', 'By the shining': 'Big-Sea-Water', 'At the': 'doorway of his wigwam', 'In the': 'pleasant Summer morning', 'Hiawatha': 'stood and waited.', 'I am': 'going, O Nokomis,', 'On a': 'long and distant journey,', 'To the portals': 'of the Sunset,', 'To the regions': 'of the home-wind,', 'Of the Northwest-Wind,': 'Keewaydin.'}
'\nDictionary produced by merging the :data:`THE_SONG_OF_HIAWATHA` and\n:data:`IN_THE_LODGE_OF_HIAWATHA` dictionaries.\n'
IN_THE_LODGE_OF_HIAWATHA_FAREWELL_O_HIAWATHA = {'I am': 'going, O Nokomis,', 'On a': 'long and distant journey,', 'To the portals': 'of the Sunset,', 'To the regions': 'of the home-wind,', 'Of the Northwest-Wind,': 'Keewaydin.', 'Thus departed': 'Hiawatha,', 'Hiawatha': 'the Beloved,', 'In the': 'glory of the sunset,', 'In the purple': 'mists of evening,'}
'\nDictionary produced by merging the :data:`IN_THE_LODGE_OF_HIAWATHA` and\n:data:`FAREWELL_O_HIAWATHA` dictionaries.\n'
FROM_THE_BROW_OF_HIAWATHA_IN_THE_LODGE_OF_HIAWATHA_FAREWELL_O_HIAWATHA = {'From the': 'brow of Hiawatha', 'Gone was': 'every trace of sorrow,', 'As the fog': 'from off the water,', 'As the mist': 'from off the meadow.', 'I am': 'going, O Nokomis,', 'On a': 'long and distant journey,', 'To the portals': 'of the Sunset,', 'To the regions': 'of the home-wind,', 'Of the Northwest-Wind,': 'Keewaydin.', 'Thus departed': 'Hiawatha,', 'Hiawatha': 'the Beloved,', 'In the': 'glory of the sunset,', 'In the purple': 'mists of evening,'}
'\nDictionary produced by merging the :data:`FROM_THE_BROW_OF_HIAWATHA`,\n:data:`IN_THE_LODGE_OF_HIAWATHA`, and :data:`FAREWELL_O_HIAWATHA` dictionaries.\n'

def test_die_if_mappings_two_items_collide() -> None:
    """
    Test the
    :func:`beartype._util.kind.utilkinddict.die_if_mappings_two_items_collide`
    validator.
    """
    from beartype.roar._roarexc import _BeartypeUtilMappingException
    from beartype._util.kind.utilkinddict import die_if_mappings_two_items_collide
    with raises(_BeartypeUtilMappingException):
        die_if_mappings_two_items_collide(THE_SONG_OF_HIAWATHA, FAREWELL_O_HIAWATHA)
    with raises(_BeartypeUtilMappingException):
        die_if_mappings_two_items_collide(FAREWELL_O_HIAWATHA, THE_SONG_OF_HIAWATHA)
    with raises(_BeartypeUtilMappingException):
        die_if_mappings_two_items_collide(THE_SONG_OF_HIAWATHA, THE_SONG_OF_HIAWATHA_SINGING_IN_THE_SUNSHINE)

def test_is_mapping_keys_all() -> None:
    """
    Test the
    :func:`beartype._util.kind.utilkinddict.is_mapping_keys_all` tester.
    """
    from beartype.roar._roarexc import _BeartypeUtilMappingException
    from beartype._util.kind.utilkinddict import is_mapping_keys_all
    assert is_mapping_keys_all(mapping=THE_SONG_OF_HIAWATHA_SINGING_IN_THE_SUNSHINE, keys=THE_SONG_OF_HIAWATHA.keys()) is True
    assert is_mapping_keys_all(mapping=THE_SONG_OF_HIAWATHA_SINGING_IN_THE_SUNSHINE, keys=THE_SONG_OF_HIAWATHA.keys() | {'As the mist'}) is False

def test_is_mapping_keys_any() -> None:
    """
    Test the
    :func:`beartype._util.kind.utilkinddict.is_mapping_keys_any` tester.
    """
    from beartype.roar._roarexc import _BeartypeUtilMappingException
    from beartype._util.kind.utilkinddict import is_mapping_keys_any
    assert is_mapping_keys_any(mapping=FAREWELL_O_HIAWATHA, keys={'Thus departed', 'By the shore', 'To the portals'}) is True
    assert is_mapping_keys_any(mapping=FAREWELL_O_HIAWATHA, keys={'By the shore', 'To the portals'}) is False

def test_update_mapping() -> None:
    """
    Test the :func:`beartype._util.kind.utilkinddict.update_mapping` function.
    """
    from beartype._util.kind.utilkinddict import update_mapping
    farewell_o_hiawatha = FAREWELL_O_HIAWATHA.copy()
    the_song_of_hiawatha = THE_SONG_OF_HIAWATHA.copy()
    update_mapping(farewell_o_hiawatha, {})
    assert farewell_o_hiawatha == FAREWELL_O_HIAWATHA
    update_mapping(the_song_of_hiawatha, IN_THE_LODGE_OF_HIAWATHA)
    assert the_song_of_hiawatha == THE_SONG_OF_HIAWATHA_IN_THE_LODGE_OF_HIAWATHA
    update_mapping(farewell_o_hiawatha, IN_THE_LODGE_OF_HIAWATHA)
    assert farewell_o_hiawatha == IN_THE_LODGE_OF_HIAWATHA_FAREWELL_O_HIAWATHA

def test_merge_mappings_two() -> None:
    """
    Test the :func:`beartype._util.kind.utilkinddict.merge_mappings` function
    passed exactly two mappings.
    """
    from beartype._util.kind.utilkinddict import merge_mappings
    assert merge_mappings({}, {}) == {}
    assert merge_mappings(THE_SONG_OF_HIAWATHA, {}) == THE_SONG_OF_HIAWATHA
    assert merge_mappings({}, THE_SONG_OF_HIAWATHA) == THE_SONG_OF_HIAWATHA
    assert merge_mappings(THE_SONG_OF_HIAWATHA, IN_THE_LODGE_OF_HIAWATHA) == THE_SONG_OF_HIAWATHA_IN_THE_LODGE_OF_HIAWATHA
    assert merge_mappings(IN_THE_LODGE_OF_HIAWATHA, THE_SONG_OF_HIAWATHA) == THE_SONG_OF_HIAWATHA_IN_THE_LODGE_OF_HIAWATHA
    assert merge_mappings(IN_THE_LODGE_OF_HIAWATHA, FAREWELL_O_HIAWATHA) == IN_THE_LODGE_OF_HIAWATHA_FAREWELL_O_HIAWATHA
    assert merge_mappings(FAREWELL_O_HIAWATHA, IN_THE_LODGE_OF_HIAWATHA) == IN_THE_LODGE_OF_HIAWATHA_FAREWELL_O_HIAWATHA

def test_merge_mappings_three() -> None:
    """
    Test the :func:`beartype._util.kind.utilkinddict.merge_mappings` function
    passed exactly three mappings.
    """
    from beartype._util.kind.utilkinddict import merge_mappings
    assert merge_mappings({}, {}, {}) == {}
    assert merge_mappings(THE_SONG_OF_HIAWATHA, {}, {}) == THE_SONG_OF_HIAWATHA
    assert merge_mappings({}, THE_SONG_OF_HIAWATHA, {}) == THE_SONG_OF_HIAWATHA
    assert merge_mappings({}, {}, THE_SONG_OF_HIAWATHA) == THE_SONG_OF_HIAWATHA
    assert merge_mappings(FROM_THE_BROW_OF_HIAWATHA, IN_THE_LODGE_OF_HIAWATHA, FAREWELL_O_HIAWATHA) == FROM_THE_BROW_OF_HIAWATHA_IN_THE_LODGE_OF_HIAWATHA_FAREWELL_O_HIAWATHA