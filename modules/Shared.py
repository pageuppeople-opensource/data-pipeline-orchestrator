import logging
import argparse


class Constants:
    APP_NAME = 'model-change-detector'
    DATA_PIPELINE_EXECUTION_SCHEMA_NAME = 'data_pipeline'

    class DataPipelineExecutionStatus:
        STARTED = 1
        COMPLETED_SUCCESSFULLY = 0


appVersion = '0.0.1'  # where to do version-ing and then, read this from there?

_logLevelStrings = [logging.getLevelName(logging.CRITICAL),
                    logging.getLevelName(logging.ERROR),
                    logging.getLevelName(logging.WARNING),
                    logging.getLevelName(logging.INFO),
                    logging.getLevelName(logging.DEBUG)]

_defaultLogLevelString = logging.getLevelName(logging.INFO)


def configure_root_logger(log_level):
    # get the root logger
    logger = logging.getLogger()

    # with the given log level
    logger.setLevel(logging.DEBUG)

    # and one handler, at the same log level
    console_stream_handler = logging.StreamHandler()
    console_stream_handler.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_stream_handler.setFormatter(formatter)
    logger.addHandler(console_stream_handler)

    return


def get_default_arguments(app_name, app_version):
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('-v', '--version',
                        action='version',
                        version=f'{app_name} {app_version}')

    parser.add_argument('-l', '--log-level',
                        action='store',
                        const=_defaultLogLevelString,
                        default=_defaultLogLevelString,
                        metavar=",".join(_logLevelStrings),
                        type=get_log_level_int_from_string,
                        nargs='?',
                        help=f'choose program\'s logging level, from {", ".join(_logLevelStrings)}; '
                             f'default is {_defaultLogLevelString}')

    return parser


def get_log_level_int_from_string(log_level_string):
    if log_level_string not in _logLevelStrings:
        message = f'invalid choice: {log_level_string} (choose from {", ".join(_logLevelStrings)})'
        raise argparse.ArgumentTypeError(message)

    log_level_int = getattr(logging, log_level_string, logging.getLevelName(_defaultLogLevelString))

    # check the logging log_level_choices have not changed from our expected values
    assert isinstance(log_level_int, int)

    return log_level_int
