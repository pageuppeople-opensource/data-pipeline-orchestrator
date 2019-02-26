from modules.commands.BaseCommand import BaseCommand


class GetLastSuccessfulExecutionCommand(BaseCommand):
    def __init__(self, db_connection_string, logger=None):
        super().__init__(db_connection_string, logger)

    def execute(self):
        data_pipeline_execution = self.repository.get_last_successful_execution()
        self.logger.debug('Found last successful data_pipeline_execution to be ' + str(data_pipeline_execution))
        print(str(data_pipeline_execution.id) if data_pipeline_execution is not None else '')
