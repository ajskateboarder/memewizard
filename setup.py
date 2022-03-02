from setuptools import setup, find_packages
setup(
    name="memewizard",
    version="0.1",
    package_data={'library': ['library.py']},
    packages=find_packages('src'),
    entry_points={'console_scripts': ['memewizard = memewizard.cli:main'], },
    install_requires=[
     'thefuzz',
     'prompt_toolkit==1.0.14',
     'tqdm',
     'requests',
     'beautifulsoup4',
     'html2image',
     'tabulate',
     'PyInquirer',
     'sklearn',
     'pandas',
     'numpy',
     'pytrends',
     'matplotlib',   
    ]
)
