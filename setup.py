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
    zip_safe=False,
    install_requires = [
        'setuptools',
        'docutils',
        'Pygments',
        'jinja2',
        'html5writer',
    ],
    dependency_links = [
        'https://github.com/MeirKriheli/rst-to-semantic-html5/tarball/master#egg=html5writer',
    ],
    entry_points = {
        'console_scripts': [
            'statirator = statirator.main:main',
        ]
    },
    classifiers = [
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
    ]
)
