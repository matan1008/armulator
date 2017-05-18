from enums import *

number_of_mpu_regions = 12


def HaveSecurityExt():
    return True


def HaveVirtExt():
    return False


def ArchVersion():
    return 6


def JazelleAcceptsExecution():
    return False


def MemorySystemArchitecture():
    return MemArch.MemArch_PMSA


def HaveLPAE():
    return False


def HaveMPExt():
    return False


def HaveAdvSIMDorVFP():
    return False


def HaveThumbEE():
    return False


def HaveJazelle():
    return False


def ImplementationSupportsTransient():
    return False


def ProcessorID():
    return 0


def is_armv7r_profile():
    return False


def HasIMPDEFResetVactor():
    return False


memory_list = [
    # ("RAM", 0x000000, 0xFF0000)
]
