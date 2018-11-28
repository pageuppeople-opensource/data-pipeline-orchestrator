import argparse
import logging
from modules import Shared
from modules.Shared import Constants
from modules.commands import Commands
from modules.commands.CommandFactory import CommandFactory
from modules.BaseObject import BaseObject


class ModelChangeDetector(BaseObject):

    _commandNames = [Commands.get_name(Commands.START)]

    def __init__(self, logger=None):
        self.args = self.get_arguments()
        Shared.configure_root_logger(self.args.log_level)

        super().__init__(logger)

        self.logger.debug(self.args)
        self.logger.debug(f'args.log_level = {self.args.log_level} = {logging.getLevelName(self.args.log_level)}')

        self.command_factory = CommandFactory()

    def main(self):
        command_executor = self.command_factory.create_command(self.args.command.upper(), self.args.db_connection_string)
        # command_executor.execute()
        # command_executor.execute(self.args.execution_id)


    def get_arguments(self):
        parser = argparse.ArgumentParser(description=Constants.APP_NAME,
                                         usage='mcd [options] <COMMAND> [COMMAND-parameters]\n\n'
                                         'To see help text, you can run\n'
                                         '  mcd --help\n'
                                         '  mcd <command> --help',
                                         parents=[Shared.get_default_arguments()])
        
        subparsers = parser.add_subparsers(title='commands', metavar='', dest='command')

        start_command_parser = subparsers.add_parser('start', help='help text for \'start\' command')
        # start_command_parser.set_defaults(func=start_new_execution)
        start_command_parser.add_argument('db_connection_string',
                                          metavar='db-connection-string',
                                          help='provide in PostgreSQL & Psycopg format, '
                                               'postgresql+psycopg2://username:password@host:port/dbname')

        finish_command_parser = subparsers.add_parser('finish', help='help text for \'finish\' command')
        # start_command_parser.set_defaults(func=finish_execution)
        finish_command_parser.add_argument('db_connection_string',
                                           metavar='db-connection-string',
                                           help='provide in PostgreSQL & Psycopg format, '
                                                'postgresql+psycopg2://username:password@host:port/dbname')
        finish_command_parser.add_argument('execution_id',
                                           metavar='execution_id',
                                           help='data pipeline execution id as received using \'start\' command')

        args = parser.parse_args()

        return args

    def get_command_value_from_name(self, command_name):
        if command_name not in self._commandNames:
            message = f'invalid choice: {command_name} (choose from {", ".join(self._commandNames)})'
            raise argparse.ArgumentTypeError(message)

        command_value = getattr(Commands, command_name, Commands.UNKNOWN)

        return command_value
