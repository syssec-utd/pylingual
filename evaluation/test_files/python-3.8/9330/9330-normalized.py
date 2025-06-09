def popup_html(self, callback_name=None, indent=None, title='Login | {0}', custom=None, stay_open=False):
    """
        Returns a HTML with JavaScript that:

        #.  Triggers the ``options.onLoginComplete(result, closer)`` handler
            set with the :ref:`authomatic.setup() <js_setup>` function of
            :ref:`javascript.js <js>`.
        #.  Calls the JavasScript callback specified by :data:`callback_name`
            on the opener of the *login handler popup* and passes it the
            *login result* JSON object as first argument and the `closer`
            function which you should call in your callback to close the popup.

        :param str callback_name:
            The name of the javascript callback e.g ``foo.bar.loginCallback``
            will result in ``window.opener.foo.bar.loginCallback(result);``
            in the HTML.

        :param int indent:
            The number of spaces to indent the JSON result object.
            If ``0`` or negative, only newlines are added.
            If ``None``, no newlines are added.

        :param str title:
            The text of the HTML title. You can use ``{0}`` tag inside,
            which will be replaced by the provider name.

        :param custom:
            Any JSON serializable object that will be passed to the
            ``result.custom`` attribute.

        :param str stay_open:
            If ``True``, the popup will stay open.

        :returns:
            :class:`str` with HTML.

        """
    return '\n        <!DOCTYPE html>\n        <html>\n            <head><title>{title}</title></head>\n            <body>\n            <script type="text/javascript">\n                {js}\n            </script>\n            </body>\n        </html>\n        '.format(title=title.format(self.provider.name if self.provider else ''), js=self.popup_js(callback_name, indent, custom, stay_open))