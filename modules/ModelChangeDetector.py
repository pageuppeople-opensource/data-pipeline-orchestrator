import argparse
import logging

from modules import Shared
from modules.BaseObject import BaseObject
from modules.Shared import Constants
from modules.commands.CompareCommand import CompareCommand
from modules.commands.FinishCommand import FinishCommand
from modules.commands.StartCommand import StartCommand


class ModelChangeDetector(BaseObject):
    def __init__(self, logger=None):
        self.args = self.__get_arguments()
        Shared.configure_root_logger(self.args.log_level)

        super().__init__(logger)

        self.logger.debug(self.args)
        self.logger.debug(f'args.log_level = {self.args.log_level} = {logging.getLevelName(self.args.log_level)}')

        self.args.func()

    def __process_start_command(self):
        StartCommand(self.args.db_connection_string).execute()

    def __process_compare_command(self):
        CompareCommand(self.args.db_connection_string, self.args.execution_id, self.args.model_type,
                       self.args.base_path, self.args.model_patterns).execute()

    def __process_finish_command(self):
        FinishCommand(self.args.db_connection_string, self.args.execution_id).execute()

    def __get_arguments(self):
        parser = argparse.ArgumentParser(description=Constants.APP_NAME,
                                         usage='mcd [options] <db-connection-string> <command> [command-parameters]\n\n'
                                               'To see help text, you can run\n'
                                               '  mcd --help\n'
                                               '  mcd <db-connection-string> <command> --help\n\n',
                                         parents=[Shared.get_default_arguments()])

        parser.add_argument('db_connection_string',
                            metavar='db-connection-string',
                            help='provide in PostgreSQL & Psycopg format, '
                                 'postgresql+psycopg2://username:password@host:port/dbname')

        subparsers = parser.add_subparsers(title='commands', metavar='', dest='command')

        start_command_parser = subparsers.add_parser('start', help='starts a new data pipeline execution')
        start_command_parser.set_defaults(func=self.__process_start_command)

        compare_command_parser = subparsers.add_parser('compare', help='compares given models with those of the last '
                                                                       'successfully processed data pipeline '
                                                                       'execution. also persists given models against '
                                                                       'the given data pipeline execution.')
        compare_command_parser.set_defaults(func=self.__process_compare_command)
        compare_command_parser.add_argument('execution_id',
                                            metavar='execution-id',
                                            help='data pipeline execution id as received using \'start\' command')
        compare_command_parser.add_argument('model_type',
                                            metavar='model-type',
                                            help='a string name for the type of models to compare. used to group '
                                                 'models between various calls to this command for same data pipeline '
                                                 'execution. e.g. load, transform')
        compare_command_parser.add_argument('base_path',
                                            metavar='base-path',
                                            help='absolute or relative path to the base directory of all models')
        compare_command_parser.add_argument('model_patterns',
                                            metavar='model-patterns',
                                            nargs='+',
                                            help='one or more unix-style search patterns for model files. e.g.: '
                                                 '*.txt, **/*.json, ./path/to/some_models/**/*.csv, '
                                                 'path/to/some/more/related/models/**/*.sql')

        finish_command_parser = subparsers.add_parser('finish', help='finishes the given data pipeline execution.')
        finish_command_parser.set_defaults(func=self.__process_finish_command)
        finish_command_parser.add_argument('execution_id',
                                           metavar='execution-id',
                                           help='data pipeline execution id as received using \'start\' command')

        args = parser.parse_args()

        return args
