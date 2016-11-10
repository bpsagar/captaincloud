from setuptools import find_packages, setup

setup(
    name='captaincloud',
    version='1.0.0-alpha',
    description='',
    url='https://github.com/bpsagar/captaincloud',
    author='Sagar Chakravarthy',
    license='MIT',
    packages=find_packages(exclude=('tests',)),
    install_requires=[
        'six'
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest',
        'pytest-cov'
    ],
    zip_safe=False)
