
from typing import Any, Dict

import generator

class Pythia8(generator.Generator):
    """ Base generator class.

    """
    def __init__(self, parameters: Dict[str, Any]):
        self._parameters = parameters

    def run(self, *args: Any, **kwargs: Any) -> bool:
        return "Run pythia8"

    @classmethod
    def description(self) -> str:
        return "Pythia 8"

    def help(self) -> str:
        return "Pythia8 help"

    def any_other_func(self):
        ...

