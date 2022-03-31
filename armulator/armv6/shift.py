from enum import Enum, auto

from armulator.armv6 import bits_ops
from armulator.armv6.bits_ops import substring, bit_at, chain, lower_chunk


class SRType(Enum):
    LSL = auto()
    LSR = auto()
    ASR = auto()
    ROR = auto()
    RRX = auto()


def decode_imm_shift(type_o, imm5):
    if type_o == 0b00:
        shift_t = SRType.LSL
        shift_n = imm5
    elif type_o == 0b01:
        shift_t = SRType.LSR
        shift_n = 32 if imm5 == 0b00000 else imm5
    elif type_o == 0b10:
        shift_t = SRType.ASR
        shift_n = 32 if imm5 == 0b00000 else imm5
    elif type_o == 0b11:
        if imm5 == 0b00000:
            shift_t = SRType.RRX
            shift_n = 1
        else:
            shift_t = SRType.ROR
            shift_n = imm5
    return shift_t, shift_n


def decode_reg_shift(type_o: int) -> SRType:
    if type_o == 0b00:
        shift_t = SRType.LSL
    elif type_o == 0b01:
        shift_t = SRType.LSR
    elif type_o == 0b10:
        shift_t = SRType.ASR
    elif type_o == 0b11:
        shift_t = SRType.ROR
    return shift_t


def lsl_c(x, x_len, shift):
    assert shift > 0
    extended_x = x << shift
    return bits_ops.lower_chunk(extended_x, x_len), (extended_x >> x_len) & 1


def lsl(x, x_len, shift):
    assert shift >= 0
    if shift == 0:
        result = x
    else:
        result = lsl_c(x, x_len, shift)[0]
    return result


def lsr_c(x, x_len, shift):
    assert shift > 0
    result = substring(x, shift + x_len - 1, shift)
    carry_out = bit_at(x, shift - 1)
    return result, carry_out


def lsr(x, x_len, shift):
    assert shift >= 0
    if shift == 0:
        result = x
    else:
        result = lsr_c(x, x_len, shift)[0]
    return result


def asr_c(x, x_len, shift):
    assert shift > 0
    extended_x = bits_ops.sign_extend(x, x_len, shift + x_len)
    result = substring(extended_x, shift + x_len - 1, shift)
    carry_out = bit_at(extended_x, shift - 1)
    return result, carry_out


def asr(x, x_len, shift):
    assert shift >= 0
    if shift == 0:
        result = x
    else:
        result = asr_c(x, x_len, shift)[0]
    return result


def ror_c(x, x_len, shift):
    assert shift != 0
    m = shift % x_len
    result = lsr(x, x_len, m) | lsl(x, x_len, x_len - m)
    carry_out = bit_at(result, x_len - 1)
    return result, carry_out


def ror(x, x_len, shift):
    if shift == 0:
        result = x
    else:
        result = ror_c(x, x_len, shift)[0]
    return result


def rrx_c(x, x_len, carry_in):
    result = chain(carry_in, substring(x, x_len - 1, 1), x_len - 1)
    carry_out = bit_at(x, 0)
    return result, carry_out


def rrx(x, x_len, carry_in):
    result = rrx_c(x, x_len, carry_in)[0]
    return result


def shift_c(value, value_len, type_o, amount, carry_in):
    assert not (type_o == SRType.RRX and amount != 1)
    if amount == 0:
        result, carry_out = value, int(carry_in)
    else:
        if type_o == SRType.LSL:
            result, carry_out = lsl_c(value, value_len, amount)
        elif type_o == SRType.LSR:
            result, carry_out = lsr_c(value, value_len, amount)
        elif type_o == SRType.ASR:
            result, carry_out = asr_c(value, value_len, amount)
        elif type_o == SRType.ROR:
            result, carry_out = ror_c(value, value_len, amount)
        elif type_o == SRType.RRX:
            result, carry_out = rrx_c(value, value_len, int(carry_in))
    return result, carry_out


def shift(value, value_len, type_o, amount, carry_in):
    result = shift_c(value, value_len, type_o, amount, carry_in)[0]
    return result


def arm_expand_imm_c(imm12: int, carry_in: int):
    unrotated_value = substring(imm12, 7, 0)
    return shift_c(unrotated_value, 32, SRType.ROR, 2 * substring(imm12, 11, 8), carry_in)


def arm_expand_imm(imm12: int):
    # APSR.C argument to following function call does not affect the imm32 result.
    return arm_expand_imm_c(imm12, 0)[0]


def thumb_expand_imm_c(imm12: int, carry_in: int):
    if substring(imm12, 11, 10) == 0b00:
        imm_9_8 = substring(imm12, 9, 8)
        lower_byte = lower_chunk(imm12, 8)
        if imm_9_8 == 0b00:
            imm32 = lower_byte
        elif imm_9_8 == 0b01:
            if lower_byte == 0b00000000:
                print('unpredictable')
            imm32 = chain(lower_byte, lower_byte, 16)
        elif imm_9_8 == 0b10:
            if lower_byte == 0b00000000:
                print('unpredictable')
            imm32 = chain(lower_byte, lower_byte << 8, 24)
        elif imm_9_8 == 0b11:
            if lower_byte == 0b00000000:
                print('unpredictable')
            imm32 = chain(lower_byte, chain(lower_byte, chain(lower_byte, lower_byte, 8), 16), 24)
        carry_out = carry_in
    else:
        unrotated_value = chain(1, substring(imm12, 6, 0), 7)
        imm32, carry_out = ror_c(unrotated_value, 8, substring(imm12, 11, 7))
    return imm32, carry_out


def thumb_expand_imm(imm12: int) -> int:
    # APSR.C argument to following function call does not affect the imm32 result.
    return thumb_expand_imm_c(imm12, 0)[0]
