from typing import Callable, Optional
import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.components.bend_s import bend_s
from gdsfactory.components.straight import straight
from gdsfactory.port import select_ports_optical
from gdsfactory.types import ComponentSpec, CrossSectionSpec

@gf.cell
def fanout2x2(component: ComponentSpec=straight, port_spacing: float=20.0, bend_length: Optional[float]=None, npoints: int=101, select_ports: Callable=select_ports_optical, cross_section: CrossSectionSpec='strip', **kwargs) -> Component:
    """Returns component with Sbend fanout routes.

    Args:
        component: to fanout.
        port_spacing: for the returned component.
        bend_length: length of the bend (defaults to port_spacing).
        npoints: for sbend.
        select_ports: function to select  optical_ports ports.
        cross_section: cross_section spec.
        kwargs: cross_section settings.

    .. plot::
        :include-source:

        import gdsfactory as gf
        c = gf.components.nxn(west=2, east=2)

        cc = gf.routing.fanout2x2(component=c, port_spacing=20)
        cc.plot()

    """
    c = gf.Component()
    component = gf.get_component(component)
    component.component = component
    ref = c << component
    ref.movey(-ref.y)
    if bend_length is None:
        bend_length = port_spacing
    dx = bend_length
    y = port_spacing / 2.0
    p_w0 = ref.ports['o1'].center
    p_w1 = ref.ports['o2'].center
    p_e1 = ref.ports['o3'].center
    p_e0 = ref.ports['o4'].center
    y0 = p_e1[1]
    dy = y - y0
    x = gf.get_cross_section(cross_section, **kwargs)
    bend = bend_s(size=(dx, dy), nb_points=npoints, cross_section=x)
    b_tr = bend.ref(port_id='o1', position=p_e1)
    b_br = bend.ref(port_id='o1', position=p_e0, v_mirror=True)
    b_tl = bend.ref(port_id='o1', position=p_w1, h_mirror=True)
    b_bl = bend.ref(port_id='o1', position=p_w0, rotation=180)
    c.add([b_tr, b_br, b_tl, b_bl])
    c.add_port('o1', port=b_bl.ports['o2'])
    c.add_port('o2', port=b_tl.ports['o2'])
    c.add_port('o3', port=b_tr.ports['o2'])
    c.add_port('o4', port=b_br.ports['o2'])
    c.min_bend_radius = bend.info['min_bend_radius']
    optical_ports = select_ports(ref.ports)
    for port_name in ref.ports.keys():
        if port_name not in optical_ports:
            c.add_port(port_name, port=ref.ports[port_name])
    c.copy_child_info(component)
    return c
if __name__ == '__main__':
    c = gf.components.nxn(west=2, east=2)
    cc = fanout2x2(component=c, port_spacing=20)
    print(cc.ports['o3'].y - cc.ports['o4'].y)
    cc.show(show_ports=True)