"""Detailed document reading address: https://baidu.gitee.io/amis/zh-CN/components"""
import os
from typing import Any, Dict, List, Optional, Tuple, Union
from pydantic import Field
from typing_extensions import Literal
from .constants import BarcodeEnum, DisplayModeEnum, LevelEnum, PlacementEnum, ProgressEnum, SizeEnum, StepStatusEnum, TabsModeEnum, TriggerEnum
from .types import API, AmisNode, BaseAmisModel, Expression, OptionsNode, SchemaNode, Template, Tpl
from .utils import amis_templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Html(AmisNode):
    """Html"""
    type: str = 'html'
    html: str

class Icon(AmisNode):
    """icon"""
    type: str = 'icon'
    className: str = None
    icon: str = None
    vendor: str = None

class Remark(AmisNode):
    """mark"""
    type: str = 'remark'
    className: str = None
    content: str = None
    placement: str = None
    trigger: str = None
    icon: str = None

class Badge(AmisNode):
    """Subscript"""
    mode: str = 'dot'
    text: Union[str, int] = None
    size: int = None
    level: str = None
    overflowCount: int = None
    position: str = None
    offset: int = None
    className: str = None
    animation: bool = None
    style: dict = None
    visibleOn: Expression = None

class Page(AmisNode):
    """page"""
    __default_template_path__: str = f'{BASE_DIR}/templates/page.html'
    type: str = 'page'
    title: SchemaNode = None
    subTitle: SchemaNode = None
    remark: 'Remark' = None
    aside: SchemaNode = None
    asideResizor: bool = None
    asideMinWidth: int = None
    asideMaxWidth: int = None
    toolbar: SchemaNode = None
    body: SchemaNode = None
    className: str = None
    cssVars: dict = None
    css: str = None
    mobileCSS: str = None
    toolbarClassName: str = None
    bodyClassName: str = None
    asideClassName: str = None
    headerClassName: str = None
    initApi: API = None
    initFetch: bool = None
    initFetchOn: Expression = None
    interval: int = None
    silentPolling: bool = None
    stopAutoRefreshWhen: Expression = None
    regions: List[str] = None

    def amis_html(self, template_path: str='', locale: str='zh_CN', cdn: str='https://unpkg.com', pkg: str='amis@1.10.2', site_title: str='Amis', site_icon: str='', theme: str='cxd'):
        """Render html template"""
        template_path = template_path or self.__default_template_path__
        theme_css = f'<link href="{cdn}/{pkg}/sdk/{theme}.css" rel="stylesheet"/>' if theme != 'cxd' else ''
        return amis_templates(template_path).safe_substitute({'AmisSchemaJson': self.amis_json(), 'locale': locale.replace('_', '-'), 'cdn': cdn, 'pkg': pkg, 'site_title': site_title, 'site_icon': site_icon, 'theme': theme, 'theme_css': theme_css})

class Divider(AmisNode):
    """Dividing line"""
    type: str = 'divider'
    className: str = None
    lineStyle: str = None

class Flex(AmisNode):
    """layout"""
    type: str = 'flex'
    className: str = None
    justify: str = None
    alignItems: str = None
    style: dict = None
    items: List[SchemaNode] = None

class Grid(AmisNode):
    """Horizontal layout"""

    class Column(AmisNode):
        """Column configuration"""
        xs: int = None
        ClassName: str = None
        sm: int = None
        md: int = None
        lg: int = None
        valign: str = None
        body: List[SchemaNode] = None
    type: str = 'grid'
    className: str = None
    gap: str = None
    valign: str = None
    align: str = None
    columns: List[SchemaNode] = None

class Panel(AmisNode):
    """panel"""
    type: str = 'panel'
    className: str = None
    headerClassName: str = None
    footerClassName: str = None
    actionsClassName: str = None
    bodyClassName: str = None
    title: SchemaNode = None
    header: SchemaNode = None
    body: SchemaNode = None
    footer: SchemaNode = None
    affixFooter: bool = None
    actions: List['Action'] = None

class Tabs(AmisNode):
    """Tab"""

    class Item(AmisNode):
        title: str = None
        icon: Union[str, Icon] = None
        tab: SchemaNode = None
        hash: str = None
        reload: bool = None
        unmountOnExit: bool = None
        className: str = None
        iconPosition: str = None
        closable: bool = None
        disabled: bool = None
    type: str = 'tabs'
    className: str = None
    mode: str = None
    tabsClassName: str = None
    tabs: List[Item] = None
    source: str = None
    toolbar: SchemaNode = None
    toolbarClassName: str = None
    mountOnEnter: bool = None
    unmountOnExit: bool = None
    scrollable: bool = None
    tabsMode: TabsModeEnum = None
    addable: bool = None
    addBtnText: str = None
    closable: bool = None
    draggable: bool = None
    showTip: bool = None
    showTipClassName: str = None
    editable: bool = None
    sidePosition: str = None

class Portlet(Tabs):
    """Portal column"""

    class Item(Tabs.Item):
        toolbar: SchemaNode = None
    type: str = 'portlet'
    contentClassName: str = None
    tabs: List[Item] = None
    style: Union[str, dict] = None
    description: Template = None
    hideHeader: bool = None
    divider: bool = None

class Horizontal(AmisNode):
    left: int = None
    right: int = None
    offset: int = None

class Action(AmisNode):
    """Behavior button"""
    type: str = 'button'
    actionType: str = None
    label: str = None
    level: LevelEnum = None
    size: str = None
    icon: str = None
    iconClassName: str = None
    rightIcon: str = None
    rightIconClassName: str = None
    active: bool = None
    activeLevel: str = None
    activeClassName: str = None
    block: bool = None
    confirmText: Template = None
    reload: str = None
    tooltip: str = None
    disabledTip: str = None
    tooltipPlacement: str = None
    close: Union[bool, str] = None
    required: List[str] = None
    onClick: str = None
    componentId: str = None
    args: Union[dict, str] = None
    script: str = None

class ActionType:
    """Behavior button type"""

    class Ajax(Action):
        actionType: str = 'ajax'
        api: API = None
        redirect: Template = None
        feedback: 'Dialog' = None
        messages: dict = None

    class Dialog(Action):
        actionType: str = 'dialog'
        dialog: Union['Dialog', 'Service', SchemaNode]
        nextCondition: bool = None

    class Drawer(Action):
        actionType: str = 'drawer'
        drawer: Union['Drawer', 'Service', SchemaNode]

    class Copy(Action):
        actionType: str = 'copy'
        content: Template
        copyFormat: str = None

    class Url(Action):
        """Jump directly"""
        actionType: str = 'url'
        url: str
        blank: bool = None

    class Link(Action):
        """Single page jump"""
        actionType: str = 'link'
        link: str

    class Toast(Action):
        """Toast light"""

        class ToastItem(AmisNode):
            title: Union[str, SchemaNode] = None
            body: Union[str, SchemaNode] = None
            level: str = None
            position: str = None
            closeButton: bool = None
            showIcon: bool = None
            timeout: int = None
        actionType: str = 'toast'
        items: List[ToastItem] = None
        position: str = None
        closeButton: bool = None
        showIcon: bool = None
        timeout: int = None

