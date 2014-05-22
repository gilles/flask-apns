"""
Try to make a package
"""

from setuptools import setup


def desc():
    with open('README.rst') as fp:
        info = fp.read()
    return info


setup(
    name='Flask-APNS',
    version='0.1.0',
    url='https://github.com/gilles/flask-apns/',
    license='MIT',
    author='Gilles Devaux',
    author_email='gilles.devaux@gmail.com',
    description='Send APNS messages from flask',
    long_description=desc(),
    packages=['flask_apns'],
    platforms='any',
    install_requires=[
        'Flask>=0.7',
        'apns-client>=0.1'
    ],
    tests_require=[
        'nose==1.3.1',
        'MiniMock==1.2.8'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    test_suite='nose.collector'
)
