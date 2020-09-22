

import abc
from typing import Any, Dict

class Generator(abc.ABC):
    """ Base generator class.

    """
    def __init__(self, parameters: Dict[str, Any]):
        self._parameters = parameters

    @abc.abstractmethod
    def run(self, /, **kwargs: Any) -> bool:
        """ Run the generator.

        Each setting must be passed by keyword.
        """
        ...

    @abc.abstractmethod
    def description(self) -> str:
        ...

    @abc.abstractmethod
    def help(self) -> str:
        ...

    @abc.abstractmethod
    def any_other_func(self):
        ...