class PageSchema(AmisNode):
    """Page configuration"""
    label: str = None
    icon: str = 'fa fa-flash'
    url: str = None
    schema_: Union[Page, 'Iframe'] = Field(None, alias='schema')
    schemaApi: API = None
    link: str = None
    redirect: str = None
    rewrite: str = None
    isDefaultPage: Union[str, bool] = None
    visible: str = None
    className: str = None
    children: List['PageSchema'] = None
    sort: int = None

    def as_tabs_item(self, tabs_extra: Dict[str, Any]=None, item_extra: Dict[str, Any]=None):
        if self.children:
            tab = Tabs(tabs=[item.as_tabs_item(tabs_extra, item_extra) for item in self.children]).update_from_dict(tabs_extra or {})
        elif self.schema_:
            tab = self.schema_
            if isinstance(tab, Iframe):
                tab.height = 1080
        elif self.schemaApi:
            tab = Service(schemaApi=self.schemaApi)
        elif self.link:
            tab = Page(body=Link(href=self.link, body=self.label, blank=True))
        else:
            tab = None
        return Tabs.Item(title=self.label, icon=self.icon, tab=tab).update_from_dict(item_extra or {})

class App(Page):
    """Multi-page application"""
    __default_template_path__: str = f'{BASE_DIR}/templates/app.html'
    type: str = 'app'
    api: API = None
    brandName: str = None
    logo: str = None
    className: str = None
    header: str = None
    asideBefore: str = None
    asideAfter: str = None
    footer: str = None
    pages: List[PageSchema] = None

class ButtonGroup(AmisNode):
    """Button group"""
    type: str = 'button-group'
    buttons: List[Action]
    className: str = None
    vertical: bool = None
    tiled: bool = None
    btnLevel: LevelEnum = None
    btnActiveLevel: LevelEnum = None

class Custom(AmisNode):
    """Custom Components"""
    type: str = 'custom'
    id: str = None
    name: str = None
    className: str = None
    inline: bool = False
    html: str = None
    onMount: str = None
    onUpdate: str = None
    onUnmount: str = None

class Service(AmisNode):
    """Functional container"""
    type: str = 'service'
    name: str = None
    data: dict = None
    className: str = None
    body: SchemaNode = None
    api: API = None
    ws: str = None
    dataProvider: str = None
    initFetch: bool = None
    schemaApi: API = None
    initFetchSchema: bool = None
    messages: dict = None
    interval: int = None
    silentPolling: bool = None
    stopAutoRefreshWhen: Expression = None

class Nav(AmisNode):
    """navigation"""

    class Link(AmisNode):
        label: str = None
        to: Template = None
        target: str = None
        icon: str = None
        children: List['Link'] = None
        unfolded: bool = None
        active: bool = None
        activeOn: Expression = None
        defer: bool = None
        deferApi: API = None
    type: str = 'nav'
    className: str = None
    stacked: bool = True
    source: API = None
    deferApi: API = None
    itemActions: SchemaNode = None
    draggable: bool = None
    dragOnSameLevel: bool = None
    saveOrderApi: API = None
    itemBadge: Badge = None
    links: list = None

class AnchorNav(AmisNode):
    """Anchor Navigation"""

    class Link(AmisNode):
        label: str = None
        title: str = None
        href: str = None
        body: SchemaNode = None
        className: str = None
    type: str = 'anchor-nav'
    className: str = None
    linkClassName: str = None
    sectionClassName: str = None
    links: list = None
    direction: str = None
    active: str = None

class ButtonToolbar(AmisNode):
    """Button Toolbar"""
    type: str = 'button-toolbar'
    buttons: List[Action]

class Validation(BaseAmisModel):
    isEmail: bool = None
    isUrl: bool = None
    isNumeric: bool = None
    isAlpha: bool = None
    isAlphanumeric: bool = None
    isInt: bool = None
    isFloat: bool = None
    isLength: int = None
    minLength: int = None
    maxLength: int = None
    maximum: int = None
    minimum: int = None
    equals: str = None
    equalsField: str = None
    isJson: bool = None
    isUrlPath: bool = None
    isPhoneNumber: bool = None
    isTelNumber: bool = None
    isZipcode: bool = None
    isId: bool = None
    matchRegexp: str = None

class FormItem(AmisNode):
    """Form item common"""

    class AutoFill(BaseAmisModel):
        showSuggestion: bool = None
        api: API = None
        silent: bool = None
        fillMappinng: SchemaNode = None
        trigger: str = None
        mode: str = None
        labelField: str = None
        position: str = None
        size: str = None
        columns: List['TableColumn'] = None
        filter: SchemaNode = None
    type: str = 'input-text'
    className: str = None
    inputClassName: str = None
    labelClassName: str = None
    name: str = None
    label: Template = None
    labelAlign: str = None
    value: Union[int, str] = None
    labelRemark: 'Remark' = None
    description: Template = None
    placeholder: str = None
    inline: bool = None
    submitOnChange: bool = None
    disabled: bool = None
    disabledOn: Expression = None
    visible: Expression = None
    visibleOn: Expression = None
    required: bool = None
    requiredOn: Expression = None
    validations: Union[Validation, Expression] = None
    validateApi: API = None
    copyable: Union[bool, dict] = None
    autoFill: AutoFill = None
    static: bool = None
    staticClassName: str = None
    staticLabelClassName: str = None
    staticInputClassName: str = None
    staticSchema: Union[str, list] = None

class ButtonGroupSelect(FormItem):
    """Button group select"""
    type: str = 'button-group-select'
    vertical: bool = None
    tiled: bool = None
    btnLevel: LevelEnum = LevelEnum.default
    btnActiveLevel: LevelEnum = LevelEnum.default
    options: OptionsNode = None
    source: Union[str, API] = None
    multiple: bool = None
    labelField: str = None
    valueField: str = None
    joinValues: bool = None
    extractValue: bool = None
    autoFill: dict = None

class ListSelect(FormItem):
    """List select, allows images"""
    type: str = 'list-select'
    options: OptionsNode = None
    source: Union[str, API] = None
    multiple: bool = None
    labelField: str = None
    valueField: str = None
    joinValues: bool = None
    extractValue: bool = None
    autoFill: dict = None
    listClassName: str = None

class Form(AmisNode):
    """Form"""

    class Messages(AmisNode):
        fetchSuccess: str = None
        fetchFailed: str = None
        saveSuccess: str = None
        saveFailed: str = None
    type: str = 'form'
    name: str = None
    mode: DisplayModeEnum = None
    horizontal: Horizontal = None
    title: Optional[str] = None
    submitText: Optional[str] = None
    className: str = None
    body: List[Union[FormItem, SchemaNode]] = None
    actions: List['Action'] = None
    actionsClassName: str = None
    messages: Messages = None
    wrapWithPanel: bool = None
    panelClassName: str = None
    api: API = None
    initApi: API = None
    rules: list = None
    interval: int = None
    silentPolling: bool = None
    stopAutoRefreshWhen: str = None
    initAsyncApi: API = None
    initFetch: bool = None
    initFetchOn: str = None
    initFinishedField: Optional[str] = None
    initCheckInterval: int = None
    asyncApi: API = None
    checkInterval: int = None
    finishedField: Optional[str] = None
    submitOnChange: bool = None
    submitOnInit: bool = None
    resetAfterSubmit: bool = None
    primaryField: str = None
    target: str = None
    redirect: str = None
    reload: str = None
    autoFocus: bool = None
    canAccessSuperData: bool = None
    persistData: str = None
    clearPersistDataAfterSubmit: bool = None
    preventEnterSubmit: bool = None
    trimValues: bool = None
    promptPageLeave: bool = None
    columnCount: int = None
    debug: bool = None
    inheritData: bool = None
    static: bool = None
    staticClassName: str = None

