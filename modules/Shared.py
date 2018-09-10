import logging
import argparse


appVersion = '0.0.1'  # TODO: where to read-this-from?

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
                        help=f'logging output level - choose from {", ".join(logLevelStrings)}; '
                             f'default is {defaultLogLevelString}')

    group = parser.add_mutually_exclusive_group()

    group.add_argument('-q', '--quiet',
                       action='store_true',
                       help='enable quiet execution')

    group.add_argument('-v', '--verbose',
                       action='store_true',
                       help='enable verbose execution')

    return parser


def get_log_level_int_from_string(log_level_string):
    if log_level_string not in logLevelStrings:
        message = f'invalid choice: {log_level_string} (choose from {", ".join(logLevelStrings)})'
        raise argparse.ArgumentTypeError(message)

    log_level_int = getattr(logging, log_level_string, logging.INFO)

    # check the logging log_level_choices have not changed from our expected values
    assert isinstance(log_level_int, int)

    return log_level_int
