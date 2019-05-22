
from setuptools import setup, find_packages

setup(name='goal_app', packages=find_packages('.'), extras_require={
    'test': ['mockito']
})
