from setuptools import setup, find_packages

setup(name='dpo',
      version='0.1.1',
      packages=find_packages(),
      install_requires=[
          'psycopg2-binary==2.7.7',
          'SQLAlchemy==1.2.17',
          'alembic==1.0.8',
      ],
      package_data={
          '': ['alembic.ini', 'alembic/*.py', 'alembic/**/*.py'],
      },
      )
