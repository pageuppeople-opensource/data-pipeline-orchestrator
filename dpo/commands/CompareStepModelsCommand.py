from dpo.commands.BaseCommand import BaseCommand
from dpo.Shared import Constants


class CompareStepModelsCommand(BaseCommand):
    def __init__(self, db_connection_string, step_id, previous_execution_id, logger=None):
        super().__init__(db_connection_string, logger)
        self._step_id = step_id
        self._previous_execution_id = previous_execution_id
        self._changed_models_separator = ' '

    def execute(self):
        previous_models_list = []

        if self._previous_execution_id != Constants.NO_LAST_SUCCESSFUL_EXECUTION:
            step = self.repository.get_execution_step(self._step_id)
            previous_execution_steps_list = self.repository.get_execution_steps(self._previous_execution_id)
            previous_step = [step_x for step_x in previous_execution_steps_list if step_x.step_name == step.step_name][0]
            previous_models_list = self.repository.get_execution_step_models(previous_step.execution_step_id)

        current_models_list = self.repository.get_execution_step_models(self._step_id)

        previous_model_checksums = {}
        for model in previous_models_list:
            previous_model_checksums[model.model_name] = model.checksum
        self.logger.debug(f'previous_model_checksums = {previous_model_checksums}')

        current_model_checksums = {}
        for model in current_models_list:
            current_model_checksums[model.model_name] = model.checksum
        self.logger.debug(f'current_model_checksums = {current_model_checksums}')

        changed_models_list = []
        for model, new_checksum in current_model_checksums.items():
            if model not in previous_model_checksums or previous_model_checksums[model] != new_checksum:
                changed_models_list.append(model)
        self.output(changed_models_list)

    def output(self, changed_models_list):
        print(self._changed_models_separator.join(changed_models_list))
