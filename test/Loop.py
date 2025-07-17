def a0_for_over_list():
    for x in [1, 2, 3]:
        print("for over list")

def a1_for_over_list_nofallthru():
    for x in [1, 2, 3]:
        print("for over list")
    print("end")

def b0_for_over_tuples():
    for a, b in [(1, 2), (3, 4)]:
        print("tuples")

def b1_for_over_tuples_nofallthru():
    for a, b in [(1, 2), (3, 4)]:
        print("tuples")
    print("end")

# 3.6 No else template
def c0_for_else():
    for i in range(3):
        print("for body")
    else:
        print("for else")

# 3.6 No else template
def c1_for_else_nofallthru():
    for i in range(3):
        print("for body")
    else:
        print("for else")
    print("end")

# 3.6 Naive break detection, an unexpected buffer POP_BLOCK to end
# 3.9 Naive break detection, an unexpected buffer block to end
def d0_for_with_break():
    for x in range(10):
        if x == 5:
            print("breaking")
            break

# 3.6 Naive break detection, an unexpected buffer POP_BLOCK to end
def d1_for_with_break_nofallthru():
    for x in range(10):
        if x == 5:
            print("breaking")
            break
    print("end")

# Help to implement break
def d2_for_without_break():
    for x in range(10):
        if x == 5:
            print("not breaking")
    print("end")

# Help to implement break
def d3_for_return():
    for x in range(10):
        if x == 5:
            print("not breaking")
            return
    print("end")

def e0_for_with_continue():
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

def f0_nested_for_loops():
    for i in range(2):
        for j in range(3):
            print(f"nested {i},{j}")

def f1_nested_for_loops_nofallthru():
    for i in range(2):
        for j in range(3):
            print(f"nested {i},{j}")
    print("end")

def g0_for_with_try_except():
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

def h0_for_with_with_statement():
    for _ in range(1):
        with a:
            print("inside with")

def h1_for_with_with_statement_nofallthru():
    for _ in range(1):
        with a:
            print("inside with")
    print("end")

def i0_for_with_function_call_iterable():
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

def j0_for_with_empty_body_ellipsis():
    for _ in range(3):
        ...

def j1_for_with_empty_body_ellipsis_nofallthru():
    for _ in range(3):
        ...
    print("end")

# 3.6 Naive break detection, no back edge
# 3.9/3.11 No while loop detection, self false_jump edge & naive break detection
def k0_while_true_with_break():
    x = 0
    while True:
        print("while true")
        x += 1
        if x >= 1:
            break

# 3.6 Naive break detection, no back edge
# 3.9/3.11 No while loop detection, self false_jump edge & naive break detection
def k1_while_true_with_break_nofallthru():
    x = 0
    while True:
        print("while true")
        x += 1
        if x >= 1:
            break
    print("end")

# 3.6 No else template
# 3.11 No while loop detection, self false_jump edge
def l0_while_with_else():
    i = 0
    while i < 3:
        print(f"looping {i}")
        i += 1
    else:
        print("while else")

# 3.6 No else template
# 3.11 No while loop detection, self false_jump edge
def l1_while_with_else_nofallthru():
    i = 0
    while i < 3:
        print(f"looping {i}")
        i += 1
    else:
        print("while else")
    print("end")

# 3.11 No continue
def m0_while_with_continue():
    i = 0
    while i < 5:
        i += 1
        if i % 2 == 0:
            print("continue")
            continue
        print("after continue")

# 3.11 No continue
def m1_while_with_continue_nofallthru():
    i = 0
    while i < 5:
        i += 1
        if i % 2 == 0:
            print("continue")
            continue
        print("after continue")
    print("end")

# 3.6 Naive break detection, no back edge
def n0_while_with_break():
    i = 0
    while True:
        print("break in while")
        break

# 3.6 Naive break detection, no back edge
def n1_while_with_break_nofallthru():
    i = 0
    while True:
        print("break in while")
        break
    print("end")

# 3.11 While template broke
def o0_nested_while_loops():
    i = 0
    while i < 2:
        j = 0
        while j < 2:
            print(f"nested while {i},{j}")
            j += 1
        i += 1

# 3.11 While template broke
def o1_nested_while_loops_nofallthru():
    i = 0
    while i < 2:
        j = 0
        while j < 2:
            print(f"nested while {i},{j}")
            j += 1
        i += 1
    print("end")

