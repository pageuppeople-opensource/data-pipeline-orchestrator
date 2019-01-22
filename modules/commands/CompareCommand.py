import hashlib
from pathlib import Path
from modules.commands.BaseCommand import BaseCommand


class CompareCommand(BaseCommand):
    def __init__(self, db_connection_string, execution_id, model_type, base_path, model_patterns, logger=None):
        super().__init__(db_connection_string, logger)
        self._execution_id = execution_id
        self._model_type = model_type
        self._base_path = base_path
        self._model_patterns = model_patterns
        self._changed_models_separator = ' '

    def execute(self):
        model_folder = Path(self._base_path)
        if not model_folder.is_dir():
            raise NotADirectoryError(self._base_path)

        current_model_checksums = {}
        for model_pattern in self._model_patterns:
            for model_file in model_folder.rglob(model_pattern):
                if model_file.is_file():
                    current_model_checksums[model_file.stem] = self.__get_file_checksum(model_file)

        data_pipeline_execution = self.repository.save_execution_progress(self._execution_id, self._model_type, current_model_checksums)
        self.logger.debug(f'Comparing data_pipeline_execution = ${str(data_pipeline_execution)}')

        previous_model_checksums = self.repository.get_last_successful_models(self._model_type)

        if len(previous_model_checksums) == 0:
            print('*')
            self.logger.debug(f'Changed models: ALL')
            return

        changed_models = []
        for model, current_checksum in current_model_checksums.items():
            if model not in previous_model_checksums or previous_model_checksums[model] != current_checksum:
                changed_models.append(model)

        print(self._changed_models_separator.join(changed_models))
        self.logger.debug(f'Changed models: \'${str(changed_models)}\'')

    def __get_file_checksum(self, file: Path):
        data = file.read_bytes()
        hash_function = hashlib.sha256()
        hash_function.update(data)
        checksum = hash_function.hexdigest()
        self.logger.debug(f'filename={file.name}, filepath=\'{file.absolute().as_posix()}\'')
        self.logger.debug(f'hash_function={hash_function.name}, checksum_len={len(checksum)}, checksum={checksum}')
        return checksum
