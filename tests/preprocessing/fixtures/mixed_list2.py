def foo(x):
    return x + 1

x = [1, 2, foo(3), 4, 5, 6, foo(7), 8, 9]
print(x)