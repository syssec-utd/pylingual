import random
import numpy as np
import itertools
from functools import reduce
from dataclasses import asdict
from typing import Tuple
from .ParameterDefinitions import Parameters, JsonFormat, fitness_definitions
from .GraphicUserInterface import Visualizer
from .Network import Server, request_abaqus
from .FileIO import pickle_io, pickles_io, remove_file, get_sorted_file_numbers_from_pattern
from .PostProcessing import evaluate_all_fitness_values, selection
from .MutateAndValidate import mutate_and_validate_topology

class NSGAModel:

    def __init__(self, params: Parameters, material_properties: dict, visualizer: Visualizer=None, random_topology_density: float=0.5):
        self.params = params
        self.visualizer = visualizer
        self.material_properties = material_properties
        self.random_topology_density = random_topology_density

    def load_parent_data(self, gen: int, server: Server) -> Tuple[np.ndarray, dict]:
        try:
            parent_topologies = pickle_io(f'Topologies_{gen}', mode='r')['parent']
        except FileNotFoundError or KeyError:
            parent_topologies = random_parent_generation(density=self.random_topology_density, params=self.params, save_file_as=f'Topologies_{gen}')
        try:
            parent_results = pickle_io(f'FieldOutput_{gen}', mode='r')
        except FileNotFoundError:
            json_data = asdict(JsonFormat(start_topology_from=1, topologies_key='parent', topologies_file_name=f'Topologies_{gen}', exit_abaqus=False))
            json_data.update(asdict(self.params))
            json_data.update(self.material_properties)
            request_abaqus(dict_data=json_data, server=server)
            parent_results = pickle_io(f'FieldOutput_offspring_{gen}', mode='r')
            remove_file(f'FieldOutput_offspring_{gen}')
            pickle_io(f'FieldOutput_{gen}', mode='w', to_dump=parent_results)
            self.visualizer.visualize(params=self.params, gen=gen - 1, use_manual_rp=False)
        assert len(parent_topologies) == len(parent_results)
        return (parent_topologies, parent_results)

    def determine_where_abaqus_start(self) -> Tuple[int, int]:
        offspring_results_file_numbers = get_sorted_file_numbers_from_pattern('FieldOutput_offspring_\\d+')
        if len(offspring_results_file_numbers) == 0:
            return (1, 1)
        else:
            last_offspring_results_file_number = offspring_results_file_numbers[-1]
            last_offspring_results = pickle_io(f'FieldOutput_offspring_{last_offspring_results_file_number}', mode='r')
            if len(last_offspring_results) < self.params.end_pop:
                needed_to_start_at_offspring = len(last_offspring_results) + 1
                return (last_offspring_results_file_number, needed_to_start_at_offspring)
            else:
                return (last_offspring_results_file_number + 1, 1)

    def generate_offspring_topologies(self, gen: int, server: Server) -> np.ndarray:
        (parent_topologies, parent_results) = self.load_parent_data(gen=gen, server=server)
        topologies = pickle_io(f'Topologies_{gen}', mode='r')
        if 'offspring' in topologies.keys():
            offspring_topologies = pickle_io(f'Topologies_{gen}', mode='r')['offspring']
        else:
            offspring_topologies = generate_offspring(gen=gen, topo_parents=parent_topologies, params=self.params, save_file_as=f'Topologies_{gen}')
        assert len(parent_topologies) == len(parent_results) == len(offspring_topologies)
        return offspring_topologies

    def run_a_generation(self, running_gen: int, start_offspring_from: int, server: Server):
        (parent_topologies, parent_results) = self.load_parent_data(gen=running_gen, server=server)
        offspring_topologies = self.generate_offspring_topologies(gen=running_gen, server=server)
        json_data = asdict(JsonFormat(start_topology_from=start_offspring_from, topologies_key='offspring', topologies_file_name=f'Topologies_{running_gen}', exit_abaqus=False))
        json_data.update(asdict(self.params))
        json_data.update(self.material_properties)
        request_abaqus(dict_data=json_data, server=server)
        offspring_results = pickle_io(f'FieldOutput_offspring_{running_gen}', mode='r')
        all_topologies = np.vstack((parent_topologies, offspring_topologies))
        all_results = parent_results.copy()
        all_results.update({entity_num + len(parent_results): offspring_results[entity_num] for entity_num in sorted(offspring_results.keys())})
        all_fitness_values = evaluate_all_fitness_values(fitness_definitions=fitness_definitions, params_dict=asdict(self.params), results=all_results, topologies=all_topologies)
        pareto_indices = selection(all_fitness_values=all_fitness_values, selected_size=self.params.end_pop)
        selected_topologies = all_topologies[pareto_indices]
        selected_results = {entity_num: all_results[pareto_idx + 1] for (entity_num, pareto_idx) in enumerate(pareto_indices, start=1)}
        assert len(selected_topologies) == len(selected_results)
        pickle_io(f'Topologies_{running_gen + 1}', mode='w', to_dump={'parent': selected_topologies})
        pickle_io(f'FieldOutput_{running_gen + 1}', mode='w', to_dump=selected_results)
        if self.visualizer is not None:
            self.visualizer.visualize(params=self.params, gen=running_gen, use_manual_rp=False)

    def run(self, server):
        (start_gen, start_offspring) = self.determine_where_abaqus_start()
        for gen in range(start_gen, self.params.end_gen):
            self.run_a_generation(running_gen=gen, start_offspring_from=start_offspring, server=server)
            start_offspring = 1
        request_abaqus(dict_data={'exit_abaqus': True}, server=server)

