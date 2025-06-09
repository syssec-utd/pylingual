from atom.api import Bool, Int, Typed
from enaml.core.declarative import d_, observe
from enaml.layout.layout_helpers import align, hbox
from enaml.layout.spacers import Spacer
from .container import Container

class HGroup(Container):
    """ A Container subclass which groups child widgets horizontally.

    User constraints are applied *in addition* to the horizontal group
    constraints. Widgets are aligned along their vertical center.

    """
    spacing = d_(Int(10))
    leading_spacer = d_(Typed(Spacer))
    trailing_spacer = d_(Typed(Spacer))
    align_widths = d_(Bool(True))

    @observe('spacing', 'leading_spacer', 'trailing_spacer', 'align_widths')
    def _layout_invalidated(self, change):
        """ A private observer which invalidates the layout.

        """
        super(HGroup, self)._layout_invalidated(change)

    def layout_constraints(self):
        """ The constraints generation for a HGroup.

        This method supplies horizontal group constraints for the
        children of the container in addition to any user-supplied
        constraints.

        This method cannot be overridden from Enaml syntax.

        """
        widgets = self.visible_widgets()
        items = [self.leading_spacer] + widgets + [self.trailing_spacer]
        cns = self.constraints[:]
        cns.append(hbox(*items, spacing=self.spacing))
        cns.append(align('v_center', *widgets))
        if self.align_widths:
            cns.append(align('width', *widgets))
        return cns