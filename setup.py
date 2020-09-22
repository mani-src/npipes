from setuptools import setup, find_packages

setup(
    name='npipes',
    version='1.0.0',
    license='GPL-3.0',
    description='Wrapper Library for Named Pipes',
    author='Manikanta Ambadipudi',
    author_email='ambadipudi.manikanta@gmail.com',
    url='https://github.com/mani-src/npipes.git',
    download_url='https://github.com/mani-src/npipes/archive/v1.0.tar.gz',
    install_requires=['pywin32'],
    packages=find_packages()
)