def find_where_same_array_locates(arr_to_find: np.ndarray, big_arr: np.ndarray) -> np.ndarray:
    axis_range = tuple((dim for dim in range(len(big_arr.shape) - len(arr_to_find.shape), len(big_arr.shape))))
    return np.argwhere(np.all(big_arr == arr_to_find, axis=axis_range))

def get_cutting_section_and_candidates(topologies: np.ndarray) -> Tuple[int, np.ndarray]:
    topologies_flattened = topologies.reshape((len(topologies), -1))
    possible_cutting_sections = np.random.permutation(topologies_flattened.shape[1])
    for possible_cutting_section in possible_cutting_sections:
        candidates_for_cutting = np.empty((0,), dtype=int)
        for topo_idx in range(len(topologies)):
            if topologies_flattened[topo_idx, possible_cutting_section] == 1:
                candidates_for_cutting = np.hstack((candidates_for_cutting, topo_idx))
        if len(candidates_for_cutting) >= 2:
            return (possible_cutting_section, candidates_for_cutting)
    raise RuntimeError

def get_candidate_pairs(candidates):
    candidates_results = list(itertools.combinations(candidates, 2))
    random.shuffle(candidates_results)
    return candidates_results

def crossover(chromosome_1, chromosome_2, cutting_section):
    chromosome_1_flattened = chromosome_1.flatten()
    chromosome_2_flattened = chromosome_2.flatten()
    cross_overed_chromosome_1 = np.empty_like(chromosome_1_flattened)
    cross_overed_chromosome_2 = np.empty_like(chromosome_2_flattened)
    cross_overed_chromosome_1[0:cutting_section] = chromosome_1_flattened[0:cutting_section]
    cross_overed_chromosome_1[cutting_section:] = chromosome_2_flattened[cutting_section:]
    cross_overed_chromosome_2[0:cutting_section] = chromosome_2_flattened[0:cutting_section]
    cross_overed_chromosome_2[cutting_section:] = chromosome_1_flattened[cutting_section:]
    return (cross_overed_chromosome_1.reshape(chromosome_1.shape), cross_overed_chromosome_2.reshape(chromosome_2.shape))

