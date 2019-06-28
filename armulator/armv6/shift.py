from bitstring import BitArray
from enum import Enum
import bits_ops

SRType = Enum("SRType", "SRType_LSL SRType_LSR SRType_ASR SRType_ROR SRType_RRX")


def decode_imm_shift(type_o, imm5):
    if type_o.bin == "00":
        shift_t = SRType.SRType_LSL
        shift_n = imm5.uint
    elif type_o.bin == "01":
        shift_t = SRType.SRType_LSR
        shift_n = 32 if imm5.bin == "00000" else imm5.uint
    elif type_o.bin == "10":
        shift_t = SRType.SRType_ASR
        shift_n = 32 if imm5.bin == "00000" else imm5.uint
    elif type_o.bin == "11":
        if imm5.bin == "00000":
            shift_t = SRType.SRType_RRX
            shift_n = 1
        else:
            shift_t = SRType.SRType_ROR
            shift_n = imm5.uint
    return shift_t, shift_n


def decode_reg_shift(type_o):
    if type_o.bin == "00":
        shift_t = SRType.SRType_LSL
    elif type_o.bin == "01":
        shift_t = SRType.SRType_LSR
    elif type_o.bin == "10":
        shift_t = SRType.SRType_ASR
    elif type_o.bin == "11":
        shift_t = SRType.SRType_ROR
    return shift_t


def lsl_c(x, shift):
    assert shift > 0
    extended_x = x + bits_ops.zeros(shift)
    result = extended_x[-x.len:]
    carry_out = extended_x[-(x.len + 1)]
    return result, carry_out


def lsl(x, shift):
    assert shift >= 0
    if shift == 0:
        result = x
    else:
        result = lsl_c(x, shift)[0]
    return result


def lsr_c(x, shift):
    assert shift > 0
    extended_x = bits_ops.zero_extend(x, shift + x.len)
    result = extended_x[-(x.len + shift):-shift]
    carry_out = extended_x[-shift]
    return result, carry_out


def lsr(x, shift):
    assert shift >= 0
    if shift == 0:
        result = x
    else:
        result = lsr_c(x, shift)[0]
    return result


def asr_c(x, shift):
    assert shift > 0
    extended_x = bits_ops.sign_extend(x, shift + x.len)
    result = extended_x[-(x.len + shift):-shift]
    carry_out = extended_x[-shift]
    return result, carry_out


def asr(x, shift):
    assert shift >= 0
    if shift == 0:
        result = x
    else:
        result = asr_c(x, shift)[0]
    return result


def ror_c(x, shift):
    assert shift != 0
    m = shift % x.len
    result = lsr(x, m) | lsl(x, x.len - m)
    carry_out = result[0]
    return result, carry_out


def ror(x, shift):
    if shift == 0:
        result = x
    else:
        result = ror_c(x, shift)[0]
    return result


def rrx_c(x, carry_in):
    result = BitArray(uint=carry_in, length=1) + x[:-1]
    carry_out = x[-1]
    return result, carry_out


def rrx(x, carry_in):
    result = rrx_c(x, carry_in)[0]
    return result


def shift_c(value, type_o, amount, carry_in):
    assert not (type_o == SRType.SRType_RRX and amount != 1)
    if amount == 0:
        result, carry_out = value, int(carry_in)
    else:
        if type_o == SRType.SRType_LSL:
            result, carry_out = lsl_c(value, amount)
        elif type_o == SRType.SRType_LSR:
            result, carry_out = lsr_c(value, amount)
        elif type_o == SRType.SRType_ASR:
            result, carry_out = asr_c(value, amount)
        elif type_o == SRType.SRType_ROR:
            result, carry_out = ror_c(value, amount)
        elif type_o == SRType.SRType_RRX:
            result, carry_out = rrx_c(value, int(carry_in))
    return result, carry_out


def shift(value, type_o, amount, carry_in):
    result = shift_c(value, type_o, amount, carry_in)[0]
    return result


def arm_expand_imm_c(imm12, carry_in):
    unrotated_value = bits_ops.zero_extend(imm12[4:], 32)
    return shift_c(unrotated_value, SRType.SRType_ROR, 2 * imm12[0:4].uint, carry_in)


def arm_expand_imm(imm12):
    # APSR.C argument to following function call does not affect the imm32 result.
    return arm_expand_imm_c(imm12, "0")[0]


def thumb_expand_imm_c(imm12, carry_in):
    if imm12[0:2] == "0b00":
        if imm12[2:4] == "0b00":
            imm32 = bits_ops.zero_extend(imm12[4:12], 32)
        elif imm12[2:4] == "0b01":
            if imm12[4:12] == "0b00000000":
                print("unpredictable")
            imm32 = "0b00000000" + imm12[4:12] + "0b00000000" + imm12[4:12]
        elif imm12[2:4] == "0b10":
            if imm12[4:12] == "0b00000000":
                print("unpredictable")
            imm32 = imm12[4:12] + "0b00000000" + imm12[4:12] + "0b00000000"
        elif imm12[2:4] == "0b11":
            if imm12[4:12] == "0b00000000":
                print("unpredictable")
            imm32 = imm12[4:12] + imm12[4:12] + imm12[4:12] + imm12[4:12]
        carry_out = carry_in
    else:
        unrotated_value = bits_ops.zero_extend("0b1" + imm12[5:12], 32)
        imm32, carry_out = ror_c(unrotated_value, imm12[0:5].uint)
    return imm32, carry_out


def thumb_expand_imm(imm12):
    # APSR.C argument to following function call does not affect the imm32 result.
    return thumb_expand_imm_c(imm12, "0")[0]
