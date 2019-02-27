from modules.commands.BaseCommand import BaseCommand


class GetExecutionsLastUpdateTimestampCommand(BaseCommand):
    def __init__(self, db_connection_string, execution_id, logger=None):
        super().__init__(db_connection_string, logger)
        self._execution_id = execution_id

    def execute(self):
        data_pipeline_execution = self.repository.get_execution(self._execution_id)
        self.logger.debug(f'Found requested data_pipeline_execution to be {str(data_pipeline_execution)}')
        if data_pipeline_execution is None:
            raise ValueError(self._execution_id)
        print(str(data_pipeline_execution.last_updated_on))
