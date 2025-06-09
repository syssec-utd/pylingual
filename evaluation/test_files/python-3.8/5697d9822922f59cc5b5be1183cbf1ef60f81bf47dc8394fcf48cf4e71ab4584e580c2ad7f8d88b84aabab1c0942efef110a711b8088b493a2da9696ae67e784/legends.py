"""

"""
from __future__ import annotations
import logging
log = logging.getLogger(__name__)
from ...core.enums import AlternationPolicy, Anchor, LegendClickPolicy, LegendLocation, Location, Orientation
from ...core.has_props import abstract
from ...core.properties import Auto, Bool, Dict, Either, Enum, Float, Include, Instance, InstanceDefault, Int, List, Nullable, NullStringSpec, Override, Positive, Seq, String, TextLike, Tuple, value
from ...core.property.vectorization import Field
from ...core.property_mixins import ScalarFillProps, ScalarLineProps, ScalarTextProps
from ...core.validation import error
from ...core.validation.errors import BAD_COLUMN_NAME, NON_MATCHING_DATA_SOURCES_ON_LEGEND_ITEM_RENDERERS
from ...model import Model
from ..formatters import TickFormatter
from ..labeling import LabelingPolicy, NoOverlap
from ..mappers import ColorMapper
from ..renderers import GlyphRenderer
from ..tickers import Ticker
from .annotation import Annotation
__all__ = ('ColorBar', 'ContourColorBar', 'Legend', 'LegendItem')

@abstract
class BaseColorBar(Annotation):
    """ Abstract base class for color bars.

    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    location = Either(Enum(Anchor), Tuple(Float, Float), default='top_right', help="\n    The location where the color bar should draw itself. It's either one of\n    ``bokeh.core.enums.Anchor``'s enumerated values, or a ``(x, y)``\n    tuple indicating an absolute location absolute location in screen\n    coordinates (pixels from the bottom-left corner).\n\n    .. warning::\n        If the color bar is placed in a side panel, the location will likely\n        have to be set to `(0,0)`.\n    ")
    orientation = Either(Enum(Orientation), Auto, default='auto', help='\n    Whether the color bar should be oriented vertically or horizontally.\n    ')
    height = Either(Auto, Int, help='\n    The height (in pixels) that the color scale should occupy.\n    ')
    width = Either(Auto, Int, help='\n    The width (in pixels) that the color scale should occupy.\n    ')
    scale_alpha = Float(1.0, help='\n    The alpha with which to render the color scale.\n    ')
    title = Nullable(String, help='\n    The title text to render.\n    ')
    title_props = Include(ScalarTextProps, prefix='title', help='\n    The {prop} values for the title text.\n    ')
    title_text_font_size = Override(default='13px')
    title_text_font_style = Override(default='italic')
    title_standoff = Int(2, help='\n    The distance (in pixels) to separate the title from the color bar.\n    ')
    ticker = Either(Instance(Ticker), Auto, default='auto', help='\n    A Ticker to use for computing locations of axis components.\n    ')
    formatter = Either(Instance(TickFormatter), Auto, default='auto', help='\n    A ``TickFormatter`` to use for formatting the visual appearance of ticks.\n    ')
    major_label_overrides = Dict(Either(Float, String), TextLike, default={}, help='\n    Provide explicit tick label values for specific tick locations that\n    override normal formatting.\n    ')
    major_label_policy = Instance(LabelingPolicy, default=InstanceDefault(NoOverlap), help='\n    Allows to filter out labels, e.g. declutter labels to avoid overlap.\n    ')
    margin = Int(30, help='\n    Amount of margin (in pixels) around the outside of the color bar.\n    ')
    padding = Int(10, help='\n    Amount of padding (in pixels) between the color scale and color bar border.\n    ')
    major_label_props = Include(ScalarTextProps, prefix='major_label', help='\n    The {prop} of the major tick labels.\n    ')
    major_label_text_font_size = Override(default='11px')
    label_standoff = Int(5, help='\n    The distance (in pixels) to separate the tick labels from the color bar.\n    ')
    major_tick_props = Include(ScalarLineProps, prefix='major_tick', help='\n    The {prop} of the major ticks.\n    ')
    major_tick_line_color = Override(default='#ffffff')
    major_tick_in = Int(default=5, help='\n    The distance (in pixels) that major ticks should extend into the\n    main plot area.\n    ')
    major_tick_out = Int(default=0, help='\n    The distance (in pixels) that major ticks should extend out of the\n    main plot area.\n    ')
    minor_tick_props = Include(ScalarLineProps, prefix='minor_tick', help='\n    The {prop} of the minor ticks.\n    ')
    minor_tick_line_color = Override(default=None)
    minor_tick_in = Int(default=0, help='\n    The distance (in pixels) that minor ticks should extend into the\n    main plot area.\n    ')
    minor_tick_out = Int(default=0, help='\n    The distance (in pixels) that major ticks should extend out of the\n    main plot area.\n    ')
    bar_props = Include(ScalarLineProps, prefix='bar', help='\n    The {prop} for the color scale bar outline.\n    ')
    bar_line_color = Override(default=None)
    border_props = Include(ScalarLineProps, prefix='border', help='\n    The {prop} for the color bar border outline.\n    ')
    border_line_color = Override(default=None)
    background_props = Include(ScalarFillProps, prefix='background', help='\n    The {prop} for the color bar background style.\n    ')
    background_fill_color = Override(default='#ffffff')
    background_fill_alpha = Override(default=0.95)

class ColorBar(BaseColorBar):
    """ Render a color bar based on a color mapper.

    See :ref:`ug_basic_annotations_color_bars` for information on plotting color bars.

    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    color_mapper = Instance(ColorMapper, help="\n    A color mapper containing a color palette to render.\n\n    .. warning::\n        If the `low` and `high` attributes of the ``ColorMapper`` aren't set, ticks\n        and tick labels won't be rendered. Additionally, if a ``LogTicker`` is\n        passed to the `ticker` argument and either or both of the logarithms\n        of `low` and `high` values of the color_mapper are non-numeric\n        (i.e. `low=0`), the tick and tick labels won't be rendered.\n    ")
    display_low = Nullable(Float, help='\n    The lowest value to display in the color bar. The whole of the color entry\n    containing this value is shown.\n    ')
    display_high = Nullable(Float, help='\n    The highest value to display in the color bar. The whole of the color entry\n    containing this value is shown.\n    ')

