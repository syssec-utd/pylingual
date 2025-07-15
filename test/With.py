def a0_bare_with():
    with a:
        print(1)

def a1_bare_with_fallthrough():
    with a:
        print(1)
    print(2)

# Fails in 3.10, duplicate blocks explained further in issue 32
def b0_multi_with():
    with a, b:
        print(1)

def b1_multi_with_fallthrough():
    with a, b:
        print(1)
    print(2)

def c0_with_as():
    with a as c:
        print(1)

def c1_with_as_fallthrough():
    with a as c:
        print(1)
    print(2)

# Fails in 3.10, same issue as b
def d0_multi_with_as():
    with a, b as c:
        print(1)

def d1_multi_with_as_fallthrough():
    with a, b as c:
        print(1)
    print(2)

# Fails in 3.10, same issue as b
def e0_with_multi_as():
    with a as b, c:
        print(1)

def e1_with_multi_as_fallthrough():
    with a as b, c:
        print(1)
    print(2)

# Fails in 3.10, same issue as b
def f0_multi_with_multi_as():
    with a as b, c as d:
        print(1)

def f1_multi_with_multi_as_fallthrough():
    with a as b, c as d:
        print(1)
    print(2)

# Fails in 3.10, same issue as b
def g0_multi_with_multi_as_alt():
    with a, b as c, d:
        print(1)

def g1_multi_with_multi_as_fallthrough_alt():
    with a, b as c, d:
        print(1)
    print(2)

# Fails in 3.13, unexpected JUMP_BACKWARD_NO_INTERRUPT messes up the template
def h0_try_with_except():
    try:
        with a:
            print(1)
    except:
        print(2)
    print(3)

def i0_with_return():
    with a:
        return 1
    print(1)

def j0_with_raise():
    with a:
        raise Exc
    print(1)

async def k0_bare_async_with():
    async with a:
        print(1)

async def k1_bare_async_with_fallthrough():
    async with a:
        print(1)
    print(2)

async def l0_multi_async_with():
    async with a, b:
        print(1)

async def l1_multi_async_with_fallthrough():
    async with a, b:
        print(1)
    print(2)

async def m0_async_with_as():
    async with a as c:
        print(1)

async def m1_async_with_as_fallthrough():
    async with a as c:
        print(1)
    print(2)

async def n0_multi_async_with_as():
    async with a, b as c:
        print(1)

async def n1_multi_async_with_as_fallthrough():
    async with a, b as c:
        print(1)
    print(2)

async def o0_async_with_multi_as():
    async with a as b, c:
        print(1)

async def o1_async_with_multi_as_fallthrough():
    async with a as b, c:
        print(1)
    print(2)

async def p0_multi_async_with_multi_as():
    async with a as b, c as d:
        print(1)

async def p1_multi_async_with_multi_as_fallthrough():
    async with a as b, c as d:
        print(1)
    print(2)

async def q0_multi_async_with_multi_as_alt():
    async with a, b as c, d:
        print(1)

async def q1_multi_async_with_multi_as_fallthrough_alt():
    async with a, b as c, d:
        print(1)
    print(2)