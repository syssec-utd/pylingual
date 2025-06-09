from __future__ import absolute_import
from m3_ext.ui.containers import ExtContextMenu
from m3_ext.ui.containers import ExtContextMenuItem
from m3_ext.ui.containers.container_complex import ExtContainerTable
from m3_ext.ui.containers.containers import ExtContainer
from m3_ext.ui.containers.containers import ExtToolBar
from m3_ext.ui.containers.containers import ExtToolbarMenu
from m3_ext.ui.containers.forms import ExtFieldSet
from m3_ext.ui.containers.grids import ExtGrid
from m3_ext.ui.containers.trees import ExtTree
from m3_ext.ui.controls.buttons import ExtButton
from m3_ext.ui.fields.simple import ExtCheckBox
from m3_ext.ui.fields.simple import ExtStringField
from m3_ext.ui.fields.simple import ExtTextArea
from m3_ext.ui.misc.store import ExtDataStore
from objectpack.ui import ColumnsConstructor
from objectpack.ui import ComboBoxWithStore
from objectpack.ui import WindowTab
from objectpack.ui import _create_control_for_field
from objectpack.ui import make_combo_box
from educommon.objectpack.ui import BaseListWindow
from educommon.objectpack.ui import TabbedEditWindow
from educommon.utils.ui import local_template
from .. import constants
from .. import models
from ..models import ReportTemplate

class ListWindow(BaseListWindow):
    u"""Окно просмотра списка шаблонов отчетов."""

    def _init_components(self):
        super(ListWindow, self)._init_components()
        self.grid.top_bar.button__build = ExtButton(text=u'Собрать отчет', icon_cls='database_table', handler='buildReport', disabled=True)
        self.grid.context_menu_row.menuitem__build = ExtContextMenuItem(text=u'Собрать отчет', icon_cls='database_table', handler='buildReport')

    def _do_layout(self):
        super(ListWindow, self)._do_layout()
        self.grid.top_bar.items.insert(0, self.grid.top_bar.button__build)
        self.grid.context_menu_row.items.append(self.grid.context_menu_row.menuitem__build)

    def set_params(self, params):
        super(ListWindow, self).set_params(params)
        self.template_globals = local_template('list-window.js')
        self.build_action_url = params['build_action_url']

class AvailableColumnsTree(ExtTree):
    u"""Дерево доступных для использования в отчете столбцов."""

    class ToolBar(ExtToolBar):

        def __init__(self, *args, **kwargs):
            super(AvailableColumnsTree.ToolBar, self).__init__(*args, **kwargs)
            self.button__add = ExtButton(text=u'Добавить в шаблон', icon_cls='add_item', handler='addColumnToReport', disabled=True)
            self.items[:] = (self.button__add,)

    def __init__(self, *args, **kwargs):
        kwargs.update(title=u'Доступные наименования столбцов', header=True, read_only=True)
        super(AvailableColumnsTree, self).__init__(*args, **kwargs)
        self.style = {'border-width': '1px'}
        ColumnsConstructor.from_config((dict(data_index='title', header=u'Наименование', sortable=False),)).configure_grid(self)
        self.top_bar = self.ToolBar()

    def set_params(self, params):
        self.available_columns_url = params['available_columns_action_url']

