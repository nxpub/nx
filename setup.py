from setuptools import setup, find_packages

setup(
    name='nx',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'nx=nx.cli:run',
        ],
    },
)
