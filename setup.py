import pathlib
from setuptools import setup

exec(open('openserver/version.py').read())

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(name='openserver',
      version=__version__,
      description='Petroleum Experts OpenServer calculations',
      long_description=README,
      long_description_content_type="text/markdown",
      author='Equinor ASA',
      author_email='thokn@equinor.com',
      license='GNU GPL',
      url='https://github.com/equinor/openserver',
      classifiers=["Programming Language :: Python :: 3"],
      packages=['openserver'],
      install_requires=['pywin32>=227']
)