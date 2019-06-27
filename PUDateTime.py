from datetime import datetime


def iso2str(input_datetime: datetime) -> str:
    """
    Convert Iso Datetime to ISO string that are compliant with file pathing requirement across OS.
    :return:
    """
    iso_datetime_string = input_datetime.isoformat()
    iso_datetime_string_cleaned = iso_datetime_string.replace(":", "")
    return iso_datetime_string_cleaned


def str2iso(input_string: str) -> datetime:
    """
    Convert a specific type of ISO string that are compliant with file pathing requirement to ISO datetime.
    :return:
    """
    iso_datetime = datetime.strptime(input_string, "%Y-%m-%d %H:%M:%S")
    return iso_datetime


def tstr2iso(input_string: str) -> datetime:
    """
    Convert a specific type of ISO string that are compliant with file pathing requirement to ISO datetime.
    :return:
    """
    no_colon_input_string = input_string.replace(":", "")
    iso_datetime = tstr2iso_nocolon(no_colon_input_string)
    return iso_datetime


def tstr2iso_nocolon(input_string: str) -> datetime:
    """
    Convert a specific type of ISO string that are compliant with file pathing requirement to ISO datetime.
    :return:
    """
    iso_datetime = datetime.strptime(input_string, "%Y-%m-%dT%H%M%S")
    return iso_datetime


def iso2tstr(input_datetime: datetime) -> str:
    """
    Convert ISO string that are compliant with file pathing requirement to ISO datetime with T.
    :return:
    """
    iso_datetime_string_cleaned = iso2str(input_datetime)
    iso_datetime_string_t_replaced = iso_datetime_string_cleaned.replace("T", " ")
    return iso_datetime_string_t_replaced
