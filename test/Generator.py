import asyncio

# Test 1: Simple async generator
async def gen1():
    yield 1
    yield 2

# Test 2: Async generator with await
async def gen2():
    await asyncio.sleep(0)
    yield "done"

# Test 3: Async generator using a loop
async def gen3():
    for i in range(3):
        yield i

# Test 4: Async generator with async for loop (consuming another async generator)
async def gen4():
    async for x in gen3():
        yield x

# Test 5: Async generator with async with
class DummyContext:
    async def __aenter__(self): return self
    async def __aexit__(self, exc_type, exc, tb): pass

async def gen5():
    async with DummyContext():
        yield "inside context"

# Test 6: Async generator that returns (implicitly ends)
async def gen6():
    yield "hello"
    return  # Ends the generator

# Test 7: Nested yield and await
async def gen7():
    yield await asyncio.sleep(0, result="nested")

# Test 8: Function using 'yield' but not 'async def' (should be a regular generator)
def regular_gen():
    yield "normal generator"

# Test 9: Coroutine consuming async generator
async def consume_gen():
    async for item in gen2():
        pass

# Test 10: Calling an async generator (should return an async generator object)
g = gen1()
assert hasattr(g, '__anext__')  # Just to test that it's an async generator object

# Test 11: Async generator with try/finally
async def gen11():
    try:
        yield "try"
    finally:
        await asyncio.sleep(0)

# Test 12: Async generator with exception handling
async def gen12():
    try:
        raise ValueError("fail")
    except ValueError:
        yield "handled"
