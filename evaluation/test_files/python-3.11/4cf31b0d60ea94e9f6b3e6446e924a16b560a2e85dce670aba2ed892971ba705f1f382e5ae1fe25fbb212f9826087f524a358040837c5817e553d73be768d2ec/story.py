import re
from datetime import datetime
from decimal import Decimal
from operator import attrgetter
from typing import Any, Optional
from dateutil import parser
from .excel_definition import ExcelDefinition, ExcelDefinitionColumn
from .milestone import *
from .priority import *
from .sprint_schedule import SprintScheduleStore
__all__ = ['Story', 'StoryFactory', 'convert_to_bool', 'convert_to_datetime', 'convert_to_decimal', 'sort_stories_by_property_and_order', 'sort_stories_by_raise_ranking']

def convert_to_bool(raw: Any) -> bool:
    if type(raw) is bool:
        return raw
    value = str(raw).strip().upper()
    if value == 'YES' or value == 'TRUE':
        return True
    else:
        return False

def convert_to_decimal(raw: Any) -> Decimal:
    if type(raw) is Decimal:
        return raw
    raw = str(raw).strip()
    pattern = re.compile('[0-9.]{1,10}')
    result = pattern.search(raw)
    if result is not None:
        return Decimal(result.group())
    else:
        return Decimal(0)

def convert_to_datetime(raw: Any) -> 'datetime | None':
    if type(raw) is datetime:
        return raw
    if raw is None:
        return
    raw = str(raw).strip()
    return parser.parse(raw)

class Story(object):

    def __init__(self, factory: 'StoryFactory') -> None:
        self.need_sort = True
        if factory is None:
            raise ValueError('Story must be created from a specific factory!')
        self.factory = factory
        for column in self.factory.columns:
            if column['name'] is None:
                continue
            if column['type'] is str:
                setattr(self, column['name'], '')
            elif column['type'] is bool:
                setattr(self, column['name'], False)
            elif column['type'] is Priority:
                setattr(self, column['name'], Priority.NA)
            elif column['type'] is Milestone:
                setattr(self, column['name'], None)
            elif column['type'] is datetime:
                setattr(self, column['name'], None)
            else:
                setattr(self, column['name'], None)

    @property
    def need_sort(self) -> bool:
        return self._need_sort

    @need_sort.setter
    def need_sort(self, value: bool):
        self._need_sort = value

    def __getitem__(self, property_name) -> Any:
        return getattr(self, property_name)

    def format_value(self, property_name: str) -> str:
        property = getattr(self, property_name, None)
        if property is None:
            return ''
        elif type(property) is datetime:
            return property.date().isoformat()
        elif type(property) is bool:
            if property:
                return 'Yes'
            else:
                return 'No'
        elif type(property) is float:
            return str(property)
        else:
            return str(property)

    def set_value(self, property_type: Any, property_name: str, property_value: Any):
        if property_type is str:
            setattr(self, property_name, property_value)
        elif property_type is bool:
            setattr(self, property_name, convert_to_bool(property_value))
        elif property_type is Priority:
            setattr(self, property_name, convert_to_priority(property_value))
        elif property_type is datetime:
            setattr(self, property_name, convert_to_datetime(property_value))
        elif property_type is Milestone:
            milestone = Milestone(property_value)
            setattr(self, property_name, milestone)
        else:
            setattr(self, property_name, property_value)

    def __setitem__(self, property_name, property_value):
        self.set_value(type(property_value), property_name, property_value)

    def calc_sprint_schedule(self, sprint_schedule: SprintScheduleStore):
        for column in self.factory.columns:
            if column['type'] is Milestone and self[column['name']] is not None:
                self[column['name']].calc_priority(sprint_schedule)

    def __lt__(self, __o: 'Story | None') -> bool:
        return self.factory.compare_story(self, __o) < 0

    def __le__(self, __o: 'Story | None') -> bool:
        return self.factory.compare_story(self, __o) <= 0

    def __gt__(self, __o: 'Story | None') -> bool:
        return self.factory.compare_story(self, __o) > 0

    def __ge__(self, __o: 'Story | None') -> bool:
        return self.factory.compare_story(self, __o) >= 0

    def __eq__(self, __o: 'Story | None') -> bool:
        return self.factory.compare_story(self, __o) == 0

    def __str__(self):
        result = ''
        if self is None:
            return result
        separator = ', '
        for column in self.factory.columns:
            if column['name'] is not None and hasattr(self, column['name']):
                result += f"{str(getattr(self, column['name']))}{separator}"
        return result

