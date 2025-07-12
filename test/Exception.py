def a0_bare_try_except():
    try:
        print(1)
    except:
        print(2)

def a1_bare_try_except_fallthrough():
    try:
        print(1)
    except:
        print(2)
    print(3)

# 3.11/3.12/3.13 Duplicate blocks causing blocks to not match
def b0_nested_try_except():
    try:
        print(1)
    except:
        print(2)
        try:
            print(3)
        except:
            print(4)

def b1_nested_try_except_fallthrough():
    try:
        print(1)
    except:
        print(2)
        try:
            print(3)
        except:
            print(4)
        print(5)

# 3.13 Duplicate blocks 
def b2_nested_try_except_early_fallthrough():
    try:
        print(1)
    except:
        print(2)
        try:
            print(3)
        except:
            print(4)
    print(5)

def b3_nested_try_except_double_fallthrough():
    try:
        print(1)
    except:
        print(2)
        try:
            print(3)
        except:
            print(4)
        print(5)
    print(6)

# 3.11/3.12/3.13 Duplicate blocks causing blocks to not match
def c0_multi_except_nested():
    try:
        print(1)
    except a:
        print(2)
        try:
            print(3)
        except:
            print(4)
    except b:
        print(5)
        try:
            print(6)
        except:
            print(7)

# 3.11/3.12/3.13 Duplicate blocks causing blocks to not match
def c1_multi_except_nested_fallthrough():
    try:
        print(1)
    except a:
        print(2)
        try:
            print(3)
        except:
            print(4)
        print(5)
    except b:
        print(6)
        try:
            print(7)
        except:
            print(8)

def c2_multi_except_nested_fallthrough2():
    try:
        print(1)
    except a:
        print(2)
        try:
            print(3)
        except:
            print(4)
        print(5)
    except b:
        print(6)
        try:
            print(7)
        except:
            print(8)
        print(9)

# 3.13 Duplicate blocks 
def c3_multi_except_nested_early_fallthrough():
    try:
        print(1)
    except a:
        print(2)
        try:
            print(3)
        except:
            print(4)
    except b:
        print(5)
        try:
            print(6)
        except:
            print(7)
    print(8)

def c4_multi_except_nested_all_fallthrough():
    try:
        print(1)
    except a:
        print(2)
        try:
            print(3)
        except:
            print(4)
        print(5)
    except b:
        print(6)
        try:
            print(7)
        except:
            print(8)
        print(9)
    print(10)

# 3.10/3.11/3.12/3.13 Duplicate blocks causing templates to not match
# Discussed in issue 41
def d0_named_except_nested():
    try:
        print(1)
    except A as a:
        print(2)
        try:
            print(3)
        except:
            print(4)

def d1_named_except_nested_fallthrough():
    try:
        print(1)
    except A as a:
        print(2)
        try:
            print(3)
        except:
            print(4)
        print(5)

# 3.13 Duplicate blocks 
def d2_named_except_nested_early_fallthrough():
    try:
        print(1)
    except A as a:
        print(2)
        try:
            print(3)
        except:
            print(4)
    print(5)

def d3_named_except_nested_double_fallthrough():
    try:
        print(1)
    except A as a:
        print(2)
        try:
            print(3)
        except:
            print(4)
        print(5)
    print(6)

def e0_try_except_else():
    try:
        print(1)
    except:
        print(2)
    else:
        print(3)
    print(4)

def f0_try_except_else_finally():
    try:
        print(1)
    except:
        print(2)
    else:
        print(3)
    finally:
        print(4)
    print(5)

def g0_multi_except_with_else():
    try:
        print(1)
    except a:
        print(2)
    except b:
        print(3)
    else:
        print(4)
    print(5)

def h0_multi_except_fallback_with_else():
    try:
        print(1)
    except a:
        print(2)
    except b:
        print(3)
    except:
        print(4)
    else:
        print(5)
    print(6)

def i0_mixed_named_unnamed_except_with_else():
    try:
        print(1)
    except A as a:
        print(2)
    except b:
        print(3)
    except:
        print(4)
    else:
        print(5)
    print(6)

def j0_named_except_with_else():
    try:
        print(1)
    except A as a:
        print(2)
    except B as b:
        print(3)
    else:
        print(4)
    print(5)

def k0_try_except_finally():
    try:
        print(1)
    except:
        print(2)
    finally:
        print(3)
    print(4)

def l0_specific_except_finally():
    try:
        print(1)
    except a:
        print(2)
    finally:
        print(3)
    print(4)

def m0_multi_except():
    try:
        print(1)
    except a:
        print(2)
    except b:
        print(3)
    except c:
        print(4)
    print(5)

def n0_multi_except_with_fallback():
    try:
        print(1)
    except a:
        print(2)
    except b:
        print(3)
    except:
        print(4)
    print(5)

def o0_multi_except_fallback_finally():
    try:
        print(1)
    except a:
        print(2)
    except:
        print(3)
    finally:
        print(4)
    print(5)

