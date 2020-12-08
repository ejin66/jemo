from typing import List
from model import Node


class IParser:

    def parse(self, data: bytes) -> List[Node]:
        raise NotImplementedError
