def a_if():
    if a > b:
        print(1)

def b_elif():
    if a > b:
        print(1)
    elif a == b:
        print(2)

def c_else():
    if a > b:
        print(1)
    else:
        print(2)

def d_elif_else():
    if a > b:
        print(1)
    elif a == b:
        print(2)
    else:
        print(3)

def e_oneline():
    print(1) if a > b else print(2) if a == b else print(3)

def a1_if_and():
    if a > b and c > d:
        print(1)

def b1_elif_and():
    if a > b and c > d:
        print(1)
    elif a == b:
        print(2)

def c1_else_and():
    if a > b and c > d:
        print(1)
    else:
        print(2)

def d1_elif_else_and():
    if a > b and c > d:
        print(1)
    elif a == b:
        print(2)
    else:
        print(3)

def a2_if_or():
    if a > b or c > d:
        print(1)

def b2_elif_or():
    if a > b or c > d:
        print(1)
    elif a == b:
        print(2)

def c2_else_or():
    if a > b or c > d:
        print(1)
    else:
        print(2)

def d2_elif_else_or():
    if a > b or c > d:
        print(1)
    elif a == b:
        print(2)
    else:
        print(3)

def a3_if_not():
    if not a > b:
        print(1)

def b3_elif_not():
    if not a > b:
        print(1)
    elif a == b:
        print(2)

def c3_else_not():
    if not a > b:
        print(1)
    else:
        print(2)

def d3_elif_else_not():
    if not a > b:
        print(1)
    elif a == b:
        print(2)
    else:
        print(3)

def e_nested_if():
    if a > b:
        print(1)
        if a == b:
            print(2)
        else:
            print(3)
    else:
        print(4)

def e_nested_else():
    if a > b:
        print(1)
    else:
        print(2)
        if a == b:
            print(3)
        else:
            print(4)

def f_if_pass():
    if a > b:
        pass


def a_nofallthru_if():
    if a > b:
        print(1)
    print("end")

def b_nofallthru_elif():
    if a > b:
        print(1)
    elif a == b:
        print(2)
    print("end")

def c_nofallthru_else():
    if a > b:
        print(1)
    else:
        print(2)
    print("end")

def d_nofallthru_elif_else():
    if a > b:
        print(1)
    elif a == b:
        print(2)
    else:
        print(3)
    print("end")

def e_nofallthru_oneline():
    print(1) if a > b else print(2) if a == b else print(3)
    print("end")

def a_nofallthru1_if_and():
    if a > b and c > d:
        print(1)
    print("end")

def b_nofallthru1_elif_and():
    if a > b and c > d:
        print(1)
    elif a == b:
        print(2)
    print("end")

def c_nofallthru1_else_and():
    if a > b and c > d:
        print(1)
    else:
        print(2)
    print("end")

def d_nofallthru1_elif_else_and():
    if a > b and c > d:
        print(1)
    elif a == b:
        print(2)
    else:
        print(3)
    print("end")

def a_nofallthru2_if_or():
    if a > b or c > d:
        print(1)
    print("end")

def b_nofallthru2_elif_or():
    if a > b or c > d:
        print(1)
    elif a == b:
        print(2)
    print("end")

def c_nofallthru2_else_or():
    if a > b or c > d:
        print(1)
    else:
        print(2)
    print("end")

def d_nofallthru2_elif_else_or():
    if a > b or c > d:
        print(1)
    elif a == b:
        print(2)
    else:
        print(3)
    print("end")

def a_nofallthru3_if_not():
    if not a > b:
        print(1)
    print("end")

def b_nofallthru3_elif_not():
    if not a > b:
        print(1)
    elif a == b:
        print(2)
    print("end")

def c_nofallthru3_else_not():
    if not a > b:
        print(1)
    else:
        print(2)
    print("end")

def d_nofallthru3_elif_else_not():
    if not a > b:
        print(1)
    elif a == b:
        print(2)
    else:
        print(3)
    print("end")

def e_nofallthru_nested_if():
    if a > b:
        print(1)
        if a == b:
            print(2)
        else:
            print(3)
    else:
        print(4)
    print("end")

def e_nofallthru_nested_else():
    if a > b:
        print(1)
    else:
        print(2)
        if a == b:
            print(3)
        else:
            print(4)
    print("end")

def f_nofallthru_if_pass():
    if a > b:
        pass
    print("end")
