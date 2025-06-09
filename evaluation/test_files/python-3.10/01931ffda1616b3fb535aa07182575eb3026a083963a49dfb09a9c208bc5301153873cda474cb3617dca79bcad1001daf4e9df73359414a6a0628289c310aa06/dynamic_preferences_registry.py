from dynamic_preferences import types
from dynamic_preferences.registries import global_preferences_registry
playlists = types.Section('playlists')

@global_preferences_registry.register
class MaxTracks(types.IntegerPreference):
    show_in_api = True
    section = playlists
    name = 'max_tracks'
    default = 250
    verbose_name = 'Max tracks per playlist'
    field_kwargs = {'required': False}