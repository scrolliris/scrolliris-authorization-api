import os

from setuptools import setup, find_packages

# pylint: disable=invalid-name
here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, *('doc', 'DESCRIPTION.rst'))) as f:
    DESCRIPTION = f.read()
with open(os.path.join(here, 'CHANGELOG')) as f:
    CHANGELOG = f.read()

requires = [
    'colorlog',
    'Paste',
    'PasteScript',
    'python-dotenv',
    'pyramid',
    'pyramid_assetviews',
    'pyramid_services',
]

development_requires = [
    'flake8',
    'flake8_docstrings',
    'pylint',
    'waitress',
]

testing_requires = [
    'pytest',
    'pytest-cov',
    'pytest-mock',
    'WebTest',
]

production_requires = [
    'CherryPy',
    'honcho',
]

setup(
    name='bern',
    version='0.1',
    description='bern',
    long_description=DESCRIPTION + '\n\n' + CHANGELOG,
    classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='',
    author_email='',
    url='',
    keywords='web wsgi pylons pyramid',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'development': development_requires,
        'testing': testing_requires,
        'production': production_requires,
    },
    install_requires=requires,
    entry_points="""\
    [paste.app_factory]
    main = bern:main
    [console_scripts]
    bern_pserve = bern.scripts.pserve:main
    bern_pstart = bern.scripts.pstart:main
    bern_manage = bern.scripts.manage:main
    """,
)
