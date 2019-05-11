import argparse
import logging

from dpo import Shared
from dpo.BaseObject import BaseObject
from dpo.Shared import Constants
from dpo.commands import InitialiseExecutionCommand
from dpo.commands import GetLastSuccessfulExecutionCommand
from dpo.commands import GetExecutionCompletionTimestampCommand
from dpo.commands import InitialiseStepCommand
from dpo.commands import CompareStepModelsCommand
from dpo.commands import CompleteStepCommand
from dpo.commands import CompleteExecutionCommand


class DataPipelineOrchestrator(BaseObject):
    def __init__(self, logger=None):
        self.args = self.__get_arguments()
        Shared.configure_root_logger(self.args.log_level)

        super().__init__(logger)

        self.logger.debug(self.args)
        self.logger.debug(f'args.log_level = {self.args.log_level} = {logging.getLevelName(self.args.log_level)}')

        self.args.func()

    def __process_init_execution_command(self):
        InitialiseExecutionCommand(self.args.db_connection_string).execute()

    def __process_get_last_successful_execution_command(self):
        GetLastSuccessfulExecutionCommand(self.args.db_connection_string).execute()

    def __process_get_execution_completion_timestamp_command(self):
        GetExecutionCompletionTimestampCommand(self.args.db_connection_string, self.args.execution_id).execute()

    def __process_init_step_command(self):
        InitialiseStepCommand(
            self.args.db_connection_string, self.args.execution_id, self.args.step_name.upper(),
            self.args.base_path, self.args.model_patterns
        ).execute()

    def __process_compare_step_models_command(self):
        CompareStepModelsCommand(
            self.args.db_connection_string, self.args.step_id, self.args.previous_execution_id
        ).execute()

    def __process_complete_step_command(self):
        CompleteStepCommand(self.args.db_connection_string, self.args.step_id).execute()

    def __process_complete_execution_command(self):
        CompleteExecutionCommand(self.args.db_connection_string, self.args.execution_id).execute()

    def __get_arguments(self):
        parser = argparse.ArgumentParser(
            description=Constants.APP_NAME,
            usage='dpo [options] <db-connection-string> <command> [command-args]\n\n'
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
            'init-execution', help='initialises a new execution')
        init_execution_command_parser.set_defaults(func=self.__process_init_execution_command)

        get_last_successful_execution_command_parser = subparsers.add_parser(
            'get-last-successful-execution',
            help='returns execution id of the last successful execution, if any. '
                 'if no such execution is found, then returns an empty string.')
        get_last_successful_execution_command_parser.set_defaults(
            func=self.__process_get_last_successful_execution_command)

        get_execution_completion_timestamp_command_parser = subparsers.add_parser(
            'get-execution-completion-timestamp',
            help='returns the completed-on timestamp (datetime with timezone) of a given execution-id. '
                 'raises error if given execution-id is invalid.')
        get_execution_completion_timestamp_command_parser.set_defaults(
            func=self.__process_get_execution_completion_timestamp_command)
        get_execution_completion_timestamp_command_parser.add_argument(
            'execution_id',
            metavar='execution-id',
            help='an existing execution id')

        init_step_command_parser = subparsers.add_parser(
            'init-step',
            help='Saves models of the given \'model-type\' within the given \'execution-id\' '
                 'by persisting hashed checksums of the given models.')
        init_step_command_parser.set_defaults(func=self.__process_init_step_command)
        init_step_command_parser.add_argument(
            'execution_id',
            metavar='execution-id',
            help='identifier of an existing execution, ideally as returned by the \'init\' command.')
        init_step_command_parser.add_argument(
            'step_name',
            metavar='step-name',
            help=f'name of step being processed, choose from {", ".join(Shared.STEP_NAMES)}.')
        init_step_command_parser.add_argument(
            'base_path',
            metavar='base-path',
            help='absolute or relative path to the base directory of all models'
                 'e.g.: ./load, /home/local/transform, C:/path/to/models')
        init_step_command_parser.add_argument(
            'model_patterns',
            metavar='model-patterns',
            nargs='+',
            help='one or more unix-style search patterns (relative to \'base-path\') for model files. '
                 'models within a model-type must be named uniquely regardless of their file extension.'
                 'e.g.: *.txt, **/*.json, ./path/to/some_models/**/*.csv, path/to/some/more/related/models/**/*.sql')

        compare_step_models_command_parser = subparsers.add_parser(
            'compare-step-models',
            help='Compares the hashed checksums of models between two execution steps. '
                 'Returns comma-separated string of changed model names.')
        compare_step_models_command_parser.set_defaults(func=self.__process_compare_step_models_command)
        compare_step_models_command_parser.add_argument(
            'step_id',
            metavar='step-id',
            help='identifier of an existing execution\'s step, as returned by the \'init-step\' command.')
        compare_step_models_command_parser.add_argument(
            'previous_execution_id',
            metavar='previous-execution-id',
            help='identifier of an existing execution used to find a corresponding step to compare, '
                 'ideally as returned by the \'get-last-successful-execution\' command.')

        complete_step_command_parser = subparsers.add_parser(
            'complete-step', help='completes the given execution\'s step.')
        complete_step_command_parser.set_defaults(func=self.__process_complete_step_command)
        complete_step_command_parser.add_argument(
            'step_id',
            metavar='step-id',
            help='an execution\'s step id as received using \'init-step\' command')

        complete_execution_command_parser = subparsers.add_parser(
            'complete-execution', help='completes the given execution.')
        complete_execution_command_parser.set_defaults(func=self.__process_complete_execution_command)
        complete_execution_command_parser.add_argument(
            'execution_id',
            metavar='execution-id',
            help='an execution id as received using \'init-execution\' command')

        args = parser.parse_args()

        return args