class StoryFactory(object):

    def __init__(self, columns: 'list[ExcelDefinitionColumn]') -> None:
        if columns is None:
            raise ValueError('Columns must be provided!')
        self._columns = columns
        self._compare_rules = self.__generate_compare_rules()

    def __generate_compare_rules(self) -> 'list[tuple[str, int]]':
        compare_rules = []
        for column in self._columns:
            if column['inline_weights'] > 0:
                compare_rules.append((column['name'], column['inline_weights']))
        compare_rules.sort(key=lambda r: r[1], reverse=True)
        return compare_rules

    @property
    def columns(self):
        return self._columns

    @property
    def compare_rules(self) -> 'list[tuple[str, int]]':
        return self._compare_rules

    def create_story(self) -> Story:
        return Story(self)

    def compare_story(self, a: 'Story | None', b: 'Story | None') -> int:
        """
        Compare two stories.

        :parm a:
            First story
        :parm b:
            Second story
        :parm sort_rule:
            Priority information
        :return
            1: means a > b
            0: means a == b
            -1: means a < b
        """
        if a is None or b is None:
            raise ValueError('The compare stories cannot be None.')
        if a.factory != b.factory or a.factory != self or b.factory != self:
            raise ValueError('The compare stories were built by different factory.')
        rules_count = len(self.compare_rules)
        if rules_count == 0:
            return 0
        skip_index_of_a = []
        skip_index_of_b = []
        count = rules_count
        while count > 0:
            highest_property_of_a = None
            highest_property_of_b = None
            for i in range(len(self.compare_rules)):
                if i in skip_index_of_a:
                    continue
                if highest_property_of_a is None:
                    highest_property_of_a = (a[self.compare_rules[i][0]], i)
                if a[self.compare_rules[i][0]] > highest_property_of_a[0]:
                    highest_property_of_a = (a[self.compare_rules[i][0]], i)
            for i in range(len(self.compare_rules)):
                if i in skip_index_of_b:
                    continue
                if highest_property_of_b is None:
                    highest_property_of_b = (b[self.compare_rules[i][0]], i)
                if b[self.compare_rules[i][0]] > highest_property_of_b[0]:
                    highest_property_of_b = (b[self.compare_rules[i][0]], i)
            if highest_property_of_a is None:
                highest_property_of_a = (Priority.NA, count)
            else:
                skip_index_of_a.append(highest_property_of_a[1])
            if highest_property_of_b is None:
                highest_property_of_b = (Priority.NA, count)
            else:
                skip_index_of_b.append(highest_property_of_b[1])
            if highest_property_of_a[0] > highest_property_of_b[0]:
                return 1
            elif highest_property_of_a[0] == highest_property_of_b[0]:
                if highest_property_of_a[1] < highest_property_of_b[1]:
                    return 1
                elif highest_property_of_a[1] > highest_property_of_b[1]:
                    return -1
            else:
                return -1
            if highest_property_of_a[1] > highest_property_of_b[1]:
                return 1
            elif highest_property_of_a[1] == highest_property_of_b[1]:
                if highest_property_of_a[0] > highest_property_of_b[0]:
                    return 1
                elif highest_property_of_a[0] < highest_property_of_b[0]:
                    return -1
            else:
                return -1
            count -= 1
            continue
        return 0

def sort_stories_by_property_and_order(stories: 'list[Story]', excel_definition: ExcelDefinition, config: dict):
    sort_rules: list[tuple[str, bool]] = []
    excel_definition_columns = excel_definition.get_columns()
    if 'ParentScopeIndexRange' in config:
        column_definitions: dict[int, ExcelDefinitionColumn] = {c['index']: c for c in excel_definition_columns}
        for column in excel_definition_columns:
            if column['scope_require_sort'] is True and column['name'] is not None:
                sort_rules.append((column['name'], column['scope_sort_order']))
        _internal_sort_stories_by_property_and_order_considering_parent_range(stories, column_definitions, sort_rules, config['ParentScopeIndexRange'])
    else:
        for column in excel_definition_columns:
            if column['require_sort'] is True and column['name'] is not None:
                sort_rules.append((column['name'], column['sort_order']))
        _internal_sort_stories_by_property_and_order(stories, sort_rules)

