import argparse
import logging
from modules import Shared
from modules.Shared import Constants
from modules.commands import Commands
from modules.commands.CommandFactory import CommandFactory


class ModelChangeDetector:

    commandNames = [Commands.get_name(Commands.START)]

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

        self.args = ModelChangeDetector.get_arguments()
        Shared.args = self.args
        Shared.write_output(self.args, self.args.verbose)
        Shared.write_output(f'args.log_level = {self.args.log_level} = {logging.getLevelName(self.args.log_level)}',
                            self.args.verbose)

        Shared.configure_logging(self.logger, self.args.log_level)
        Shared.write_output(self.logger, self.args.verbose)

        self.command_factory = CommandFactory()

    def main(self):

        command_executor = self.command_factory.create_command(self.args.command, self.args.db_connection_string)
        execution_result = command_executor.execute()
        Shared.write_output(f'execution_result = {execution_result}', self.args.verbose)

        return execution_result

    @staticmethod
    def get_arguments():
        parser = argparse.ArgumentParser(description=Constants.APP_NAME,
                                         parents=[Shared.get_default_arguments(
                                             Constants.APP_NAME,
                                             Shared.appVersion)])

        parser.add_argument('command',
                            type=ModelChangeDetector.get_command_value_from_name,
                            help=f'choose from {", ".join(ModelChangeDetector.commandNames)}, more coming soon..')

        parser.add_argument('db_connection_string',
                            metavar='db-connection-string',
                            help='provide in PostgreSQL & Psycopg format, '
                                 'postgresql+psycopg2://username:password@host:port/dbname')

        args = parser.parse_args()
        return args

    @staticmethod
    def get_command_value_from_name(command_name):
        if command_name not in ModelChangeDetector.commandNames:
            message = f'invalid choice: {command_name} (choose from {", ".join(ModelChangeDetector.commandNames)})'
            raise argparse.ArgumentTypeError(message)

        command_value = getattr(Commands, command_name, logging.INFO)

        return command_value
