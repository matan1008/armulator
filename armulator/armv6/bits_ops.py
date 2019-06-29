from bitstring import BitArray
from builtins import range


def top_bit(value):
    return value.bin[0]


def replicate(x, n):
    return BitArray(bin=n * x.bin)


def zeros(n):
    return replicate(BitArray(bin="0"), n)


def ones(n):
    return replicate(BitArray(bin="1"), n)


def add(b_array1, b_array2, leng):
    return BitArray(uint=((b_array1.uint + b_array2.uint) % (2 ** leng)), length=leng)


def sub(b_array1, b_array2, leng):
    return BitArray(uint=((b_array1.uint - b_array2.uint) % (2 ** leng)), length=leng)


def zero_extend(x, i):
    return replicate(BitArray(bin="0"), i - x.len) + x


def sign_extend(x, i):
    return replicate(BitArray(bin=top_bit(x)), i - x.len) + x


def int_f(x, unsigned):
    return x.uint if unsigned else x.int


def add_with_carry(x, y, carry_in):
    unsigned_sum = x.uint + y.uint + int(carry_in)
    signed_sum = x.int + y.int + int(carry_in)
    result = BitArray(uint=unsigned_sum, length=x.len + 1)[-x.len:]
    carry_out = "0" if result.uint == unsigned_sum else "1"
    overflow = "0" if result.int == signed_sum else "1"
    return result, carry_out, overflow


def highest_set_bit(x):
    tup = x.find("0b1")
    return tup[0] if tup else -1


def count_leading_zero_bits(x):
    return x.len - 1 - highest_set_bit(x)


def signed_sat_q(i, n):
    if i > (2 ** (n - 1) - 1):
        result = 2 ** (n - 1) - 1
        saturated = True
    elif i < -1 * (2 ** (n - 1)):
        result = -1 * (2 ** (n - 1))
        saturated = True
    else:
        result = i
        saturated = False
    return BitArray(uint=result, length=n), saturated


def unsigned_sat_q(i, n):
    if i > (2 ** n - 1):
        result = 2 ** n - 1
        saturated = True
    elif i < 0:
        result = 0
        saturated = True
    else:
        result = i
        saturated = False
    return BitArray(uint=result, length=n), saturated


def signed_sat(i, n):
    result = signed_sat_q(i, n)[0]
    return result


def unsigned_sat(i, n):
    result = unsigned_sat_q(i, n)[0]
    return result


def sat_q(i, n, unsigned):
    return unsigned_sat_q(i, n) if unsigned else signed_sat_q(i, n)


def sat(i, n, unsigned):
    result = unsigned_sat(i, n) if unsigned else signed_sat(i, n)
    return result


def align_int(x, y):
    return y * (x // y)


def align(x, y):
    return BitArray(uint=align_int(x.uint, y), length=x.len)


def lowest_set_bit_ref(x):
    if x.all(False):
        return x.len
    else:
        for i in range(x.find("0b1")[0], x.len):
            if x.uint % (2 ** i) == 0:
                return i
