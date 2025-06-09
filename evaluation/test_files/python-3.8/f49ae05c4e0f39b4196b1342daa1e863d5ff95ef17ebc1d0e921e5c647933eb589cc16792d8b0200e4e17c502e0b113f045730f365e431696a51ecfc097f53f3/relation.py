""".. Ignore pydocstyle D400.

=======================
Relations Template Tags
=======================

"""
from resolwe.flow.expression_engines.jinja.filters import id_, type_
from resolwe.flow.models.entity import Entity, RelationPartition

def background_pairs(data):
    """Get a list of (case, background) pairs for given data.

    A list of data objects is re-arranged to a list of (case, background) pairs
    based on the background relation between their corresponding samples.

    """
    if not isinstance(data, list):
        raise ValueError('Argument data must be a list')
    if not data:
        return []
    data_types = [type_(d) for d in data]
    if len(set(data_types)) != 1:
        raise ValueError('All data must be of the same type')
    data_ids = [id_(d) for d in data]
    data_type = data_types[0]
    backround_query = RelationPartition.objects.filter(label='background', entity__data__process__type=data_type, relation__type__name='background', relation__relationpartition__label='case', relation__relationpartition__entity__data__in=data_ids).values('entity__data', 'relation__relationpartition__entity__data')
    returned_cases = set()
    returned_backgrounds = set()
    background_pairs_list = []
    for backround_dict in backround_query:
        case = backround_dict['relation__relationpartition__entity__data']
        background = backround_dict['entity__data']
        assert case in data_ids
        background_pairs_list.append((case, background))
        returned_cases.add(case)
        returned_backgrounds.add(background)
    for case in set(data_ids).difference(returned_cases).difference(returned_backgrounds):
        background_pairs_list.append((case, None))
    return sorted(background_pairs_list)

def replicate_groups(data):
    """Get replicate groups."""
    if not isinstance(data, list):
        raise ValueError('List of data must be given')
    data_ids = [id_(d) for d in data]
    if len(data_ids) != len(set(data_ids)):
        raise ValueError('Repeated data objects not allowed')
    samples = Entity.objects.filter(data__id__in=data_ids)
    if len(samples) != len(data_ids):
        raise ValueError('Can not get replicates of data without sample')
    partitions = RelationPartition.objects.filter(relation__category='Replicate', relation__type__name='group', entity__in=samples)
    sample_group = {}
    for p in partitions:
        if p.entity.id in sample_group:
            raise ValueError('More than one replicate relation on sample: {}'.format(p.entity.id))
        sample_group[p.entity.id] = p.label
    group_map = {}
    group_index = 1
    repl_groups = []
    for d in data_ids:
        sample_id = Entity.objects.filter(data__id=d).values('id').first()['id']
        if sample_id in sample_group:
            group_label = sample_group[sample_id]
            if group_label not in group_map:
                group_map[group_label] = group_index
                group_index += 1
            repl_groups.append(group_map[group_label])
        else:
            repl_groups.append(group_index)
            group_index += 1
    return repl_groups
filters = {'background_pairs': background_pairs, 'replicate_groups': replicate_groups}