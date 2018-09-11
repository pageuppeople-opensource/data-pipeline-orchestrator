from modules.commands import Commands
from modules.commands.BaseCommand import BaseCommand


class StartCommand(BaseCommand):
    def __init__(self, db_connection_string, logger=None):
        super().__init__(db_connection_string, logger)

    @staticmethod
    def can_execute_command(command):
        return command == Commands.START

    def execute(self):
        data_pipeline_execution = self.repository.start_new()
        execution_result = str(data_pipeline_execution.uuid)
        return execution_result
