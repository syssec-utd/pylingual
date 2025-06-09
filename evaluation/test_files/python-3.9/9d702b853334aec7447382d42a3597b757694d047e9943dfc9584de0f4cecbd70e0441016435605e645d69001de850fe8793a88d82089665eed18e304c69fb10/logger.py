from __future__ import annotations
import typing as t
from inspect import currentframe
from time import sleep
from ._print import debug
from .console import con_print
from .pipeline import pipeline
__all__ = ['LKLogger', 'lk']

class T:
    from types import FrameType as _FrameType
    from .markup import T as _TMarkup
    Frame = _FrameType
    Args = t.Tuple[t.Any, ...]
    MarkupPos = int
    Markup = str
    Marks = _TMarkup.Marks
    MarksMeaning = _TMarkup.MarksMeaning
    Info = t.TypedDict('Info', {'file_path': str, 'line_number': str, 'is_external_lib': bool, 'function_name': str, 'variable_names': t.Iterable[str]})
    FlushScheme = int
    ComposedMessage = t.Tuple[str, FlushScheme]

class LKLogger:

    def __init__(self):
        from atexit import register
        from collections import deque
        from threading import Thread
        from .cache import LoggingCache
        from .config import LoggingConfig
        from .markup import MarkupAnalyser
        from .message_builder import MessageBuilder
        self._analyser = MarkupAnalyser()
        self._builder = MessageBuilder()
        self._cache = LoggingCache()
        self._config = LoggingConfig()
        self._running = False
        self._message_queue = deque()
        register(self._stop_running)
        self._thread = Thread(target=self._start_running)
        self._thread.daemon = True
        self._thread.start()

    def configure(self, clear_preset=False, **kwargs) -> None:
        self._cache.clear_cache()
        if clear_preset:
            self._config.reset()
        if 'show_varname' in kwargs:
            kwargs['show_varnames'] = kwargs.pop('show_varname')
        self._config.update(**kwargs)
        self._builder.update_config(separator=self._config.separator, show_source=self._config.show_source, show_funcname=self._config.show_funcname, show_varnames=self._config.show_varnames)

    @property
    def config(self) -> dict:
        return self._config.to_dict()

    def _start_running(self):
        self._running = True
        while self._running or self._message_queue:
            if self._message_queue:
                try:
                    (msg, kwargs, custom_print) = self._message_queue.popleft()
                    if custom_print:
                        custom_print(*msg, **kwargs)
                    else:
                        con_print(msg, **kwargs)
                except Exception as e:
                    debug(e)
            else:
                sleep(0.01)

    def _stop_running(self):
        self._running = False
        if self._config.clear_unfinished_stream:
            self._message_queue.clear()
        self._thread.join()

    def log(self, *args, **kwargs) -> None:
        caller_frame = currentframe().f_back
        if (path := caller_frame.f_globals.get('__file__')) and (custom_print := pipeline.get(path)):
            if self._config.async_:
                self._message_queue.append((args, kwargs, custom_print))
            else:
                custom_print(*args, **kwargs)
            return
        (msg, flush_scheme) = self._build_message(caller_frame, *args)
        if flush_scheme == 0:
            if self._config.async_:
                self._message_queue.append((msg, kwargs, None))
            else:
                con_print(msg, **kwargs)
        elif flush_scheme == 1:
            con_print(msg, **kwargs)
        elif flush_scheme == 2:
            if (skipped_count := len(self._message_queue)):
                self._message_queue.clear()
                print(':frp', f'[red dim](... skipped {skipped_count} messages)[/]')
            con_print(msg, **kwargs)
        elif flush_scheme == 3:
            while self._message_queue:
                sleep(0.01)
            con_print(msg, **kwargs)

    def fmt(self, *args, **_) -> str:
        return str(self._build_message(currentframe().f_back, *args)[0])

    def _build_message(self, frame: T.Frame, *args) -> T.ComposedMessage:
        """
        return: (str message, bool is_flush, bool is_drain)
            flush: print the message immediately.
            drain: drain the message queue.
                if drain is True, the flush must be True.
        """
        from .markup import MarkMeaning
        frame_id = f'{id(frame)}#{frame.f_lineno}'
        (args, markup_pos, markup) = self._extract_markup_from_arguments(frame_id, args)
        marks = self._analyser.extract(markup)
        marks_meaning = self._analyser.analyse(marks)
        flush_scheme: T.FlushScheme = 0
        if MarkMeaning.FLUSH in marks_meaning:
            flush_scheme = 1
        elif MarkMeaning.FLUSH_AND_DRAIN in marks_meaning:
            flush_scheme = 2
        elif MarkMeaning.WAIT_TO_FLUSH in marks_meaning:
            flush_scheme = 3
        if self._cache.is_cached(frame_id, markup):
            cached_info = self._cache.get_cache(frame_id, markup)
            return (self._builder.compose(args, marks_meaning, cached_info), flush_scheme)
        if MarkMeaning.AGRESSIVE_PRUNE in marks_meaning:
            return (self._builder.quick_compose(args), flush_scheme)
        elif MarkMeaning.RICH_OBJECT in marks_meaning:
            return (args[0] if args else None, flush_scheme)
        info: T.Info = {'file_path': '', 'line_number': '0', 'is_external_lib': False, 'function_name': '', 'variable_names': ()}
        show_source = self._config.show_source
        show_funcname = self._config.show_funcname
        show_varnames = self._config.show_varnames and MarkMeaning.MODERATE_PRUNE not in marks_meaning
        if any((show_source, show_funcname, show_varnames)):
            from .sourcemap import sourcemap
            srcmap = sourcemap.get_sourcemap(frame=frame, traceback_level=marks['p'], advanced=show_varnames)
            if show_source:

                def update_sourcemap():
                    """
                    this function updates follows:
                        info['is_external_lib']
                        info['file_path']
                        info['line_number']
                    """
                    from .path_helper import path_helper
                    path = srcmap.filepath
                    info['is_external_lib'] = path_helper.is_external_lib(path)
                    if info['is_external_lib']:
                        if self._config.show_external_lib:
                            style = self._config.path_style_for_external_lib
                            info['file_path'] = path_helper.reformat_external_lib_path(path, style)
                        else:
                            info['file_path'] = ''
                    else:
                        info['file_path'] = path_helper.relpath(path)
                    info['line_number'] = str(srcmap.lineno)
                update_sourcemap()
            if show_funcname:
                info['function_name'] = srcmap.funcname
            if show_varnames:
                if markup_pos == 0:
                    info['variable_names'] = srcmap.varnames
                elif markup_pos == 1:
                    info['variable_names'] = srcmap.varnames[1:]
                else:
                    info['variable_names'] = srcmap.varnames[:-1]
        self._cache.store_info(frame_id, markup, info)
        return (self._builder.compose(args, marks_meaning, info), flush_scheme)

    def _extract_markup_from_arguments(self, frame_id: str, args: T.Args) -> tuple[T.Args, T.MarkupPos, T.Markup]:
        """
        return: (args, markup_pos, markup)
            markup_pos: which position of `markup` in `args`.
                0 not exists, 1 first place, -1 last place.
        """
        if (markup_pos := self._cache.get_markup_pos(frame_id)) is None:
            is_markup = self._analyser.is_valid_markup
            if len(args) > 0 and isinstance(args[0], str) and args[0].startswith(':') and is_markup(args[0]):
                markup_pos = 1
            elif len(args) > 1 and isinstance(args[-1], str) and args[-1].startswith(':') and is_markup(args[-1]):
                markup_pos = -1
            else:
                markup_pos = 0
            self._cache.record_markup_pos(frame_id, markup_pos)
        if markup_pos == 0:
            return (args, markup_pos, '')
        elif markup_pos == 1:
            return (args[1:], markup_pos, args[0])
        else:
            return (args[:-1], markup_pos, args[-1])
lk = LKLogger()