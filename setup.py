from setuptools import setup
from pip.req import parse_requirements
import sys, os
sys.path.append("wutu_compiler/")

install_reqs = list(parse_requirements("requirements.txt", session={}))


def version():
    import version
    return version.get_version()


setup(name="wutu",
        version=version(),
        description="An utility library designed to create JavaScript out of Python code",
        author="Šarūnas Navickas",
        author_email="zaibacu@gmail.com",
        url="https://github.com/zaibacu/wutu-compiler",
        license="MIT",
        packages=["wutu_compiler"],
        install_requires=[str(ir.req) for ir in install_reqs],
        tests_require=["pytest"],
        setup_require=["pytest-runner"])
