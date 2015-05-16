# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    import distribute_setup
    distribute_setup.use_setuptools()
    from setuptools import setup

setup(
    name='packed',
    version='0.1.0',
    url='https://github.com/michaeljones/packed',
    download_url='https://github.com/michaeljones/packed',
    license='BSD',
    author='Michael Jones',
    author_email='m.pricejones@gmail.com',
    description='JSX style syntax for Python',
    zip_safe=False,
    classifiers=[
        'Development Status :: 1 - Beta',
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Pre-processors',
    ],
    platforms='any',
    py_modules=['packed'],
    include_package_data=True,
    install_requires=open('requirements.txt', 'r').read(),
)
