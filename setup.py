from setuptools import setup

setup(
    name='educats-cli',
    version='0.1.0',
    py_modules=['educats'],
    install_requires=[
        'Click',
    ],
    entry_points={
        'console_scripts': [
            'educats = educats:cli',
        ],
    },
)