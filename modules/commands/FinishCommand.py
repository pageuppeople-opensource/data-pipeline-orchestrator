from modules.commands.BaseCommand import BaseCommand


class FinishCommand(BaseCommand):
    def __init__(self, db_connection_string, execution_id, logger=None):
        super().__init__(db_connection_string, logger)
        self._executionId = execution_id

    def execute(self):
        data_pipeline_execution = self.repository.finish_existing(self._executionId)
        self.logger.debug('Finised data_pipeline_execution = ' + str(data_pipeline_execution))
