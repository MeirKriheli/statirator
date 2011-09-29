from setuptools import setup

setup(
    name='statirator',
    version='0.1.0',
    author='Meir Kriheli',
    author_email='mkriheli@gmail.com',
    packages=['statirator'],
    url='http://pypi.python.org/pypi/statirator/',
    license='LICENSE.txt',
    description='Multilingual static site and blog generator',
    long_description=open('README.rst').read(),
    install_requires = [
        'setuptools',
        'docutils',
        'Pygments',
        'tornado',
    ]
)