class InputSubForm(FormItem):
    """Subform"""
    type: str = 'input-sub-form'
    multiple: bool = None
    labelField: str = None
    btnLabel: str = None
    minLength: int = None
    maxLength: int = None
    draggable: bool = None
    addable: bool = None
    removable: bool = None
    addButtonClassName: str = None
    itemClassName: str = None
    itemsClassName: str = None
    form: Form = None
    addButtonText: str = None
    showErrorMsg: bool = None

class Button(FormItem):
    """Button"""
    className: str = None
    href: str = None
    size: str = None
    actionType: str = None
    level: LevelEnum = None
    tooltip: Union[str, dict] = None
    tooltipPlacement: str = None
    tooltipTrigger: str = None
    disabled: bool = None
    block: bool = None
    loading: bool = None
    loadingOn: str = None

class InputFormula(FormItem):
    """Input Formula Editor"""
    type: str = 'input-formula'
    title: str = None
    header: str = None
    evalMode: bool = None
    variables: List[dict] = None
    variableMode: Literal['tabs', 'tree', 'list'] = 'list'
    inputMode: Literal['button', 'input-button', 'input-group'] = None
    icon: str = None
    btnLabel: str = None
    level: LevelEnum = LevelEnum.default
    allowInput: bool = None
    btnSize: Literal['xs', 'sm', 'md', 'lg'] = None
    borderMode: Literal['full', 'half', 'none'] = None
    placeholder: str = None
    className: str = None
    variableClassName: str = None
    functionClassName: str = None
    mixedMode: bool = None

class InputArray(FormItem):
    """Array input box"""
    type: str = 'input-array'
    items: FormItem = None
    addable: bool = None
    removable: bool = None
    draggable: bool = None
    draggableTip: str = None
    addButtonText: str = None
    minLength: int = None
    maxLength: int = None

class Hidden(FormItem):
    """Hidden fields"""
    type: str = 'hidden'

class Checkbox(FormItem):
    """Check box"""
    type: str = 'checkbox'
    option: str = None
    trueValue: Any = None
    falseValue: Any = None

class Radios(FormItem):
    """Single box"""
    type: str = 'radios'
    options: List[Union[dict, str]] = None
    source: API = None
    labelField: bool = None
    valueField: bool = None
    columnsCount: int = None
    inline: bool = None
    selectFirst: bool = None
    autoFill: dict = None

class ChartRadios(Radios):
    """Single box"""
    type: str = 'chart-radios'
    config: dict = None
    showTooltipOnHighlight: bool = None
    chartValueField: str = None

class Checkboxes(FormItem):
    """Checkbox"""
    type: str = 'checkboxes'
    options: OptionsNode = None
    source: API = None
    delimiter: str = None
    labelField: str = None
    valueField: str = None
    joinValues: bool = None
    extractValue: bool = None
    columnsCount: int = None
    checkAll: bool = None
    inline: bool = None
    defaultCheckAll: bool = None
    creatable: bool = None
    createBtnLabel: str = None
    addControls: List[FormItem] = None
    addApi: API = None
    editable: bool = None
    editControls: List[FormItem] = None
    editApi: API = None
    removable: bool = None
    deleteApi: API = None

class InputCity(FormItem):
    """City selector"""
    type: str = 'input-city'
    allowCity: bool = None
    allowDistrict: bool = None
    searchable: bool = None
    extractValue: bool = None

class InputColor(FormItem):
    """Color picker"""
    type: str = 'input-color'
    format: str = None
    presetColors: List[str] = None
    allowCustomColor: bool = None
    clearable: bool = None
    resetValue: str = None

class Combo(FormItem):
    """combination"""
    type: str = 'combo'
    formClassName: str = None
    addButtonClassName: str = None
    items: List[FormItem] = None
    noBorder: bool = False
    scaffold: dict = {}
    multiple: bool = False
    multiLine: bool = False
    minLength: int = None
    maxLength: int = None
    flat: bool = False
    joinValues: bool = True
    delimiter: str = None
    addable: bool = False
    addButtonText: str = None
    removable: bool = False
    deleteApi: API = None
    deleteConfirmText: str = None
    draggable: bool = False
    draggableTip: str = None
    subFormMode: str = None
    placeholder: str = None
    canAccessSuperData: bool = False
    conditions: dict = None
    typeSwitchable: bool = False
    strictMode: bool = True
    syncFields: List[str] = []
    nullable: bool = False

class ConditionBuilder(FormItem):
    """Combined conditions"""

    class Field(AmisNode):
        type: str = 'text'
        label: str = None
        placeholder: str = None
        operators: List[str] = None
        defaultOp: str = None

    class Text(Field):
        """text"""

    class Number(Field):
        """number"""
        type: str = 'number'
        minimum: float = None
        maximum: float = None
        step: float = None

    class Date(Field):
        """date"""
        type: str = 'date'
        defaultValue: str = None
        format: str = None
        inputFormat: str = None

    class Datetime(Date):
        """Date Time"""
        type: str = 'datetime'
        timeFormat: str = None

    class Time(Date):
        """time"""
        type: str = 'datetime'

    class Select(Field):
        """Drop down to select"""
        type: str = 'select'
        options: OptionsNode = None
        source: API = None
        searchable: bool = None
        autoComplete: API = None
    type: str = 'condition-builder'
    fields: List[Field] = None
    className: str = None
    fieldClassName: str = None
    source: str = None

class Editor(FormItem):
    """Code Editor"""
    type: str = 'editor'
    language: str = None
    size: str = None
    allowFullscreen: bool = None
    options: dict = None

class DiffEditor(FormItem):
    """Code Editor"""
    type: str = 'diff-editor'
    language: str = None
    diffValue: Template = None

class Formula(AmisNode):
    """Formula for fields, linked by 'name'"""
    type: str = 'formula'
    name: str = None
    formula: Expression = None
    condition: Expression = None
    initSet: bool = None
    autoSet: bool = None
    id: bool = None

class DropDownButton(AmisNode):
    """Formula for fields, linked by 'name'"""
    type: str = 'dropdown-button'
    label: str = None
    className: str = None
    btnClassName: str = None
    menuClassName: str = None
    block: bool = None
    size: Literal['xs', 'sm', 'md', 'lg'] = None
    align: Literal['left', 'right'] = None
    buttons: List[Button] = []
    iconOnly: bool = None
    defaultIsOpened: bool = None
    closeOnOutside: bool = None
    closeOnClick: bool = None
    trigger: TriggerEnum = TriggerEnum.click
    hideCaret: bool = None

class EachLoop(AmisNode):
    """Each loop renderer"""
    type: str = 'each'
    value: list = []
    name: str = None
    source: str = None
    items: dict = None
    placeholder: str = None

