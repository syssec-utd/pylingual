import gdsfactory as gf
from gdsfactory.component import Component
from gdsfactory.components import bend_s
from gdsfactory.types import CrossSectionSpec

@gf.cell
def coupler_full(coupling_length: float=40.0, dx: float=10.0, dy: float=5.0, gap: float=0.5, dw: float=0.1, cross_section: CrossSectionSpec='strip', **kwargs) -> Component:
    """Adiabatic Full coupler.

    Design based on asymmetric adiabatic full
    coupler designs, such as the one reported in 'Integrated Optic Adiabatic
    Devices on Silicon' by Y. Shani, et al (IEEE Journal of Quantum
    Electronics, Vol. 27, No. 3 March 1991).

    1. is the first half of the input S-bend straight where the
    input straights widths taper by +dw and -dw,
    2. is the second half of the S-bend straight with constant,
    unbalanced widths,
    3. is the coupling region where the straights from unbalanced widths to
    balanced widths to reverse polarity unbalanced widths,
    4. is the fixed width straight that curves away from the coupling region,
    5.is the final curve where the straights taper back to the regular width
    specified in the straight template.

    Args:
        coupling_length: Length of the coupling region in um.
        dx: Length of the bend regions in um.
        dy: Port-to-port distance between the bend regions in um.
        gap: Distance between the two straights in um.
        dw: delta width. Top arm tapers to width - dw, bottom to width + dw in um.
        cross_section: cross-section spec.

    Keyword Args:
        cross_section kwargs.
    """
    c = gf.Component()
    x = gf.get_cross_section(cross_section=cross_section, **kwargs)
    x_top = x.copy(width=x.width + dw)
    x_bottom = x.copy(width=x.width - dw)
    taper_top = c << gf.components.taper(length=coupling_length, width1=x_top.width, width2=x_bottom.width, cross_section=x_top)
    taper_bottom = c << gf.components.taper(length=coupling_length, width1=x_bottom.width, width2=x_top.width, cross_section=x_bottom)
    bend_input_top = c << bend_s(size=(dx, (dy - gap - x_top.width) / 2.0), cross_section=x_top).mirror()
    bend_input_top.movey(origin=0, destination=(x_top.width + gap) / 2.0)
    bend_input_bottom = c << bend_s(size=(dx, (-dy + gap + x_bottom.width) / 2.0), cross_section=x_bottom).mirror()
    bend_input_bottom.movey(origin=0, destination=-(x_bottom.width + gap) / 2.0)
    taper_top.connect('o1', bend_input_top.ports['o1'])
    taper_bottom.connect('o1', bend_input_bottom.ports['o1'])
    bend_output_top = c << bend_s(size=(dx, (dy - gap - x_top.width) / 2.0), cross_section=x_bottom)
    bend_output_top.move(destination=taper_top.ports['o2'])
    bend_output_bottom = c << bend_s(size=(dx, (-dy + gap + x_bottom.width) / 2.0), cross_section=x_top)
    bend_output_bottom.move(destination=taper_bottom.ports['o2'])
    bend_output_top.connect('o2', taper_top.ports['o2'])
    bend_output_bottom.connect('o2', taper_bottom.ports['o2'])
    c.absorb(bend_input_bottom)
    c.absorb(bend_input_top)
    c.absorb(bend_output_top)
    c.absorb(bend_output_bottom)
    c.absorb(taper_top)
    c.absorb(taper_bottom)
    if x.add_bbox:
        c = x.add_bbox(c)
    if x.info:
        c.info = x.info
    c.add_port('o1', port=bend_input_bottom.ports['o2'])
    c.add_port('o2', port=bend_input_top.ports['o2'])
    c.add_port('o3', port=bend_output_top.ports['o1'])
    c.add_port('o4', port=bend_output_bottom.ports['o1'])
    return c
if __name__ == '__main__':
    c = coupler_full(coupling_length=40, gap=0.2, dw=0.1, cladding_layers=[(111, 0)], cladding_offsets=[3])
    c.show(show_ports=True)