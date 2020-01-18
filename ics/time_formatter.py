import re


def from_iso(dt: str) -> str:
    """
    convert from iso datetime format to icalendar string with the help of regex
    """
    p = re.compile("[-:]")
    string = p.sub("", str(dt))
    p = re.compile(r"\s")
    string = p.sub("T", string)

    return string
