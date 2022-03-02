def add(bits1: int, bits2: int, length: int) -> int:
    return (bits1 + bits2) % (2 ** length)


def sub(bits1: int, bits2: int, length: int) -> int:
    return (bits1 - bits2) % (2 ** length)


def sign_extend(x: int, src_length: int, dst_length: int) -> int:
    return to_unsigned(to_signed(x, src_length), dst_length)


def to_signed(bits: int, length: int) -> int:
    real_num_length = (length - 1)
    negative_bit = bits >> real_num_length
    if negative_bit:
        # Negative
        return (bits - (negative_bit << real_num_length)) - (2 ** real_num_length)
    else:
        return bits


def to_unsigned(bits: int, length: int) -> int:
    return bits % (2 ** length)


def lower_chunk(bits: int, chunk_length: int) -> int:
    return bits & ((2 ** chunk_length) - 1)


def add_with_carry(x: int, y: int, carry_in: int, size: int = 32):
    unsigned_sum = x + y + carry_in
    signed_sum = to_signed(x, size) + to_signed(y, size) + carry_in
    result = lower_chunk(unsigned_sum, size)
    carry_out = 0 if result == unsigned_sum else 1
    overflow = 0 if to_signed(result, size) == signed_sum else 1
    return result, carry_out, overflow


def signed_sat_q(i: int, n: int):
    if i > (2 ** (n - 1) - 1):
        result = 2 ** (n - 1) - 1
        saturated = True
    elif i < -1 * (2 ** (n - 1)):
        result = -1 * (2 ** (n - 1))
        saturated = True
    else:
        result = i
        saturated = False
    return to_unsigned(result, n), saturated


def unsigned_sat_q(i: int, n: int):
    if i > (2 ** n - 1):
        result = 2 ** n - 1
        saturated = True
    elif i < 0:
        result = 0
        saturated = True
    else:
        result = i
        saturated = False
    return result, saturated


def signed_sat(i: int, n: int) -> int:
    result = signed_sat_q(i, n)[0]
    return result


def unsigned_sat(i: int, n: int) -> int:
    result = unsigned_sat_q(i, n)[0]
    return result


def sat_q(i: int, n: int, unsigned: bool):
    return unsigned_sat_q(i, n) if unsigned else signed_sat_q(i, n)


def sat(i: int, n: int, unsigned: bool):
    result = unsigned_sat(i, n) if unsigned else signed_sat(i, n)
    return result


def align(x: int, y: int) -> int:
    return y * (x // y)


def lowest_set_bit_ref(x: int, length: int = 32) -> int:
    if not x:
        return length
    for i in range(length - 1, -1, -1):
        if x % (2 ** i) == 0:
            return i


def substring(bits: int, msb: int, lsb: int) -> int:
    return lower_chunk(bits, msb + 1) >> lsb


def bit_not(bits: int, length: int) -> int:
    return bits ^ ((1 << length) - 1)


def set_substring(bits: int, msb: int, lsb: int, value: int) -> int:
    mask_length = msb + 1 - lsb
    mask = ((2 ** mask_length) - 1) << lsb
    return (bits & bit_not(mask, 256)) | value << lsb


def bit_at(bits: int, index: int) -> int:
    return substring(bits, index, index)


def set_bit_at(bits: int, index: int, value: int) -> int:
    return set_substring(bits, index, index, value)


def chain(higher: int, lower: int, lower_length: int) -> int:
    return (higher << lower_length) + lower


def bit_count(bits: int, bit: int, length: int) -> int:
    bits_ones = bin(bits).count('1')
    if bit:
        return bits_ones
    else:
        return length - bits_ones


def big_endian_reverse(value: int, n: int) -> int:
    assert n == 1 or n == 2 or n == 4 or n == 8
    result = 0
    if n == 1:
        result = value
    elif n == 2:
        result = chain(lower_chunk(value, 8), substring(value, 15, 8), 8)
    elif n == 4:
        result = chain(lower_chunk(value, 8), substring(value, 15, 8), 8)
        result = chain(result, substring(value, 23, 16), 8)
        result = chain(result, substring(value, 31, 24), 8)
    elif n == 8:
        result = chain(lower_chunk(value, 8), substring(value, 15, 8), 8)
        result = chain(result, substring(value, 23, 16), 8)
        result = chain(result, substring(value, 31, 24), 8)
        result = chain(result, substring(value, 39, 32), 8)
        result = chain(result, substring(value, 47, 40), 8)
        result = chain(result, substring(value, 55, 48), 8)
        result = chain(result, substring(value, 63, 56), 8)
    return result


def is_ones(bits: int, length: int) -> bool:
    return bit_count(bits, 1, length) == length
