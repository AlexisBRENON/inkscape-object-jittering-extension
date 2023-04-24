import math
import random


def correlation(n: int) -> list[float]:
    """ https://en.wikipedia.org/wiki/Low-discrepancy_sequence#Random_numbers """
    return [random.random() + (0.5 * (i % 2)) for i in range(n)]

def additive_recurrence(n: int) -> list[float]:
    """ https://en.wikipedia.org/wiki/Low-discrepancy_sequence#Additive_recurrence """
    alpha = math.sqrt(random.choice((2, 3, 5, 7, 11, 13, 17, 19, 23))) % 1
    init = random.random()
    return [(init + i * alpha) % 1 for i in range(n)]

def additive_recurrence2(n: int) -> list[float]:
    """ https://en.wikipedia.org/wiki/Low-discrepancy_sequence#Additive_recurrence """
    alpha = math.sqrt(random.choice((2, 3, 5, 7, 11, 13, 17, 19, 23))) % 1
    previous = random.random()
    values = [previous]
    for _ in range(1, n):
        values.append((previous + alpha) % 1)
    return values

def vdc(n: int, base: int = 2) -> list[float]:
    """
    https://en.wikipedia.org/wiki/Low-discrepancy_sequence#van_der_Corput_sequence
    """
    def corput(n: int):
        q = 0
        bk = 1.0 / base
        while n > 0:
            q += (n % base) * bk
            n //= base
            bk /= base
        return q

    return [corput(i) for i in range(n)]

def sobol(n: int) -> list[float]:
    """
    https://en.wikipedia.org/wiki/Low-discrepancy_sequence#Sobol%E2%80%99_sequence
    """
    result = [0.0] * n
    v = 1
    for i in range(n):
        v ^= v >> 1
        result[i] = v / 2**32
    return result


def poisson_disk_sampling(n: int, r: float = 0.01, k: int = 30) -> list[float]:
    """
    https://en.wikipedia.org/wiki/Low-discrepancy_sequence#Poisson_disk_sampling
    """
    raise NotImplementedError()
