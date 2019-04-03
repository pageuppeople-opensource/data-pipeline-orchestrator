from dpo.commands.BaseCommand import BaseCommand


class InitialiseExecutionCommand(BaseCommand):
    def __init__(self, db_connection_string, logger=None):
        super().__init__(db_connection_string, logger)

    def execute(self):
        data_pipeline_execution = self.repository.initialise_execution()
        self.logger.debug('Initialiseed new data_pipeline_execution = ' + str(data_pipeline_execution))
        print(str(data_pipeline_execution.id))