def p0_multi_named_except():
    try:
        print(1)
    except A as a:
        print(2)
    except B as b:
        print(3)
    except C as c:
        print(4)
    print(5)

def q0_mixed_named_unnamed_except():
    try:
        print(1)
    except A as a:
        print(2)
    except b:
        print(3)
    except:
        print(4)
    print(5)

def r0_mixed_named_unnamed_except_finally():
    try:
        print(1)
    except A as a:
        print(2)
    except b:
        print(3)
    except:
        print(4)
    finally:
        print(5)
    print(6)

def s0_named_except_fallback():
    try:
        print(1)
    except A as a:
        print(2)
    except:
        print(3)
    print(4)

def t0_named_except_fallback_finally():
    try:
        print(1)
    except A as a:
        print(2)
    except:
        print(3)
    finally:
        print(4)
    print(5)

def u0_multi_named_except_finally():
    try:
        print(1)
    except A as a:
        print(2)
    except B as b:
        print(3)
    finally:
        print(4)
    print(5)

def v0_multi_except_finally():
    try:
        print(1)
    except a:
        print(2)
    except b:
        print(3)
    finally:
        print(4)
    print(5)

def w0_try_except_raise():
    try:
        print(1)
    except:
        print(2)
        raise Exc

def x0_multi_except_raise():
    try:
        print(1)
    except a:
        print(2)
        raise Exc
    except b:
        print(3)
        raise Exc

def y0_named_except_raise():
    try:
        print(1)
    except A as a:
        print(2)
        raise Exc

# 3.11 Try return getting left outside of TryExcept
def z0_try_except_return():
    try:
        print(1)
        return 2
    except:
        print(2)

# 3.11 Try return getting left outside of TryExcept
def z1_try_except_return_both():
    try:
        print(1)
        return 2
    except:
        print(2)
        return 3

# 3.11 Try return getting left outside of TryExcept
def aa0_multi_except_return():
    try:
        print(1)
        return 2
    except a:
        print(2)
    except b:
        print(3)

# 3.6/3.7/3.8 ExceptExc abandons tail node. 
# Could be fixed (?) but breaks other test cases
# 3.11 Try return getting left outside of TryExcept
def aa1_multi_except_return_both():
    try:
        print(1)
        return 2
    except a:
        print(2)
        return 3
    except b:
        print(3)

# 3.11 Try return getting left outside of TryExcept
def ab0_named_except_raise_return():
    try:
        print(1)
        return 2
    except A as a:
        print(2)
        raise Exc
    except b:
        print(3)
        raise Exc

# 3.8 Double natural edge graph error (?)
# 3.11 Try return getting left outside of TryExcept
def ab1_named_except_return():
    try:
        print(1)
        return 2
    except A as a:
        print(2)
        return 3

# 3.11/3.12/3.13 No template match
def ac0_empty_try_finally():
    try:
        pass
    finally:
        print(1)

def ad0_multiple_try_blocks():
    try:
        print(1)
    except:
        print(2)

    try:
        print(3)
    except:
        print(4)

# 3.10/3.11 Try matching before TryElse
def ae0_try_except_else_nested_try():
    try:
        print(1)
    except:
        print(2)
    else:
        try:
            print(3)
        except:
            print(4)

# 3.9 Duplicate blocks (?)
# 3.11/3.12/3.13 Matching priority TryElse TryFinally (?)
def af0_try_finally_nested_except():
    try:
        print(1)
    finally:
        try:
            print(2)
        except:
            print(3)

def ag0_try_except_tuple():
    try:
        print(1)
    except (A, B):
        print(2)

# 3.9 Difficult template ambiguity between Try/TryFinally
# 3.11/3.12/3.13 Matching priority TryElse TryFinally (?)
def ah0_try_finally_return():
    try:
        print(1)
    finally:
        return 2

# 3.11/3.12/3.13 No template match (?)
def ai0_try_return_finally():
    try:
        return 1
    finally:
        print(2)

# 3.9/3.10 Difficult template ambiguity between Try/TryFinally
# 3.11/3.12/3.13 No template match (?)
def aj0_try_return_finally_return():
    try:
        return 1
    finally:
        return 2

def ak0_try_except_raise_return():
    try:
        print(1)
        return 2
    except:
        raise Exception()

# 3.8/3.9/3.10 No template match
def al0_try_except_return_finally():
    try:
        raise Exception()
    except:
        print(1)
        return 2
    finally:
        print(3)

# 3.8/3.9/3.10 No template match
# 3.11/3.12/3.13 Matching priority TryElse TryFinally (?)
def am0_try_finally_raise():
    try:
        print(1)
        return 2
    finally:
        raise Exception()

def an0_try_finally_fallthrough():
    try:
        print(1)
    finally:
        print(2)
    print(3)

def ao0_try_finally_simple():
    try:
        print(1)
    finally:
        print(2)