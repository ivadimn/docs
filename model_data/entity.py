from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass()
class Entity(ABC):
    pk: int = None

    @abstractmethod
    def row(self) -> tuple: ...
