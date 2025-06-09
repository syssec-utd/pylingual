from typing import Callable
from .handler import Handler

class InlineQueryHandler(Handler):
    """The InlineQuery handler class. Used to handle inline queries.
    It is intended to be used with :meth:`~pyrogram.Client.add_handler`

    For a nicer way to register this handler, have a look at the
    :meth:`~pyrogram.Client.on_inline_query` decorator.

    Parameters:
        callback (``Callable``):
            Pass a function that will be called when a new InlineQuery arrives. It takes *(client, inline_query)*
            as positional arguments (look at the section below for a detailed description).

        filters (:obj:`Filters`):
            Pass one or more filters to allow only a subset of inline queries to be passed
            in your callback function.

    Other parameters:
        client (:obj:`~pyrogram.Client`):
            The Client itself, useful when you want to call other API methods inside the inline query handler.

        inline_query (:obj:`~pyrogram.types.InlineQuery`):
            The received inline query.
    """

    def __init__(self, callback: Callable, filters=None):
        super().__init__(callback, filters)