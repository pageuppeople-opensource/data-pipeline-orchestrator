from modules.commands import Commands
from modules.commands.BaseCommand import BaseCommand


class FinishCommand(BaseCommand):
    def __init__(self, db_connection_string, logger=None):
        super().__init__(db_connection_string, logger)

    @staticmethod
    def can_execute_command(command):
        return command == Commands.FINISH

    def execute(self, execution_id):
        data_pipeline_execution = self.repository.finish_existing(execution_id)
        self.logger.debug('Finised data_pipeline_execution = ' + str(data_pipeline_execution))
