import argparse
import logging
from modules import Shared
from modules.Shared import Constants
from modules.commands import Commands
from modules.commands.CommandFactory import CommandFactory
import pip

class ModelChangeDetector:

    commandNames = [Commands.get_name(Commands.START)]

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def main(self):
        Shared.args = ModelChangeDetector.get_arguments()
        self.command_factory = CommandFactory()
        Shared.configure_logging(self.logger, Shared.args.log_level)

        command_executor = self.command_factory.create_command(Shared.args.command, Shared.args.db_connection_string)
        execution_result = command_executor.execute()

        Shared.write_output(Shared.args, Shared.args.verbose)
        Shared.write_output(f'args.log_level = {Shared.args.log_level} = {logging.getLevelName(Shared.args.log_level)}',
                        Shared.args.verbose)
        Shared.write_output(self.logger, Shared.args.verbose)
        Shared.write_output(f'execution_result = {execution_result}', Shared.args.verbose)

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
