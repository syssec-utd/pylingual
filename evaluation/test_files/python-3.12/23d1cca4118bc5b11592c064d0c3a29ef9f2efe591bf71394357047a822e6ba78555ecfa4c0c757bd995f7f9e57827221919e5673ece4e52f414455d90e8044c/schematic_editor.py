from pathlib import Path
from typing import Optional, Union
import ipywidgets as widgets
import yaml
import gdsfactory as gf
from . import circuitviz
from .picmodel import PicYamlConfiguration, Route, RouteSettings, SchematicConfiguration

class SchematicEditor:

    def __init__(self, filename: Union[str, Path], pdk: Optional[gf.Pdk]=None):
        """An interactive Schematic editor, meant to be used from a Jupyter Notebook.

        Args:
            filename: the filename or path to use for the input/output schematic
            pdk: the PDK to use (uses the current active PDK if None)
        """
        if isinstance(filename, Path):
            filepath = filename
        else:
            filepath = Path(filename)
        self.path = filepath
        if pdk:
            self.pdk = pdk
        else:
            self.pdk = gf.get_active_pdk()
        self.component_list = list(gf.get_active_pdk().cells.keys())
        self.on_instance_added = []
        self.on_instance_removed = []
        self.on_settings_updated = []
        self.on_nets_modified = []
        self._notebook_handle = None
        self._inst_boxes = []
        self._connected_ports = {}
        if filepath.is_file():
            self.load_netlist()
        else:
            self._schematic = SchematicConfiguration(instances={}, schematic_placements={}, nets=[], ports={})
            self._instance_grid = widgets.VBox()
            self._net_grid = widgets.VBox()
        first_inst_box = self._get_instance_selector()
        first_inst_box.children[0].observe(self._add_row_when_full, names=['value'])
        first_inst_box.children[1].observe(self._on_instance_component_modified, names=['value'])
        self._instance_grid.children += (first_inst_box,)
        first_net_box = self._get_net_selector()
        first_net_box.children[0].observe(self._add_net_row_when_full, names=['value'])
        self._net_grid.children += (first_net_box,)
        for row in self._net_grid.children:
            for child in row.children:
                child.observe(self._on_net_modified, names=['value'])
        self.on_instance_added.append(self.write_netlist)
        self.on_settings_updated.append(self.write_netlist)
        self.on_nets_modified.append(self.write_netlist)
        self.on_instance_removed.append(self.write_netlist)
        self.on_instance_added.append(self._update_instance_options)
        self.on_instance_added.append(self._make_instance_removable)

    def _get_instance_selector(self, inst_name=None, component_name=None):
        component_selector = widgets.Combobox(placeholder='Pick a component', options=self.component_list, ensure_option=True, disabled=False)
        instance_box = widgets.Text(placeholder='Enter a name', disabled=False)
        component_selector._instance_selector = instance_box
        can_remove = False
        if inst_name:
            instance_box.value = inst_name
        if component_name:
            component_selector.value = component_name
            can_remove = True
        remove_button = widgets.Button(description='Remove', icon='xmark', disabled=not can_remove, tooltip='Remove this instance from the schematic', button_style='')
        remove_button.on_click(self._on_remove_button_clicked)
        row = widgets.Box([instance_box, component_selector, remove_button])
        row._component_selector = component_selector
        row._instance_box = instance_box
        row._remove_button = remove_button
        remove_button._row = row
        instance_box._row = row
        component_selector._row = row
        return row

    def _update_instance_options(self, **kwargs):
        inst_names = self._schematic.instances.keys()
        for inst_box in self._inst_boxes:
            inst_box.options = list(inst_names)

    def _make_instance_removable(self, instance_name, **kwargs):
        for row in self._instance_grid.children:
            if row._instance_box.value == instance_name:
                row._remove_button.disabled = False
                return

    def _get_net_selector(self, inst1=None, port1=None, inst2=None, port2=None):
        inst_names = list(self._schematic.instances.keys())
        inst1_selector = widgets.Combobox(placeholder='inst1', options=inst_names, ensure_option=True, disabled=False)
        inst2_selector = widgets.Combobox(placeholder='inst2', options=inst_names, ensure_option=True, disabled=False)
        self._inst_boxes.extend([inst1_selector, inst2_selector])
        port1_selector = widgets.Text(placeholder='port1', disabled=False)
        port2_selector = widgets.Text(placeholder='port2', disabled=False)
        if inst1:
            inst1_selector.value = inst1
        if inst2:
            inst2_selector.value = inst2
        if port1:
            port1_selector.value = port1
        if port2:
            port2_selector.value = port2
        return widgets.Box([inst1_selector, port1_selector, inst2_selector, port2_selector])

    def _add_row_when_full(self, change):
        if change['old'] == '' and change['new'] != '':
            this_box = change['owner']
            last_box = self._instance_grid.children[-1].children[0]
            if this_box is last_box:
                new_row = self._get_instance_selector()
                self._instance_grid.children += (new_row,)
                new_row.children[0].observe(self._add_row_when_full, names=['value'])
                new_row.children[1].observe(self._on_instance_component_modified, names=['value'])
                new_row._associated_component = None

    def _add_net_row_when_full(self, change):
        if change['old'] == '' and change['new'] != '':
            this_box = change['owner']
            last_box = self._net_grid.children[-1].children[0]
            if this_box is last_box:
                new_row = self._get_net_selector()
                self._net_grid.children += (new_row,)
                new_row.children[0].observe(self._add_net_row_when_full, names=['value'])
                for child in new_row.children:
                    child.observe(self._on_net_modified, names=['value'])
                new_row._associated_component = None

    def _update_schematic_plot(self, **kwargs):
        circuitviz.update_schematic_plot(schematic=self._schematic, instances=self.instances)

    def _on_instance_component_modified(self, change):
        this_box = change['owner']
        inst_box = this_box._instance_selector
        inst_name = inst_box.value
        component_name = this_box.value
        if change['old'] == '':
            if change['new'] != '':
                self.add_instance(instance_name=inst_name, component=component_name)
        elif change['new'] != change['old']:
            self.update_component(instance=inst_name, component=component_name)

    def _on_remove_button_clicked(self, button):
        row = button._row
        self.remove_instance(instance_name=row._instance_box.value)
        self._instance_grid.children = tuple((child for child in self._instance_grid.children if child is not row))

    def _get_data_from_row(self, row):
        inst_name, component_name = (w.value for w in row.children)
        return {'instance_name': inst_name, 'component_name': component_name}

    def _get_instance_data(self):
        inst_data = [self._get_data_from_row(row) for row in self._instance_grid.children]
        inst_data = [d for d in inst_data if d['instance_name'] != '']
        return inst_data

    def _get_net_from_row(self, row):
        values = [c.value for c in row.children]
        return values

    def _get_net_data(self):
        net_data = [self._get_net_from_row(row) for row in self._net_grid.children]
        net_data = [d for d in net_data if '' not in d]
        return net_data

    def _on_net_modified(self, change):
        if change['new'] != change['old']:
            net_data = self._get_net_data()
            new_nets = [[f'{n[0]},{n[1]}', f'{n[2]},{n[3]}'] for n in net_data]
            connected_ports = {}
            for n1, n2 in new_nets:
                connected_ports[n1] = n2
                connected_ports[n2] = n1
                self._connected_ports = connected_ports
            old_nets = self._schematic.nets
            self._schematic.nets = new_nets
            for callback in self.on_nets_modified:
                callback(old_nets=old_nets, new_nets=new_nets)

    @property
    def instance_widget(self):
        return self._instance_grid

    @property
    def net_widget(self):
        return self._net_grid

    def visualize(self):
        circuitviz.show_netlist(self.schematic, self.instances, self.path)
        self.on_instance_added.append(self._update_schematic_plot)
        self.on_settings_updated.append(self._update_schematic_plot)
        self.on_nets_modified.append(self._update_schematic_plot)
        self.on_instance_removed.append(self._update_schematic_plot)

    @property
    def instances(self):
        insts = {}
        inst_data = self._schematic.instances
        for inst_name, inst in inst_data.items():
            component_spec = inst.dict()
            insts[inst_name] = gf.get_component(component_spec)
        return insts

    def add_instance(self, instance_name: str, component: Union[str, gf.Component]):
        self._schematic.add_instance(name=instance_name, component=component)
        for callback in self.on_instance_added:
            callback(instance_name=instance_name)

    def remove_instance(self, instance_name: str):
        self._schematic.instances.pop(instance_name)
        if instance_name in self._schematic.placements:
            self._schematic.placements.pop(instance_name)
        for callback in self.on_instance_removed:
            callback(instance_name=instance_name)

    def update_component(self, instance, component):
        self._schematic.instances[instance].component = component
        self.update_settings(instance=instance, clear_existing=True)

    def update_settings(self, instance, clear_existing: bool=False, **settings):
        old_settings = self._schematic.instances[instance].settings.copy()
        if clear_existing:
            self._schematic.instances[instance].settings.clear()
        if settings:
            self._schematic.instances[instance].settings.update(settings)
        for callback in self.on_settings_updated:
            callback(instance_name=instance, settings=settings, old_settings=old_settings)

    def add_net(self, inst1, port1, inst2, port2):
        p1 = f'{inst1},{port1}'
        p2 = f'{inst2},{port2}'
        if p1 in self._connected_ports:
            if self._connected_ports[p1] == p2:
                return
            else:
                current_port = self._connected_ports[p1]
                raise ValueError(f"{p1} is already connected to {current_port}. Can't connect to {p2}")
        self._connected_ports[p1] = p2
        self._connected_ports[p2] = p1
        old_nets = self._schematic.nets.copy()
        self._schematic.nets.append([p1, p2])
        new_row = self._get_net_selector(inst1=inst1, inst2=inst2, port1=port1, port2=port2)
        existing_rows = self._net_grid.children
        new_rows = existing_rows[:-1] + (new_row, existing_rows[-1])
        self._net_grid.children = new_rows
        for callback in self.on_nets_modified:
            callback(old_nets=old_nets, new_nets=self._schematic.nets)

    def get_netlist(self):
        return self._schematic.dict()

    @property
    def schematic(self):
        return self._schematic

    def write_netlist(self, **kwargs):
        netlist = self.get_netlist()
        with open(self.path, mode='w') as f:
            yaml.dump(netlist, f, default_flow_style=None, sort_keys=False)

    def load_netlist(self):
        with open(self.path) as f:
            netlist = yaml.safe_load(f)
        schematic = SchematicConfiguration.parse_obj(netlist)
        self._schematic = schematic
        instances = netlist['instances']
        nets = netlist.get('nets', [])
        new_rows = []
        for inst_name, inst in instances.items():
            component_name = inst['component']
            new_row = self._get_instance_selector(inst_name=inst_name, component_name=component_name)
            new_row.children[0].observe(self._add_row_when_full, names=['value'])
            new_row.children[1].observe(self._on_instance_component_modified, names=['value'])
            new_rows.append(new_row)
        self._instance_grid = widgets.VBox(new_rows)
        unpacked_nets = []
        net_rows = []
        for net in nets:
            unpacked_net = []
            for net_entry in net:
                inst_name, port_name = net_entry.split(',')
                unpacked_net.extend([inst_name, port_name])
            unpacked_nets.append(unpacked_net)
            net_rows.append(self._get_net_selector(*unpacked_net))
            self._connected_ports[net[0]] = net[1]
            self._connected_ports[net[1]] = net[0]
        self._net_grid = widgets.VBox(net_rows)

    def instantiate_layout(self, output_filename, default_router='get_bundle', default_cross_section='strip'):
        schematic = self._schematic
        routes = {}
        for inet, net in enumerate(schematic.nets):
            route = Route(routing_strategy=default_router, links={net[0]: net[1]}, settings=RouteSettings(cross_section=default_cross_section))
            routes[f'r{inet}'] = route
        pic_conf = PicYamlConfiguration(instances=schematic.instances, placements=schematic.placements, routes=routes, ports=schematic.ports)
        pic_conf.to_yaml(output_filename)
        return pic_conf