y = [x**2 for x in range(10)]
x = [1, 2, 3]
for x in x[1:-1]:
    x = sorted(lambda x: x, x)
    if x > 1:
        pass
    while (len(x) > 1 and len(x) < 10) or True:
        x = sorted(lambda x: -x, x)
