from setuptools import setup, find_packages

setup(
    name='npipes',
    version='1.0.0',
    description='Wrapper Library for Named Pipes',
    author='Manikanta Ambadipudi',
    author_email='ambadipudi.manikanta@gmail.com',
    url='https://github.com/mani-src/npipes.git',
    install_requires=['pywin32'],
    packages=find_packages()
)