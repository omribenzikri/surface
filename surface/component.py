from abc import ABC, abstractmethod

import pygame.mouse
from pygame import Rect, Surface
from pygame.constants import MOUSEBUTTONDOWN
from pygame.event import Event

from .types import Position, Size


class Component(ABC):
    def __init__(self, position: Position, size: Size) -> None:
        self._rect = Rect(*position, *size)

    @property
    def position(self) -> Position:
        return self._rect.topleft

    @property
    def size(self) -> Size:
        return self._rect.size

    @position.setter
    def position(self, new_position: Position) -> None:
        self._rect.topleft = new_position

    @abstractmethod
    def update(self, events: list[Event]) -> None: ...

    @abstractmethod
    def render(self, window: Surface) -> None: ...


class ClickableComponent(Component, ABC):
    def __init__(self, position: Position, size: Size) -> None:
        super().__init__(position, size)
        self._is_clicked = False

    def is_hovered(self) -> bool:
        return self._rect.collidepoint(pygame.mouse.get_pos())

    def is_clicked(self) -> bool:
        return self._is_clicked

    def update(self, events: list[Event]) -> None:
        self._is_clicked = False
        for event in events:
            if (
                self.is_hovered()
                and event.type == MOUSEBUTTONDOWN
                and event.button == 1
            ):
                self._is_clicked = True