class GridNav(AmisNode):
    """Grid navigation
    menu navigation, does not support the configuration of the initialization interface to initialize the data field,
    so you need to work with similar to Service, Form or CRUD, with the configuration of the interface to initialize
    the data field components, or manually initialize the data field, and then through the source property,
    to obtain the data in the data chain to complete the menu display.
    """

    class OptionsItem(AmisNode):
        icon: str = None
        text: str = None
        badge: Badge = None
        link: str = None
        blank: bool = None
        clickAction: Action = None
    type: str = 'grid-nav'
    className: str = None
    itemClassName: str = None
    value: List = None
    source: str = None
    square: bool = None
    center: bool = None
    border: bool = None
    gutter: int = None
    reverse: bool = None
    iconRatio: int = None
    direction: Literal['horizontal', 'vertical'] = 'vertical'
    columnNum: int = None
    options: List[OptionsItem] = None

class CollapseGroup(AmisNode):
    """Grid navigation
    menu navigation, does not support the configuration of the initialization interface to initialize the data field,
    so you need to work with similar to Service, Form or CRUD, with the configuration of the interface to initialize
    the data field components, or manually initialize the data field, and then through the source property,
    to obtain the data in the data chain to complete the menu display.
    """

    class CollapseItem(AmisNode):
        type: str = 'collapse'
        disabled: bool = None
        collapsed: bool = None
        key: Union[str, int] = None
        header: Union[str, SchemaNode] = None
        body: Union[str, SchemaNode] = None
    type: str = 'collapse-group'
    activeKey: Union[str, int, List[Union[int, str]]] = None
    disabled: bool = None
    accordion: bool = None
    expandIcon: SchemaNode = None
    expandIconPosition: Literal['left', 'right'] = 'left'
    body: List[Union[CollapseItem, SchemaNode]] = None

class Markdown(AmisNode):
    """Markdown rendering"""
    type: str = 'markdown'
    name: str = None
    value: Union[int, str] = None
    className: str = None
    src: API = None
    options: dict = None

class InputFile(FormItem):
    """File Upload"""
    type: str = 'input-file'
    receiver: API = None
    accept: str = None
    asBase64: bool = None
    asBlob: bool = None
    maxSize: int = None
    maxLength: int = None
    multiple: bool = None
    joinValues: bool = None
    extractValue: bool = None
    delimiter: str = None
    autoUpload: bool = None
    hideUploadButton: bool = None
    stateTextMap: dict = None
    fileField: str = None
    nameField: str = None
    valueField: str = None
    urlField: str = None
    btnLabel: str = None
    downloadUrl: Union[str, bool] = None
    useChunk: bool = None
    chunkSize: int = None
    startChunkApi: API = None
    chunkApi: API = None
    finishChunkApi: API = None
    autoFill: Dict[str, str] = None

class InputExcel(FormItem):
    """Parse Excel"""
    type: str = 'input-excel'
    allSheets: bool = None
    parseMode: str = None
    includeEmpty: bool = None
    plainText: bool = None

class InputTable(FormItem):
    """sheet"""
    type: str = 'input-table'
    showIndex: bool = None
    perPage: int = None
    addable: bool = None
    editable: bool = None
    removable: bool = None
    showAddBtn: bool = None
    addApi: API = None
    updateApi: API = None
    deleteApi: API = None
    addBtnLabel: str = None
    addBtnIcon: str = None
    copyBtnLabel: str = None
    copyBtnIcon: str = None
    editBtnLabel: str = None
    editBtnIcon: str = None
    deleteBtnLabel: str = None
    deleteBtnIcon: str = None
    confirmBtnLabel: str = None
    confirmBtnIcon: str = None
    cancelBtnLabel: str = None
    cancelBtnIcon: str = None
    needConfirm: bool = None
    canAccessSuperData: bool = None
    strictMode: bool = None
    columns: list = None

class InputGroup(FormItem):
    """Combination of input boxes"""
    type: str = 'input-group'
    className: str = None
    body: List[FormItem] = None

class Group(InputGroup):
    """Form item group"""
    type: str = 'group'
    mode: DisplayModeEnum = None
    gap: str = None
    direction: str = None

class InputImage(FormItem):
    """upload picture"""

    class CropInfo(BaseAmisModel):
        aspectRatio: float = None
        rotatable: bool = None
        scalable: bool = None
        viewMode: int = None

    class Limit(BaseAmisModel):
        width: int = None
        height: int = None
        minWidth: int = None
        minHeight: int = None
        maxWidth: int = None
        maxHeight: int = None
        aspectRatio: float = None
    type: str = 'input-image'
    receiver: API = None
    accept: str = None
    maxSize: int = None
    maxLength: int = None
    multiple: bool = None
    joinValues: bool = None
    extractValue: bool = None
    delimiter: str = None
    autoUpload: bool = None
    hideUploadButton: bool = None
    fileField: str = None
    crop: Union[bool, CropInfo] = None
    cropFormat: str = None
    cropQuality: int = None
    limit: Limit = None
    frameImage: str = None
    fixedSize: bool = None
    fixedSizeClassName: str = None
    autoFill: Dict[str, str] = None

class LocationPicker(FormItem):
    """Location"""
    type: str = 'location-picker'
    vendor: str = 'baidu'
    ak: str = ...
    clearable: bool = None
    placeholder: str = None
    coordinatesType: str = None

class InputNumber(FormItem):
    """Number input box"""
    type: str = 'input-number'
    min: Union[int, Template] = None
    max: Union[int, Template] = None
    step: int = None
    precision: int = None
    showSteps: bool = None
    prefix: str = None
    suffix: str = None
    kilobitSeparator: bool = None

class Picker(FormItem):
    """List selector"""
    type: str = 'picker'
    size: Union[str, SizeEnum] = None
    options: OptionsNode = None
    source: API = None
    multiple: bool = None
    delimiter: bool = None
    labelField: str = None
    valueField: str = None
    joinValues: bool = None
    extractValue: bool = None
    autoFill: dict = None
    modalMode: Literal['dialog', 'drawer'] = None
    pickerSchema: Union['CRUD', SchemaNode] = None
    embed: bool = None

class Switch(FormItem):
    """switch"""
    type: str = 'switch'
    option: str = None
    onText: str = None
    offText: str = None
    trueValue: Any = None
    falseValue: Any = None

class Static(FormItem):
    """Static display/label"""
    type: str = 'static'

    class Json(FormItem):
        type: str = 'static-json'
        value: Union[dict, str]

    class Datetime(FormItem):
        """Display date"""
        type: str = 'static-datetime'
        value: Union[int, str]

class InputText(FormItem):
    """Input box"""
    type: str = 'input-text'
    options: Union[List[str], List[dict]] = None
    source: Union[str, API] = None
    autoComplete: Union[str, API] = None
    multiple: bool = None
    delimiter: str = None
    labelField: str = None
    valueField: str = None
    joinValues: bool = None
    extractValue: bool = None
    addOn: SchemaNode = None
    trimContents: bool = None
    creatable: bool = None
    clearable: bool = None
    resetValue: str = None
    prefix: str = None
    suffix: str = None
    showCounter: bool = None
    minLength: int = None
    maxLength: int = None

class InputPassword(InputText):
    """Password input box"""
    type: str = 'input-password'

class InputRichText(FormItem):
    """Rich Text Editor"""
    type: str = 'input-rich-text'
    saveAsUbb: bool = None
    receiver: API = None
    videoReceiver: API = None
    size: str = None
    options: dict = None
    buttons: List[str] = None
    vendor: str = None

