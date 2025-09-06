from abc import ABC, abstractmethod

class Led(ABC):
    @abstractmethod
    def on(self) -> None:
        pass

    @abstractmethod
    def off(self) -> None:
        pass

    @abstractmethod
    def toggle(self) -> None:
        pass