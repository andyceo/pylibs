from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pylibs',
    version='0.2.x',
    author="andyceo",
    author_email="andyceo@yandex.ru",
    description="Python libraries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andyceo/pylibs",
    packages=['pylibs'],
    package_dir={
        'pylibs': '.',
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
