from setuptools import find_packages, setup

setup(
    name='captaincloud',
    version='1.0.0-alpha',
    description='',
    url='https://github.com/bpsagar/captaincloud',
    author='Sagar Chakravarthy',
    license='MIT',
    packages=find_packages(exclude=('tests',)),
    entry_points={'console_scripts': [
        'cc-task-executor = captaincloud.processes.task_executor.main:main',
    ]},
    install_requires=[
        'six',
        'bottle',
        'requests',
    ],
    setup_requires=[
        'pytest-runner'
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
        'WebTest',
    ],
    zip_safe=False)
