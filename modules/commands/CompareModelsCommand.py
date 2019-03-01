from modules.commands.BaseCommand import BaseCommand
from modules.Shared import Constants


class CompareModelsCommand(BaseCommand):
    def __init__(self, db_connection_string, previous_execution_id, current_execution_id, model_type, logger=None):
        super().__init__(db_connection_string, logger)
        self._previous_execution_id = previous_execution_id
        self._current_execution_id = current_execution_id
        self._model_type = model_type
        self._changed_models_separator = ' '

    def execute(self):
        old_models = [] if self._previous_execution_id == Constants.NO_LAST_SUCCESSFUL_EXECUTION \
            else self.repository.get_execution_models(self._previous_execution_id, self._model_type)
        new_models = self.repository.get_execution_models(self._current_execution_id, self._model_type)

        # kept for later validation
        # if len(old_models) == 0:
        #     self.logger.debug(f'Changed models: ALL')
        #     print('*')
        #     return

        old_model_checksums = {}
        for model in old_models:
            old_model_checksums[model.name] = model.checksum

        new_model_checksums = {}
        for model in new_models:
            new_model_checksums[model.name] = model.checksum

        changed_models = []
        for model, new_checksum in new_model_checksums.items():
            if model not in old_model_checksums or old_model_checksums[model] != new_checksum:
                changed_models.append(model)

        print(self._changed_models_separator.join(changed_models))
        self.logger.debug(f'Changed models: \'${str(changed_models)}\'')
