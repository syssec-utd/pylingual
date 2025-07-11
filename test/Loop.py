def a_for_over_list():
    for x in [1, 2, 3]:
        print("for over list")

def a1_for_over_list_nofallthru():
    for x in [1, 2, 3]:
        print("for over list")
    print("end")

def b_for_over_tuples():
    for a, b in [(1, 2), (3, 4)]:
        print("tuples")

def b1_for_over_tuples_nofallthru():
    for a, b in [(1, 2), (3, 4)]:
        print("tuples")
    print("end")

def c_for_else():
    for i in range(3):
        print("for body")
    else:
        print("for else")

def c1_for_else_nofallthru():
    for i in range(3):
        print("for body")
    else:
        print("for else")
    print("end")

def d_for_with_break():
    for x in range(10):
        if x == 5:
            print("breaking")
            break

def d1_for_with_break_nofallthru():
    for x in range(10):
        if x == 5:
            print("breaking")
            break
    print("end")

def e_for_with_continue():
    for x in range(5):
        if x % 2 == 0:
            print("continuing")
            continue
        print("after continue")

def e1_for_with_continue_nofallthru():
    for x in range(5):
        if x % 2 == 0:
            print("continuing")
            continue
        print("after continue")
    print("end")

def f_nested_for_loops():
    for i in range(2):
        for j in range(3):
            print(f"nested {i},{j}")

def f1_nested_for_loops_nofallthru():
    for i in range(2):
        for j in range(3):
            print(f"nested {i},{j}")
    print("end")

def g_for_with_try_except():
    for x in range(2):
        try:
            print("try block")
        except Exception:
            print("except block")

def g1_for_with_try_except_nofallthru():
    for x in range(2):
        try:
            print("try block")
        except Exception:
            print("except block")
    print("end")

def h_for_with_with_statement():
    for _ in range(1):
        with a:
            print("inside with")

def h1_for_with_with_statement_nofallthru():
    for _ in range(1):
        with a:
            print("inside with")
    print("end")

def i_for_with_function_call_iterable():
    def get_items():
        return [1, 2, 3]

    for item in get_items():
        print(f"item: {item}")

def i1_for_with_function_call_iterable_nofallthru():
    def get_items():
        return [1, 2, 3]

    for item in get_items():
        print(f"item: {item}")
    print("end")

def j_for_with_empty_body_ellipsis():
    for _ in range(3):
        ...

def j1_for_with_empty_body_ellipsis_nofallthru():
    for _ in range(3):
        ...
    print("end")

def k_while_true_with_break():
    while True:
        print("while true")
        break

def k1_while_true_with_break_nofallthru():
    while True:
        print("while true")
        break
    print("end")

def l_while_with_else():
    i = 0
    while i < 3:
        print(f"looping {i}")
        i += 1
    else:
        print("while else")

def l1_while_with_else_nofallthru():
    i = 0
    while i < 3:
        print(f"looping {i}")
        i += 1
    else:
        print("while else")
    print("end")

def m_while_with_continue():
    i = 0
    while i < 5:
        i += 1
        if i % 2 == 0:
            print("continue")
            continue
        print("after continue")

def m1_while_with_continue_nofallthru():
    i = 0
    while i < 5:
        i += 1
        if i % 2 == 0:
            print("continue")
            continue
        print("after continue")
    print("end")

def n_while_with_break():
    i = 0
    while True:
        print("break in while")
        break

def n1_while_with_break_nofallthru():
    i = 0
    while True:
        print("break in while")
        break
    print("end")

def o_nested_while_loops():
    i = 0
    while i < 2:
        j = 0
        while j < 2:
            print(f"nested while {i},{j}")
            j += 1
        i += 1

def o1_nested_while_loops_nofallthru():
    i = 0
    while i < 2:
        j = 0
        while j < 2:
            print(f"nested while {i},{j}")
            j += 1
        i += 1
    print("end")

def p_while_with_try_except():
    while True:
        try:
            print("try in while")
        except:
            print("except in while")

def p1_while_with_try_except_nofallthru():
    while True:
        try:
            print("try in while")
        except:
            print("except in while")
    print("end")

def q_while_with_with_statement():
    while True:
        with a:
            print("inside while with")

def q1_while_with_with_statement_nofallthru():
    while True:
        with a:
            print("inside while with")
    print("end")

def r_for_inside_while():
    while True:
        for x in [1, 2]:
            print("for in while")

def r1_for_inside_while_nofallthru():
    while True:
        for x in [1, 2]:
            print("for in while")
    print("end")

def s_while_inside_for():
    for _ in range(1):
        while True:
            print("while in for")
            break

def s1_while_inside_for_nofallthru():
    for _ in range(1):
        while True:
            print("while in for")
            break
    print("end")

def t_while_with_empty_body_ellipsis():
    while True:
        ...

def t1_while_with_empty_body_ellipsis_nofallthru():
    while True:
        ...
    print("end")