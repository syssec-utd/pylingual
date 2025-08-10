def a0_bare_match():
    match x:
        case 1:
            print(1)
    print(2)


def a1_bare_match(x):
    match x:
        case 1:
            print(1)
        case _:
            print(2)
    print(3)


def a2_bare_match(x):
    match x:
        case 1:
            print(1)
        case 2:
            print(2)
        case _:
            print(3)
    print(4)


def a3_bare_match(x):
    match x:
        case 1:
            print(1)
        case 2:
            print(2)
        case 3:
            print(3)
        case _:
            print(4)
    print(5)


def a4_bare_match(x):
    match x:
        case 1:
            print(1)
        case 2:
            print(2)
        case 3:
            print(3)
        case 4:
            print(4)
    print(5)


def b0_multi_case():
    match x:
        case 1 | 2:
            print(1)


def b1_multi_case_fallthrough():
    match x:
        case 1 | 2:
            print(1)
    print(2)


def c0_match_with_as():
    match x:
        case [1, 2] as y:
            print(1)


def c1_match_with_as():
    match x:
        case [1, 2] as y:
            print(1)
        case [3, 4] as z:
            print(2)


def c1_match_with_as_fallthrough():
    match x:
        case [1, 2] as y:
            print(1)
    print(2)


def d0_match_sequence():
    match x:
        case [a, b, c]:
            print(1)


def d1_match_sequence_fallthrough():
    match x:
        case [a, b, c]:
            print(1)
    print(2)


def e0_match_mapping():
    match x:
        case {'key': value}:
            print(1)


def e1_match_mapping_fallthrough():
    match x:
        case {'key': value}:
            print(1)
    print(2)


def f0_match_class():
    match x:
        case Point(x=0, y=0):
            print(1)


def f1_match_class_fallthrough():
    match x:
        case Point(x=0, y=0):
            print(1)
    print(2)


def g0_match_complex():
    match x:
        case [Point(x1, y1), Point(x2, y2) as p2]:
            print(1)


def g1_match_complex_fallthrough():
    match x:
        case [Point(x1, y1), Point(x2, y2) as p2]:
            print(1)
    print(2)


def h0_try_match_except():
    try:
        match x:
            case 1:
                print(1)
    except:
        print(2)
    print(3)


def i0_match_return():
    match x:
        case 1:
            return 1
    print(1)


def j0_match_raise():
    match x:
        case 1:
            raise Exc
    print(1)


async def k0_bare_match():
    match x:
        case 1:
            print(1)


async def k1_bare_match_fallthrough():
    match x:
        case 1:
            print(1)
    print(2)


def n0_match_guard():
    match x:
        case [a, b] if a > b:
            print(1)


def n1_match_guard_fallthrough():
    match x:
        case [a, b] if a > b:
            print(1)
    print(2)


def m0_nested_match():
    match x:
        case [a, b]:
            match b:
                case 1:
                    print(1)
            print(2)


def m1_nested_match_fallthrough():
    match x:
        case [a, b]:
            match b:
                case 1:
                    print(1)
            print(2)
    print(3)