class InputRating(FormItem):
    """Input Rating"""
    type: str = 'input-rating'
    half: bool = None
    count: int = None
    readOnly: bool = None
    allowClear: bool = None
    colors: Union[str, dict] = None
    inactiveColor: str = None
    texts: dict = None
    textPosition: Literal['right', 'left'] = 'right'
    char: str = None
    charClassNme: str = None
    textClassName: str = None

class InputRange(FormItem):
    """Input Range"""
    type: str = 'input-range'
    min: int = None
    max: int = None
    step: int = None
    showSteps: bool = None
    parts: Union[int, List[int]] = None
    marks: Union[str, dict] = None
    tooltipVisible: bool = None
    tooltipPlacement: PlacementEnum = None
    multiple: bool = None
    joinValues: bool = None
    delimiter: str = None
    unit: str = None
    clearable: bool = None
    showInput: bool = None

class Timeline(AmisNode):
    """Timeline"""

    class TimelineItem(AmisNode):
        time: str
        title: Union[str, SchemaNode] = None
        detail: str = None
        detailCollapsedText: str = None
        detailExpandedText: str = None
        color: Union[str, LevelEnum] = None
        icon: str = None
    type: str = 'timeline'
    items: List[TimelineItem] = None
    source: API = None
    mode: Literal['left', 'right', 'alternate'] = 'right'
    direction: Literal['vertical', 'horizontal'] = 'vertical'
    reverse: bool = None

class Steps(AmisNode):
    """Steps Bar"""

    class StepItem(AmisNode):
        title: Union[str, SchemaNode] = None
        subTitle: Union[str, SchemaNode] = None
        description: Union[str, SchemaNode] = None
        value: str = None
        icon: str = None
        className: str = None
    type: str = 'steps'
    steps: List[StepItem] = None
    source: API = None
    name: str = None
    value: Union[str, int] = None
    status: Union[StepStatusEnum, dict] = None
    className: str = None
    mode: Literal['vertical', 'horizontal'] = 'horizontal'
    labelPlacement: Literal['vertical', 'horizontal'] = 'horizontal'
    progressDot: bool = None

class TooltipWrapper(AmisNode):
    type: str = 'tooltip-wrapper'
    className: str = None
    tooltipClassName: str = None
    style: Union[str, dict] = None
    tooltipStyle: Union[str, dict] = None
    body: SchemaNode = None
    wrapperComponent: str = None
    inline: bool = None
    rootClose: bool = None
    mouseEnterDelay: int = None
    mouseLeaveDelay: int = None
    trigger: Union[TriggerEnum, List[TriggerEnum]] = None
    disabled: bool = None
    enterable: bool = None
    showArrow: bool = None
    offset: Tuple[int, int] = None
    tooltipTheme: Literal['light', 'dark'] = 'light'
    placement: PlacementEnum = PlacementEnum.top
    content: str = None
    title: str = None

class InputTag(FormItem):
    """Input Tag"""
    type: str = 'input-tag'
    options: List[Union[str, dict]] = None
    optionsTip: List[Union[str, dict]] = None
    source: Union[str, API] = None
    delimiter: str = None
    labelField: str = None
    valueField: str = None
    joinValues: bool = None
    extractValue: bool = None
    clearable: bool = None
    resetValue: str = None
    max: int = None
    maxTagLength: int = None
    maxTagCount: int = None
    overflowTagPopover: TooltipWrapper = None
    enableBatchAdd: bool = None
    separator: str = None

class Select(FormItem):
    """Drop down box"""
    type: str = 'select'
    options: OptionsNode = None
    source: API = None
    autoComplete: API = None
    delimiter: Union[bool, str] = None
    labelField: str = None
    valueField: str = None
    joinValues: bool = None
    extractValue: bool = None
    checkAll: bool = None
    checkAllLabel: str = None
    checkAllBySearch: bool = None
    defaultCheckAll: bool = None
    creatable: bool = None
    multiple: bool = None
    searchable: bool = None
    createBtnLabel: str = None
    addControls: List[FormItem] = None
    addApi: API = None
    editable: bool = None
    editControls: List[FormItem] = None
    editApi: API = None
    removable: bool = None
    deleteApi: API = None
    autoFill: dict = None
    menuTpl: str = None
    clearable: bool = None
    hideSelected: bool = None
    mobileClassName: str = None
    selectMode: str = None
    searchResultMode: str = None
    columns: List[dict] = None
    leftOptions: List[dict] = None
    leftMode: str = None
    rightMode: str = None

class ChainedSelect(FormItem):
    """Chained Drop down boxs"""
    type: str = 'chained-select'
    options: OptionsNode = None
    source: API = None
    autoComplete: API = None
    delimiter: str = None
    labelField: str = None
    valueField: str = None
    joinValues: bool = None
    extractValue: bool = None

class NestedSelect(Select):
    """Cascade selector"""
    type: str = 'nested-select'
    cascade: bool = None
    withChildren: bool = None
    onlyChildren: bool = None
    searchPromptText: str = None
    noResultsText: str = None
    hideNodePathLabel: bool = None
    onlyLeaf: bool = None

class Breadcrumb(AmisNode):
    """Breadcrumb line"""

    class BreadcrumbItem(AmisNode):
        label: str = None
        href: str = None
        icon: str = None
        dropdown: List = None
    type: str = 'breadcrumb'
    className: str = None
    itemClassName: str = None
    separatorClassName: str = None
    dropdownClassName: str = None
    dropdownItemClassName: str = None
    separator: str = '>'
    labelMaxLength: int = None
    tooltipPosition: PlacementEnum = PlacementEnum.top
    source: Union[str, API] = None
    items: List[BreadcrumbItem] = None

class Card(AmisNode):
    """Card"""

    class Media(AmisNode):
        type: Literal['image', 'video'] = 'image'
        url: str = None
        position: PlacementEnum = PlacementEnum.left
        className: str = None
        isLive: bool = None
        autoPlay: bool = None
        poster: Union[str, bool] = None

    class Header(AmisNode):
        className: str = None
        title: str = None
        titleClassName: str = None
        subTitle: Template = None
        subTitleClassName: str = None
        subTitlePlaceholder: str = None
        description: Template = None
        descriptionClassName: str = None
        descriptionPlaceholder: str = None
        avatar: Template = None
        avatarClassName: str = None
        imageClassName: str = None
        avatarText: Template = None
        avatarTextBackground: str = None
        avatarTextClassName: str = None
        highlight: bool = None
        highlightClassName: str = None
        href: str = None
        blank: bool = None
    type: str = 'card'
    className: str = None
    href: str = None
    header: Header = None
    body: List = []
    bodyClassName: str = None
    actions: List[Action] = None
    actionsCount: int = None
    itemAction: Action = None
    media: Media = None
    secondary: Template = None
    toolbar: List[Action] = None
    dragging: bool = None
    selectable: bool = None
    checkable: bool = None
    selected: bool = None
    hideCheckToggler: bool = None
    multiple: bool = None
    useCardLabel: bool = None

class Cards(AmisNode):
    """Cards deck, allows to use data source to display data items as cards, or manual"""
    type: str = 'cards'
    title: str = None
    source: str = None
    placeholder: str = None
    className: str = None
    headerClassName: str = None
    footerClassName: str = None
    itemClassName: str = None
    card: Card = None