def generate_offspring(gen: int, params: Parameters, topo_parents: np.ndarray, save_file_as: str=None) -> np.ndarray:
    """
    Generating topo_offspring from parents. Crossover & Mutation & Validating processes will be held.
    Validating processes contain, checking 3d-print-ability without support, one voxel tree contacting six faces
    in a cube
    :param save_file_as: Save pickle file of offspring topologies as this.
    :param topo_parents: Topology array of parent, shape: (end_pop, lx, ly, lz)
    :param gen: Current generation
    :param params: Parameters for GA
    The more timeout, the longer time will be allowed for the function "mutate_and_validate_topology".
    :return:
    """
    topo_offspring = np.empty((0, params.lx, params.ly, params.lz), int)
    validation_count = 0
    all_topos = pickles_io(file_names=[f'Topologies_{g}' for g in range(1, gen + 1)], mode='r', key_option='int')
    all_topos_parent = np.array([topos['parent'] for topos in all_topos.values()], dtype=int)
    while True:
        (cutting_section, candidates) = get_cutting_section_and_candidates(topologies=topo_parents)
        candidate_pairs = get_candidate_pairs(candidates=candidates)
        print('<info> Candidate lists:', len(candidates))
        print('<info> Candidate pairs:', len(candidate_pairs))
        for pair_idx in range(len(candidate_pairs)):
            chromosome_1_idx = candidate_pairs[pair_idx][0]
            chromosome_2_idx = candidate_pairs[pair_idx][1]
            (cross_overed_chromosome_1, cross_overed_chromosome_2) = crossover(chromosome_1=topo_parents[chromosome_1_idx], chromosome_2=topo_parents[chromosome_2_idx], cutting_section=cutting_section)
            validated_chromosome_1 = mutate_and_validate_topology(cross_overed_chromosome_1, params.mutation_rate)
            validated_chromosome_2 = mutate_and_validate_topology(cross_overed_chromosome_2, params.mutation_rate)
            for validated_chromosome in (validated_chromosome_1, validated_chromosome_2):
                if validated_chromosome is None:
                    print('<!> Non-connected tree detected')
                    continue
                elif len(find_where_same_array_locates(arr_to_find=validated_chromosome, big_arr=all_topos_parent)):
                    print('<!> Clone structure found in parents!')
                    continue
                elif len(find_where_same_array_locates(arr_to_find=validated_chromosome, big_arr=topo_offspring)):
                    print('<!> Clone structure found in current offsprings!')
                    continue
                else:
                    topo_offspring = np.vstack((topo_offspring, np.expand_dims(validated_chromosome, axis=0)))
                    validation_count += 1
                    print(f'<info> Validation of chromosome {validation_count} complete!')
                    if len(topo_offspring) == params.end_pop:
                        print('<info> Generating topo_offspring complete')
                        if save_file_as is not None:
                            pickle_io(save_file_as, mode='a', to_dump={'offspring': topo_offspring})
                        return topo_offspring

def random_array(shape, probability):
    return np.random.choice([1, 0], size=reduce(lambda x, y: x * y, shape), p=[probability, 1 - probability]).reshape(shape)

def random_parent_generation(density: float, params: Parameters, save_file_as: str=None) -> np.ndarray:
    parents = np.empty((params.end_pop, params.lx, params.ly, params.lz))
    total_parent_generation_count = 0
    total_volume_frac = 0
    while total_parent_generation_count < params.end_pop:
        print(f'<<<<< Parent {total_parent_generation_count + 1} >>>>>')
        while True:
            rand_arr = random_array(shape=(params.lx, params.ly, params.lz), probability=density)
            parent = mutate_and_validate_topology(rand_arr, mutation_probability=params.mutation_rate)
            if parent is not None:
                break
        volume_frac = np.count_nonzero(parent) / (params.lx * params.ly * params.lz / 100)
        total_volume_frac += volume_frac
        print(f'Volume fraction: {volume_frac:.1f} %\n')
        parents[total_parent_generation_count] = parent
        total_parent_generation_count += 1
    print(f'Average volume fraction: {total_volume_frac / params.end_pop:.1f} %')
    if save_file_as is not None:
        pickle_io(save_file_as, mode='w', to_dump={'parent': parents})
    return parents