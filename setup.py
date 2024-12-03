from setuptools import setup, find_packages

from python_logging import __version__

setup(
    name='python-logging',
    version=__version__,

    url='https://github.com/envalue-real-estate/python-logging',
    author='Theo van Oostrum',
    author_email='theo.vanoostrum@envalue.com',

    packages=find_packages(),

    install_requires=[
        'fastapi~=0.115.0',
        'redis~=5.2'
    ]
)