class ContourColorBar(BaseColorBar):
    """ Color bar used for contours.

    Supports displaying hatch patterns and line styles that contour plots may
    have as well as the usual fill styles.

    Do not create these objects manually, instead use ``ContourRenderer.color_bar``.

    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    fill_renderer = Instance(GlyphRenderer, help='\n    Glyph renderer used for filled contour polygons.\n    ')
    line_renderer = Instance(GlyphRenderer, help='\n    Glyph renderer used for contour lines.\n    ')
    levels = Seq(Float, default=[], help='\n    Levels at which the contours are calculated.\n    ')

class LegendItem(Model):
    """

    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if isinstance(self.label, str):
            self.label = value(self.label)
    label = NullStringSpec(help="\n    A label for this legend. Can be a string, or a column of a\n    ColumnDataSource. If ``label`` is a field, then it must\n    be in the renderers' data_source.\n    ")
    renderers = List(Instance(GlyphRenderer), help='\n    A list of the glyph renderers to draw in the legend. If ``label`` is a field,\n    then all data_sources of renderers must be the same.\n    ')
    index = Nullable(Int, help='\n    The column data index to use for drawing the representative items.\n\n    If None (the default), then Bokeh will automatically choose an index to\n    use. If the label does not refer to a data column name, this is typically\n    the first data point in the data source. Otherwise, if the label does\n    refer to a column name, the legend will have "groupby" behavior, and will\n    choose and display representative points from every "group" in the column.\n\n    If set to a number, Bokeh will use that number as the index in all cases.\n    ')
    visible = Bool(default=True, help='\n    Whether the legend item should be displayed. See\n    :ref:`ug_basic_annotations_legends_item_visibility` in the user guide.\n    ')

    @error(NON_MATCHING_DATA_SOURCES_ON_LEGEND_ITEM_RENDERERS)
    def _check_data_sources_on_renderers(self):
        if isinstance(self.label, Field):
            if len({r.data_source for r in self.renderers}) != 1:
                return str(self)

    @error(BAD_COLUMN_NAME)
    def _check_field_label_on_data_source(self):
        if isinstance(self.label, Field):
            if len(self.renderers) < 1:
                return str(self)
            source = self.renderers[0].data_source
            if self.label.field not in source.column_names:
                return str(self)

