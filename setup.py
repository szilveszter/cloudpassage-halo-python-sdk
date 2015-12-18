import os
from setuptools import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
        name = "cloudpassage",
        version = "0.9.9",
        author = "CloudPassage",
        author_email = "toolbox@cloudpassage.com",
        description = "Python SDK for CloudPassage Halo API",
        license = "BSD",
        keywords = "cloudpassage halo api sdk",
        url = "http://github.com/cloudpassage/cloudpassage-halo-python-sdk",
        packages = ["cloudpassage"],
        install_requires = ["requests", "pyaml"],
        long_description = read("README.md"),
        classifiers = [
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: POSIX :: Linux",
            "Programming Language :: Python :: 2.7",
            "Topic :: Security",
            "License :: OSI Approved :: BSD License"
            ],
        )
