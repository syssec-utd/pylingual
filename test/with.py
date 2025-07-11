def bare_with():
    with a:
        print(1)


def bare_with_fallthrough():
    with a:
        print(1)
    print(2)


## Known to fail on 3.10
def multi_with():
    with a, b:
        print(1)


def multi_with_fallthrough():
    with a, b:
        print(1)
    print(2)


def with_as():
    with a as c:
        print(1)


def with_as_fallthrough():
    with a as c:
        print(1)
    print(2)


def multi_with_as():
    with a, b as c:
        print(1)


def multi_with_as_fallthrough():
    with a, b as c:
        print(1)
    print(2)


def with_multi_as():
    with a as b, c:
        print(1)


def with_multi_as_fallthrough():
    with a as b, c:
        print(1)
    print(2)


def multi_with_multi_as():
    with a as b, c as d:
        print(1)


# Known to fail on 3.10
def multi_with_multi_as_fallthrough():
    with a as b, c as d:
        print(1)
    print(2)


def multi_with_multi_as_alt():
    with a, b as c, d:
        print(1)


# Known to fail on 3.10
def multi_with_multi_as_fallthrough_alt():
    with a, b as c, d:
        print(1)
    print(2)


async def bare_async_with():
    async with a:
        print(1)


async def bare_async_with_fallthrough():
    async with a:
        print(1)
    print(2)


## Known to fail on 3.10
async def multi_async_with():
    async with a, b:
        print(1)


async def multi_async_with_fallthrough():
    async with a, b:
        print(1)
    print(2)


async def with_as():
    async with a as c:
        print(1)


async def with_as_fallthrough():
    async with a as c:
        print(1)
    print(2)


async def multi_async_with_as():
    async with a, b as c:
        print(1)


async def multi_async_with_as_fallthrough():
    async with a, b as c:
        print(1)
    print(2)


async def with_multi_as():
    async with a as b, c:
        print(1)


async def with_multi_as_fallthrough():
    async with a as b, c:
        print(1)
    print(2)


async def multi_async_with_multi_as():
    async with a as b, c as d:
        print(1)


# Known to fail on 3.10
async def multi_async_with_multi_as_fallthrough():
    async with a as b, c as d:
        print(1)
    print(2)


async def multi_async_with_multi_as_alt():
    async with a, b as c, d:
        print(1)


# Known to fail on 3.10
async def multi_async_with_multi_as_fallthrough_alt():
    async with a, b as c, d:
        print(1)
    print(2)


def try_with_except():
    # With statement with outer exception handler
    try:
        with a:
            print(1)
    except:
        print(2)
    print(3)


def with_return():
    # With statement with return
    with a:
        return 1
    print(1)


def with_raise():
    # With statement with raise
    with a:
        raise Exc
    print(1)
