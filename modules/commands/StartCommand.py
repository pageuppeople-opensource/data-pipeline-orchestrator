from modules.commands.BaseCommand import BaseCommand


class StartCommand(BaseCommand):
    def __init__(self, db_connection_string, logger=None):
        super().__init__(db_connection_string, logger)

    def execute(self):
        data_pipeline_execution = self.repository.start_execution()
        self.logger.debug('Started new data_pipeline_execution = ' + str(data_pipeline_execution))
        print(str(data_pipeline_execution.id))
