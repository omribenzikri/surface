import pygame.draw
from pygame import Color, Surface
from pygame.event import Event

from surface.defaults import (
    DEFAULT_BORDER_COLOR,
    DEFAULT_BORDER_RADIUS,
    DEFAULT_BORDER_WIDTH,
    DEFAULT_HOVERED_BACKGROUND_COLOR,
    DEFAULT_UNHOVERED_BACKGROUND_COLOR,
)

from .component import ClickableComponent
from .types import Position, Size


class Checkbox(ClickableComponent):
    def __init__(
        self,
        position: Position,
        size: Size,
        unhovered_color: Color = DEFAULT_UNHOVERED_BACKGROUND_COLOR,
        hovered_color: Color = DEFAULT_HOVERED_BACKGROUND_COLOR,
        border_color: Color = DEFAULT_BORDER_COLOR,
        border_width: int = DEFAULT_BORDER_WIDTH,
        border_radius: int = DEFAULT_BORDER_RADIUS,
        cross_color: Color = Color("white"),
        cross_width: int = 3,
        cross_padding: int = 6,
    ) -> None:
        super().__init__(position, size)
        self.unhovered_color = unhovered_color
        self.hovered_color = hovered_color
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius
        self.cross_color = cross_color
        self.cross_width = cross_width
        self.cross_padding = cross_padding
        self.is_checked = False

    def update(self, events: list[Event]) -> None:
        super().update(events)
        if self.is_clicked():
            self.is_checked = not self.is_checked

    def render(self, window: Surface) -> None:
        background_color = (
            self.hovered_color if self.is_hovered() else self.unhovered_color
        )
        pygame.draw.rect(
            surface=window,
            color=background_color,
            rect=self._rect,
            border_radius=self.border_radius,
        )
        pygame.draw.rect(
            surface=window,
            color=self.border_color,
            rect=self._rect,
            width=self.border_width,
            border_radius=self.border_radius,
        )
        if self.is_checked:
            self._render_cross(window)

    def _render_cross(self, window: Surface) -> None:
        cross_top_left = (
            self._rect.x + self.cross_padding,
            self._rect.y + self.cross_padding,
        )
        cross_top_right = (
            self._rect.x + self._rect.width - self.cross_padding,
            self._rect.y + self.cross_padding,
        )
        cross_bottom_left = (
            self._rect.x + self.cross_padding,
            self._rect.y + self._rect.height - self.cross_padding,
        )
        cross_bottom_right = (
            self._rect.x + self._rect.width - self.cross_padding,
            self._rect.y + self._rect.height - self.cross_padding,
        )
        pygame.draw.line(
            window,
            self.cross_color,
            cross_top_left,
            cross_bottom_right,
            self.cross_width,
        )
        pygame.draw.line(
            window,
            self.cross_color,
            cross_top_right,
            cross_bottom_left,
            self.cross_width,
        )
