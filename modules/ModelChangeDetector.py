import argparse
import logging
import uuid

class ModelChangeDetector(object):

    _appName = 'model-change-detector'  # TODO: where to save-this and read-this-from?
    _appVersion = '0.0.1'  # TODO: where to save-this and read-this-from?

    # may need to become something like logging.INFO etc. which are integers with corresponding strings.. or may not :S
    _executionModes = ['NEW']

    def __init__(self, logger=None):
        self.logger = logger or logging.getLogger(__name__)
        self._logLevelStrings = [logging.getLevelName(logging.CRITICAL),
                                logging.getLevelName(logging.ERROR),
                                logging.getLevelName(logging.WARNING),
                                logging.getLevelName(logging.INFO),
                                logging.getLevelName(logging.DEBUG)]
        self._defaultLogLevelString = logging.getLevelName(logging.INFO)

    def main(self):
        args = self.get_arguments()
        self.configure_logging(args.log_level)

        # TODO add logic to
        # - figure out how to separate args.execution_mode code/logic.. a class per execution-mode? IExecutionMode.Execute(...)? DI?
        # - connect to db using args.db_connection_string and add a record to DataPipelineExecution table with str(uuid.uuid4())
        execution_result = str(uuid.uuid4())
        
        if args.verbose:
            print(args)
            print(f'args.log_level = {args.log_level} = {logging.getLevelName(args.log_level)}')
            print(self.logger)
            print(f'execution_result = {execution_result}')
        return execution_result

    def configure_logging(self, log_level):
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        console_stream_handler = logging.StreamHandler()
        console_stream_handler.setFormatter(formatter)
        self.logger.addHandler(console_stream_handler)
        self.logger.setLevel(log_level)
        return

    def get_arguments(self):
        parser = argparse.ArgumentParser(description=ModelChangeDetector._appName,
                                         parents=[self.get_default_arguments(
                                             ModelChangeDetector._appName,
                                             ModelChangeDetector._appVersion)])

        parser.add_argument('execution_mode',
                            action='store',
                            # metavar='execution-mode',
                            choices=ModelChangeDetector._executionModes,
                            help='execution mode; choose from {0}'.format(", ".join(ModelChangeDetector._executionModes)))

        parser.add_argument('db_connection_string',
                            metavar='db-connection-string',
                            help='database connection string, e.g. postgresql+psycopg2://postgres:xxxx@localhost/dest_dw')

        args = parser.parse_args()
        return args

    def get_default_arguments(self, app_name, app_version):
        parser = argparse.ArgumentParser(add_help=False)

        parser.add_argument('-v', '--version',
                            action='version',
                            version='{0} {1}'.format(app_name, app_version))

        parser.add_argument('-l', '--log-level',
                            action='store',
                            const=self._defaultLogLevelString,
                            default=self._defaultLogLevelString,
                            metavar=",".join(self._logLevelStrings),
                            type=self.get_log_level_int_from_string,
                            nargs='?',
                            help='logging output level - choose from {0}; default is {1}'.format(
                                ", ".join(self._logLevelStrings), self._defaultLogLevelString))

        group = parser.add_mutually_exclusive_group()

        group.add_argument('-Q', '--quiet',
                           action='store_true',
                           help='enable quiet execution')

        group.add_argument('-V', '--verbose',
                           action='store_true',
                           help='enable verbose execution')

        return parser

    def get_log_level_int_from_string(self, log_level_string):
        if log_level_string not in self._logLevelStrings:
            message = 'invalid choice: {0} (choose from {1})'.format(
                log_level_string, ", ".join(self._logLevelStrings))
            raise argparse.ArgumentTypeError(message)

        log_level_int = getattr(logging, log_level_string, logging.INFO)
   
        # check the logging log_level_choices have not changed from our expected values
        assert isinstance(log_level_int, int)

        return log_level_int
