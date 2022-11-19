from setuptools import find_packages, setup

with open("README.md", encoding="utf-8") as fh:
    long_description = fh.read()

if __name__ == "__main__":
    setup(
        name="memewizard",
        author="themysticsavages",
        description="One good source for all things memes",
        license="MIT",
        version="0.2",
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        long_description=long_description,
        long_description_content_type="text/markdown",
        packages=find_packages(),
        install_requires=[
            "prompt_toolkit",
            "requests",
            "beautifulsoup4",
            "html2image",
            "tabulate",
            "inquirerpy",
            "scikit-learn",
            "pandas",
            "numpy",
            "pytrends",
            "matplotlib",
        ],
    )
