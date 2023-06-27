from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass()
class Entity(ABC):
    id: int

    @abstractmethod
    def row(self) -> tuple: ...
