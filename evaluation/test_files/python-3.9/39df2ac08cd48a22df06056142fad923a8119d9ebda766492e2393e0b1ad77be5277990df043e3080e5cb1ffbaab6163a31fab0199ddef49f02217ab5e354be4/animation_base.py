"""Base class implementation for the animation.
"""
from abc import ABC
from abc import abstractmethod
from typing import Callable
from typing import Generic
from typing import Optional
from typing import TypeVar
from typing import Union
from typing_extensions import final
from apysc._animation.easing import Easing
from apysc._event import animation_event
from apysc._event.custom_event_interface import CustomEventInterface
from apysc._html.debug_mode import add_debug_info_setting
from apysc._type.boolean import Boolean
from apysc._type.int import Int
from apysc._type.variable_name_interface import VariableNameInterface
from apysc._validation import arg_validation_decos
_T = TypeVar('_T', bound=VariableNameInterface)
_O = TypeVar('_O')
_Handler = Callable[['animation_event.AnimationEvent', _O], None]

class AnimationBase(VariableNameInterface, CustomEventInterface, Generic[_T], ABC):
    _target: _T
    _duration: Int
    _delay: Int
    _easing: Easing
    _started: Boolean

    @arg_validation_decos.not_empty_string(arg_position_index=1)
    @add_debug_info_setting(module_name=__name__)
    def __init__(self, *, variable_name: str) -> None:
        """
        Base class for each animation setting.

        Parameters
        ----------
        variable_name : str
            Variable name.
        """
        self.variable_name = variable_name
        self._started = Boolean(False)

    @abstractmethod
    def _get_animation_func_expression(self) -> str:
        """
        Get an animation function expression.
        """

    @final
    @add_debug_info_setting(module_name=__name__)
    def _set_basic_animation_settings(self, *, target: _T, duration: Union[int, Int]=3000, delay: Union[int, Int]=0, easing: Easing=Easing.LINEAR) -> None:
        """
        Set the basic animation settings.

        Parameters
        ----------
        target : VariableNameInterface
            A target instance of the animation target
            (e.g., `DisplayObject` instance).
        duration : int or Int, default 3000
            Milliseconds before an animation ends.
        delay : int or Int, default 0
            Milliseconds before an animation starts.
        easing : Easing, default Easing.LINEAR
            Easing setting. If None, Linear calculation is used.
        """
        from apysc._converter import to_apysc_val_from_builtin
        self._target = target
        self._duration = to_apysc_val_from_builtin.get_copied_int_from_builtin_val(integer=duration)
        self._delay = to_apysc_val_from_builtin.get_copied_int_from_builtin_val(integer=delay)
        self._easing = easing

    @final
    def _get_animation_basic_expression(self) -> str:
        """
        Get an animation basic expression string.

        Returns
        -------
        expression : str
            An animation basic expression string.
        """
        expression: str = f'{self._target.variable_name}\n  .animate({{\n    duration: {self._duration.variable_name},\n    delay: {self._delay.variable_name}}})\n  .ease({self._easing.value})'
        expression += self._get_animation_complete_handler_expression()
        return expression

    @final
    @add_debug_info_setting(module_name=__name__)
    def start(self) -> 'AnimationBase':
        """
        Start an animation with current settings.

        Returns
        -------
        self : AnimatonBase
            This instance.

        References
        ----------
        - AnimationBase class start interface
            - https://simon-ritchie.github.io/apysc/en/animation_base_start.html  # noqa

        Examples
        --------
        >>> import apysc as ap
        >>> stage: ap.Stage = ap.Stage()
        >>> sprite: ap.Sprite = ap.Sprite()
        >>> sprite.graphics.begin_fill(color="#0af")
        >>> rectangle: ap.Rectangle = sprite.graphics.draw_rect(
        ...     x=50, y=50, width=50, height=50
        ... )
        >>> _ = rectangle.animation_x(x=100).start()
        """
        import apysc as ap
        expression: str = self._get_animation_basic_expression()
        animation_expresssion: str = self._get_animation_func_expression()
        expression += animation_expresssion
        ap.append_js_expression(expression=expression)
        self._started.value = True
        return self

    @final
    def _get_animation_complete_handler_expression(self) -> str:
        """
        Get an expression of the animation complete handlers setting.

        Returns
        -------
        expression : str
            Target expression string.
            e.g., '
  .after(handler_name)'

        Notes
        -----
        If multiple handlers are registered, then this method
        returns multiple lines expression.
        """
        from apysc._event.custom_event_type import CustomEventType
        event_type: str = CustomEventType.ANIMATION_COMPLETE.value
        self._initialize_custom_event_handlers_if_not_initialized(custom_event_type_str=event_type)
        if event_type not in self._custom_event_handlers:
            return ''
        expression: str = ''
        for handler_name in self._custom_event_handlers[event_type].keys():
            expression += f'\n  .after({handler_name})'
        return expression

    @final
    @arg_validation_decos.handler_args_num(arg_position_index=1)
    @arg_validation_decos.handler_options_type(arg_position_index=2)
    @add_debug_info_setting(module_name=__name__)
    def animation_complete(self, handler: _Handler[_O], *, options: Optional[_O]=None) -> 'AnimationBase':
        """
        Add an animation complete event listener setting.

        Notes
        -----
        This interface can only use before an animation starts

        Parameters
        ----------
        handler : _Handler
            A callable that an instance calls when an animation
            is complete.
        options : dict or None, default None
            Optional arguments dictionary to be passed to a handler.

        Returns
        -------
        self : AnimatonBase
            This instance.

        Raises
        ------
        Exception
            If calling this interface after an animation starts

        References
        ----------
        - AnimationBase class animation_complete interface document
            - https://simon-ritchie.github.io/apysc/en/animation_complete.html
        - About the handler options' type document
            - https://simon-ritchie.github.io/apysc/en/about_handler_options_type.html  # noqa

        Examples
        --------
        >>> import apysc as ap
        >>> def on_animation_complete(
        ...     e: ap.AnimationEvent[ap.Rectangle], options: dict
        ... ) -> None:
        ...     ap.trace("Animation completed!")
        >>> stage: ap.Stage = ap.Stage()
        >>> sprite: ap.Sprite = ap.Sprite()
        >>> sprite.graphics.begin_fill(color="#0af")
        >>> rectangle: ap.Rectangle = sprite.graphics.draw_rect(
        ...     x=50, y=50, width=50, height=50
        ... )
        >>> _ = (
        ...     rectangle.animation_x(
        ...         x=100,
        ...     )
        ...     .animation_complete(on_animation_complete)
        ...     .start()
        ... )
        """
        import apysc as ap
        from apysc._event.custom_event_type import CustomEventType
        self._validate_animation_not_started()
        e: ap.AnimationEvent[_T] = ap.AnimationEvent(this=self)
        in_handler_head_expression: str = self._get_complete_event_in_handler_head_expression()
        self.bind_custom_event(custom_event_type=CustomEventType.ANIMATION_COMPLETE, handler=handler, e=e, options=options, in_handler_head_expression=in_handler_head_expression)
        return self

    @abstractmethod
    def _get_complete_event_in_handler_head_expression(self) -> str:
        """
        Get an expression to be inserted into the complete event
        handler's head.
        """

    @final
    def _validate_animation_not_started(self) -> None:
        """
        Validate whether an animation has not already started.

        Raises
        ------
        Exception
            If an animation has already started.
        """
        if not self._started._value:
            return
        raise Exception('This interface can not be called after the animation is started.')

    @property
    def target(self) -> _T:
        """
        Get an animation target instance.

        Returns
        -------
        target : VariableNameInterface
            An animation target instance.

        References
        ----------
        - AnimationBase class target property interface document
            - https://simon-ritchie.github.io/apysc/en/animation_base_target.html  # noqa

        Examples
        --------
        >>> import apysc as ap
        >>> def on_animation_complete(
        ...     e: ap.AnimationEvent[ap.Rectangle], options: dict
        ... ) -> None:
        ...     rectangle: ap.Rectangle = e.this.target
        >>> stage: ap.Stage = ap.Stage()
        >>> sprite: ap.Sprite = ap.Sprite()
        >>> sprite.graphics.begin_fill(color="#0af")
        >>> rectangle: ap.Rectangle = sprite.graphics.draw_rect(
        ...     x=50, y=50, width=50, height=50
        ... )
        >>> _ = (
        ...     rectangle.animation_x(
        ...         x=100,
        ...     )
        ...     .animation_complete(on_animation_complete)
        ...     .start()
        ... )
        """
        return self._target