class ListDisplay(AmisNode):
    """Cards deck, allows to use data source to display data items as cards, or manual"""

    class ListItem(AmisNode):
        title: str = None
        titleClassName: str = None
        subTitle: Template = None
        avatar: Template = None
        avatarClassName: str = None
        desc: Template = None
        body: List = None
        actions: List[Action] = None
        actionsPosition: Literal['left', 'right'] = 'right'
    type: str = 'list'
    title: str = None
    source: str = None
    placeholder: str = None
    className: str = None
    headerClassName: str = None
    footerClassName: str = None
    listItem: ListItem = None

class Textarea(FormItem):
    """Multi-line text input box"""
    type: str = 'textarea'
    minRows: int = None
    maxRows: int = None
    trimContents: bool = None
    readOnly: bool = None
    showCounter: bool = True
    minLength: int = None
    maxLength: int = None

class InputMonth(FormItem):
    """month"""
    type: str = 'input-month'
    value: str = None
    format: str = None
    inputFormat: str = None
    placeholder: str = None
    clearable: bool = None

class InputTime(FormItem):
    """time"""
    type: str = 'input-time'
    value: str = None
    timeFormat: str = None
    format: str = None
    inputFormat: str = None
    placeholder: str = None
    clearable: bool = None
    timeConstraints: dict = None

class InputDatetime(FormItem):
    """date"""
    type: str = 'input-datetime'
    value: str = None
    format: str = None
    inputFormat: str = None
    placeholder: str = None
    shortcuts: str = None
    minDate: str = None
    maxDate: str = None
    utc: bool = None
    clearable: bool = None
    embed: bool = None
    timeConstraints: dict = None

class InputDate(FormItem):
    """date"""
    type: str = 'input-date'
    value: str = None
    format: str = None
    inputFormat: str = None
    placeholder: str = None
    shortcuts: str = None
    minDate: str = None
    maxDate: str = None
    utc: bool = None
    clearable: bool = None
    embed: bool = None
    timeConstraints: dict = None
    closeOnSelect: bool = None
    schedules: Union[list, str] = None
    scheduleClassNames: List[str] = None
    scheduleAction: SchemaNode = None
    largeMode: bool = None

class InputQuarter(InputDate):
    """InputQuarter"""
    type: str = 'input-quarter'

class InputQuarterRange(FormItem):
    """Quarter range"""
    type: str = 'input-quarter-range'
    format: str = None
    inputFormat: str = None
    placeholder: str = None
    minDate: str = None
    maxDate: str = None
    minDuration: str = None
    maxDuration: str = None
    utc: bool = None
    clearable: bool = None
    embed: bool = None
    animation: bool = None

class Calendar(FormItem):
    """Calendar"""

    class CalendarItem(AmisNode):
        startTime: str
        endTime: str
        content: Union[str, int, dict] = None
        className: str = None
    type: str = 'calendar'
    schedules: Union[List[CalendarItem], str] = None
    scheduleClassNames: List[str] = None
    scheduleAction: SchemaNode = None
    largeMode: bool = None
    todayActiveStyle: Union[str, dict] = None

class InputKV(FormItem):
    """Input key-value pair"""
    type: str = 'input-kv'
    valueType: str = None
    keyPlaceholder: str = None
    valuePlaceholder: str = None
    draggable: bool = None
    defaultValue: Union[str, int, dict] = None

class InputKVS(FormItem):
    """Input key-value pair, where value can be a deep structure"""
    type: str = 'input-kvs'
    addButtonText: str = None
    draggable: bool = None
    keyItem: Union[str, SchemaNode] = None
    valueItems: List[Union[str, SchemaNode]] = None

class InputTimeRange(FormItem):
    """time limit"""
    type: str = 'input-time-range'
    timeFormat: str = None
    format: str = None
    inputFormat: str = None
    placeholder: str = None
    clearable: bool = None
    embed: bool = None

class InputDatetimeRange(InputTimeRange):
    """Date time range"""
    type: str = 'input-datetime-range'
    ranges: Union[str, List[str]] = None
    minDate: str = None
    maxDate: str = None
    utc: bool = None

class InputDateRange(InputDatetimeRange):
    """Date Range"""
    type: str = 'input-date-range'
    minDuration: str = None
    maxDuration: str = None

class InputMonthRange(InputDateRange):
    """month range"""
    type: str = 'input-month-range'

class Transfer(FormItem):
    """Shuttle"""
    type: Literal['transfer', 'transfer-picker', 'tabs-transfer', 'tabs-transfer-picker'] = 'transfer'
    options: OptionsNode = None
    source: API = None
    delimiter: str = None
    joinValues: bool = None
    extractValue: bool = None
    searchable: bool = None
    searchApi: API = None
    statistics: bool = None
    selectTitle: str = None
    resultTitle: str = None
    sortable: bool = None
    selectMode: str = None
    searchResultMode: str = None
    columns: List[dict] = None
    leftOptions: List[dict] = None
    leftMode: str = None
    rightMode: str = None
    menuTpl: SchemaNode = None
    valueTpl: SchemaNode = None

class TransferPicker(Transfer):
    """Shuttle selector"""
    type: str = 'transfer-picker'

class TabsTransfer(Transfer):
    """Combination shuttle"""
    type: str = 'tabs-transfer'

class TabsTransferPicker(Transfer):
    """Combination shuttle selector"""
    type: str = 'tabs-transfer-picker'

class InputTree(FormItem):
    """Tree selection box"""
    type: str = 'input-tree'
    options: OptionsNode = None
    source: API = None
    autoComplete: API = None
    multiple: bool = None
    delimiter: str = None
    labelField: str = None
    valueField: str = None
    iconField: str = None
    joinValues: bool = None
    extractValue: bool = None
    creatable: bool = None
    addControls: List[FormItem] = None
    addApi: API = None
    editable: bool = None
    editControls: List[FormItem] = None
    editApi: API = None
    removable: bool = None
    deleteApi: API = None
    searchable: bool = None
    hideRoot: bool = None
    rootLabel: bool = None
    showIcon: bool = None
    showRadio: bool = None
    initiallyOpen: bool = None
    unfoldedLevel: int = None
    cascade: bool = None
    withChildren: bool = None
    onlyChildren: bool = None
    rootCreatable: bool = None
    rootCreateTip: str = None
    minLength: int = None
    maxLength: int = None
    treeContainerClassName: str = None
    enableNodePath: bool = None
    pathSeparator: str = None
    deferApi: API = None
    selectFirst: bool = None

class TreeSelect(InputTree):
    """Tree selector"""
    type: str = 'tree-select'
    hideNodePathLabel: bool = None

class Image(AmisNode):
    """picture"""
    type: str = 'image'
    className: str = None
    imageClassName: str = None
    thumbClassName: str = None
    height: int = None
    width: int = None
    title: str = None
    imageCaption: str = None
    placeholder: str = None
    defaultImage: str = None
    src: str = None
    href: Template = None
    originalSrc: str = None
    enlargeAble: bool = None
    enlargeTitle: str = None
    enlargeCaption: str = None
    thumbMode: str = None
    thumbRatio: str = None
    imageMode: str = None

