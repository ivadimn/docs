from abc import ABC, abstractmethod
from PyQt6.QtWidgets import QTableView


class View(QTableView):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setSelectionBehavior(self.SelectionBehavior.SelectRows)
        self.setSelectionMode(self.SelectionMode.SingleSelection)
        self.setWordWrap(False)

        vh = self.verticalHeader()
        vh.setSectionResizeMode(vh.ResizeMode.Fixed)

        hh = self.horizontalHeader()
        hh.setSectionResizeMode(hh.ResizeMode.ResizeToContents)

    @abstractmethod
    def add(self) -> None: ...

    @abstractmethod
    def update(self) -> None: ...

    @abstractmethod
    def delete(self) -> None: ...