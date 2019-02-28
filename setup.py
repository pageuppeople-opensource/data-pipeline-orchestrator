from setuptools import setup, find_packages

setup(name='mcd',
      version='0.0.2',
      packages=find_packages(),
      install_requires=[
          'psycopg2-binary==2.7.7',
          'SQLAlchemy==1.2.17'
      ]
      )
