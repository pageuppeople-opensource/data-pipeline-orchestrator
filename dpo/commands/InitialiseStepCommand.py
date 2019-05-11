import hashlib
from pathlib import Path
from dpo.commands.BaseCommand import BaseCommand


class InitialiseStepCommand(BaseCommand):
    def __init__(self, db_connection_string, execution_id, step_name, base_path, model_patterns, logger=None):
        super().__init__(db_connection_string, logger)
        self._execution_id = execution_id
        self._step_name = step_name
        self._base_path = base_path
        self._model_patterns = model_patterns

    def execute(self):
        model_folder = Path(self._base_path)
        if not model_folder.is_dir():
            raise NotADirectoryError(self._base_path)

        execution_step = self.repository.initialise_execution_step(self._execution_id, self._step_name)
        self.logger.debug('Initialised new execution_step = ' + str(execution_step))

        current_model_checksums = {}
        for model_pattern in self._model_patterns:
            for model_file in model_folder.glob(model_pattern):
                if model_file.is_file():
                    current_model_checksums[model_file.stem] = self.__get_file_checksum(model_file)

        execution_step = self.repository.save_execution_step_models(
            execution_step.execution_step_id, current_model_checksums)

        self.logger.debug('Saved {number_of_models} models for execution_step: {step_details}'
                          .format(number_of_models=len(current_model_checksums.keys()),
                                  step_details=str(execution_step)))
        self.output(execution_step.execution_step_id)

    def output(self, execution_step_id):
        print(str(execution_step_id))

    def __get_file_checksum(self, file: Path):
        data = file.read_bytes()
        hash_function = hashlib.sha256()
        hash_function.update(data)
        checksum = hash_function.hexdigest()
        self.logger.debug(f'filename={file.name}, filepath=\'{file.absolute().as_posix()}\'')
        self.logger.debug(f'hash_function={hash_function.name}, checksum_len={len(checksum)}, checksum={checksum}')
        return checksum
