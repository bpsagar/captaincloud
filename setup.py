from setuptools import setup

setup(
    name='captaincloud',
    version='1.0.0-alpha',
    description='',
    url='https://github.com/bpsagar/captaincloud',
    author='Sagar Chakravarthy',
    license='MIT',
    packages=['captaincloud'],
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