def _internal_sort_stories_by_property_and_order(stories: 'list[Story]', sort_rules: 'list[tuple[str, bool]]'):
    for column_name, sort_order in reversed(sort_rules):
        stories.sort(key=attrgetter(column_name), reverse=sort_order)

def _internal_sort_stories_by_property_and_order_considering_parent_range(stories: 'list[Story]', story_columns: 'dict[int, ExcelDefinitionColumn]', sort_rules: 'list[tuple[str, bool]]', parent_level_index_range: 'set[int]') -> 'list[Story]':
    begin_index = 0
    end_index = 0
    while end_index <= len(stories) - 1:
        for i in range(begin_index, len(stories) - 1):
            all_parent_column_matched = True
            for column_index in parent_level_index_range:
                if stories[i][story_columns[column_index]['name']] != stories[i + 1][story_columns[column_index]['name']]:
                    all_parent_column_matched = False
                    break
            if all_parent_column_matched:
                continue
            else:
                end_index = i
                break
        for column_name, sort_order in reversed(sort_rules):
            if begin_index != end_index:
                stories[begin_index:end_index + 1] = sorted(stories[begin_index:end_index + 1], key=attrgetter(column_name), reverse=sort_order)
        begin_index = end_index + 1
        end_index = begin_index
    return stories

def sort_stories_by_raise_ranking(stories: 'list[Story]', excel_definition: ExcelDefinition, config: dict) -> 'list[Story]':
    if stories is None:
        return []
    sort_rules: list[tuple[str, int]] = []
    excel_definition_columns = excel_definition.get_columns()
    result = []
    if 'ParentScopeIndexRange' in config:
        for column in excel_definition_columns:
            if column['scope_raise_ranking'] > 0 and column['name'] is not None:
                sort_rules.append((column['name'], column['scope_raise_ranking']))
        if len(sort_rules) == 0:
            return stories
        sort_rules.sort(key=lambda x: x[1], reverse=True)
        column_definitions: dict[int, ExcelDefinitionColumn] = {c['index']: c for c in excel_definition_columns}
        result = _internal_raise_story_ranking_by_property_considering_parent_level(stories, column_definitions, sort_rules, config['ParentScopeIndexRange'])
    else:
        for column in excel_definition_columns:
            if column['raise_ranking'] > 0 and column['name'] is not None:
                sort_rules.append((column['name'], column['raise_ranking']))
        if len(sort_rules) == 0:
            return stories
        sort_rules.sort(key=lambda x: x[1], reverse=True)
        for property_name, _ in sort_rules:
            result = _internal_raise_story_ranking_by_property(stories, property_name)
    return result

def _internal_raise_story_ranking_by_property(stories: 'list[Story]', property_name: str) -> 'list[Story]':
    if stories is None or len(stories) == 0:
        return stories
    if not hasattr(stories[0], property_name):
        return stories
    return _raise_story_ranking_by_property(stories, property_name)

def _internal_raise_story_ranking_by_property_considering_parent_level(stories: 'list[Story]', story_columns: 'dict[int, ExcelDefinitionColumn]', sort_rules: 'list[tuple[str, int]]', parent_level_index_range: 'set[int]') -> 'list[Story]':
    begin_index = 0
    end_index = 0
    while end_index <= len(stories) - 1:
        for i in range(begin_index, len(stories) - 1):
            all_parent_column_matched = True
            for column_index in parent_level_index_range:
                if stories[i][story_columns[column_index]['name']] != stories[i + 1][story_columns[column_index]['name']]:
                    all_parent_column_matched = False
                    break
            if all_parent_column_matched:
                continue
            else:
                end_index = i
                break
        for column_name, _ in reversed(sort_rules):
            stories[begin_index:end_index + 1] = _raise_story_ranking_by_property(stories[begin_index:end_index + 1], column_name)
        begin_index = end_index + 1
        end_index = begin_index
    return stories

def _raise_story_ranking_by_property(stories: 'list[Story]', property_name: str) -> 'list[Story]':
    if type(getattr(stories[0], property_name)) is not bool:
        return stories
    result: list[Story] = [stories[0]] * len(stories)
    j = 0
    for i in range(len(stories)):
        if getattr(stories[i], property_name) is True:
            result[j] = stories[i]
            j += 1
    for i in range(len(stories)):
        if getattr(stories[i], property_name) is False:
            result[j] = stories[i]
            j += 1
    return result