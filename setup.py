from setuptools import setup, find_packages
import codecs
import os.path


def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()


def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")


setup(
    name='apache_logs_parser',
    version=get_version("apache_logs_parser/__init__.py"),
    description='Example for log parsing tool for Python classes',
    author='Martin DENIZET',
    author_email='martin.denizet@gmail.com',
    url='https://github.com/martin-denizet/',
    packages=find_packages(exclude=['tests']),
    license_files=('LICENSE',),
    license=read("LICENSE"),
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    python_requires='>=3.7',
    install_requires=[],
    setup_requires=[],
    tests_require=[],
    entry_points={
        'console_scripts':
            ['apache_logs_parser=apache_logs_parser.__main__:main']
    },
    test_suite="tests",
)