class Images(AmisNode):
    """Photo album"""
    type: str = 'images'
    className: str = None
    defaultImage: str = None
    value: Union[str, List[str], List[dict]] = None
    source: str = None
    delimiter: str = None
    src: str = None
    originalSrc: str = None
    enlargeAble: bool = None
    thumbMode: str = None
    thumbRatio: str = None

class Carousel(AmisNode):
    """Carousel"""

    class Item(AmisNode):
        image: str = None
        href: str = None
        imageClassName: str = None
        title: str = None
        titleClassName: str = None
        description: str = None
        descriptionClassName: str = None
        html: str = None
    type: str = 'carousel'
    className: str = None
    options: List[Item] = None
    itemSchema: dict = None
    auto: bool = True
    interval: str = None
    duration: str = None
    width: str = None
    height: str = None
    controls: List[str] = None
    controlsTheme: str = None
    animation: str = None
    thumbMode: str = None

class Mapping(AmisNode):
    """Mapping"""
    type: str = 'mapping'
    className: str = None
    placeholder: str = None
    map: dict = None
    source: API = None

class CRUD(AmisNode):
    """Add, delete, modify, check"""

    class Messages(AmisNode):
        fetchFailed: str = None
        saveOrderFailed: str = None
        saveOrderSuccess: str = None
        quickSaveFailed: str = None
        quickSaveSuccess: str = None
    type: str = 'crud'
    mode: str = None
    title: str = None
    className: str = None
    api: API = None
    loadDataOnce: bool = None
    loadDataOnceFetchOnFilter: bool = None
    source: str = None
    filter: Union[SchemaNode, Form] = None
    filterTogglable: bool = None
    filterDefaultVisible: bool = None
    initFetch: bool = None
    interval: int = None
    silentPolling: bool = None
    stopAutoRefreshWhen: str = None
    stopAutoRefreshWhenModalIsOpen: bool = None
    syncLocation: bool = None
    draggable: bool = None
    itemDraggableOn: bool = None
    saveOrderApi: API = None
    quickSaveApi: API = None
    quickSaveItemApi: API = None
    bulkActions: List[Action] = None
    defaultChecked: bool = None
    messages: Messages = None
    primaryField: str = None
    perPage: int = None
    defaultParams: dict = None
    pageField: str = None
    perPageField: str = None
    perPageAvailable: List[int] = None
    orderField: str = None
    hideQuickSaveBtn: bool = None
    autoJumpToTopOnPagerChange: bool = None
    syncResponse2Query: bool = None
    keepItemSelectionOnPageChange: bool = None
    labelTpl: str = None
    headerToolbar: list = None
    footerToolbar: list = None
    alwaysShowPagination: bool = None
    affixHeader: bool = None
    autoGenerateFilter: bool = None
    itemAction: Action = None

class TableColumn(AmisNode):
    """Column configuration"""
    type: str = None
    label: Template = None
    name: str = None
    tpl: Template = None
    fixed: str = None
    popOver: Union[bool, dict] = None
    quickEdit: Union[bool, dict] = None
    copyable: Union[bool, dict] = None
    sortable: bool = None
    searchable: Union[bool, SchemaNode] = None
    width: Union[str, int] = None
    remark: Remark = None
    breakpoint: str = None
    filterable: Dict[str, Any] = None
    toggled: bool = None
    backgroundScale: int = None

class ColumnOperation(TableColumn):
    """Action column"""
    type: str = 'operation'
    buttons: List[Union[Action, AmisNode]] = None

class ColumnImage(Image, TableColumn):
    """Picture column"""
    pass

class ColumnImages(Images, TableColumn):
    """Picture collection column"""
    pass

class ColumnMapping(Mapping, TableColumn):
    """Map column"""
    pass

class Table(AmisNode):
    """sheet"""
    type: str = 'table'
    title: str = None
    source: str = None
    affixHeader: bool = None
    columnsTogglable: Union[str, bool] = None
    placeholder: str = None
    className: str = None
    tableClassName: str = None
    headerClassName: str = None
    footerClassName: str = None
    toolbarClassName: str = None
    columns: List[Union[TableColumn, SchemaNode]] = None
    combineNum: int = None
    itemActions: List[Action] = None
    itemCheckableOn: Expression = None
    itemDraggableOn: Expression = None
    checkOnItemClick: bool = None
    rowClassName: str = None
    rowClassNameExpr: Template = None
    prefixRow: list = None
    affixRow: list = None
    itemBadge: 'Badge' = None
    autoFillHeight: bool = None
    footable: Union[bool, dict] = None

class Chart(AmisNode):
    """Chart: https://echarts.apache.org/en/option.html#title"""
    type: str = 'chart'
    className: str = None
    body: SchemaNode = None
    api: API = None
    source: dict = None
    initFetch: bool = None
    interval: int = None
    config: Union[dict, str] = None
    style: dict = None
    width: str = None
    height: str = None
    replaceChartOption: bool = None
    trackExpression: str = None

class Code(AmisNode):
    """Code highlighting"""
    type: str = 'code'
    className: str = None
    value: str = None
    name: str = None
    language: str = None
    tabSize: int = None
    editorTheme: str = None
    wordWrap: str = None

class Json(AmisNode):
    """JSON display component"""
    type: str = 'json'
    className: str = None
    value: Union[dict, str] = None
    source: str = None
    placeholder: str = None
    levelExpand: int = None
    jsonTheme: str = None
    mutable: bool = None
    displayDataTypes: bool = None

class Link(AmisNode):
    """Link"""
    type: str = 'link'
    body: str = None
    href: str = None
    blank: bool = None
    htmlTarget: str = None
    title: str = None
    disabled: bool = None
    icon: str = None
    rightIcon: str = None

class Log(AmisNode):
    """Real-time log"""
    type: str = 'log'
    source: API = None
    height: int = None
    className: str = None
    autoScroll: bool = None
    placeholder: str = None
    encoding: str = None

class Property(AmisNode):
    """Property sheet"""

    class Item(AmisNode):
        label: Template = None
        content: Template = None
        span: int = None
        visibleOn: Expression = None
        hiddenOn: Expression = None
    type: str = 'property'
    className: str = None
    style: dict = None
    labelStyle: dict = None
    contentStyle: dict = None
    column: int = None
    mode: str = None
    separator: str = None
    source: Template = None
    title: str = None
    items: List[Item] = None

class QRCode(AmisNode):
    """QR code"""
    type: str = 'qr-code'
    value: Template
    className: str = None
    qrcodeClassName: str = None
    codeSize: int = None
    backgroundColor: str = None
    foregroundColor: str = None
    level: str = None

class Barcode(AmisNode):
    """Barcode"""

    class Options(AmisNode):
        format: BarcodeEnum = BarcodeEnum.auto
        width: int = None
        height: int = None
        displayValue: bool = None
        text: str = None
        fontOptions: str = ''
        font: str = None
        textAlign: str = None
        textPosition: str = None
        textMargin: int = None
        fontSize: int = None
        background: str = None
        lineColor: str = None
        margin: int = None
        marginTop: int = None
        marginBottom: int = None
        marginLeft: int = None
        marginRight: int = None
        flat: bool = None
    type: str = 'barcode'
    value: str = None
    className: str = None
    options: Options = None

