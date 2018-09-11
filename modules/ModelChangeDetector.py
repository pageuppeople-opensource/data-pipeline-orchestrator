import argparse
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modules import Constants
from modules import Shared
from modules.DataPipelineExecutionRepository import DataPipelineExecutionRepository


class ModelChangeDetector:

    # may need to become something like logging.INFO etc. which are integers with corresponding strings.. or may not :S
    _executionModes = ['NEW']

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def main(self):
        Shared.args = self.get_arguments()
        Shared.configure_logging(self.logger, Shared.args.log_level)

        execution_result = None

        # TODO add logic to
        # - figure out how to separate args.execution_mode code/logic..
        # a class per execution-mode? IExecutionMode.Execute(...)? Factory? DI?

        if Shared.args.execution_mode == 'NEW':
            db_engine = create_engine(Shared.args.db_connection_string, echo=Shared.args.verbose)
            session_maker = sessionmaker(bind=db_engine)
            repository = DataPipelineExecutionRepository(session_maker)
            repository.create_schema(engine=db_engine)
            data_pipeline_execution = repository.start_new()
            execution_result = str(data_pipeline_execution.uuid)
            if Shared.args.verbose:
                print(data_pipeline_execution)

        if Shared.args.verbose:
            print(Shared.args)
            print(f'args.log_level = {Shared.args.log_level} = {logging.getLevelName(Shared.args.log_level)}')
            print(self.logger)
            print(f'execution_result = {execution_result}')

        return execution_result

    def get_arguments(self):
        parser = argparse.ArgumentParser(description=Constants.APP_NAME,
                                         parents=[Shared.get_default_arguments(
                                             Constants.APP_NAME,
                                             Shared.appVersion)])

        parser.add_argument('execution_mode',
                            action='store',
                            # metavar='execution-mode',
                            choices=ModelChangeDetector._executionModes,
                            help=f'execution mode; choose from {", ".join(self._executionModes)}')

        parser.add_argument('db_connection_string',
                            metavar='db-connection-string',
                            help='database connection string, e.g. '
                                 'postgresql+psycopg2://username:password@host:port/dbname')

        args = parser.parse_args()
        return args
