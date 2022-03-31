import json

from armulator.armv6.enums import *

__all__ = ['configurations', 'number_of_mpu_regions', 'have_security_ext', 'have_virt_ext', 'arch_version',
           'jazelle_accepts_execution', 'memory_system_architecture', 'have_lpae', 'have_mp_ext',
           'have_adv_simd_or_vfp', 'have_thumbee', 'have_jazelle', 'implementation_supports_transient', 'processor_id',
           'is_armv7r_profile', 'has_imp_def_reset_vector']


class Configurations:
    def __init__(self):
        self.configs = {}

    def load(self, path):
        with open(path) as f:
            self.configs = json.load(f)

    def __getattr__(self, name):
        try:
            return self.configs[name]
        except KeyError:
            raise AttributeError(name)


configurations = Configurations()


def number_of_mpu_regions():
    return configurations.number_of_mpu_regions


def have_security_ext():
    return configurations.have_security_ext


def have_virt_ext():
    return configurations.have_virt_ext


def arch_version():
    return configurations.arch_version


def jazelle_accepts_execution():
    return configurations.jazelle_accepts_execution


def memory_system_architecture():
    return {'PMSA': MemArch.PMSA, 'VMSA': MemArch.VMSA}[configurations.memory_system_architecture]


def have_lpae():
    return configurations.have_lpae


def have_mp_ext():
    return configurations.have_mp_ext


def have_adv_simd_or_vfp():
    return configurations.have_adv_simd_or_vfp


def have_thumbee():
    return configurations.have_thumbee


def have_jazelle():
    return configurations.have_jazelle


def implementation_supports_transient():
    return configurations.implementation_supports_transient


def processor_id():
    return configurations.processor_id


def is_armv7r_profile():
    return configurations.is_armv7r_profile


def has_imp_def_reset_vector():
    return configurations.has_imp_def_reset_vector
