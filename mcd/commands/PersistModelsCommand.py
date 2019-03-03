import hashlib
from pathlib import Path
from modules.commands.BaseCommand import BaseCommand


class PersistModelsCommand(BaseCommand):
    def __init__(self, db_connection_string, execution_id, model_type, base_path, model_patterns, logger=None):
        super().__init__(db_connection_string, logger)
        self._execution_id = execution_id
        self._model_type = model_type
        self._base_path = base_path
        self._model_patterns = model_patterns

    def execute(self):
        model_folder = Path(self._base_path)
        if not model_folder.is_dir():
            raise NotADirectoryError(self._base_path)

        current_model_checksums = {}
        for model_pattern in self._model_patterns:
            for model_file in model_folder.glob(model_pattern):
                if model_file.is_file():
                    current_model_checksums[model_file.stem] = self.__get_file_checksum(model_file)

        data_pipeline_execution = self.repository.save_execution_models(
            self._execution_id, self._model_type, current_model_checksums)
        self.logger.debug(
            'Persisting {model_type} models of data_pipeline_execution = {execution_details}'
            .format(model_type=self._model_type, execution_details=str(data_pipeline_execution)))

    def __get_file_checksum(self, file: Path):
        data = file.read_bytes()
        hash_function = hashlib.sha256()
        hash_function.update(data)
        checksum = hash_function.hexdigest()
        self.logger.debug(f'filename={file.name}, filepath=\'{file.absolute().as_posix()}\'')
        self.logger.debug(f'hash_function={hash_function.name}, checksum_len={len(checksum)}, checksum={checksum}')
        return checksum
