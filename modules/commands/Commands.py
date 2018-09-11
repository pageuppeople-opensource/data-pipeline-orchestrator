# inspired by python logging module

UNKNOWN = 0
START = 1

_valueToName = {
    UNKNOWN: 'UNKNOWN',
    START: 'START'
}
_nameToValue = {
    'UNKNOWN': UNKNOWN,
    'START': START
}


def get_name(command_value):
    """
    Return the textual representation of integer command value.

    If the value is one of the predefined values (START) then you get the corresponding string.
    Else, name for the value UNKNOWN is returned.

    If a numeric value corresponding to one of the defined levels is passed
    in, the corresponding string representation is returned.
    """
    result = _valueToName.get(command_value)
    if result is not None:
        return result
    # result = Command._nameToValue.get(command_value)
    # if result is not None:
    #     return result
    return UNKNOWN


def get_value(command_name):
    """
    Return the textual representation of integer command value.

    If the value is one of the predefined values (START) then you get the corresponding string.
    Else, name for the value UNKNOWN is returned.

    If a numeric value corresponding to one of the defined levels is passed
    in, the corresponding string representation is returned.
    """
    # result = Command._valueToName.get(command_name)
    # if result is not None:
    #     return result
    result = _nameToValue.get(command_name)
    if result is not None:
        return result
    return UNKNOWN
