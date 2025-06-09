"""Implementations of the Rectangle class.
"""
from typing import Optional as Op
from typing import Union
from apysc._display import graphics
from apysc._display.child_interface import ChildInterface
from apysc._display.ellipse_height_interface import EllipseHeightInterface
from apysc._display.ellipse_width_interface import EllipseWidthInterface
from apysc._display.graphics_base import GraphicsBase
from apysc._display.height_interface import HeightInterface
from apysc._display.line_caps import LineCaps
from apysc._display.line_dash_dot_setting import LineDashDotSetting
from apysc._display.line_dash_setting import LineDashSetting
from apysc._display.line_dot_setting import LineDotSetting
from apysc._display.line_joints import LineJoints
from apysc._display.line_round_dot_setting import LineRoundDotSetting
from apysc._display.width_interface import WidthInterface
from apysc._display.x_interface import XInterface
from apysc._display.y_interface import YInterface
from apysc._html.debug_mode import add_debug_info_setting
from apysc._type.int import Int
from apysc._type.number import Number
from apysc._type.string import String
from apysc._validation import arg_validation_decos

class Rectangle(XInterface, YInterface, GraphicsBase, WidthInterface, HeightInterface, EllipseWidthInterface, EllipseHeightInterface):
    """
    The rectangle vector graphics class.

    References
    ----------
    - Rectangle class document
        - https://simon-ritchie.github.io/apysc/en/rectangle.html
    - Graphics draw_rect interface document
        - https://simon-ritchie.github.io/apysc/en/graphics_draw_rect.html

    Examples
    --------
    >>> import apysc as ap
    >>> stage: ap.Stage = ap.Stage()
    >>> sprite: ap.Sprite = ap.Sprite()
    >>> sprite.graphics.begin_fill(color='#0af')
    >>> rectangle: ap.Rectangle = sprite.graphics.draw_rect(
    ...     x=50, y=50, width=100, height=75)
    >>> rectangle.x
    Int(50)

    >>> rectangle.y
    Int(50)

    >>> rectangle.width
    Int(100)

    >>> rectangle.height
    Int(75)

    >>> rectangle.fill_color
    String('#00aaff')
    """

    @arg_validation_decos.multiple_line_settings_are_not_set(arg_position_index=0)
    @arg_validation_decos.is_integer(arg_position_index=1)
    @arg_validation_decos.is_integer(arg_position_index=2)
    @arg_validation_decos.is_integer(arg_position_index=3)
    @arg_validation_decos.num_is_gte_zero(arg_position_index=3)
    @arg_validation_decos.is_integer(arg_position_index=4)
    @arg_validation_decos.num_is_gte_zero(arg_position_index=4)
    @arg_validation_decos.is_integer(arg_position_index=5)
    @arg_validation_decos.num_is_gte_zero(arg_position_index=5)
    @arg_validation_decos.is_integer(arg_position_index=6)
    @arg_validation_decos.num_is_gte_zero(arg_position_index=6)
    @arg_validation_decos.is_hex_color_code_format(arg_position_index=7)
    @arg_validation_decos.num_is_0_to_1_range(arg_position_index=8)
    @arg_validation_decos.is_hex_color_code_format(arg_position_index=9)
    @arg_validation_decos.num_is_0_to_1_range(arg_position_index=10)
    @arg_validation_decos.is_integer(arg_position_index=11)
    @arg_validation_decos.num_is_gte_zero(arg_position_index=11)
    @arg_validation_decos.is_line_cap(arg_position_index=12, optional=True)
    @arg_validation_decos.is_line_joints(arg_position_index=13, optional=True)
    @arg_validation_decos.is_line_dot_setting(arg_position_index=14)
    @arg_validation_decos.is_line_dash_setting(arg_position_index=15)
    @arg_validation_decos.is_line_round_dot_setting(arg_position_index=16)
    @arg_validation_decos.is_line_dash_dot_setting(arg_position_index=17)
    @arg_validation_decos.is_display_object_container(arg_position_index=18, optional=True)
    @add_debug_info_setting(module_name=__name__)
    def __init__(self, *, x: Union[int, Int], y: Union[int, Int], width: Union[int, Int], height: Union[int, Int], ellipse_width: Union[int, Int]=0, ellipse_height: Union[int, Int]=0, fill_color: Union[str, String]='', fill_alpha: Union[float, Number]=1.0, line_color: Union[str, String]='', line_alpha: Union[float, Number]=1.0, line_thickness: Union[int, Int]=1, line_cap: Op[Union[String, LineCaps]]=None, line_joints: Op[Union[String, LineJoints]]=None, line_dot_setting: Op[LineDotSetting]=None, line_dash_setting: Op[LineDashSetting]=None, line_round_dot_setting: Op[LineRoundDotSetting]=None, line_dash_dot_setting: Op[LineDashDotSetting]=None, parent: Op[ChildInterface]=None) -> None:
        """
        Create a rectangle vector graphic.

        Parameters
        ----------
        x : Int or int
            X-coordinate to start drawing.
        y : Int or int
            Y-coordinate to start drawing.
        width : Int or int
            Rectangle width.
        height : Int or int
            Rectangle height.
        ellipse_width : int or Int
            Ellipse width.
        ellipse_height : int or Int
            Ellipse height.
        fill_color : str or String, default ''
            A fill-color to set.
        fill_alpha : float or Number, default 1.0
            A fill-alpha to set.
        line_color : str or String, default ''
            A line-color to set.
        line_alpha : float or Number, default 1.0
            A line-alpha to set.
        line_thickness : int or Int, default 1
            A line-thickness (line-width) to set.
        line_cap : String or LineCaps or None, default None
            A line-cap setting to set.
        line_joints : String or LineJoints or None, default None
            A line-joints setting to set.
        line_dot_setting : LineDotSetting or None, default None
            A dot setting to set.
        line_dash_setting : LineDashSetting or None, default None
            A dash setting to set.
        line_round_dot_setting : LineRoundDotSetting or None, default None
            A round-dot setting to set.
        line_dash_dot_setting : LineDashDotSetting or None, default None
            A dash dot (1-dot chain) setting to set.
        parent : ChildInterface or None, default None
            A parent instance to add this instance.
            If a specified value is None, this interface uses
            a stage instance.

        References
        ----------
        - Rectangle class document
            - https://simon-ritchie.github.io/apysc/en/rectangle.html

        Examples
        --------
        >>> import apysc as ap
        >>> stage: ap.Stage = ap.Stage()
        >>> rectangle: ap.Rectangle = ap.Rectangle(
        ...     x=50, y=50, width=100, height=100, fill_color='#00aaff')
        >>> rectangle.x
        Int(50)
        >>> rectangle.y
        Int(50)
        >>> rectangle.width
        Int(100)
        >>> rectangle.height
        Int(100)
        >>> rectangle.fill_color
        String('#00aaff')
        """
        from apysc._expression import expression_variables_util
        from apysc._expression import var_names
        variable_name: str = expression_variables_util.get_next_variable_name(type_name=var_names.RECTANGLE)
        self.variable_name = variable_name
        self._update_x_and_skip_appending_exp(x=x)
        self._update_y_and_skip_appending_exp(y=y)
        self._update_width_and_skip_appending_exp(value=width)
        self._update_height_and_skip_appending_exp(value=height)
        self._set_initial_basic_values(fill_color=fill_color, fill_alpha=fill_alpha, line_color=line_color, line_thickness=line_thickness, line_alpha=line_alpha, line_cap=line_cap, line_joints=line_joints)
        self._append_constructor_expression()
        self._set_line_setting_if_not_none_value_exists(line_dot_setting=line_dot_setting, line_dash_setting=line_dash_setting, line_round_dot_setting=line_round_dot_setting, line_dash_dot_setting=line_dash_dot_setting)
        self._set_ellipse_settings_if_values_are_not_zero(ellipse_width=ellipse_width, ellipse_height=ellipse_height)
        super(Rectangle, self).__init__(parent=parent, variable_name=variable_name)

    def _set_ellipse_settings_if_values_are_not_zero(self, *, ellipse_width: Union[int, Int], ellipse_height: Union[int, Int]) -> None:
        """
        Set ellipse-related settings if values are not zero.

        Parameters
        ----------
        ellipse_width : Union[int, Int]
            Ellipse width to set.
        ellipse_height : Union[int, Int]
            Ellipse height to set.
        """
        if isinstance(ellipse_width, int) and ellipse_width == 0:
            return
        if isinstance(ellipse_height, int) and ellipse_height == 0:
            return
        if isinstance(ellipse_width, Int) and ellipse_width._value == 0:
            return
        if isinstance(ellipse_height, Int) and ellipse_height._value == 0:
            return
        if isinstance(ellipse_width, int):
            ellipse_width = Int(ellipse_width)
        if isinstance(ellipse_height, int):
            ellipse_height = Int(ellipse_height)
        self.ellipse_width = ellipse_width
        self.ellipse_height = ellipse_height

    @classmethod
    def _create_with_graphics(cls, *, graphics: 'graphics.Graphics', x: Union[int, Int], y: Union[int, Int], width: Union[int, Int], height: Union[int, Int]) -> 'Rectangle':
        """
        Create a rectangle instance with the instance of
        specified graphics..

        Parameters
        ----------
        graphics : Graphics
            Graphics instance to link this instance.
        x : Int or int
            X-coordinate to start drawing.
        y : Int or int
            Y-coordinate to start drawing.
        width : Int or int
            Rectangle width.
        height : Int or int
            Rectangle height.

        Returns
        -------
        rectangle : Rectangle
            A created rectangle instance.
        """
        rectangle: Rectangle = Rectangle(x=x, y=y, width=width, height=height, fill_color=graphics._fill_color, fill_alpha=graphics._fill_alpha, line_color=graphics._line_color, line_alpha=graphics._line_alpha, line_thickness=graphics._line_thickness, line_cap=graphics._line_cap, line_joints=graphics._line_joints, line_dot_setting=graphics._line_dot_setting, line_dash_setting=graphics._line_dash_setting, line_round_dot_setting=graphics._line_round_dot_setting, line_dash_dot_setting=graphics._line_dash_dot_setting, parent=graphics)
        return rectangle

    def __repr__(self) -> str:
        """
        Get a string representation of this instance (for the sake of
        debugging).

        Returns
        -------
        repr_str : str
            Type name and variable name will be set
            (e.g., `Rectangle('<variable_name>')`).
        """
        repr_str: str = f"Rectangle('{self.variable_name}')"
        return repr_str

    @add_debug_info_setting(module_name=__name__)
    def _append_constructor_expression(self) -> None:
        """
        Append constructor expression.
        """
        import apysc as ap
        from apysc._display.stage import get_stage_variable_name
        variable_name: str = self.variable_name
        stage_variable_name: str = get_stage_variable_name()
        expression: str = f'var {variable_name} = {stage_variable_name}\n  .rect({self.width.variable_name}, {self.height.variable_name})\n  .attr({{'
        expression = self._append_basic_vals_expression(expression=expression, indent_num=2)
        expression += '\n  });'
        ap.append_js_expression(expression=expression)