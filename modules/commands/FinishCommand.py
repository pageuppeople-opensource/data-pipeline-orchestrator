import hashlib
from pathlib import Path
from modules.commands.BaseCommand import BaseCommand


class FinishCommand(BaseCommand):
    def __init__(self, db_connection_string, execution_id, logger=None):
        super().__init__(db_connection_string, logger)
        self._execution_id = execution_id

    def execute(self):
        data_pipeline_execution = self.repository.finish_execution(self._execution_id)
        self.logger.debug('Finished data_pipeline_execution = ' + str(data_pipeline_execution))
