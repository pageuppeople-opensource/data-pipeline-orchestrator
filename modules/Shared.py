import logging
import argparse


appVersion = '0.0.1'  # where to do version-ing and then, read this from there?

args = None

logLevelStrings = [logging.getLevelName(logging.CRITICAL),
                   logging.getLevelName(logging.ERROR),
                   logging.getLevelName(logging.WARNING),
                   logging.getLevelName(logging.INFO),
                   logging.getLevelName(logging.DEBUG)]

defaultLogLevelString = logging.getLevelName(logging.INFO)


def configure_logging(logger, log_level):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_stream_handler = logging.StreamHandler()
    console_stream_handler.setFormatter(formatter)

    logger.addHandler(console_stream_handler)
    logger.setLevel(log_level)

    return


def write_output(object, verbose):
    if(verbose):
        print(object)


def get_default_arguments(app_name, app_version):
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('-V', '--version',
                        action='version',
                        version=f'{app_name} {app_version}')

    parser.add_argument('-l', '--log-level',
                        action='store',
                        const=defaultLogLevelString,
                        default=defaultLogLevelString,
                        metavar=",".join(logLevelStrings),
                        type=get_log_level_int_from_string,
                        nargs='?',
                        help=f'choose program\'s logging level, from {", ".join(logLevelStrings)}; '
                             f'default is {defaultLogLevelString}')

    group = parser.add_mutually_exclusive_group()

    group.add_argument('-q', '--quiet',
                       action='store_true',
                       help='enable quiet execution, give less output.')

    group.add_argument('-v', '--verbose',
                       action='store_true',
                       help='enable verbose execution, give more output.')

    return parser


def get_log_level_int_from_string(log_level_string):
    if log_level_string not in logLevelStrings:
        message = f'invalid choice: {log_level_string} (choose from {", ".join(logLevelStrings)})'
        raise argparse.ArgumentTypeError(message)

    log_level_int = getattr(logging, log_level_string, logging.INFO)

    # check the logging log_level_choices have not changed from our expected values
    assert isinstance(log_level_int, int)

    return log_level_int


class Constants:
    APP_NAME = 'model-change-detector'
    DATA_PIPELINE_EXECUTION_SCHEMA_NAME = 'data_pipeline'

    class DataPipelineExecutionStatus:
        STARTED = 1
        COMPLETED_SUCCESSFULLY = 0
