# First 100 primes.
primes = [  2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
            31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
            73, 79, 83, 89, 97, 101, 103, 107, 109, 113,
            127, 131, 137, 139, 149, 151, 157, 163, 167, 173,
            179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
            233, 239, 241, 251, 257, 263, 269, 271, 277, 281,
            283, 293, 307, 311, 313, 317, 331, 337, 347, 349,
            353, 359, 367, 373, 379, 383, 389, 397, 401, 409,
            419, 421, 431, 433, 439, 443, 449, 457, 461, 463,
            467, 479, 487, 491, 499, 503, 509, 521, 523, 541,]

def factorize(n: int) -> dict[int, int]:
    f"""Outputs the prime factors of input and the number of time it appeared. 
    e.g. 984 should output [(2,3), (3,1), (41,1)]. Limited to the {len(primes)} first primes."""

    output = {}
    for prime in primes:
        if n == 1:
            return output       
        factor_quantity = 0
        while n % prime == 0:
            n = n/prime
            factor_quantity += 1
        if factor_quantity == 0:
            continue
        output[prime] = factor_quantity
    assert False, f"The input number has factor beyond the first {len(primes)} primes."