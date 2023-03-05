import random


def fast_pow(number: int, exp: int, mod: int) -> int:
    result = 1
    while exp:
        if exp & 1:
            result = result * number % mod
        exp >>= 1
        number = number * number % mod
    return result


def euclidean_algorithm_simple(a: int, b: int) -> int:
    if a < b:
        a, b = b, a
    while a % b:
        temp_b = b
        b = a % b
        a = temp_b
    return b


def miller_rabin(num: int, rounds: int | None = None) -> bool:
    if rounds is None:
        rounds = num.bit_length()
    if num == 2:
        return True
    if num % 2 == 0:
        return False
    t = num - 1
    s = 0
    while t % 2 == 0:
        t //= 2
        s += 1

    for _ in range(rounds):
        a = random.randint(2, num - 1)
        x = fast_pow(a, t, num)
        if x == 1 or x == num - 1:
            continue
        for _ in range(s - 1):
            x = fast_pow(x, 2, num)
            if x == 1:
                return False
            if x == num - 1:
                break
        else:
            return False
    return True


def get_safe_prime(bit_len: int) -> int:
    x = random.randint(2 ** (bit_len - 1), 2**bit_len)
    while not miller_rabin(x) or not miller_rabin((x - 1) // 2):
        x = random.randint(2 ** (bit_len - 1), 2**bit_len)
    return x


def get_primitive_root(bit_len: int, p: int) -> int:
    euler = p - 1
    g = random.randint(2 ** (bit_len - 1), 2**bit_len)
    while True:
        if (
            fast_pow(g, euler, p) == 1
            and euclidean_algorithm_simple(g, p) == 1
            and fast_pow(g, euler // 2, p) != 1
            and miller_rabin(g)
        ):
            return g
        g = random.randint(2 ** (bit_len - 1), 2**bit_len)