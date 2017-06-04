from enums import *

number_of_mpu_regions = 12


def have_security_ext():
    return True


def have_virt_ext():
    return False


def arch_version():
    return 6


def jazelle_accepts_execution():
    return False


def memory_system_architecture():
    return MemArch.MemArch_PMSA


def have_lpae():
    return False


def have_mp_ext():
    return False


def have_adv_simd_or_vfp():
    return False


def have_thumbee():
    return False


def have_jazelle():
    return False


def implementation_supports_transient():
    return False


def processor_id():
    return 0


def is_armv7r_profile():
    return False


def has_imp_def_reset_vector():
    return False


memory_list = [
    # ("RAM", 0x000000, 0xFF0000)
]
