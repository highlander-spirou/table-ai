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

class ExistingRoomInterface(HTMXBaseInterface):
    status: bool
    message: str