# PEP 798: Unpacking in comprehensions (3.15+)


def a0_star_list_comp():
    lists = [[1, 2], [3, 4], [5]]
    [*L for L in lists]


def a1_star_list_comp_nofallthru():
    lists = [[1, 2], [3, 4], [5]]
    [*L for L in lists]
    print("end")


def b0_star_set_comp():
    sets = [{1, 2}, {2, 3}, {3, 4}]
    {*s for s in sets}


def b1_star_set_comp_nofallthru():
    sets = [{1, 2}, {2, 3}, {3, 4}]
    {*s for s in sets}
    print("end")


def c0_star_dict_comp():
    dicts = [{'a': 1}, {'b': 2}]
    {**d for d in dicts}


def c1_star_dict_comp_nofallthru():
    dicts = [{'a': 1}, {'b': 2}]
    {**d for d in dicts}
    print("end")


def d0_star_gen_expr():
    lists = [[1, 2], [3, 4]]
    (*L for L in lists)


def d1_star_gen_expr_nofallthru():
    lists = [[1, 2], [3, 4]]
    (*L for L in lists)
    print("end")


# PEP 798: Unpacking in comprehensions combined with control flow


def e0_star_list_comp_in_if():
    lists = [[1, 2], [3, 4]]
    if lists:
        [*L for L in lists]


def e1_star_list_comp_in_if_nofallthru():
    lists = [[1, 2], [3, 4]]
    if lists:
        [*L for L in lists]
    print("end")


def f0_star_list_comp_in_loop():
    lists = [[1, 2], [3, 4]]
    for _ in range(2):
        [*L for L in lists]


def f1_star_list_comp_in_loop_nofallthru():
    lists = [[1, 2], [3, 4]]
    for _ in range(2):
        [*L for L in lists]
    print("end")


# Unary plus in match literal patterns (3.15+)


def g0_match_unary_plus():
    match x:
        case +1:
            print(1)


def g1_match_unary_plus_fallthrough():
    match x:
        case +1:
            print(1)
    print(2)


def h0_match_unary_plus_multi_case():
    match x:
        case +1:
            print(1)
        case +2:
            print(2)
        case _:
            print(3)
    print(4)


def i0_match_unary_plus_with_guard():
    match x:
        case +1 if y > 0:
            print(1)
    print(2)


# PEP 810: Lazy imports (3.15+) — module scope only
# These are at module level since lazy imports are not allowed inside functions

lazy import json
lazy from pathlib import Path


def j0_lazy_import_usage():
    data = json.loads('{"key": "value"}')
    print(data)


def j1_lazy_import_usage_nofallthru():
    data = json.loads('{"key": "value"}')
    print(data)
    print("end")


def k0_lazy_from_import_usage():
    p = Path(".")
    print(p)


def k1_lazy_from_import_usage_nofallthru():
    p = Path(".")
    print(p)
    print("end")


def l0_lazy_import_in_if():
    if x:
        data = json.loads('{"key": "value"}')
        print(data)


def l1_lazy_import_in_if_nofallthru():
    if x:
        data = json.loads('{"key": "value"}')
        print(data)
    print("end")