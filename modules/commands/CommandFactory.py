import logging
from modules.commands.StartCommand import StartCommand
from modules import Shared

class CommandFactory(object):
    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        Shared.write_output(self.logger, Shared.args.verbose)
        self.commandTypes = [StartCommand]

    def create_command(self, command, db_connection_string):
        for commandType in self.commandTypes:
            if commandType.can_execute_command(command):
                self.logger.debug(f'Found command type {commandType} for command {command}.')
                return commandType(db_connection_string)

            raise RuntimeError(f'There are no command types that can handle the {command} command')
