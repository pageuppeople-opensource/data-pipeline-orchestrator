# inspired by the python logging module

UNKNOWN = 'UNKNOWN'
START = 'START'
FINISH = 'FINISH'

_valueToName = {
    UNKNOWN: 'UNKNOWN',
    START: 'START',
    FINISH: 'FINISH',
}
_nameToValue = {
    'UNKNOWN': UNKNOWN,
    'START': START,
    'FINISH': FINISH,
}


def get_name(command_value):
    """
    Return the textual representation of numeric command value.

    If the value is one of the predefined values then you get the corresponding string name.
    Else, name for the value UNKNOWN is returned.
    """
    result = _valueToName.get(command_value.upper())

    if result is not None:
        return result

    return get_value('UNKNOWN')


def get_value(command_name):
    """
    Return the numeric representation of textual command name.

    If the name is one of the predefined names then you get the corresponding numeric value.
    Else, value for the name UNKNOWN is returned.
    """
    result = _nameToValue.get(command_name.upper())

    if result is not None:
        return result

    return get_name(UNKNOWN)
