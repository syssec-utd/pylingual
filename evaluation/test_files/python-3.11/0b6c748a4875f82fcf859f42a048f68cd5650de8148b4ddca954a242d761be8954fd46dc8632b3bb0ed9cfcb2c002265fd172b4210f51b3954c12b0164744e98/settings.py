from django.utils.translation import ugettext_lazy as _
from mayan.apps.smart_settings.classes import SettingNamespace
from .literals import DEFAULT_SEARCH_BACKEND, DEFAULT_SEARCH_BACKEND_ARGUMENTS, DEFAULT_SEARCH_DISABLE_SIMPLE_SEARCH, DEFAULT_SEARCH_INDEXING_CHUNK_SIZE, DEFAULT_SEARCH_MATCH_ALL_DEFAULT_VALUE, DEFAULT_SEARCH_RESULTS_LIMIT
namespace = SettingNamespace(label=_('Search'), name='search')
setting_backend = namespace.add_setting(default=DEFAULT_SEARCH_BACKEND, global_name='SEARCH_BACKEND', help_text=_('Full path to the backend to be used to handle the search.'))
setting_backend_arguments = namespace.add_setting(default=DEFAULT_SEARCH_BACKEND_ARGUMENTS, global_name='SEARCH_BACKEND_ARGUMENTS', help_text=_('Arguments to pass to the search backend. For example values to change the behavior, host names, or authentication arguments.'))
setting_disable_simple_search = namespace.add_setting(default=DEFAULT_SEARCH_DISABLE_SIMPLE_SEARCH, global_name='SEARCH_DISABLE_SIMPLE_SEARCH', help_text=_('Disables the single term bar search leaving only the advanced search button.'))
setting_indexing_chunk_size = namespace.add_setting(default=DEFAULT_SEARCH_INDEXING_CHUNK_SIZE, global_name='SEARCH_INDEXING_CHUNK_SIZE', help_text=_('Amount of objects to process when performing bulk indexing.'))
setting_match_all_default_value = namespace.add_setting(global_name='SEARCH_MATCH_ALL_DEFAULT_VALUE', default=DEFAULT_SEARCH_MATCH_ALL_DEFAULT_VALUE, help_text=_('Sets the default state of the "Match all" checkbox.'))
setting_results_limit = namespace.add_setting(default=DEFAULT_SEARCH_RESULTS_LIMIT, global_name='SEARCH_RESULTS_LIMIT', help_text=_('Maximum number search results to fetch and display.'))