import os
import base64
from epyk.core.py import types
from epyk.core import html
from epyk.core.js.packages import JsFontAwesome
from epyk.interfaces import Arguments
from epyk.core.css import Colors

class Icons:

    def __init__(self, ui):
        self.page = ui.page

    @property
    def get(self):
        return JsFontAwesome

    def awesome(self, icon: str, text: str=None, tooltip: str=None, position: str=None, width: types.SIZE_TYPE=(25, 'px'), height: types.SIZE_TYPE=(25, 'px'), html_code: str=None, options: types.OPTION_TYPE=None, profile: types.PROFILE_TYPE=None, align: str='left', size: types.SIZE_TYPE=(None, 'px')):
        """
    Generic function to create icon components. Default icon library used is font awesome but this might change
    depending on the web framework used.

    Usage::

      page.ui.icons.awesome(icon="fas fa-align-center")

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlButton.IconEdit`

    Templates:

      https://github.com/epykure/epyk-templates/blob/master/locals/components/banners.py
      https://github.com/epykure/epyk-templates/blob/master/locals/components/icons.py

    :param icon: Optional. The font awesome icon reference
    :param text: Optional. The text to be displayed to this component. Default None
    :param position: Optional. The position of the icon in the line (left, right, center)
    :param tooltip: Optional. A string with the value of the tooltip
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        width = Arguments.size(width, unit='px')
        size = Arguments.size(size, unit='px')
        height = Arguments.size(height, unit='px')
        options = options or {}
        if 'icon_family' not in options:
            icon_details = self.page.icons.get(icon)
            options['icon_family'] = icon_details['icon_family']
        else:
            icon_details = {'icon': icon, 'icon_family': options['icon_family']}
        icon_size = size if size[0] is not None else width
        html_edit = html.HtmlButton.IconEdit(self.page, position, icon_details['icon'], text, tooltip, icon_size, height, html_code, options, profile)
        html_edit.css({'margin': 0, 'cursor': 'pointer'})
        html_edit.style.css.float = position
        html_edit.style.css.text_align = align
        if width[0] is not None:
            html_edit.style.css.width = '%s%s' % (width[0], width[1])
        if width[0] == 100 and width[1] == '%':
            html_edit.icon.style.css.display = 'block'
        html_edit.style.css.display = 'inline-block'
        html.Html.set_component_skin(html_edit)
        return html_edit

    def fluent(self, icon: str, text: str=None, tooltip: str=None, position: str=None, width: types.SIZE_TYPE=(25, 'px'), height: types.SIZE_TYPE=(25, 'px'), html_code: str=None, options: types.OPTION_TYPE=None, profile: types.PROFILE_TYPE=None):
        """

    Usage::

      page.ui.icons.awesome(icon="fas fa-align-center")

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlButton.IconEdit`
    ms-Icon ms-Icon--AdminDLogoInverse32

    :param icon: Optional. The FluentUI icon reference
    :param text: Optional. The text to be displayed to this component. Default None
    :param position: Optional. The position of the icon in the line (left, right, center)
    :param tooltip: Optional. A string with the value of the tooltip
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    """
        width = Arguments.size(width, unit='px')
        height = Arguments.size(height, unit='px')
        icon_details = self.page.icons.get(icon)
        options = options or {}
        options['icon_family'] = icon_details['icon_family']
        html_edit = html.HtmlButton.IconEdit(self.page, position, icon_details['icon'], text, tooltip, width, height, html_code, options, profile)
        html_edit.css({'margin': '5px 0', 'cursor': 'pointer'})
        html_edit.style.css.float = position
        html_edit.style.css.display = 'inline-block'
        html.Html.set_component_skin(html_edit)
        return html_edit

    def fixed(self, icon: str=None, family: str=None, width: types.SIZE_TYPE=(None, 'px'), html_code: str=None, height: types.SIZE_TYPE=(None, 'px'), color: str=None, tooltip: str=None, align: str='left', options: types.OPTION_TYPE=None, profile: types.PROFILE_TYPE=None):
        """


    :param icon: Optional. The icon value
    :param family: Optional. The icon family
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param color: Optional.
    :param tooltip: Optional. A string with the value of the tooltip
    :param align: Optional. A string with the horizontal position of the component
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    """
        options = options or {}
        component = self.page.ui.icon(icon, family, width, html_code, height, color, tooltip, align, options, profile)
        component.style.css.fixed(bottom=options.get('bottom', 20), right=options.get('right', 20))
        component.style.add_classes.div.background_hover()
        component.style.css.border_radius = 15
        component.style.css.padding = 8
        html.Html.set_component_skin(component)
        return component

    def edit(self, text: str=None, position: str=None, tooltip: str='Edit', width: types.SIZE_TYPE=(None, 'px'), height: types.SIZE_TYPE=(None, 'px'), html_code: str=None, options: types.OPTION_TYPE=None, profile: types.PROFILE_TYPE=None, align: str='left', size: types.SIZE_TYPE=(None, 'px')):
        """

    Usage::

      page.ui.icons.edit()
      page.ui.icons.edit().color("red")

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlButton.IconEdit`

    Templates:

      https://github.com/epykure/epyk-templates/blob/master/locals/components/icons.py

    :param text: Optional. The text to be displayed to this component. Default None
    :param position: Optional. The position of the icon in the line (left, right, center)
    :param tooltip: Optional. A string with the value of the tooltip
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        component = self.awesome('edit', text, tooltip, position, width, height, html_code, options, profile, align, size)
        html.Html.set_component_skin(component)
        return component

    def clock(self, text=None, position=None, tooltip='Last Updated Time', width=(None, 'px'), height=(None, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """

    Usage::

      page.ui.icons.clock()
      page.ui.icons.clock().color("red")

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlButton.IconEdit`

    templates:

      https://github.com/epykure/epyk-templates/blob/master/locals/components/icons.py

    :param text: Optional. The text to be displayed to this component. Default None
    :param position: Optional. The position of the icon in the line (left, right, center)
    :param tooltip: Optional. A string with the value of the tooltip
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        component = self.awesome('clock', text, tooltip, position, width, height, html_code, options, profile, align, size)
        html.Html.set_component_skin(component)
        return component

    def next(self, text=None, position=None, tooltip='', width=(None, 'px'), height=(None, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """

    Usage::

    :param text: Optional. The text to be displayed to this component. Default None
    :param position: Optional. The position of the icon in the line (left, right, center)
    :param tooltip: Optional. A string with the value of the tooltip
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        components = self.awesome('next', text, tooltip, position, width, height, html_code, options, profile, align, size)
        components.icon.style.css.font_factor(10)
        html.Html.set_component_skin(components)
        return components

    def previous(self, text=None, position=None, tooltip='', width=(None, 'px'), height=(None, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """

    Usage::

    :param text: Optional. The text to be displayed to this component. Default None
    :param position: Optional. The position of the icon in the line (left, right, center)
    :param tooltip: Optional. A string with the value of the tooltip
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        components = self.awesome('previous', text, tooltip, position, width, height, html_code, options, profile, align, size)
        components.icon.style.css.font_factor(10)
        html.Html.set_component_skin(components)
        return components

    def play(self, text=None, position=None, tooltip='', width=(None, 'px'), height=(None, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """
    Shortcut to the play icon.

    Usage::

      page.ui.icons.play()

    :param text: Optional. The text to be displayed to this component. Default None
    :param position: Optional. The position of the icon in the line (left, right, center)
    :param tooltip: Optional. A string with the value of the tooltip
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        components = self.awesome('play', text, tooltip, position, width, height, html_code, options, profile, align, size)
        html.Html.set_component_skin(components)
        return components

    def stop(self, text=None, position=None, tooltip='', width=(None, 'px'), height=(None, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """
    Shortcut to the stop icon.

    Usage::

      page.ui.icons.stop()

    :param text: Optional. The text to be displayed to this component. Default None
    :param position: Optional. The position of the icon in the line (left, right, center)
    :param tooltip: Optional. A string with the value of the tooltip
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        components = self.awesome('stop', text, tooltip, position, width, height, html_code, options, profile, align, size)
        html.Html.set_component_skin(components)
        return components

    def zoom_out(self, text=None, position=None, tooltip='', width=(None, 'px'), height=(None, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """

    Usage::

    :param text: Optional. The text to be displayed to this component. Default None
    :param position: Optional. The position of the icon in the line (left, right, center)
    :param tooltip: Optional. A string with the value of the tooltip
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        components = self.awesome('zoom_out', text, tooltip, position, width, height, html_code, options, profile, align, size)
        components.style.css.color = self.page.theme.greys[-6]
        html.Html.set_component_skin(components)
        return components

    def zoom_in(self, text=None, position=None, tooltip='', width=(None, 'px'), height=(None, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """

    Usage::


    :param text: Optional. The text to be displayed to this component. Default None
    :param position: Optional. The position of the icon in the line (left, right, center)
    :param tooltip: Optional. A string with the value of the tooltip
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        components = self.awesome('zoom_in', text, tooltip, position, width, height, html_code, options, profile, align, size)
        components.style.css.color = self.page.theme.greys[-6]
        html.Html.set_component_skin(components)
        return components

    def warning(self, text=None, position=None, tooltip='', width=(None, 'px'), height=(None, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """

    Usage::

    :param text: Optional. The text to be displayed to this component. Default None
    :param position: Optional. The position of the icon in the line (left, right, center)
    :param tooltip: Optional. A string with the value of the tooltip
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        components = self.awesome('warning', text, tooltip, position, width, height, html_code, options, profile, align, size)
        components.style.css.color = self.page.theme.warning.base
        html.Html.set_component_skin(components)
        return components

    def success(self, text=None, position=None, tooltip='', width=(None, 'px'), height=(None, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """

    Usage::

    :param text: Optional. The text to be displayed to this component. Default None
    :param position: Optional. The position of the icon in the line (left, right, center)
    :param tooltip: Optional. A string with the value of the tooltip
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        components = self.awesome('success', text, tooltip, position, width, height, html_code, options, profile, align, size)
        components.style.css.color = self.page.theme.success.base
        html.Html.set_component_skin(components)
        return components

    def danger(self, text=None, position=None, tooltip='', width=(None, 'px'), height=(None, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """

    Usage::

    :param text: Optional. The text to be displayed to this component. Default None
    :param position: Optional. The position of the icon in the line (left, right, center)
    :param tooltip: Optional. A string with the value of the tooltip
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        components = self.awesome('danger', text, tooltip, position, width, height, html_code, options, profile, align, size)
        components.style.css.color = self.page.theme.danger.base
        html.Html.set_component_skin(components)
        return components

    def error(self, text=None, position=None, tooltip='', width=(None, 'px'), height=(None, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """

    Usage::

    :param text: Optional. The text to be displayed to this component. Default None
    :param position: Optional. The position of the icon in the line (left, right, center)
    :param tooltip: Optional. A string with the value of the tooltip
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        components = self.awesome('error', text, tooltip, position, width, height, html_code, options, profile, align, size)
        components.style.css.color = self.page.theme.danger.base
        html.Html.set_component_skin(components)
        return components

    def info(self, text=None, position=None, tooltip='', width=(None, 'px'), height=(None, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """

    Usage::

    :param text: Optional. The text to be displayed to this component. Default None
    :param position: Optional. The position of the icon in the line (left, right, center)
    :param tooltip: Optional. A string with the value of the tooltip
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        components = self.awesome('info', text, tooltip, position, width, height, html_code, options, profile, align, size)
        html.Html.set_component_skin(components)
        return components

    def save(self, text=None, position=None, tooltip='', width=(None, 'px'), height=(None, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """

    Usage::


    :param text: Optional. The text to be displayed to this component. Default None
    :param position: Optional. The position of the icon in the line (left, right, center)
    :param tooltip: Optional. A string with the value of the tooltip
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        component = self.awesome('save', text, tooltip, position, width, height, html_code, options, profile, align, size)
        html.Html.set_component_skin(component)
        return component

    def refresh(self, text=None, position=None, tooltip='Refresh Component', width=(None, 'px'), height=(None, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """


    Usage::

      page.ui.icons.refresh()
      page.ui.icons.refresh().color("red")

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlButton.IconEdit`

    :param text: Optional. The text to be displayed to this component. Default None
    :param position: Optional. The position of the icon in the line (left, right, center)
    :param tooltip: Optional. A string with the value of the tooltip
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        component = self.awesome('refresh', text, tooltip, position, width, height, html_code, options, profile, align, size)
        html.Html.set_component_skin(component)
        return component

    def pdf(self, text=None, position=None, tooltip='Convert to PDF', width=(None, 'px'), height=(None, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """


    Usage::

      page.ui.icons.pdf(tooltip="helper")

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlButton.IconEdit`

    :param text: Optional. The text to be displayed to this component. Default None
    :param position: Optional. The position of the icon in the line (left, right, center)
    :param tooltip: Optional. A string with the value of the tooltip
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        component = self.awesome('pdf', text, tooltip, position, width, height, html_code, options, profile, align, size)
        html.Html.set_component_skin(component)
        return component

    def plus(self, text=None, position=None, tooltip='Add line', width=(None, 'px'), height=(None, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """


   Usage::

      page.ui.icons.plus()

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlButton.IconEdit`

    :param text: Optional. The text to be displayed to this component. Default None
    :param position: Optional. The position of the icon in the line (left, right, center)
    :param tooltip: Optional. A string with the value of the tooltip
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        component = self.awesome('plus', text, tooltip, position, width, height, html_code, options, profile, align, size)
        html.Html.set_component_skin(component)
        return component

    def excel(self, text=None, position=None, tooltip='Convert to Excel', width=(None, 'px'), height=(None, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """


    Usage::

      page.ui.icons.excel()

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlButton.IconEdit`

    :param text: Optional. The text to be displayed to this component. Default None
    :param position: Optional. The position of the icon in the line (left, right, center...)
    :param tooltip: Optional. A string with the value of the tooltip
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        component = self.awesome('excel', text, tooltip, position, width, height, html_code, options, profile, align, size)
        html.Html.set_component_skin(component)
        return component

    def download(self, text=None, position=None, tooltip='Download', width=(None, 'px'), height=(None, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """


    Usage::

      page.ui.icons.download()

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlButton.IconEdit`

    :param text: Optional. The text to be displayed to this component. Default None
    :param position: Optional. The position of the icon in the line (left, right, center)
    :param tooltip: Optional. A string with the value of the tooltip
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        component = self.awesome('download', text, tooltip, position, width, height, html_code, options, profile, align, size)
        html.Html.set_component_skin(component)
        return component

    def delete(self, text=None, position=None, tooltip='Delete Component on the page', width=(None, 'px'), height=(None, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """


    Usage::

      page.ui.icons.delete()

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlButton.IconEdit`

    :param text: Optional. The text to be displayed to this component. Default None
    :param position: Optional. The position of the icon in the line (left, right, center)
    :param tooltip: Optional. A string with the value of the tooltip
    :param align: Optional. The text-align property within this component
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        component = self.awesome('delete', text, tooltip, position, width, height, html_code, options, profile, align, size)
        component.hover_color = 'danger'
        component.style.css.white_space = 'nowrap'
        html.Html.set_component_skin(component)
        return component

    def zoom(self, text=None, position=None, tooltip='Zoom on Component', width=(None, 'px'), height=(None, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """


    Usage::

      page.ui.icons.zoom()

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlButton.IconEdit`

    :param text: Optional. The text to be displayed to this component. Default None
    :param position: Optional. The position of the icon in the line (left, right, center)
    :param tooltip: Optional. A string with the value of the tooltip
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        component = self.awesome('zoom', text, tooltip, position, width, height, html_code, options, profile, align, size)
        html.Html.set_component_skin(component)
        return component

    def capture(self, text=None, position=None, tooltip='Save to clipboard', width=(None, 'px'), height=(None, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """


    Usage::

      page.ui.icons.capture()

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlButton.IconEdit`

    :param text: Optional. The text to be displayed to this component. Default None
    :param position: Optional. The position of the icon in the line (left, right, center)
    :param tooltip: Optional. A string with the value of the tooltip
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        component = self.awesome('capture', text, tooltip, position, width, height, html_code, options, profile, align, size)
        html.Html.set_component_skin(component)
        return component

    def remove(self, text=None, position=None, tooltip='Remove Item', width=(None, 'px'), height=(None, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """


    Usage::

      page.ui.icons.remove()

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlButton.IconEdit`

    :param text: Optional. The text to be displayed to this component. Default None
    :param position: Optional. The position of the icon in the line (left, right, center)
    :param tooltip: Optional. A string with the value of the tooltip
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        component = self.awesome('remove', text, tooltip, position, width, height, html_code, options, profile, align, size)
        component.hover_color = 'danger'
        component.style.css.white_space = 'nowrap'
        html.Html.set_component_skin(component)
        return component

    def clear(self, text=None, position=None, tooltip='', width=(None, 'px'), height=(None, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """

    Same as :func:`epyk.interfaces.components.CompIcons.Icons.awesome` with a `fas fa-times-circle <https://fontawesome.com/icons/fas fa-eraser>`_ icon

    Usage::

      page.ui.icons.clear()

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlButton.IconEdit`

    :param text: Optional. The text to be displayed to this component. Default None
    :param align:
    :param position: Optional. The position of the icon in the line (left, right, center)
    :param tooltip: Optional. A string with the value of the tooltip
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        component = self.awesome('clear', text, tooltip, position, width, height, html_code, options, profile, align, size)
        component.hover_color = 'danger'
        component.style.css.white_space = 'nowrap'
        component.style.css.margin = align
        html.Html.set_component_skin(component)
        return component

    def table(self, text=None, position=None, tooltip='Convert to Table', width=(None, 'px'), height=(None, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """


    Usage::

      page.ui.icons.table(tooltip="helper")

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlButton.IconEdit`

    :param text: Optional. The text to be displayed to this component. Default None
    :param position: Optional. The position of the icon in the line (left, right, center)
    :param tooltip: Optional. A string with the value of the tooltip
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        component = self.awesome('table', text, tooltip, position, width, height, html_code, options, profile, align, size)
        html.Html.set_component_skin(component)
        return component

    def wrench(self, text=None, position=None, tooltip='Processing Time', width=(None, 'px'), height=(None, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """


    Usage::

      page.ui.icons.wrench()

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlButton.IconEdit`

    :param text: Optional. The text to be displayed to this component. Default None
    :param position: Optional. The position of the icon in the line (left, right, center)
    :param tooltip: Optional. A string with the value of the tooltip
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        component = self.awesome('wrench', text, tooltip, position, width, height, html_code, options, profile, align, size)
        html.Html.set_component_skin(component)
        return component

    def rss(self, text='RSS', position=None, tooltip='', width=('auto', ''), height=(25, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """


    Usage::

      page.ui.icons.rss()

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlButton.IconEdit`

    :param text: Optional. The text to be displayed to this component. Default None
    :param position: Optional. The position of the icon in the line (left, right, center)
    :param tooltip: Optional. A string with the value of the tooltip
    :param align: Optional. A string with the horizontal position of the component
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param html_code: String. Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        icon = self.awesome('rss', text, tooltip, position, width, height, html_code, options, profile, align, size)
        icon.style.css.color = '#cc9547'
        icon.style.css.display = 'inline-block'
        icon.icon.style.css.font_size = self.page.body.style.globals.font.normal(5)
        if text is not None:
            icon.span.style.css.text_align = 'left'
            icon.span.style.css.float = None
        if align == 'center':
            icon.style.css.width = '100%'
            icon.style.css.text_align = 'center'
        html.Html.set_component_skin(icon)
        return icon

    def facebook(self, text=None, url='https://en-gb.facebook.com/', position=None, tooltip='Facebook', width=(25, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """


    Usage::

      page.ui.icons.facebook()

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlButton.IconEdit`

    :param text:
    :param url:
    :param position:
    :param tooltip: Optional. A string with the value of the tooltip
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        if width[0] is None:
            width = (self.page.body.style.globals.icon.big, 'px')
        options = options or {'target': '_blank', 'font-factor': 8}
        icon = self.awesome('facebook', text, tooltip, position, width, width, html_code, options, profile, align, size)
        icon.css({'border-radius': '%spx' % width[0], 'text-align': 'center', 'line-height': '%s%s' % (width[0], width[1])})
        icon.icon.css({'margin-right': 'auto', 'margin': 'auto', 'color': '#4267B2', 'padding-bottom': '3px'})
        icon.style.add_classes.div.background_hover()
        icon.click([self.page.js.navigateTo(url, options=options)])
        html.Html.set_component_skin(icon)
        return icon

    def messenger(self, text=None, url='https://en-gb.facebook.com/', position=None, tooltip='Facebook', width=(25, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """


    Usage::

      page.ui.icons.facebook()

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlButton.IconEdit`

    :param text: Optional. The text to be displayed to this component. Default None
    :param url:
    :param position:
    :param tooltip:
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        options = options or {'target': '_blank', 'font-factor': self.page.body.style.globals.font.size - 6}
        icon = self.awesome('messenger', text, tooltip, position, width, width, html_code, options, profile, align, size)
        icon.css({'border-radius': '%spx' % width[0], 'text-align': 'center', 'line-height': '%s%s' % (width[0], width[1])})
        icon.icon.css({'margin-right': 'auto', 'margin': 'auto', 'color': '#0078FF', 'padding': '3px'})
        icon.style.add_classes.div.background_hover()
        icon.click([self.page.js.navigateTo(url, options=options)])
        html.Html.set_component_skin(icon)
        return icon

    def twitter(self, text=None, url='https://twitter.com/Epykure1', position=None, tooltip='', width=(None, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """


    Usage::

      page.ui.icons.twitter()

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlButton.IconEdit`

    :param text:
    :param url:
    :param position:
    :param tooltip:
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        if width[0] is None:
            width = (self.page.body.style.globals.icon.big, 'px')
        options = options or {'target': '_blank', 'font-factor': 6}
        icon = self.awesome('twitter', text, tooltip, position, width, width, html_code, options, profile, align, size)
        icon.css({'border-radius': '%spx' % width[0], 'text-align': 'center', 'line-height': '%s%s' % (width[0], width[1])})
        icon.icon.css({'margin-right': 'auto', 'margin': 'auto', 'color': '#1DA1F2', 'padding': '3px 3px 6px 3px'})
        icon.style.add_classes.div.background_hover()
        icon.click([self.page.js.navigateTo(url, options=options)])
        html.Html.set_component_skin(icon)
        return icon

    def twitch(self, text=None, url='https://www.twitch.tv/epykure1', position=None, tooltip='', width=(None, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """


    Usage::

      page.ui.icons.twitter()

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlButton.IconEdit`

    :param text:
    :param url:
    :param position:
    :param tooltip:
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        if width[0] is None:
            width = (self.page.body.style.globals.icon.big, 'px')
        options = options or {'target': '_blank', 'font-factor': 6}
        icon = self.awesome('twitch', text, tooltip, position, width, width, html_code, options, profile, align, size)
        icon.css({'border-radius': '%spx' % width[0], 'text-align': 'center', 'line-height': '%s%s' % (width[0], width[1])})
        icon.icon.css({'margin-right': 'auto', 'margin': 'auto', 'color': '#6441a5', 'padding': '3px'})
        icon.style.add_classes.div.background_hover()
        icon.click([self.page.js.navigateTo(url, options=options)])
        html.Html.set_component_skin(icon)
        return icon

    def instagram(self, text=None, url='https://www.instagram.com/?hl=en', position=None, tooltip='Twitter', width=(None, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """


    Usage::

      page.ui.icons.twitter()

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlButton.IconEdit`

    :param text:
    :param url:
    :param position:
    :param tooltip:
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        if width[0] is None:
            width = (self.page.body.style.globals.icon.big, 'px')
        options = options or {'target': '_blank', 'font-factor': 8}
        icon = self.awesome('instagram', text, tooltip, position, width, width, html_code, options, profile, align, size)
        icon.css({'border-radius': '%spx' % width[0], 'text-align': 'center', 'line-height': '%s%s' % (width[0], width[1])})
        icon.icon.css({'margin-right': 'auto', 'margin': 'auto', 'color': '#3f729b', 'padding': '0px 3px 5px 3px'})
        icon.style.add_classes.div.background_hover()
        icon.click([self.page.js.navigateTo(url, options=options)])
        html.Html.set_component_skin(icon)
        return icon

    def linkedIn(self, text=None, url='https://www.linkedin.com/in/epykure-python-58278a1b8/', position=None, tooltip='', width=(None, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """
    Create a LinkedIn icon button which will by default point to the Epykure account.
    Epykure account is the official account for the development of this framework.

    Usage::

      page.ui.icons.linkedIn()

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlButton.IconEdit`

    :param text: Optional. The text for the Icon
    :param url: Optional. The url when clicked
    :param position:
    :param tooltip: Optional. The tooltip when the mouse is hover
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Boolean | Dictionary. Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        if width[0] is None:
            width = (self.page.body.style.globals.icon.big, 'px')
        options = options or {'target': '_blank', 'font-factor': 6}
        icon = self.awesome('linkedIn', text, tooltip, position, width, width, html_code, options, profile, align, size)
        icon.css({'border-radius': '%spx' % width[0], 'text-align': 'center', 'line-height': '%s%s' % (width[0], width[1])})
        icon.icon.css({'margin-right': 'auto', 'margin': 'auto', 'color': '#0e76a8', 'padding': '3px 3px 6px 3px'})
        icon.style.add_classes.div.background_hover()
        icon.click([self.page.js.navigateTo(url, options=options)])
        html.Html.set_component_skin(icon)
        return icon

    def youtube(self, text=None, url='https://www.youtube.com/', position=None, tooltip='Follow us on Youtube', width=(None, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """


    Usage::

      page.ui.icons.youtube()

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlButton.IconEdit`

    :param text:
    :param url:
    :param position:
    :param tooltip:
    :param width: Tuple. Optional. A tuple with the integer for the component width and its unit
    :param html_code: String. Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Dictionary. Optional. Specific Python options available for this component
    :param profile: Boolean | Dictionary. Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        if width[0] is None:
            width = (self.page.body.style.globals.icon.big, 'px')
        options = options or {'target': '_blank', 'font-factor': 8}
        icon = self.awesome('youtube', text, tooltip, position, width, width, html_code, options, profile, align, size)
        icon.css({'border-radius': '%spx' % width[0], 'text-align': 'center', 'line-height': '%s%s' % (width[0], width[1])})
        icon.icon.css({'margin-right': 'auto', 'margin': 'auto', 'color': '#FF0000', 'padding': '3px 3px 8px 3px'})
        icon.style.add_classes.div.background_hover()
        icon.click([self.page.js.navigateTo(url, options=options)])
        html.Html.set_component_skin(icon)
        return icon

    def github(self, text=None, url='https://github.com/epykure/epyk-ui', position=None, tooltip='Go the the Github project', width=(None, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """
    Link to a GitHub repository.

    By default this icon button will redirect to the Epyk UI repository.

    Usage::

      page.ui.icons.github()

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlButton.IconEdit`

    :param text: optional. The text on the icon
    :param url: Optional. The url link
    :param position:
    :param tooltip:
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        options = options or {'target': '_blank', 'font-factor': -2}
        icon = self.awesome('github', text, tooltip, position, width, width, html_code, options, profile, align, size)
        icon.css({'text-align': 'center', 'line-height': '%s%s' % (self.page.body.style.globals.font.size, 'px')})
        icon.icon.css({'margin-right': 'auto', 'margin': 'auto', 'color': 'blue', 'padding': '3px'})
        icon.style.add_classes.div.background_hover()
        icon.click([self.page.js.navigateTo(url, options=options)])
        html.Html.set_component_skin(icon)
        return icon

    def python(self, text=None, url='https://pypi.org/', position=None, tooltip='', width=(25, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """


    Usage::

      page.ui.icons.python()

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlButton.IconEdit`

    :param text:
    :param url:
    :param position:
    :param tooltip:
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        icon = self.awesome('python', text, tooltip, position, width if text is None else 'auto', None, html_code, options, profile, align, size)
        icon.css({'border-radius': '%spx' % width[0], 'padding-bottom': '3px', 'text-align': 'center', 'line-height': '%s%s' % (width[0], width[1])})
        icon.icon.css({'margin-right': 'auto', 'margin': 'auto', 'padding': '3px'})
        icon.style.add_classes.div.background_hover()
        icon.click([self.page.js.navigateTo(url)])
        html.Html.set_component_skin(icon)
        return icon

    def stackoverflow(self, text=None, url='https://stackoverflow.com/', position=None, tooltip='Share your comments', width=(25, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """


    Usage::

      page.ui.icons.stackoverflow()

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlButton.IconEdit`

    :param text:
    :param url:
    :param position:
    :param tooltip:
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        icon = self.awesome('stackoverflow', text, tooltip, position, width, width, html_code, options, profile, align, size)
        icon.css({'border-radius': '%spx' % width[0], 'text-align': 'center', 'line-height': '%s%s' % (width[0], width[1])})
        icon.icon.css({'margin-right': 'auto', 'margin': 'auto', 'color': 'blue', 'padding': '3px'})
        icon.style.add_classes.div.background_hover()
        icon.click([self.page.js.navigateTo(url)])
        html.Html.set_component_skin(icon)
        return icon

    def mail(self, text=None, url='', position=None, tooltip='Share by mail', width=(25, 'px'), html_code=None, options=None, profile=None, align: str='left', size=(None, 'px')):
        """

    Same as :func:`epyk.interfaces.components.CompIcons.Icons.awesome` with a `fab fa-stack-overflow <https://fontawesome.com/icons/stack-overflow>`_ icon

    Usage::

      page.ui.icons.mail()

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlButton.IconEdit`

    :param text:
    :param url:
    :param position:
    :param tooltip:
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional. A tuple with the integer for the component size and its unit
    """
        icon = self.awesome('envelope', text, tooltip, position, width, width, html_code, options, profile, align, size)
        icon.css({'border-radius': '%spx' % width[0], 'text-align': 'center', 'line-height': '%s%s' % (width[0], width[1])})
        icon.icon.css({'margin-right': 'auto', 'margin': 'auto', 'padding': '3px'})
        icon.style.add_classes.div.background_hover()
        html.Html.set_component_skin(icon)
        return icon

    def tick(self, flag=True, text=None, icons=(JsFontAwesome.ICON_CHECK, JsFontAwesome.ICON_TIMES), position=None, tooltip='', width=(None, 'px'), html_code=None, options=None, profile=None):
        """
    Display a tick box component

    Usage::

      page.ui.icons.tick()

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlRadio.Tick`

    :param flag: Optional. The state for the tick component
    :param text: optional. The text for this component. Default none
    :param icons: Optional. The two icons to use for the component state
    :param position: Optional. A string with the vertical position of the component
    :param tooltip: Optional. A string with the value of the tooltip
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    """
        width = Arguments.size(width, unit='px')
        dftl_options = {'true': icons[0], 'false': icons[1]}
        dftl_options.update(options or {})
        icon = html.HtmlRadio.Tick(self.page, position, icons[0] if flag else icons[1], text, tooltip, width, width, html_code, dftl_options, profile)
        icon.click([icon.icon.dom.switchClass(icons[0] if flag else icons[1], icons[1] if flag else icons[0]), icon.icon.dom.transition('background', self.page.theme.success.light, duration=0.2, reverse=True)])
        html.Html.set_component_skin(icon)
        return icon

    def epyk(self, align: str='center', size: types.SIZE_TYPE=(32, 'px')):
        """
    Add the Epyk Icon.

    Usage::

      page.ui.icons.epyk()

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlImage.Image`

    Templates:

      https://github.com/epykure/epyk-templates/blob/master/locals/components/image.py

    :param align: Optional. A string with the horizontal position of the component
    :param size: Optional.
    """
        if size is not None:
            (width, height) = (size, size)
        else:
            (width, height) = (None, None)
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', '..', 'static', 'images', 'epyklogo.ico'), 'rb') as fp:
            base64_bytes = base64.b64encode(fp.read())
            base64_message = base64_bytes.decode('ascii')
            img = 'data:image/x-icon;base64,%s' % base64_message
        icon = self.page.ui.img(img, align=align, width=width, height=height)
        icon.css({'text-align': 'center', 'padding': 'auto', 'vertical-align': 'middle'})
        html.Html.set_component_skin(icon)
        return icon

    def signin(self, text: str, width: types.SIZE_TYPE=(40, 'px'), icon: str=None, colored: bool=True):
        """

    Usage::

      page.ui.icons.signin("test")

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlEvent.SignIn

    Templates:

      https://github.com/epykure/epyk-templates/blob/master/locals/components/icons.py

    :param text:
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param icon: Optional. The component icon content from font-awesome references
    :param colored: Optional.
    """
        width = Arguments.size(width, unit='px')
        container = html.HtmlEvent.SignIn(self.page, text, width, icon)
        if colored:
            container.style.css.color = 'white'
            container.style.css.background = Colors.randColor(self.page.py.hash(text))
        html.Html.set_component_skin(container)
        return container

    def bar(self, records=None, color: str=None, width: types.SIZE_TYPE=(70, 'px'), height: types.SIZE_TYPE=(None, 'px'), options: types.OPTION_TYPE=None, profile: types.PROFILE_TYPE=None):
        """
    Add a bespoke options / actions bar with icons

    Usage::

    Related Pages:

    Templates:

        https://github.com/epykure/epyk-templates/blob/master/locals/components/chips.py

    :param records:
    :param color: Optional. The font color in the component. Default inherit
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    """
        width = Arguments.size(width, unit='px')
        height = Arguments.size(height, unit='px')
        records = records or []
        options = options or {}
        container = html.HtmlEvent.OptionsBar(self.page, records, width, height, color, options, profile)
        html.Html.set_component_skin(container)
        return container

    def avatar(self, img: str='', name: str=None, width: types.SIZE_TYPE=(30, 'px'), height: types.SIZE_TYPE=(None, ''), options: types.OPTION_TYPE=None, profile: types.PROFILE_TYPE=None):
        """
    Display an avatar component.

    Usage::


    :param img: The image full path
    :param name: Optional.The tooltip name
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    """
        img = img.replace('\\', '/')
        if height[0] is None:
            height = width
        avatar = self.page.ui.div('&nbsp;', width=width, height=height, options=options, profile=profile)
        avatar.css({'padding': '5px', 'border-radius': '30px', 'background-repeat': 'no-repeat', 'background-position': 'center', 'background-size': 'cover', 'cursor': 'pointer', 'background-image': 'url(%s)' % img})
        if name is not None:
            avatar.tooltip(name)
        html.Html.set_component_skin(avatar)
        return avatar

    def badge(self, text: str='', icon: str=None, width: types.SIZE_TYPE=(25, 'px'), height: types.SIZE_TYPE=(25, 'px'), background_color: str=None, color: str=None, url: str=None, tooltip: str=None, options: types.OPTION_TYPE=None, profile: types.PROFILE_TYPE=None):
        """
    Display a badge component using Bootstrap

    Usage::

      page.ui.images.badge("Test badge", "Label", icon="fas fa-align-center")
      page.ui.images.badge("This is a badge", background_color="red", color="white")
      page.ui.images.badge(12, icon="far fa-bell", options={"badge_position": 'right'})

      b = rptObj.ui.images.badge(
        7688, icon="fab fa-python", options={'badge_css': {'color': 'white', "background": 'red'}})
      b.options.badge_css = {"background": 'green'}

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlImage.Badge`

    Related Pages:

      https://getbootstrap.com/docs/4.0/components/badge/

    :param text: Optional. The content of the badge
    :param icon: Optional. A String with the icon to display from font-awesome
    :param background_color: Optional. The background color of the badge
    :param color: Optional. The text color of the badge
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param url: Optional
    :param tooltip: Optional. The text to display in the tooltip
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    """
        width = Arguments.size(width, unit='px')
        height = Arguments.size(height, unit='px')
        if background_color is None:
            background_color = self.page.theme.greys[0]
        if color is None:
            color = self.page.theme.white
        container = html.HtmlImage.Badge(self.page, text, width, height, None, icon, background_color, color, url, tooltip, options or {}, profile)
        html.Html.set_component_skin(container)
        container.link.style.css.padding = 5
        container.link.style.css.font_factor(-7)
        return container

    def date(self, value: str=None, label: str=None, icon: str='calendar', color: str=None, width: types.SIZE_TYPE=(None, 'px'), height: types.SIZE_TYPE=(None, 'px'), html_code: str=None, profile: types.PROFILE_TYPE=None, options: types.OPTION_TYPE=None, helper: str=None):
        """
    This component is based on the Jquery Date Picker object.

    Usage::

      page.ui.fields.date('2020-04-08', label="Date").included_dates(["2020-04-08", "2019-09-06"])

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlDates.DatePicker`

    Related Pages:

      https://jqueryui.com/datepicker/

    :param value: Optional. The value to be displayed to the time component. Default now
    :param label: Optional. The text of label to be added to the component
    :param icon: Optional. The component icon content from font-awesome references
    :param color: Optional. The font color in the component. Default inherit
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param profile: Optional. A flag to set the component performance storage
    :param options: Optional. Specific Python options available for this component
    :param helper: Optional. A tooltip helper
    """
        width = Arguments.size(width, unit='px')
        height = Arguments.size(height, unit='px')
        icon_details = self.page.icons.get(icon)
        dftl_options = {'dateFormat': 'yy-mm-dd', 'icon_family': icon_details['icon_family']}
        if options is not None:
            dftl_options.update(options)
        html_dt = html.HtmlDates.DatePicker(self.page, value, label, icon_details['icon'], width, height, color, html_code, profile, dftl_options, helper)
        html_dt.input.style.css.width = 0
        html_dt.input.style.css.min_width = 0
        html_dt.input.style.css.border = 0
        html_dt.input.style.css.background = 'inherit'
        html.Html.set_component_skin(html_dt)
        return html_dt

    def timer(self, time, js_funcs, icon='clock', width=(15, 'px'), height=(15, 'px'), options=None, profile=None, align: str='left', size=(None, 'px')):
        """

    Usage::


    :param time: Integer. Interval time in second
    :param js_funcs: String | List. The Javascript functions
    :param icon: String. The font awesome icon reference
    :param width: Tuple. Optional. A tuple with the integer for the component width and its unit
    :param size: Tuple. Optional. A tuple with the integer for the icon size and its unit
    :param height: Tuple. Optional. A tuple with the integer for the component height and its unit
    :param options: Dictionary. Optional. Specific Python options available for this component
    :param profile: Boolean | Dictionary. Optional. A flag to set the component performance storage
    :param align: A string with the horizontal position of the component
    """
        dflt_options = {'started': True}
        if options is not None:
            dflt_options.update(options)
        t = self.awesome(icon, width=width, height=height, profile=profile, align=align, size=size)
        if dflt_options['started']:
            t.spin().attr['data-active'] = 1
            self.page.body.onReady([self.page.js.window.setInterval(js_funcs, '%s_timer' % t.htmlCode, time * 1000)])
        else:
            t.attr['data-active'] = 0
        t.click([self.page.js.if_(t.dom.getAttribute('data-active') == 1, [t.icon.dom.removeClass(self.page.icons.get('spin')['icon']).r, t.dom.setAttribute('data-active', 0), self.page.js.window.clearInterval('%s_timer' % t.htmlCode)]).else_([t.icon.dom.addClass(self.page.icons.get('spin')['icon']), t.dom.setAttribute('data-active', 1), self.page.js.window.setInterval(js_funcs, '%s_timer' % t.htmlCode, time)])])
        html.Html.set_component_skin(t)
        return t

    def large(self, icon=None, family=None, width=(None, 'px'), height=(None, 'px'), html_code=None, color=None, tooltip=None, align='left', options=None, profile=None):
        """

    Usage::


    :param icon:
    :param family:
    :param width: Tuple. Optional. A tuple with the integer for the component width and its unit
    :param height: Tuple. Optional. A tuple with the integer for the component height and its unit
    :param html_code: String. Optional. An identifier for this component (on both Python and Javascript side)
    :param color:
    :param tooltip:
    :param align: String. Optional. The text-align property within this component
    :param options: Dictionary. Optional. Specific Python options available for this component
    :param profile: Boolean | Dictionary. Optional. A flag to set the component performance storage
    """
        icon = self.page.ui.icon(icon, family, width, html_code, height, color, tooltip, align, options, profile)
        icon.style.css.font_factor(30)
        icon.style.css.border_radius = 40
        icon.style.css.padding = 20
        icon.style.css.color = self.page.theme.greys[0]
        icon.style.css.background = self.page.theme.colors[2]
        if align == 'center':
            icon.style.css.margin = 'auto'
            icon.style.css.display = 'inline-block'
            self.page.ui.div(icon, align='center')
        html.Html.set_component_skin(icon)
        return icon

    def menu(self, data, width=(100, '%'), height=(None, 'px'), options=None, profile=False, align: str='left', size=(None, 'px')):
        """
    Add a menu bar with multiple icons.

    Usage::

      menu = page.ui.icons.menu([
        {"icon": "fab fa-github-square", "tooltip": "Github path", 'url': 'test'},
        {"icon": "far fa-eye"},
        {"icon": "fas fa-file-code"}
      ])

    :param data: List. The icons definition.
    :param width: Tuple. Optional. A tuple with the integer for the component width and its unit
    :param size: Tuple. Optional. A tuple with the integer for the icon size and its unit
    :param height: Tuple. Optional. A tuple with the integer for the component height and its unit
    :param align: String. Optional. A string with the horizontal position of the component
    :param options: Dictionary. Optional. Specific Python options available for this component
    :param profile: Boolean | Dictionary. Optional. A flag to set the component performance storage
    """
        dfl_options = {'margin-right': 5}
        if options is not None:
            dfl_options.update(options)
        div = self.page.ui.div(width=width, height=height, align=align, options=options, profile=profile)
        for d in data:
            div.add(self.page.ui.icons.awesome(icon=d['icon'], tooltip=d.get('tooltip', ''), width=self.page.body.style.globals.icon.normal, options=options, profile=profile, size=size))
            div[-1].style.css.margin_right = dfl_options['margin-right']
            div[-1].style.css.color = self.page.theme.greys[5]
            div[-1].style.add_classes.div.color_hover()
            if 'url' in d:
                div[-1].goto(d['url'], target='_blank')
        html.Html.set_component_skin(div)
        return div

    def hamburger(self, width=(15, 'px'), height=(2, 'px'), color=None, options=None, profile=None):
        """

    https://www.w3schools.com/howto/tryit.asp?filename=tryhow_css_menu_icon_js

    :param width: Tuple. Optional. A tuple with the integer for the component width and its unit
    :param height: Tuple. Optional. A tuple with the integer for the component height and its unit
    :param color: String. Optional. The font color in the component. Default inherit
    :param options: Dictionary. Optional. Specific Python options available for this component
    :param profile: Boolean | Dictionary. Optional. A flag to set the component performance storage
    """
        height = Arguments.size(height, unit='px')
        bar1 = self.page.ui.div(width=width, height=height, profile=profile)
        bar1.style.add_classes.external('bar1')
        bar1.style.css.background_color = color or self.page.theme.colors[-1]
        bar1.style.css.display = 'block'
        bar1.style.css.transition = 0.4
        bar1.style.css.margin = '%spx 0' % height[0]
        bar2 = self.page.ui.div(width=width, height=height, profile=profile)
        bar2.style.add_classes.external('bar2')
        bar2.style.css.background_color = color or self.page.theme.colors[-1]
        bar2.style.css.display = 'block'
        bar2.style.css.margin = '%spx 0' % height[0]
        bar2.style.css.transition = 0.4
        bar3 = self.page.ui.div(width=width, height=height, profile=profile)
        bar3.style.add_classes.external('bar3')
        bar3.style.css.background_color = color or self.page.theme.colors[-1]
        bar3.style.css.display = 'block'
        bar3.style.css.margin = '%spx 0' % height[0]
        bar3.style.css.transition = 0.4
        component = self.page.ui.div([bar1, bar2, bar3], width=width, options=options, profile=profile)
        component.style.add_custom_class({'transform': 'rotate(-45deg) translate(-3px, 1px)'}, 'change-hamburger .bar1')
        component.style.add_custom_class({'transform': 'rotate(45deg) translate(-4px, -3px)'}, 'change-hamburger .bar3')
        component.style.add_custom_class({'opacity': 0}, 'change-hamburger .bar2')
        component.style.css.cursor = 'pointer'
        component.set_icon = str
        component.click([component.dom.classList.toggle('change-hamburger')])
        html.Html.set_component_skin(component)
        return component

    @property
    def toggles(self):
        """
    More custom toggles icons.
    """
        return Toggles(self)

    def gallery(self, icons=None, columns=6, width=(None, '%'), height=('auto', ''), options=None, profile=None):
        """
    Mosaic of pictures.

    :tags:
    :categories:

    Usage::

    Related Pages:

    Underlying HTML Objects:

    Templates:

    :param icons: List. Optional. The list with the pictures
    :param columns: Integer. Optional. The number of column for the mosaic component
    :param width: Tuple. Optional. A tuple with the integer for the component width and its unit
    :param height: Tuple. Optional. A tuple with the integer for the component height and its unit
    :param options: Dictionary. Optional. Specific Python options available for this component
    :param profile: Boolean | Dictionary. Optional. A flag to set the component performance storage
    """
        dflt_options = {}
        if options is not None:
            dflt_options.update(options)
        grid = self.page.ui.grid(width=width, height=height, options=dflt_options, profile=profile)
        grid.style.css.margin_top = 20
        grid.style.css.overflow = 'hidden'
        grid.style.css.margin_bottom = 20
        row = self.page.ui.row(options=dflt_options)
        grid.icons = []
        grid.texts = {}
        for (i, icon) in enumerate(icons):
            if dflt_options.get('max') is not None and len(grid.icons) > dflt_options.get('max'):
                break
            if i % columns == 0:
                grid.add(row)
                row = self.page.ui.row(options=dflt_options)
            text = None
            if not hasattr(icon, 'options'):
                if isinstance(icon, dict):
                    if 'html_code' not in icon:
                        icon['html_code'] = '%s_%s' % (grid.htmlCode, i)
                    if 'align' not in icon:
                        icon['align'] = 'center'
                    if 'text' in icon:
                        text = self.page.ui.text(icon['text'], options=dflt_options)
                        text.style.css.bold()
                        text.style.css.white_space = 'nowrap'
                        grid.texts[i] = text
                        del icon['text']
                    icon = self.page.ui.icon(**icon)
                else:
                    icon = self.page.ui.icon(icon, html_code='%s_%s' % (grid.htmlCode, i), align='center')
                icon.style.css.font_factor(15)
                icon.style.css.text_align = 'center'
                grid.icons.append(icon)
            if text is not None:
                text.style.css.display = 'inline-block'
                text.style.css.width = '100%'
                text.style.css.text_align = 'center'
                row.add(self.page.ui.col([icon, text], align='center', options=dflt_options))
            else:
                row.add(icon)
            row.attr['class'].add('mt-3')
            icon.parent = row[-1]
        if len(row):
            for i in range(columns - len(row)):
                row.add(self.page.ui.text('&nbsp;'))
            row.attr['class'].add('mt-3')
            grid.add(row)
        grid.style.css.color = self.page.theme.greys[6]
        grid.style.css.padding_top = 5
        grid.style.css.padding_bottom = 5
        return grid

class Toggles:

    def __init__(self, ui):
        self.page = ui.page

    def collapse(self, icon_on='compress', icon_off='fas fa-expand', family=None, width=(None, 'px'), html_code=None, height=(None, 'px'), color=None, tooltip=None, align='left', options=None, profile=None):
        """

    Usage::

      page.ui.images.icon("fab fa-angellist")

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlImage.Icon`

    Related Pages:

      https://fontawesome.com/icons?m=free

    :param icon_on: Optional. The component icon content from font-awesome references
    :param icon_off: Optional. The component icon content from font-awesome references
    :param family: Optional. The Icon library reference
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param color: Optional. The font color in the component. Default inherit
    :param tooltip: Optional. A string with the value of the tooltip
    :param align: Optional. The text-align property within this component
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    """
        width = Arguments.size(width, 'px')
        height = Arguments.size(height, 'px')
        options = options or {}
        options['icon_family'] = family or self.page.icons.family
        html_icon = html.HtmlImage.IconToggle(self.page, icon_on, width=width, height=height, color=color, tooltip=tooltip, options=options, html_code=html_code, profile=profile)
        html_icon.icon_on = icon_on
        html_icon.icon_off = icon_off
        html.Html.set_component_skin(html_icon)
        return html_icon

    def lock(self, icon_on='lock_open', icon_off='fas fa-lock', family=None, width=(None, 'px'), html_code=None, height=(None, 'px'), color=None, tooltip=None, align='left', options=None, profile=None):
        """
    Add a lock toggle button.

    Usage::

      page.ui.icons.toggles.lock()

    Underlying HTML Objects:

      - :class:`epyk.core.html.HtmlImage.Icon`

    Related Pages:

      https://fontawesome.com/icons?m=free

    :param icon_on: Optional. The component icon content from font-awesome references
    :param icon_off: Optional. The component icon content from font-awesome references
    :param family: Optional. The Icon library reference
    :param html_code: Optional. An identifier for this component (on both Python and Javascript side)
    :param width: Optional. A tuple with the integer for the component width and its unit
    :param height: Optional. A tuple with the integer for the component height and its unit
    :param color: Optional. The font color in the component. Default inherit
    :param tooltip: Optional. A string with the value of the tooltip
    :param align: Optional. The text-align property within this component
    :param options: Optional. Specific Python options available for this component
    :param profile: Optional. A flag to set the component performance storage
    """
        width = Arguments.size(width, 'px')
        height = Arguments.size(height, 'px')
        options = options or {}
        options['icon_family'] = family or self.page.icons.family
        html_icon = html.HtmlImage.IconToggle(self.page, icon_on, width=width, height=height, color=color, tooltip=tooltip, options=options, html_code=html_code, profile=profile)
        html_icon.icon_on = icon_on
        html_icon.icon_off = icon_off
        html.Html.set_component_skin(html_icon)
        return html_icon