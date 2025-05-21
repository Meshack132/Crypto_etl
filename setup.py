from setuptools import setup, find_packages

setup(
    name="crypto_etl",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'requests',
        'pandas',
        'matplotlib',
        'sqlite3'
    ],
)