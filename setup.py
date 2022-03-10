from setuptools import setup, find_packages

long_description = open('README.md', encoding='utf-8').read()

setup(
    name="memewizard",
    author='themysticsavages',
    description='One good source for all things memes',
    license='MIT',
    version="0.0.5.1",
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    long_description=long_description,      
    long_description_content_type='text/markdown',
    packages=find_packages(),
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
