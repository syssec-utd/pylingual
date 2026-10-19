import itertools


# make windows based on the token sizes instrutions will be an instruction along with it's token size
def sliding_window(instructions: list, max_window_size: int, step_size: int = 1) -> tuple[list[str], list[int]]:
    # go through each instruction in a code object and fill up windows
    instructions_iter = enumerate(instructions)

    try:
        while True:
            # start a new window
            instructions_iter, window_source = itertools.tee(instructions_iter)

            # take elements until it would overflow the window
            window = []
            index_window = []
            window_len = 0

            # this loop will raise stopIteration when we run out of instructions
            while window_item := next(window_source):
                inst_index, (inst, inst_len) = window_item

                # end the window if we would exceed the max_window_size
                if inst_len + window_len > max_window_size:
                    break

                window.append(inst)
                index_window.append(inst_index)
                window_len += inst_len

            yield (window, index_window)

            # step forward step_size tokens
            tokens_stepped = 0

            while step_item := next(instructions_iter):
                inst_index, (inst, inst_len) = step_item
                tokens_stepped += inst_len
                if tokens_stepped >= step_size:
                    break
    except StopIteration:
        # yield the final window (partially full)
        yield (window, index_window)


# merges the bytecode together based on a point system given the division value for be results use an odd number and given the steps used in the sliding window
def merge(window_coords: list[tuple], window_segmentation_results: list[list[dict]], inst_index: list, window_size: int, step: int) -> list[list[dict]]:
    # for each codeobject align and score
    sorted_windows = align_segmentation_window_results(window_coords, window_segmentation_results, inst_index)

    weighted_segmentation_results = confidence_based_score(sorted_windows)

    # get ready for the merging

    entity_list = []
    for codeobj in weighted_segmentation_results:
        codeobj_entities = []

        for inst in codeobj:
            highest = max(inst[1], key=inst[1].get)
            final_choice = inst[0]

            if highest == "B_score":
                final_choice["entity"] = "B"
            elif highest == "I_score":
                final_choice["entity"] = "I"
            elif highest == "E_score":
                final_choice["entity"] = "E"
            codeobj_entities.append(final_choice)

        entity_list.append(codeobj_entities)

    return entity_list


# align windows to make scoring easier
def align_segmentation_window_results(
    window_coords: list[tuple],
    window_segmentation_results: list[list[dict]],
    inst_index: list,
) -> dict[int, list[list[dict]]]:
    # returns a dict of code object index -> list of instruction results, where each instruction result is a list of segmentation results for that instruction
    segmentation_result_dict = dict()
    for (codeobj_index, _), window_results, window_inst_indices in zip(window_coords, window_segmentation_results, inst_index):
        if codeobj_index not in segmentation_result_dict:
            segmentation_result_dict[codeobj_index] = dict()

        codeobj_result_dict = segmentation_result_dict[codeobj_index]
        for inst_result, inst_index in zip(window_results, window_inst_indices):
            if inst_index not in codeobj_result_dict:
                codeobj_result_dict[inst_index] = list()

            codeobj_result_dict[inst_index].append(inst_result)

        segmentation_result_dict[codeobj_index] = codeobj_result_dict

    # bake codeobj_result dicts into lists
    baked_result_dict = dict()
    for codeobj_index, codeobj_result_dict in segmentation_result_dict.items():
        codeobj_result_list = []
        if bool(codeobj_result_dict):
            codeobj_length = max(codeobj_result_dict.keys()) + 1
            codeobj_result_list = [None] * codeobj_length

        for instruction_index, instruction_result in codeobj_result_dict.items():
            codeobj_result_list[instruction_index] = instruction_result

        # make sure we didn't miss any indices!
        assert None not in codeobj_result_list

        baked_result_dict[codeobj_index] = codeobj_result_list

    return baked_result_dict


# given a list of sorted windows for each codeobject we will score b,i,e for each instruction based on the segmentation models confidence level
def confidence_based_score(aligned_segmentation_results: list[list[dict]]) -> list[list[dict]]:
    codeobj_scores = []
    for codeobj in range(len(aligned_segmentation_results)):
        inst_list = []

        for inst in aligned_segmentation_results[codeobj]:
            scores = {"B_score": 0, "I_score": 0, "E_score": 0}

            # go through each result from the windows and give a score to b,i,e based on their offsets
            for item in inst:
                confidence_score = item["score"]
                if item["entity"] == "B":
                    scores["B_score"] += confidence_score
                elif item["entity"] == "I":
                    scores["I_score"] += confidence_score
                elif item["entity"] == "E":
                    scores["E_score"] += confidence_score

            # scores for instructions
            inst_list.append((inst[0], scores))

        # scores for the instructions in each code object
        codeobj_scores.append(inst_list)

    return codeobj_scores
