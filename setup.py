from setuptools import setup, find_packages
setup(
    name="memewizard",
    version="0.1",
    package_data={'library': ['library.py']},
    packages=find_packages('src'),
    entry_points={'console_scripts': ['memewizard = memewizard.cli:main'], },
)

