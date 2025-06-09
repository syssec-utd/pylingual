from __future__ import annotations
from typing import TYPE_CHECKING
from . import _utils
if TYPE_CHECKING:
    from tabulous.widgets import TableViewerBase

def set_popup_mode(viewer: TableViewerBase):
    """Popup table."""
    table = _utils.get_table(viewer)
    table.view_mode = 'popup'

def set_dual_v_mode(viewer: TableViewerBase):
    """Vertical dual-view"""
    table = _utils.get_table(viewer)
    table.view_mode = 'vertical'

def set_dual_h_mode(viewer: TableViewerBase):
    """Horizontal dual-view"""
    table = _utils.get_table(viewer)
    table.view_mode = 'horizontal'

def reset_view_mode(viewer: TableViewerBase):
    """Reset view mode"""
    table = _utils.get_table(viewer)
    table.view_mode = 'normal'