class ReportColumnsTree(ExtTree):
    u"""Дерево используемых в шаблоне отчета столбцов."""

    class ToolBar(ExtToolBar):

        def __init__(self, *args, **kwargs):
            super(ReportColumnsTree.ToolBar, self).__init__(*args, **kwargs)
            self.button__remove = ExtButton(text=u'Убрать столбец', icon_cls='delete_item', handler='removeColumnFromReport', disabled=True)
            self.button__switch_visibility = ExtButton(text=u'Скрывать', icon_cls='report-constructor-switch-visible', handler='switchColumnVisibility', hidden=True)
            self.button__by_value_count = ExtContextMenuItem(text=u'Количество', icon_cls='icon-report-add', handler='setByValueCountAggregator')
            self.button__by_value_sum = ExtContextMenuItem(text=u'Сумма', icon_cls='icon-report-add', handler='setByValueSumAggregator')
            self.button__by_value_none = ExtContextMenuItem(text=u'Очистить', icon_cls='icon-report-delete', handler='setByValueNoneAggregator')
            context_menu__by_value = ExtContextMenu()
            context_menu__by_value.items.extend((self.button__by_value_count, self.button__by_value_sum, self.button__by_value_none))
            self.menu__by_value = ExtToolbarMenu(icon_cls='icon-report', menu=context_menu__by_value, text=u'Промежуточный итог', hidden=True)
            self.button__total_count = ExtContextMenuItem(text=u'Количество', icon_cls='icon-calculator-add', handler='setTotalCountAggregator')
            self.button__total_uniq_count = ExtContextMenuItem(text=u'Количество уникальных', icon_cls='icon-calculator-add', handler='setTotalCountUniqueAggregator')
            self.button__total_sum = ExtContextMenuItem(text=u'Сумма', icon_cls='icon-calculator-add', handler='setTotalSumAggregator')
            self.button__total_none = ExtContextMenuItem(text=u'Очистить', icon_cls='icon-calculator-delete', handler='setTotalNoneAggregator')
            context_menu__total = ExtContextMenu()
            context_menu__total.items.extend((self.button__total_count, self.button__total_uniq_count, self.button__total_sum, self.button__total_none))
            self.menu__total = ExtToolbarMenu(icon_cls='icon-calculator', menu=context_menu__total, text=u'Итог', hidden=True)
            self.items[:] = (self.button__remove, self.button__switch_visibility, self.menu__by_value, self.menu__total)

    def __init__(self, *args, **kwargs):
        kwargs.update(title=u'Столбцы в отчете', header=True)
        super(ReportColumnsTree, self).__init__(*args, **kwargs)
        self.enable_sort = False
        self.style = {'border-width': '1px'}
        ColumnsConstructor.from_config((dict(data_index='title', header=u'Наименование', sortable=False), dict(data_index='visible', hidden=True), dict(data_index='visible_title', header=u'Отображать', sortable=False, width=20, fixed=True), dict(data_index='by_value', hidden=True), dict(data_index='by_value_title', header=u'Промежуточный итог', sortable=False, width=20, fixed=True), dict(data_index='total', hidden=True), dict(data_index='total_title', header=u'Итог', sortable=False, width=20, fixed=True))).configure_grid(self)
        self.top_bar = self.ToolBar()

    def set_params(self, params):
        pass

class ColumnsTab(WindowTab):
    u"""Вкладка "Колонки" окна редактирования шаблона отчета."""
    title = u'Столбцы'

    def init_components(self, win):
        super(ColumnsTab, self).init_components(win)
        self.grid__available_columns = AvailableColumnsTree()
        self.grid__report_columns = ReportColumnsTree()

    def do_layout(self, win, tab):
        super(ColumnsTab, self).do_layout(win, tab)
        win.tab__columns = tab
        tab.grid__available_columns = self.grid__available_columns
        tab.grid__report_columns = self.grid__report_columns
        tab.items[:] = (self.grid__available_columns, ExtContainer(width=5), self.grid__report_columns)
        tab.layout = 'hbox'
        tab.layout_config = {'align': 'stretch'}
        self.grid__available_columns.flex = 2
        self.grid__report_columns.flex = 3

    def set_params(self, win, params):
        super(ColumnsTab, self).set_params(win, params)
        self.grid__available_columns.set_params(params)
        self.grid__report_columns.set_params(params)
        self.grid__report_columns.drag_drop = True
        self.grid__report_columns.handler_beforedrop = 'onBeforeDrop'

class OperatorPanel(ExtFieldSet):
    u"""Панель для поля "Оператор" на вкладке "Фильтры"."""

    def __init__(self, *args, **kwargs):
        super(OperatorPanel, self).__init__(*args, **kwargs)
        self.label_width = 55
        self.style = {'border': 0, 'padding': 0}
        self.field__operator = ComboBoxWithStore(name='operator', display_field='title', label=u'Условие', width=70)
        self.field__operator.data = (('AND', u'И'), ('OR', u'ИЛИ'))
        self.hidden = True
        self.field__operator.value = 'AND'
        self.items[:] = (self.field__operator,)

