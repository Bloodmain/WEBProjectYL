from functools import lru_cache


def moves(h):
    a, b = h
    if a <= 0 or b <= 0:
        return []

    return (a - 1, b), (a, b - 1), (a // 2, b), (a, b // 2)


@lru_cache
def ans(h):
    if sum(h) <= 20:
        return 'W'
    if any(ans(m) == 'W' for m in moves(h)):
        return 'P1'
    if all(ans(m) == 'P1' for m in moves(h)):
        return 'V1'
    if any(ans(m) == 'V1' for m in moves(h)):
        return 'P2'
    if all(ans(m) in {'P1', 'P2'} for m in moves(h)):
        return 'V2'

    return '-'


for s in range(11, 70):
    print(s, ans((10, s)))