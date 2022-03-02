import pytest

from armulator.armv6.bits_ops import *


@pytest.mark.parametrize('bits, length, result', [
    (0b01, 2, 1),
    (0b11, 2, -1),
    (0b1110, 4, -2),
])
def test_to_signed(bits, length, result):
    assert to_signed(bits, length) == result


@pytest.mark.parametrize('bits, msb, lsb, result', [
    (0b0110, 2, 0, 0b110),
    (0b1110010101, 8, 5, 0b1100),
])
def test_substring(bits, msb, lsb, result):
    assert substring(bits, msb, lsb) == result


@pytest.mark.parametrize('bits, length, result', [
    (0b01, 2, 0),
    (0b11, 2, 0),
    (0b1110, 4, 1),
    (0b00111000, 8, 3),
])
def test_lowest_set_bit_ref(bits, length, result):
    assert lowest_set_bit_ref(bits, length) == result


@pytest.mark.parametrize('bits, src_length, dst_length, result', [
    (0b00, 2, 4, 0b0000),
    (0b01, 2, 4, 0b0001),
    (0b10, 2, 4, 0b1110),
    (0b11, 2, 4, 0b1111),

])
def test_sign_extend(bits, src_length, dst_length, result):
    assert sign_extend(bits, src_length, dst_length) == result


@pytest.mark.parametrize('x, y, carry_in, x_size, result, carry_out, overflow', [
    (0x00000001, 0x00000001, 0, 32, 0x00000002, 0, 0),
    (0x00000001, 0xfffffffe, 1, 32, 0x00000000, 1, 0),
])
def test_add_with_carry(x, y, carry_in, x_size, result, carry_out, overflow):
    assert add_with_carry(x, y, carry_in, x_size) == (result, carry_out, overflow)


@pytest.mark.parametrize('bits, length, result', [
    (0b01, 2, 0b10),
    (0b11, 2, 0b00),
    (0b1110, 4, 0b0001),
    (0x00006600, 32, 0xFFFF99FF),
])
def test_bit_not(bits, length, result):
    assert bit_not(bits, length) == result


@pytest.mark.parametrize('bits, length, result', [
    (0xAA, 1, 0xAA),
    (0xAABB, 2, 0xBBAA),
    (0x11223344, 4, 0x44332211),
    (0x44000000, 4, 0x00000044),
    (0x1122334455667788, 8, 0x8877665544332211),
])
def test_big_endian_reverse(bits, length, result):
    assert big_endian_reverse(bits, length) == result
