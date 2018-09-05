import argparse
import logging


class ModelChangeDetector:

    _appName = 'model-change-detector'
    _appVersion = '0.0.1'
    _log_level_strings = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG']

    _executionModes = ['NEW']

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)

    def main(self):
        args = ModelChangeDetector.get_arguments()

    @staticmethod
    def get_arguments():
        parser = argparse.ArgumentParser(prog=ModelChangeDetector._appName,
                                         description=ModelChangeDetector._appName,
                                         parents=[ModelChangeDetector.get_default_arguments(
                                             ModelChangeDetector._appName,
                                             ModelChangeDetector._appVersion)])
        # parser.add_argument('--version',
        #                     action='version',
        #                     version='{0} {1}'.format(parser.prog, ModelChangeDetector._appVersion))

        # group = parser.add_mutually_exclusive_group()
        # group.add_argument('-q', '--quiet', action='store_true', help='Enable quiet execution')
        # group.add_argument('-v', '--verbose', action='store_true', help='Enable verbose execution')

        parser.add_argument('mode',
                            action='store',
                            metavar='mode',
                            # help= f'Sets the execution mode, choose from {ModelChangeDetector._executionModes}')
                            help='Sets the execution mode, choose from \'{0}\''.format("', '".join(ModelChangeDetector._executionModes)))

        # parser.add_argument('destination-engine', metavar='',
        #                     help='The destination engine. Eg: postgresql+psycopg2://postgres:xxxx@localhost/dest_dw')

        # parser.add_argument('-l', '--log-level',
        #                     action='store',
        #                     default='INFO',
        #                     metavar='',
        #                     # type=self.log_level_string_to_int,
        #                     nargs='?',
        #                     help='Level of logging output, choose from {0}'.format(ModelChangeDetector._logLevels))

        args = parser.parse_args()
        return args

    @staticmethod
    def get_default_arguments(app_name, app_version):
        parser = argparse.ArgumentParser(add_help=False)

        parser.add_argument('-v', '--version',
                            action='version',
                            version='{0} {1}'.format(app_name, app_version))

        parser.add_argument('-l', '--log-level',
                            action='store',
                            const='INFO',
                            default='INFO',
                            metavar='',
                            type=ModelChangeDetector.get_log_level_int_from_string,
                            nargs='?',
                            help='Level of logging output, choose from \'{0}\''.format(
                                "', '".join(ModelChangeDetector._log_level_strings)))

        # group = parser.add_mutually_exclusive_group()
        #
        # group.add_argument('-q', '--quiet',
        #                    action='store_true',
        #                    help='Enable quiet execution')
        #
        # group.add_argument('-v', '--verbose',
        #                    action='store_true',
        #                    help='Enable verbose execution')

        return parser

    @staticmethod
    def get_log_level_int_from_string(log_level_string):
        if log_level_string not in ModelChangeDetector._log_level_strings:
            message = 'invalid choice: {0} (choose from \'{1}\')'.format(
                log_level_string, "', '".join(ModelChangeDetector._log_level_strings))
            raise argparse.ArgumentTypeError(message)

        log_level_int = getattr(logging, log_level_string, logging.INFO)
        # check the logging log_level_choices have not changed from our expected values
        assert isinstance(log_level_int, int)

        return log_level_int

