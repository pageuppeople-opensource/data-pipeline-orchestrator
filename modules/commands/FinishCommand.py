import hashlib
import argparse
from pathlib import Path
from modules.commands.BaseCommand import BaseCommand


class FinishCommand(BaseCommand):
    _execution_id: str
    _models_folder_path: str
    _models_file_pattern: str

    def __init__(self, db_connection_string, execution_id, models_folder_path, logger=None):
        super().__init__(db_connection_string, logger)
        self._execution_id = execution_id
        self._models_folder_path = models_folder_path
        self._models_file_pattern = '*.sql'

    def execute(self):
        models_folder = Path(self._models_folder_path)
        if not models_folder.is_dir():
            raise argparse.ArgumentError(f'Given \'models_folder_path\' of {self._models_folder_path} is not a '
                                         f'directory.')

        file_checksums = {}
        for file in models_folder.rglob(self._models_file_pattern):
            file_name = file.name
            file_checksum = self.__get_file_checksum(file)
            file_checksums[file_name] = file_checksum

        data_pipeline_execution = self.repository.finish_existing(self._execution_id, file_checksums)
        self.logger.debug('Finished data_pipeline_execution = ' + str(data_pipeline_execution))

    def __get_file_checksum(self, file: Path):
        data = file.read_bytes()
        hash_function = hashlib.sha256()
        hash_function.update(data)
        checksum = hash_function.hexdigest()
        self.logger.debug('\nfilename={0}, filepath=\'{1}\''.format(file.name, file.absolute().as_posix()))
        self.logger.debug('hash_function={0}, checksum_len={1}, checksum={2}'.format(hash_function.name, len(checksum), checksum))
        return checksum
