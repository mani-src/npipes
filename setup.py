from setuptools import setup, find_packages

setup(
    name='npipes',
    version='1.0.2',
    license='GPL-3.0',
    description='Wrapper Library for Named Pipes',
    long_description='Provides a ready to use set of APIs to create and communicate via Named Pipes on Windows, '
                     'based on win32pipes',
    author='Manikanta Ambadipudi',
    author_email='ambadipudi.manikanta@gmail.com',
    url='https://github.com/mani-src/npipes/blob/master/README.md',
    download_url='https://github.com/mani-src/npipes/archive/v1.0.1.tar.gz',
    install_requires=['pywin32'],
    packages=find_packages()
)