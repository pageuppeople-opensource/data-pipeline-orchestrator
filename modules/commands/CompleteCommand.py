import hashlib
from pathlib import Path
from modules.commands.BaseCommand import BaseCommand


class CompleteCommand(BaseCommand):
    def __init__(self, db_connection_string, execution_id, logger=None):
        super().__init__(db_connection_string, logger)
        self._execution_id = execution_id

    def execute(self):
        data_pipeline_execution = self.repository.complete_execution(self._execution_id)
        self.logger.debug('Completed data_pipeline_execution = ' + str(data_pipeline_execution))
