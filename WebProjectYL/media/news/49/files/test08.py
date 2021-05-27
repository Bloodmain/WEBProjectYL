from random import randint
n = 100000
print(n)
print(*(randint(-100, 100) for _ in range(n)), sep=' ')