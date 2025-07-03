def a_TryExcept():
    try:
        print(1)
    except:
       print(2)
    print(3)

def b_TryExceptBareNested():
    try:
        print(1)
    except:
        print(2)
        try:
            print(3)
        except:
            print(4)

def b1_TryExceptBareNestedFallthrough():
    try:
        print(1)
    except:
        print(2)
        try:
            print(3)
        except:
            print(4)
        print(5)

def b2_TryExceptBareNestedEarlyFallthrough():
    try:
        print(1)
    except:
        print(2)
        try:
            print(3)
        except:
            print(4)
    print(5)

def b3_TryExceptBareNestedDoubleFallthrough():
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

def c_TryExceptBareMultiNested():
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

def c1_TryExceptBareMultiNestedFallthrough():
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

def c2_TryExceptBareMultiNestedFallthrough2():
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

def c3_TryExceptBareMultiNestedEarlyFallthrough():
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

def c4_TryExceptBareMultiNestedAllFallthrough():
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

def d_TryExceptBareNestedNamed():
    try:
        print(1)
    except A as a:
        print(2)
        try:
            print(3)
        except:
            print(4)

def d1_TryExceptBareNestedNamedFallthrough():
    try:
        print(1)
    except A as a:
        print(2)
        try:
            print(3)
        except:
            print(4)
        print(5)

def d2_TryExceptBareNestedNamedEarlyFallthrough():
    try:
        print(1)
    except A as a:
        print(2)
        try:
            print(3)
        except:
            print(4)
    print(5)

def d3_TryExceptBareNestedNamedDoubleFallthrough():
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

def e_TryExceptElseBare():
    try:
        print(1)
    except:
        print(2)
    else:
        print(3)
    print(4)

def f_TryExceptElseFinallyBare():
    try:
        print(1)
    except:
        print(2)
    else:
        print(3)
    finally:
        print(4)
    print(5)

def g_TryExceptElseMulti():
    try:
        print(1)
    except a:
        print(2)
    except b:
        print(3)
    else:
        print(4)
    print(5)

def h_TryExceptElseMultiFallback():
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

def i_TryExceptElseMultiNamedAndUnnamed():
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

def j_TryExceptElseNamed():
    try:
        print(1)
    except A as a:
        print(2)
    except B as b:
        print(3)
    else:
        print(4)
    print(5)

def k_TryExceptFinallyBare():
    try:
        print(1)
    except:
        print(2)
    finally:
        print(3)
    print(4)

def l_TryExceptFinallyBareSpecific():
   try:
       print(1)
   except a:
       print(2)
   finally:
       print(3)
   print(4)

def m_TryExceptMulti():
    try:
        print(1)
    except a:
       print(2)
    except b:
       print(3)
    except c:
       print(4)
    print(5)

def n_TryExceptMultiFallback():
    try:
        print(1)
    except a:
       print(2)
    except b:
       print(3)
    except:
       print(4)
    print(5)

def o_TryExceptMultiFallbackFinally():
   try:
       print(1)
   except a:
       print(2)
   except:
       print(3)
   finally:
       print(4)
   print(5)

def p_TryExceptMultiNamed():
    try:
        print(1)
    except A as a:
       print(2)
    except B as b:
       print(3)
    except C as c:
       print(4)
    print(5)

def q_TryExceptMultiNamedAndUnnamed():
    try:
        print(1)
    except A as a:
       print(2)
    except b:
       print(3)
    except:
       print(4)
    print(5)

def r_TryExceptMultiNamedAndUnnamedFinally():
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

def s_TryExceptMultiNamedFallback():
    try:
        print(1)
    except A as a:
       print(2)
    except:
       print(3)
    print(4)

def t_TryExceptMultiNamedFallbackFinally():
    try:
        print(1)
    except A as a:
        print(2)
    except:
        print(3)
    finally:
        print(4)
    print(5)

def u_TryExceptMultiNamedFinally():
    try:
        print(1)
    except A as a:
        print(2)
    except B as b:
        print(3)
    finally:
        print(4)
    print(5)

def v_TryExceptMultiFinally():
   try:
       print(1)
   except a:
       print(2)
   except b:
       print(3)
   finally:
       print(4)
   print(5)

def w_TryExceptRaise():
    try:
        print(1)
    except:
        print(2)
        raise Exc

def x_TryExceptRaiseMulti():
    try:
        print(1)
    except a:
        print(2)
        raise Exc
    except b:
        print(3)
        raise Exc

def y_TryExceptRaiseNamed():
    try:
        print(1)
    except A as a:
        print(2)
        raise Exc

def z_TryExceptReturn():
    try:
        print(1)
        return 2
    except:
        print(2)

def z1_TryExceptReturn():
    try:
        print(1)
        return 2
    except:
        print(2)
        return 3

def aa_TryExceptReturnMulti():
    try:
        print(1)
        return 2
    except a:
        print(2)
    except b:
        print(3)

def aa1_TryExceptReturnMulti():
    try:
        print(1)
        return 2
    except a:
        print(2)
        return 3

def aa2_TryExceptReturnMulti():
    try:
        print(1)
        return 2
    except a:
        print(2)
        return 3
    except b:
        print(3)

def ab_TryExceptReturnNamed():
    try:
        print(1)
        return 2
    except A as a:
        print(2)

def ab1_TryExceptReturnNamed():
    try:
        print(1)
        return 2
    except A as a:
        print(2)
        return 3

def ac_TryFinallyBareFallthrough():
    try:
        print(1)
    finally:
        print(2)
    print(3)

def ad_TryFinallyBare():
    try:
        print(1)
    finally:
        print(2)