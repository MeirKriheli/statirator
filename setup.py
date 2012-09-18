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
    install_requires=[
        'setuptools',
        'docutils',
        'Pygments',
        'html5writer',
        'Django==1.4.1',
        'django-taggit',
        'django-medusa',
        'django-disqus',
    ],
    dependency_links=[
        'https://github.com/MeirKriheli/rst-to-semantic-html5/tarball/master#egg=html5writer',
        'https://github.com/mtigas/django-medusa/tarball/master#egg=django-medusa',
    ],
    entry_points={
        'console_scripts': [
            'statirator = statirator.main:main',
        ]
    },
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Operating System :: OS Independent',
    ]
)