# 3.6 While template broke (?)
# 3.9 Disconnected with MetaTemplate[end] (?) 
def p0_while_with_try_except():
    while True:
        try:
            print("try in while")
        except:
            print("except in while")

# 3.6 While template broke (?)
# 3.9 Disconnected with MetaTemplate[end] (?) 
def p1_while_with_try_except_nofallthru():
    while True:
        try:
            print("try in while")
        except:
            print("except in while")
    print("end")

# 3.6 While template broke (?) abandoning nodes
def q0_while_with_with_statement():
    while True:
        with a:
            print("inside while with")

# 3.6 While template broke (?) abandoning nodes
def q1_while_with_with_statement_nofallthru():
    while True:
        with a:
            print("inside while with")
    print("end")

# 3.6 While template broke
def r0_for_inside_while():
    while True:
        for x in [1, 2]:
            print("for in while")

# 3.6 While template broke
def r1_for_inside_while_nofallthru():
    while True:
        for x in [1, 2]:
            print("for in while")
    print("end")

# 3.6 While template broke
def s0_while_inside_for():
    for _ in range(1):
        while True:
            print("while in for")
            break

# 3.6 While template broke
def s1_while_inside_for_nofallthru():
    for _ in range(1):
        while True:
            print("while in for")
            break
    print("end")

# 3.6 While template broke
def t0_while_with_empty_body_ellipsis():
    while True:
        ...

# 3.6 While template broke
def t1_while_with_empty_body_ellipsis_nofallthru():
    while True:
        ...
    print("end")

def u0_break_in_nested_for():
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                print("Breaking inner loop")
                break
            print(f"i={i}, j={j}")

def u1_break_in_nested_for_nofallthru():
    for i in range(3):
        for j in range(3):
            if i == 1 and j == 1:
                print("Breaking inner loop")
                break
            print(f"i={i}, j={j}")
    print("end")

def v0_continue_in_nested_for():
    for i in range(3):
        for j in range(3):
            if j == 1:
                continue
            print(f"Processing i={i}, j={j}")

def v1_continue_in_nested_for_nofallthru():
    for i in range(3):
        for j in range(3):
            if j == 1:
                continue
            print(f"Processing i={i}, j={j}")
    print("end")

# 3.6 Naive break detection, an unexpected buffer POP_BLOCK to end
# 3.9/3.11 Naive break detection, an unexpected buffer block to end
def w0_break_with_else():
    for i in range(5):
        if i == 3:
            print("Breaking before else")
            break
    else:
        print("This won't execute due to break")

# 3.6 Naive break detection, an unexpected buffer POP_BLOCK to end
# 3.9/3.11 Naive break detection, an unexpected buffer block to end
def w1_break_with_else_nofallthru():
    for i in range(5):
        if i == 3:
            print("Breaking before else")
            break
    else:
        print("This won't execute due to break")
    print("end")

# 3.6 No continue detection
def x0_continue_with_else():
    for i in range(3):
        if i == 1:
            continue
        print(f"Processing {i}")
    else:
        print("Else clause still executes after continue")

# 3.6 No continue detection
def x1_continue_with_else_nofallthru():
    for i in range(3):
        if i == 1:
            continue
        print(f"Processing {i}")
    else:
        print("Else clause still executes after continue")
    print("end")

# 3.9/3.11 Naive break detection, break statement is further up
def y0_break_in_try_except():
    for i in range(5):
        try:
            if i == 3:
                break
            print(f"Value: {i}")
        except:
            print("Exception occurred")

# 3.9/3.11 Naive break detection, break statement is further up
def y1_break_in_try_except_nofallthru():
    for i in range(5):
        try:
            if i == 3:
                break
            print(f"Value: {i}")
        except:
            print("Exception occurred")
    print("end")

# 3.9/3.11 Naive break detection, break statement is further up
def y2_return_in_try_except_nofallthru():
    for i in range(5):
        try:
            if i == 3:
                print(f"Value: {i}")
            else:
                break
        except:
            print("Exception occurred")
    print("end")

# 3.6/3.9/3.11 No continue detection
def z0_continue_in_try_except():
    for i in range(5):
        try:
            if i == 2:
                continue
            print(f"Value: {i}")
        except:
            print("Exception occurred")

# 3.6/3.9/3.11 No continue detection
def z1_continue_in_try_except_nofallthru():
    for i in range(5):
        try:
            if i == 2:
                continue
            print(f"Value: {i}")
        except:
            print("Exception occurred")
    print("end")