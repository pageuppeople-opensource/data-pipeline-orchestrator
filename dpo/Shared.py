import logging
import argparse
from sqlalchemy.ext.declarative import declarative_base

BaseEntity = declarative_base()


class Constants:
    APP_NAME = 'data-pipeline-orchestrator'
    DATA_PIPELINE_EXECUTION_SCHEMA_NAME = 'dpo'
    NO_LAST_SUCCESSFUL_EXECUTION = 'NO_LAST_SUCCESSFUL_EXECUTION'

    class DataPipelineExecutionStatus:
        INITIALISED = 'INITIALISED'
        IN_PROGRESS = 'IN_PROGRESS'
        COMPLETED = 'COMPLETED'

    class ModelType:
        LOAD = 'LOAD'
        TRANSFORM = 'TRANSFORM'


MODEL_TYPES = [Constants.ModelType.LOAD, Constants.ModelType.TRANSFORM]

_logLevelStrings = [logging.getLevelName(logging.CRITICAL),
                    logging.getLevelName(logging.ERROR),
                    logging.getLevelName(logging.WARNING),
                    logging.getLevelName(logging.INFO),
                    logging.getLevelName(logging.DEBUG)]

_defaultLogLevelString = logging.getLevelName(logging.INFO)


def configure_root_logger(log_level):
    # get the root logger
    logger = logging.getLogger()

    # set the given log level
    logger.setLevel(log_level)

    # and one handler, at the same log level, with appropriate formatting
    console_stream_handler = logging.StreamHandler()
    console_stream_handler.setLevel(log_level)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_stream_handler.setFormatter(formatter)
    logger.addHandler(console_stream_handler)

    return


def get_default_arguments():
    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('-l', '--log-level',
                        action='store',
                        const=_defaultLogLevelString,
                        default=_defaultLogLevelString,
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
