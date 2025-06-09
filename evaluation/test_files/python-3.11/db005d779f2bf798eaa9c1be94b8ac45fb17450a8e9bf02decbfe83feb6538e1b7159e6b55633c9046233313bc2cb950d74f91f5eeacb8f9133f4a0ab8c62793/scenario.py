import random
from itertools import combinations
from pathlib import Path
from smarts.sstudio import gen_scenario
from smarts.sstudio.types import Flow, Mission, Route, Scenario, Traffic, TrafficActor
normal = TrafficActor(name='car')
vertical_routes = [('E0', 0, 'E3', 0), ('-E3', 0, '-E0', 0)]
horizontal_routes = [('E4', 0, 'E1', 0), ('E4', 1, 'E1', 1), ('-E1', 0, '-E4', 0), ('-E1', 1, '-E4', 1)]
turn_left_routes = [('E0', 0, 'E1', 1), ('-E3', 0, '-E4', 1), ('-E1', 1, 'E3', 0), ('E4', 1, '-E0', 0)]
turn_right_routes = [('E0', 0, '-E4', 0), ('-E3', 0, 'E1', 0), ('-E1', 0, '-E0', 0), ('E4', 0, 'E3', 0)]
all_routes = vertical_routes + horizontal_routes + turn_left_routes + turn_right_routes
route_comb = [com for elems in range(1, 5) for com in combinations(all_routes, elems)]
traffic = {}
for name, routes in enumerate(route_comb):
    traffic[str(name)] = Traffic(flows=[Flow(route=Route(begin=(start_edge, start_lane, 0), end=(end_edge, end_lane, 'max')), rate=60 * random.uniform(5, 10), begin=random.uniform(0, 3), end=60 * 15, actors={normal: 1}) for start_edge, start_lane, end_edge, end_lane in routes])
route = Route(begin=('E0', 0, 5), end=('E1', 0, 'max'))
ego_missions = [Mission(route=route, start_time=4)]
gen_scenario(scenario=Scenario(traffic=traffic, ego_missions=ego_missions), output_dir=Path(__file__).parent)