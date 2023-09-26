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
    room_list: list

class TablesInterface(ViewBaseInterface):
    files: list

class TableInterface(HTMXBaseInterface):
    table_view: dict
    table_meta: dict


class ExistingUsernameInterface(HTMXBaseInterface):
    status: bool
    message: str