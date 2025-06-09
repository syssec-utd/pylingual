import random
from itertools import combinations
from pathlib import Path
from smarts.sstudio import gen_scenario
from smarts.sstudio.types import Flow, Mission, Route, Scenario, Traffic, TrafficActor
normal = TrafficActor(name='car')
route_opt = [(0, 0), (1, 1), (2, 2)]
min_flows = 2
max_flows = 3
route_comb = [com for elems in range(min_flows, max_flows + 1) for com in combinations(route_opt, elems)] * 100
traffic = {}
for (name, routes) in enumerate(route_comb):
    traffic[str(name)] = Traffic(flows=[Flow(route=Route(begin=('gneE3', start_lane, 0), end=('gneE4', end_lane, 'max')), rate=60 * random.uniform(10, 20), begin=random.uniform(0, 5), end=60 * 15, actors={normal: 1}, randomly_spaced=True) for (start_lane, end_lane) in routes])
route = Route(begin=('gneE6', 0, 10), end=('gneE4', 2, 'max'))
ego_missions = [Mission(route=route, start_time=15)]
gen_scenario(scenario=Scenario(traffic=traffic, ego_missions=ego_missions), output_dir=Path(__file__).parent)