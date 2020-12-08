from typing import List
from model import Node


class IGenerator:

    def generate(self, root: List[Node]) -> str:
        raise NotImplementedError
