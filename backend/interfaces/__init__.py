from typing import TypedDict, Optional, List


class ViewBaseInterface(TypedDict):
    """
    Base class for all `props` object return by normal views 
    """
    title: Optional[str]


class HTMXBaseInterface(TypedDict):
    """
    Base class for all `props` object return by htmx response
    """


class ValidateFormInterface(HTMXBaseInterface):
    status: bool
    message: str


class DashBoardInterface(ViewBaseInterface):
    files: list
    room_name: str


class TableInterface(HTMXBaseInterface):
    result: dict
    table_name: str
    room_name: str
    alias: Optional[str]


class ExistingUsernameInterface(HTMXBaseInterface):
    status: bool
    message: str