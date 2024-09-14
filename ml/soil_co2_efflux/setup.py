from setuptools import setup, find_packages

setup(
    name='soil_co2_efflux',
    version='0.1',
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=['pandas'],
    author='Ilias Karatsin',
    author_email='dev@dev.com',
    description='The project for soil CO2 Efflux ml features collection.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)