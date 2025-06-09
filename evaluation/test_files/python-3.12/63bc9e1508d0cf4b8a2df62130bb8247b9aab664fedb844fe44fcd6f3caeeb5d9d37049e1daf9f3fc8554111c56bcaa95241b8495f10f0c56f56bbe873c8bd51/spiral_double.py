from __future__ import annotations
import gdsfactory as gf
from gdsfactory.components import bend_circular
from gdsfactory.path import spiral_archimedean

@gf.cell
def spiral_double(min_bend_radius: float=10.0, separation: float=2.0, number_of_loops: float=3, npoints: int=1000, cross_section: gf.types.CrossSectionSpec='strip', bend: gf.types.ComponentSpec=bend_circular) -> gf.Component:
    """Returns a spiral double (spiral in, and then out).

    Args:
        min_bend_radius: inner radius of the spiral.
        separation: separation between the loops.
        number_of_loops: number of loops per spiral.
        npoints: points for the spiral.
        cross_section: cross-section to extrude the structure with.
        bend: factory for the bends in the middle of the double spiral.
    """
    component = gf.Component()
    bend = gf.get_component(bend, radius=min_bend_radius / 2, angle=180, cross_section=cross_section)
    bend1 = component.add_ref(bend).mirror()
    bend2 = component.add_ref(bend)
    bend2.connect('o2', bend1.ports['o1'])
    path = spiral_archimedean(min_bend_radius=min_bend_radius, separation=separation, number_of_loops=number_of_loops, npoints=npoints)
    path.start_angle = 0
    path.end_angle = 0
    spiral = path.extrude(cross_section=cross_section)
    spiral1 = component.add_ref(spiral).connect('o1', bend1.ports['o2'])
    spiral2 = component.add_ref(spiral).connect('o1', bend2.ports['o1'])
    component.add_port('o1', port=spiral1.ports['o2'])
    component.add_port('o2', port=spiral2.ports['o2'])
    component.info['length'] = float(path.length() + bend.info['length']) * 2
    return component
if __name__ == '__main__':
    c = spiral_double(min_bend_radius=10, separation=2, number_of_loops=3, npoints=1000, cross_section='nitride')
    print(c.ports['o1'].orientation)
    print(c.ports['o2'].orientation)
    c.show(show_ports=True)