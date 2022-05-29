from pathlib import Path

from setuptools import setup, find_packages

BASE_DIR = Path(__file__).parent.resolve(strict=True)
VERSION = '1.1.2'
PACKAGES = [p for p in find_packages() if not p.startswith('tests')]


def get_description():
    return (BASE_DIR / 'README.md').read_text()


if __name__ == '__main__':
    setup(
        version=VERSION,
        name='armulator',
        description='A pure Python ARM processor emulator',
        long_description=get_description(),
        long_description_content_type='text/markdown',
        url='https://github.com/matan1008/armulator',
        author='Matan Perelman',
        author_email='matan1008@gmail.com',
        classifiers=[
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
            'Programming Language :: Python :: 3.9',
            'Programming Language :: Python :: 3.10',
        ],
        keywords='arm emulator',
        packages=PACKAGES,
        license='MIT',
        package_data={
            'armulator': ['armv6/arm_configurations.json'],
        },
        tests_require=['pytest'],
    )
