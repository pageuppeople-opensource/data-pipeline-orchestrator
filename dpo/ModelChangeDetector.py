import argparse
import logging

from dpo import Shared
from dpo.BaseObject import BaseObject
from dpo.Shared import Constants
from dpo.commands.InitialiseExecutionCommand import InitialiseExecutionCommand
from dpo.commands.GetLastSuccessfulExecutionCommand import GetLastSuccessfulExecutionCommand
from dpo.commands.GetExecutionLastUpdateTimestampCommand import GetExecutionLastUpdateTimestampCommand
from dpo.commands.PersistModelsCommand import PersistModelsCommand
from dpo.commands.CompareModelsCommand import CompareModelsCommand
from dpo.commands.CompleteExecutionCommand import CompleteExecutionCommand


class ModelChangeDetector(BaseObject):
    def __init__(self, logger=None):
        self.args = self.__get_arguments()
        Shared.configure_root_logger(self.args.log_level)

        super().__init__(logger)

        self.logger.debug(self.args)
        self.logger.debug(f'args.log_level = {self.args.log_level} = {logging.getLevelName(self.args.log_level)}')

        self.args.func()

    def __process_init_execution_command(self):
        InitialiseExecutionCommand(self.args.db_connection_string).execute()

    def __process_get_execution_last_updated_timestamp_command(self):
        GetExecutionLastUpdateTimestampCommand(self.args.db_connection_string, self.args.execution_id).execute()

    def __process_get_last_successful_execution_command(self):
        GetLastSuccessfulExecutionCommand(self.args.db_connection_string).execute()

    def __process_save_models_command(self):
        PersistModelsCommand(
            self.args.db_connection_string, self.args.execution_id, self.args.model_type.upper(),
            self.args.base_path, self.args.model_patterns
        ).execute()

    def __process_compare_models_command(self):
        CompareModelsCommand(
            self.args.db_connection_string, self.args.previous_execution_id, self.args.current_execution_id,
            self.args.model_type.upper()
        ).execute()

    def __process_complete_execution_command(self):
        CompleteExecutionCommand(self.args.db_connection_string, self.args.execution_id).execute()

    def __get_arguments(self):
        parser = argparse.ArgumentParser(
            description=Constants.APP_NAME,
            usage='dpo [options] <db-connection-string> <command> [command-parameters]\n\n'
                  'To see help text, you can run\n'
                  '  dpo --help\n'
                  '  dpo <db-connection-string> <command> --help\n\n',
            parents=[Shared.get_default_arguments()])

        parser.add_argument(
            'db_connection_string',
            metavar='db-connection-string',
            help='provide in PostgreSQL & Psycopg format, postgresql+psycopg2://username:password@host:port/dbname')

        subparsers = parser.add_subparsers(title='commands', metavar='', dest='command')

        init_execution_command_parser = subparsers.add_parser(
            'init-execution', help='initialises a new data pipeline execution')
        init_execution_command_parser.set_defaults(func=self.__process_init_execution_command)

        get_last_successful_execution_command_parser = subparsers.add_parser(
            'get-last-successful-execution',
            help='returns execution id of the last successful execution, if any. '
                 'if no such execution is found, then returns an empty string.')
        get_last_successful_execution_command_parser.set_defaults(
            func=self.__process_get_last_successful_execution_command)

        get_execution_last_updated_timestamp_command_parser = subparsers.add_parser(
            'get-execution-last-updated-timestamp',
            help='returns the last-updated-on timestamp (datetime with timezone) of a given execution-id. '
                 'raises error if given execution-id is invalid.')
        get_execution_last_updated_timestamp_command_parser.set_defaults(
            func=self.__process_get_execution_last_updated_timestamp_command)
        get_execution_last_updated_timestamp_command_parser.add_argument(
            'execution_id',
            metavar='execution-id',
            help='an existing data pipeline execution id')

        persist_models_command_parser = subparsers.add_parser(
            'persist-models',
            help='Saves models of the given \'model-type\' within the given \'execution-id\' '
                 'by persisting hashed checksums of the given models.')
        persist_models_command_parser.set_defaults(func=self.__process_save_models_command)
        persist_models_command_parser.add_argument(
            'execution_id',
            metavar='execution-id',
            help='identifier of an existing data pipeline execution, ideally as returned by the \'init\' command.')
        persist_models_command_parser.add_argument(
            'model_type',
            metavar='model-type',
            help=f'type of models being processed, choose from {", ".join(Shared.MODEL_TYPES)}.')
        persist_models_command_parser.add_argument(
            'base_path',
            metavar='base-path',
            help='absolute or relative path to the base directory of all models'
                 'e.g.: ./load, /home/local/transform, C:/path/to/models')
        persist_models_command_parser.add_argument(
            'model_patterns',
            metavar='model-patterns',
            nargs='+',
            help='one or more unix-style search patterns (relative to \'base-path\') for model files. '
                 'models within a model-type must be named uniquely regardless of their file extension.'
                 'e.g.: *.txt, **/*.json, ./path/to/some_models/**/*.csv, path/to/some/more/related/models/**/*.sql')

        compare_models_command_parser = subparsers.add_parser(
            'compare-models',
            help='Compares the hashed checksums of models between two executions. '
                 'Returns comma-separated string of changed model names.')
        compare_models_command_parser.set_defaults(func=self.__process_compare_models_command)
        compare_models_command_parser.add_argument(
            'previous_execution_id',
            metavar='previous-execution-id',
            help='identifier of an existing data pipeline execution, '
                 'ideally as returned by the \'get-last-successful-execution\' command.')
        compare_models_command_parser.add_argument(
            'current_execution_id',
            metavar='current-execution-id',
            help='identifier of an existing data pipeline execution, ideally as returned by the \'init\' command.')
        compare_models_command_parser.add_argument(
            'model_type',
            metavar='model-type',
            help=f'type of models being processed, choose from {", ".join(Shared.MODEL_TYPES)}.')

        complete_execution_command_parser = subparsers.add_parser(
            'complete-execution', help='completes the given data pipeline execution.')
        complete_execution_command_parser.set_defaults(func=self.__process_complete_execution_command)
        complete_execution_command_parser.add_argument(
            'execution_id',
            metavar='execution-id',
            help='data pipeline execution id as received using \'init\' command')

        args = parser.parse_args()

        return args