class Color(AmisNode):
    type: Literal['color', 'static-color'] = 'color'
    value: str = None
    className: str = None
    defaultColor: str = None
    showValue: bool = None

class Progress(AmisNode):
    type: Literal['progress', 'static-progress'] = 'progress'
    mode: ProgressEnum = None
    value: Template = None
    className: str = None
    showLabel: bool = None
    stripe: bool = None
    animate: bool = None
    map: Union[str, List[str], List[Dict]] = None
    threshold: Union[Dict, List] = None
    showThresholdText: bool = None
    valueTpl: str = None
    strokeWidth: int = None
    gapDegree: int = None
    gapPosition: str = None

class PaginationWrapper(AmisNode):
    type: str = 'pagination-wrapper'
    showPageInput: bool = None
    maxButtons: int = None
    inputName: str = None
    outputName: str = None
    perPage: int = None
    position: Literal['top', 'none', 'bottom'] = 'top'
    body: SchemaNode = None

class Pagination(AmisNode):
    type: str = 'pagination'
    mode: Literal['simple', 'normal'] = 'normal'
    layout: Union[str, List[str]] = None
    maxButtons: int = None
    lastPage: int = None
    total: int = None
    activePage: int = None
    perPage: int = None
    showPerPage: bool = None
    perPageAvailable: List[int] = None
    showPageInput: bool = None
    disabled: bool = None

class MatrixCheckboxes(AmisNode):
    """Matrix type input box."""

    class RowItem(AmisNode):
        label: str

    class ColumnItem(AmisNode):
        label: str
    type: str = 'matrix-checkboxes'
    label: str = None
    columns: List[ColumnItem] = None
    rows: List[RowItem] = None
    rowLabel: str = None
    source: API = None
    multiple: bool = None
    singleSelectMode: Literal['false', 'cell', 'row', 'column'] = 'column'

class Wrapper(AmisNode):
    type: str = 'wrapper'
    className: str = None
    style: Union[str, dict] = None
    body: SchemaNode = None
    size: Union[str, SizeEnum] = None

class WebComponent(AmisNode):
    type: str = 'web-component'
    tag: str = None
    style: Union[str, dict] = None
    body: SchemaNode = None
    props: dict = None

class UUIDField(AmisNode):
    """Randomly generates an id that can be used to prevent repeated form submissions."""
    type: str = 'uuid'
    name: str = None
    length: int = None

class SearchBox(AmisNode):
    type: str = 'search-box'
    className: str = None
    mini: bool = None
    searchImediately: bool = None

class Sparkline(AmisNode):
    type: str = 'sparkline'
    width: int = None
    height: int = None
    value: List[Union[int, float]] = None
    clickAction: Action = None

class Tag(AmisNode):
    type: str = 'tag'
    className: str = None
    displayMode: Literal['normal', 'rounded', 'status'] = 'normal'
    closable: bool = None
    color: str = None
    label: str = None
    icon: str = None
    style: Union[str, dict] = None

class Video(AmisNode):
    """video"""
    type: str = 'video'
    className: str = None
    src: str = None
    isLive: bool = None
    videoType: str = None
    poster: str = None
    muted: bool = None
    autoPlay: bool = None
    rates: List[float] = None

class Alert(AmisNode):
    """hint"""
    type: str = 'alert'
    className: str = None
    level: str = None
    body: SchemaNode = None
    showCloseButton: bool = None
    closeButtonClassName: str = None
    showIcon: bool = None
    icon: str = None
    iconClassName: str = None

class Dialog(AmisNode):
    """Dialog"""
    type: str = 'dialog'
    title: SchemaNode = None
    body: SchemaNode = None
    size: Union[str, SizeEnum] = None
    bodyClassName: str = None
    closeOnEsc: bool = None
    showCloseButton: bool = None
    showErrorMsg: bool = None
    disabled: bool = None
    actions: List[Action] = None
    data: dict = None

class Drawer(AmisNode):
    """drawer"""
    type: str = 'drawer'
    title: SchemaNode = None
    body: SchemaNode = None
    size: Union[str, SizeEnum] = None
    position: str = None
    bodyClassName: str = None
    closeOnEsc: bool = None
    closeOnOutside: bool = None
    overlay: bool = None
    resizable: bool = None
    actions: List[Action] = None
    data: dict = None

class Iframe(AmisNode):
    """Iframe"""
    type: str = 'iframe'
    className: str = None
    frameBorder: list = None
    style: dict = None
    src: str = None
    allow: str = None
    sandbox: str = None
    referrerpolicy: str = None
    height: Union[int, str] = None
    width: Union[int, str] = None

class Spinner(AmisNode):
    """Loading"""
    type: str = 'spinner'

class TableCRUD(CRUD, Table):
    """Form Table CRUD"""
    mode = 'table'

class CardCRUD(CRUD, Cards):
    """Form Card CRUD"""
    mode = 'cards'

class ListCRUD(CRUD, ListDisplay):
    """Form Card CRUD"""
    mode = 'list'

class Avatar(AmisNode):
    """avatar"""
    type: str = 'avatar'
    className: str = None
    fit: str = None
    src: str = None
    text: str = None
    icon: str = None
    shape: str = None
    size: int = None
    style: dict = None

class Audio(AmisNode):
    """Audio"""
    type: str = 'audio'
    className: str = None
    inline: bool = None
    src: str = None
    loop: bool = None
    autoPlay: bool = None
    rates: List[float] = None
    controls: List[str] = None

class Status(AmisNode):
    """state"""
    type: str = 'status'
    className: str = None
    placeholder: str = None
    map: dict = None
    labelMap: dict = None

class Tasks(AmisNode):
    """Task operation collection"""

    class Item(AmisNode):
        label: str = None
        key: str = None
        remark: str = None
        status: str = None
    type: str = 'tasks'
    className: str = None
    tableClassName: str = None
    items: List[Item] = None
    checkApi: API = None
    submitApi: API = None
    reSubmitApi: API = None
    interval: int = None
    taskNameLabel: str = None
    operationLabel: str = None
    statusLabel: str = None
    remarkLabel: str = None
    btnText: str = None
    retryBtnText: str = None
    btnClassName: str = None
    retryBtnClassName: str = None
    statusLabelMap: List[str] = None
    statusTextMap: List[str] = None

class Wizard(AmisNode):
    """Wizard"""

    class Step(AmisNode):
        title: str = None
        mode: str = None
        horizontal: Horizontal = None
        api: API = None
        initApi: API = None
        initFetch: bool = None
        initFetchOn: Expression = None
        body: List[FormItem] = None
    type: str = 'wizard'
    mode: str = None
    api: API = None
    initApi: API = None
    initFetch: API = None
    initFetchOn: Expression = None
    actionPrevLabel: str = None
    actionNextLabel: str = None
    actionNextSaveLabel: str = None
    actionFinishLabel: str = None
    className: str = None
    actionClassName: str = None
    reload: str = None
    redirect: Template = None
    target: str = None
    steps: List[Step] = None
    startStep: int = None
PageSchema.update_forward_refs()
ActionType.Dialog.update_forward_refs()
ActionType.Drawer.update_forward_refs()
TableCRUD.update_forward_refs()
Form.update_forward_refs()
Tpl.update_forward_refs()
InputText.update_forward_refs()
InputNumber.update_forward_refs()
Picker.update_forward_refs()