from epyk.core.css.styles import GrpCls
from epyk.core.css.styles.attributes import Attrs
from epyk.core.css.styles.attributes import AttrClsLayout
from epyk.core.css import Classes

class ClassStandard(GrpCls.ClassHtml):

    @property
    def css(self) -> Attrs:
        """
    Description:
    -----------
    Property to the underlying CSS definition to be added to the style HTML tag of a component.

    Usage::

      self.css.border = "1px solid black"

    :rtype: Attrs
    """
        if self._css_struct is None:
            self._css_struct = Attrs(self.component)
        return self._css_struct

    @property
    def css_class(self) -> Classes.CatalogDiv.CatalogDiv:
        """
    Description:
    -----------
    The internal class used to put a custom Style to this object.
    Only 1 CSS class can be added to an HTML object.

    :rtype: Classes.CatalogDiv.CatalogDiv
    """
        if self._css_class is None:
            self._css_class = Classes.CatalogDiv.CatalogDiv(self.component.page, self.classList['main'], component=self.component).margin_vertical()
        return self._css_class

class ClassHelp(GrpCls.ClassHtml):

    @property
    def css(self) -> AttrClsLayout.AttrHelp:
        """
    Description:
    -----------
    Property to the underlying CSS definition to be added to the style HTML tag of a component.

    Usage::

      self.css.border = "1px solid black"

    :rtype: AttrClsLayout.AttrHelp
    """
        if self._css_struct is None:
            self._css_struct = AttrClsLayout.AttrHelp(self.component)
        return self._css_struct

    @property
    def css_class(self) -> Classes.CatalogDiv.CatalogDiv:
        """
    Description:
    -----------
    The internal class used to put a custom Style to this object.
    Only 1 CSS class can be added to an HTML object.

    :rtype: Classes.CatalogDiv.CatalogDiv
    """
        if self._css_class is None:
            self._css_class = Classes.CatalogDiv.CatalogDiv(self.component.page, self.classList['main'], component=self.component).margin_vertical()
        return self._css_class