from mcd.commands.BaseCommand import BaseCommand
from mcd.Shared import Constants


class CompareModelsCommand(BaseCommand):
    def __init__(self, db_connection_string, previous_execution_id, current_execution_id, model_type, logger=None):
        super().__init__(db_connection_string, logger)
        self._previous_execution_id = previous_execution_id
        self._current_execution_id = current_execution_id
        self._model_type = model_type
        self._changed_models_separator = ' '

    def execute(self):
        previous_models_list = [] if self._previous_execution_id == Constants.NO_LAST_SUCCESSFUL_EXECUTION \
            else self.repository.get_execution_models(self._previous_execution_id, self._model_type)
        current_models_list = self.repository.get_execution_models(self._current_execution_id, self._model_type)

        previous_model_checksums = {}
        for model in previous_models_list:
            previous_model_checksums[model.name] = model.checksum

        current_model_checksums = {}
        for model in current_models_list:
            current_model_checksums[model.name] = model.checksum

        changed_models_list = []
        for model, new_checksum in current_model_checksums.items():
            if model not in previous_model_checksums or previous_model_checksums[model] != new_checksum:
                changed_models_list.append(model)

        self.output(changed_models_list)

    def output(self, changed_models_list):
        print(self._changed_models_separator.join(changed_models_list))
