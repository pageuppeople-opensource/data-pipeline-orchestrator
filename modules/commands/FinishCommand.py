import hashlib
from pathlib import Path
from modules.commands.BaseCommand import BaseCommand


class FinishCommand(BaseCommand):
    def __init__(self, db_connection_string, execution_id, model_folder_paths, logger=None):
        super().__init__(db_connection_string, logger)
        self._execution_id = execution_id
        self._model_folder_paths = model_folder_paths
        self._model_file_extensions = ['.json', '.csv', '.sql']

    def execute(self):
        model_folders = []
        for model_folder_path in self._model_folder_paths:
            model_folder = Path(model_folder_path)
            if not model_folder.is_dir():
                raise NotADirectoryError(model_folder_path)
            model_folders.append(model_folder)

        all_model_file_checksums = {}
        for model_folder in model_folders:
            model_file_checksums = {}
            for file in model_folder.rglob('*.*'):
                if file.is_file() and file.suffix in self._model_file_extensions:
                    model_file_checksums[file.stem] = self.__get_file_checksum(file)
            all_model_file_checksums[model_folder.name] = model_file_checksums

        data_pipeline_execution = self.repository.finish_execution(self._execution_id,
                                                                   all_model_file_checksums)

        self.logger.debug('Finished data_pipeline_execution = ' + str(data_pipeline_execution))

    def __get_file_checksum(self, file: Path):
        data = file.read_bytes()
        hash_function = hashlib.sha256()
        hash_function.update(data)
        checksum = hash_function.hexdigest()
        self.logger.debug(f'filename={file.name}, filepath=\'{file.absolute().as_posix()}\'')
        self.logger.debug(f'hash_function={hash_function.name}, checksum_len={len(checksum)}, checksum={checksum}')
        return checksum
