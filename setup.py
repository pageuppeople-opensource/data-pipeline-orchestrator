from setuptools import setup, find_packages

setup(name='dpo',
      version='0.1.5',
      packages=find_packages(),
      install_requires=[
          'psycopg2-binary==2.8.2',
          'SQLAlchemy==1.3.3',
          'alembic==1.0.9',
          'sqlalchemy-redshift==0.7.3',
      ],
      package_data={
          '': ['alembic.ini', 'alembic/*.py', 'alembic/**/*.py'],
      },
      )
