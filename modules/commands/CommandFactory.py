from modules.commands.StartCommand import StartCommand
from modules.commands.FinishCommand import FinishCommand
from modules.BaseObject import BaseObject


class CommandFactory(BaseObject):
    def __init__(self, logger=None):
        super().__init__(logger)
        self.commandTypes = [StartCommand, FinishCommand]

    def create_command(self, command, db_connection_string):
        for commandType in self.commandTypes:
            if commandType.can_execute_command(command):
                self.logger.debug(f'Found command type {commandType} for command {command}.')
                return commandType(db_connection_string)

        raise RuntimeError(f'There are no command types that can handle the {command} command')