class FilterParamsPanel(ExtContainerTable):
    u"""Панель ввода параметров фильтра."""

    def __init__(self, *args, **kwargs):
        super(FilterParamsPanel, self).__init__(columns=3, rows=4)
        self.title = u'Параметры фильтра'
        self.style['padding-top'] = '5px'
        self.field__column = ComboBoxWithStore(name='column', value_field='name', display_field='title', label=u'Столбец')
        self.field__operator = ComboBoxWithStore(name='operator', display_field='title', label=u'Условие', data=())
        self.field__operator.store.id_property = self.field__operator.value_field
        self.field__exclude = ExtCheckBox(name='exclude', label=u'Обратное условие', disabled=True)
        self.field__case_sensitive = ExtCheckBox(name='case_sensitive', label=u'Учет регистра', disabled=True)
        self.field__value = ExtStringField(name='values', label=u'Значение', disabled=True)
        self.field__comment = ExtTextArea(name='comment', label=u'Описание', height=35, disabled=True)
        self.set_item(0, 0, self.field__column, 3)
        self.set_item(1, 0, self.field__operator)
        self.set_item(1, 1, self.field__exclude)
        self.set_item(1, 2, self.field__case_sensitive)
        self.set_item(2, 0, self.field__value, 3)
        self.set_item(3, 0, self.field__comment, 3)
        self.set_properties(0, 0, label_width=60)
        self.set_properties(1, 0, label_width=60)
        self.set_properties(1, 1, label_width=110, flex=0, width=150)
        self.set_properties(1, 2, label_width=85, flex=0, width=115)
        self.set_properties(2, 0, label_width=60)
        self.set_properties(3, 0, label_width=60)
        self.set_rows_height(25)
        self.set_row_height(3, 40)

class FiltersGridTopBar(ExtToolBar):
    u"""Верхняя панель грида с параметрами фильтрации."""

    def __init__(self, *args, **kwargs):
        super(FiltersGridTopBar, self).__init__(*args, **kwargs)
        self.button__add = ExtButton(text=u'Добавить', icon_cls='add_item', handler='addFilter')
        self.button__delete = ExtButton(text=u'Удалить', icon_cls='delete_item', handler='deleteFilter', disabled=True)
        self.items[:] = (self.button__add, self.button__delete)

class FiltersGrid(ExtGrid):
    u"""Грид с параметрами фильтрации данных в отчете."""

    def __init__(self, *args, **kwargs):
        super(FiltersGrid, self).__init__(*args, **kwargs)
        self.cls = 'word-wrap-grid'
        self.store = ExtDataStore(id_property='column')
        self.top_bar = FiltersGridTopBar()
        self.add_column(data_index='column', hidden=True)
        self.add_column(data_index='column_title', header=u'Столбец')
        self.add_column(data_index='operator', hidden=True)
        self.add_column(data_index='operator_title', header=u'Условие', width=110, fixed=True)
        self.add_check_column(data_index='exclude', header=u'Обратное условие', width=90, fixed=True)
        self.add_check_column(data_index='case_sensitive', header=u'Учет регистра', width=85, fixed=True)
        self.add_column(data_index='values', header=u'Значение')
        self.add_column(data_index='comment', header=u'Описание')

class FiltersTab(WindowTab):
    u"""Вкладка "Фильтры" окна редактирования шаблона отчета."""
    title = u'Фильтры'

    def init_components(self, win):
        super(FiltersTab, self).init_components(win)
        self.panel__operator = OperatorPanel()
        self.panel__filter_params = FilterParamsPanel()
        self.grid__filters = FiltersGrid()

    def do_layout(self, win, tab):
        super(FiltersTab, self).do_layout(win, tab)
        win.tab__filters = tab
        tab.panel__operator = self.panel__operator
        tab.grid__filters = self.grid__filters
        tab.panel__filter_params = self.panel__filter_params
        tab.items[:] = (self.panel__operator, self.grid__filters, self.panel__filter_params)
        tab.layout = 'vbox'
        tab.layout_config = {'align': 'stretch'}
        self.panel__filter_params.flex = 0
        self.panel__filter_params.height = 120
        self.grid__filters.flex = 1

class SortingGridTopBar(ExtToolBar):
    u"""Верхняя панель грида с параметрами сортировки."""

    def __init__(self, *args, **kwargs):
        super(SortingGridTopBar, self).__init__(*args, **kwargs)
        self.button__add = ExtButton(text=u'Добавить', icon_cls='add_item', handler='addSort')
        self.button__delete = ExtButton(text=u'Удалить', icon_cls='delete_item', handler='deleteSort', disabled=True)
        self.button__move_up = ExtButton(icon_cls='report-constructor-arrow-up', handler='moveSortUp', disabled=True)
        self.button__move_down = ExtButton(icon_cls='report-constructor-arrow-down', handler='moveSortDown', disabled=True)
        self.items[:] = (self.button__add, self.button__delete, self.button__move_up, self.button__move_down)

