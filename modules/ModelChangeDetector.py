import argparse
import logging
from modules import Shared
from modules.Shared import Constants
from modules.BaseObject import BaseObject
from modules.commands.StartCommand import StartCommand
from modules.commands.FinishCommand import FinishCommand


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

    def __process_finish_command(self):
        FinishCommand(self.args.db_connection_string, self.args.execution_id).execute()

    def __get_arguments(self):
        parser = argparse.ArgumentParser(description=Constants.APP_NAME,
                                         usage='mcd [options] <COMMAND> [COMMAND-parameters]\n\n'
                                               'To see help text, you can run\n'
                                               '  mcd --help\n'
                                               '  mcd <command> --help',
                                         parents=[Shared.get_default_arguments()])

        subparsers = parser.add_subparsers(title='commands', metavar='', dest='command')

        start_command_parser = subparsers.add_parser('start', help='help text for \'start\' command')
        start_command_parser.set_defaults(func=self.__process_start_command)
        self.__get_default_command_arguments(start_command_parser)

        finish_command_parser = subparsers.add_parser('finish', help='help text for \'finish\' command')
        finish_command_parser.set_defaults(func=self.__process_finish_command)
        self.__get_default_command_arguments(finish_command_parser)
        finish_command_parser.add_argument('execution_id',
                                           metavar='execution_id',
                                           help='data pipeline execution id as received using \'start\' command')

        args = parser.parse_args()

        return args

    @staticmethod
    def __get_default_command_arguments(command_parser):
        command_parser.add_argument('db_connection_string',
                                    metavar='db-connection-string',
                                    help='provide in PostgreSQL & Psycopg format, '
                                         'postgresql+psycopg2://username:password@host:port/dbname')