class Legend(Annotation):
    """ Render informational legends for a plot.

    See :ref:`ug_basic_annotations_legends` for information on plotting legends.

    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
    location = Either(Enum(LegendLocation), Tuple(Float, Float), default='top_right', help="\n    The location where the legend should draw itself. It's either one of\n    ``bokeh.core.enums.LegendLocation``'s enumerated values, or a ``(x, y)``\n    tuple indicating an absolute location absolute location in screen\n    coordinates (pixels from the bottom-left corner).\n    ")
    orientation = Enum(Orientation, default='vertical', help='\n    Whether the legend entries should be placed vertically or horizontally\n    when they are drawn.\n    ')
    ncols = Either(Positive(Int), Auto, default='auto', help="\n    The number of columns in the legend's layout. By default it's either\n    one column if the orientation is vertical or the number of items in\n    the legend otherwise. ``ncols`` takes precendence over ``nrows`` for\n    horizonal orientation.\n    ")
    nrows = Either(Positive(Int), Auto, default='auto', help="\n    The number of rows in the legend's layout. By default it's either\n    one row if the orientation is horizonal or the number of items in\n    the legend otherwise. ``nrows`` takes precendence over ``ncols``\n    for vertical orientation.\n    ")
    title = Nullable(String, help='\n    The title text to render.\n    ')
    title_props = Include(ScalarTextProps, prefix='title', help='\n    The {prop} values for the title text.\n    ')
    title_text_font_size = Override(default='13px')
    title_text_font_style = Override(default='italic')
    title_location = Enum(Location, default='above', help='\n    Specifies on which side of the legend the title will be located.\n    Titles on the left or right side will be rotated accordingly.\n    ')
    title_standoff = Int(5, help='\n    The distance (in pixels) to separate the title from the legend.\n    ')
    border_props = Include(ScalarLineProps, prefix='border', help='\n    The {prop} for the legend border outline.\n    ')
    border_line_color = Override(default='#e5e5e5')
    border_line_alpha = Override(default=0.5)
    background_props = Include(ScalarFillProps, prefix='background', help='\n    The {prop} for the legend background style.\n    ')
    item_background_props = Include(ScalarFillProps, prefix='item_background', help="\n    The {prop} for the legend items' background style.\n    ")
    inactive_props = Include(ScalarFillProps, prefix='inactive', help='\n    The {prop} for the legend item style when inactive. These control an overlay\n    on the item that can be used to obscure it when the corresponding glyph\n    is inactive (e.g. by making it semi-transparent).\n    ')
    click_policy = Enum(LegendClickPolicy, default='none', help="\n    Defines what happens when a lengend's item is clicked.\n    ")
    item_background_policy = Enum(AlternationPolicy, default='none', help='\n    Defines which items to style, if ``item_background_fill`` is configured.\n    ')
    background_fill_color = Override(default='#ffffff')
    background_fill_alpha = Override(default=0.95)
    item_background_fill_color = Override(default='#f1f1f1')
    item_background_fill_alpha = Override(default=0.8)
    inactive_fill_color = Override(default='white')
    inactive_fill_alpha = Override(default=0.7)
    label_props = Include(ScalarTextProps, prefix='label', help='\n    The {prop} for the legend labels.\n    ')
    label_text_baseline = Override(default='middle')
    label_text_font_size = Override(default='13px')
    label_standoff = Int(5, help='\n    The distance (in pixels) to separate the label from its associated glyph.\n    ')
    label_height = Int(20, help='\n    The minimum height (in pixels) of the area that legend labels should occupy.\n    ')
    label_width = Int(20, help='\n    The minimum width (in pixels) of the area that legend labels should occupy.\n    ')
    glyph_height = Int(20, help='\n    The height (in pixels) that the rendered legend glyph should occupy.\n    ')
    glyph_width = Int(20, help='\n    The width (in pixels) that the rendered legend glyph should occupy.\n    ')
    margin = Int(10, help='\n    Amount of margin around the legend.\n    ')
    padding = Int(10, help='\n    Amount of padding around the contents of the legend. Only applicable when\n    border is visible, otherwise collapses to 0.\n    ')
    spacing = Int(3, help='\n    Amount of spacing (in pixels) between legend entries.\n    ')
    items = List(Instance(LegendItem), help='\n    A list of :class:`~bokeh.model.annotations.LegendItem` instances to be\n    rendered in the legend.\n\n    This can be specified explicitly, for instance:\n\n    .. code-block:: python\n\n        legend = Legend(items=[\n            LegendItem(label="sin(x)",   renderers=[r0, r1]),\n            LegendItem(label="2*sin(x)", renderers=[r2]),\n            LegendItem(label="3*sin(x)", renderers=[r3, r4])\n        ])\n\n    But as a convenience, can also be given more compactly as a list of tuples:\n\n    .. code-block:: python\n\n        legend = Legend(items=[\n            ("sin(x)",   [r0, r1]),\n            ("2*sin(x)", [r2]),\n            ("3*sin(x)", [r3, r4])\n        ])\n\n    where each tuple is of the form: *(label, renderers)*.\n\n    ').accepts(List(Tuple(String, List(Instance(GlyphRenderer)))), lambda items: [LegendItem(label=item[0], renderers=item[1]) for item in items])