class SortingGrid(ExtGrid):
    u"""Грид для отображения параметров сортировки."""

    def __init__(self, *args, **kwargs):
        super(SortingGrid, self).__init__(*args, **kwargs)
        self.cls = 'word-wrap-grid'
        self.store = ExtDataStore(id_property='column')
        self.top_bar = SortingGridTopBar()
        self.add_column(data_index='column', hidden=True)
        self.add_column(data_index='column_title', header=u'Столбец', width=1)
        self.add_column(data_index='direction', hidden=True)
        self.add_column(data_index='direction_title', header=u'Направление сортировки', width=150, fixed=True)

class SortingParamsPanel(ExtFieldSet):
    u"""Панель ввода параметров сортировки."""

    def __init__(self, *args, **kwargs):
        super(SortingParamsPanel, self).__init__(*args, **kwargs)
        self.title = u'Параметры сортировки'
        self.label_width = 150
        self.style['padding'] = '5px'
        self.field__column = ComboBoxWithStore(name='column', value_field='name', display_field='title', label=u'Столбец', anchor='100%')
        self.field__direction = ComboBoxWithStore(name='direction', display_field='title', label=u'Направление сортировки', data=constants.DIRECTION_CHOICES, anchor='100%')
        self.field__direction.store.id_property = self.field__direction.value_field
        self.items[:] = (self.field__column, self.field__direction)

class SortingTab(WindowTab):
    u"""Вкладка "Сортировка" окна редактирования шаблона отчета."""
    title = u'Сортировка'

    def init_components(self, win):
        super(SortingTab, self).init_components(win)
        self.grid__sorting = SortingGrid()
        self.panel__sorting_params = SortingParamsPanel()

    def do_layout(self, win, tab):
        super(SortingTab, self).do_layout(win, tab)
        win.tab__sorting = tab
        tab.grid__sorting = self.grid__sorting
        tab.panel__sorting_params = self.panel__sorting_params
        tab.items[:] = (self.grid__sorting, self.panel__sorting_params)
        tab.layout = 'vbox'
        tab.layout_config = {'align': 'stretch'}
        self.grid__sorting.flex = 1
        self.panel__sorting_params.flex = 0
        self.panel__sorting_params.height = 80

class EditWindow(TabbedEditWindow):
    u"""Окно добавления/редактирования шаблона отчета."""
    tabs = (ColumnsTab, FiltersTab, SortingTab)

    def _init_components(self):
        super(EditWindow, self)._init_components()
        self.tab_panel = self._tab_container
        self.field__title = _create_control_for_field(getattr(ReportTemplate, '_meta').get_field('title'), allow_blank=False, anchor='100%')
        self.field__data_source_name = make_combo_box(name='data_source_name', label=u'Источник данных', display_field='title', value_field='name', allow_blank=False, anchor='100%')
        self.field__format = _create_control_for_field(getattr(ReportTemplate, '_meta').get_field('format'), anchor='100%')
        self.field__include_available_units = _create_control_for_field(getattr(ReportTemplate, '_meta').get_field('include_available_units'), anchor='100%')
        self.panel__top = ExtContainer(layout='form', label_width=190)

    def _do_layout(self):
        super(EditWindow, self)._do_layout()
        self.panel__top.items[:] = (self.field__title, self.field__data_source_name, self.field__format, self.field__include_available_units)
        self.form.layout = 'vbox'
        self.form.layout_config = {'align': 'stretch'}
        self.panel__top.height = 115
        self.panel__top.flex = 0
        self._tab_container.flex = 1
        self.form.items.insert(0, self.panel__top)

    def set_params(self, params):
        super(EditWindow, self).set_params(params)
        self.height, self.width = (600, 1000)
        self.template_globals = local_template('edit-window.js')
        self.field__data_source_name.store = ExtDataStore(tuple(((name, data_source_param.title) for name, data_source_param in params['data_sources_params'])))
        self.field__data_source_name.store.id_property = 'name'
        self.field__data_source_name.store.reader.set_fields('title')
        self.constants = constants
        self.columns = params['columns']
        self.filters = params['filters']
        self.sorting = params['sorting']
        self.models = models
        self.read_only = params.get('read_only', False)