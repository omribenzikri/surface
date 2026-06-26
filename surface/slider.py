import pygame.draw
import pygame.mouse
from pygame import Color, Surface
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP
from pygame.event import Event

from .component import Component
from .types import Position


class Slider(Component):
    def __init__(
        self,
        position: Position,
        step_count: int,
        step_width: int,
        height: int,
        initial_value: int = 1,
        bar_color: Color = Color("white"),
        bar_border_color: Color = Color("gray"),
        bar_border_width: int = 3,
        bar_border_radius: int = 4,
        unhovered_thumb_color: Color = Color((50, 50, 50)),
        hovered_thumb_color: Color = Color((100, 100, 100)),
        thumb_width: int = 10,
        thumb_vertical_overflow: int = 5,
        thumb_border_radius: int = 3,
        thumb_edge_padding: int = 5,
    ) -> None:
        width = step_count * step_width + 2 * thumb_edge_padding
        super().__init__(position, (width, height))

        self.bar_color = bar_color
        self.bar_border_color = bar_border_color
        self.bar_border_width = bar_border_width
        self.bar_border_radius = bar_border_radius
        self.hovered_thumb_color = hovered_thumb_color
        self.unhovered_thumb_color = unhovered_thumb_color
        self.thumb_border_radius = thumb_border_radius

        self._step_count = step_count
        self._step_width = step_width
        self._is_selected = False
        self._value = initial_value

        self._thumb_left_bound = self._rect.left + thumb_edge_padding
        self._thumb_right_bound = self._rect.right - thumb_edge_padding

        initial_x = self._value_to_x(initial_value)
        thumb_x = initial_x - thumb_width // 2
        thumb_y = position[1] - thumb_vertical_overflow
        self._thumb_rect = pygame.rect.Rect(
            thumb_x,
            thumb_y,
            thumb_width,
            self._rect.height + thumb_vertical_overflow * 2,
        )

    @property
    def is_selected(self) -> bool:
        return self._is_selected

    @property
    def value(self) -> int:
        return self._value

    @property
    def step_count(self) -> int:
        return self._step_count

    @property
    def step_width(self) -> int:
        return self._step_width

    def thumb_is_hovered(self) -> bool:
        return self._thumb_rect.collidepoint(pygame.mouse.get_pos())

    def _value_to_x(self, value: int) -> int:
        span = self._thumb_right_bound - self._thumb_left_bound
        t = (value - 1) / max(self._step_count - 1, 1)
        return round(self._thumb_left_bound + t * span)

    def _x_to_value(self, x: int) -> int:
        span = self._thumb_right_bound - self._thumb_left_bound
        if span == 0:
            return 1
        t = (x - self._thumb_left_bound) / span
        step = round(t * (self._step_count - 1))
        return step + 1

    def _clamped_mouse_x(self) -> int:
        mouse_x = pygame.mouse.get_pos()[0]
        return max(self._thumb_left_bound, min(self._thumb_right_bound, mouse_x))

    def update(self, events: list[Event]) -> None:
        for event in events:
            if (
                event.type == MOUSEBUTTONDOWN
                and event.button == 1
                and self.thumb_is_hovered()
            ):
                self._is_selected = True
            elif event.type == MOUSEBUTTONUP and event.button == 1:
                if self._is_selected:
                    snapped_value = self._x_to_value(self._thumb_rect.centerx)
                    snapped_x = self._value_to_x(snapped_value)
                    self._thumb_rect.centerx = snapped_x
                    self._value = snapped_value
                self._is_selected = False

        if self._is_selected:
            self._thumb_rect.centerx = self._clamped_mouse_x()

    def render(self, window: Surface) -> None:
        thumb_color = (
            self.hovered_thumb_color
            if self._is_selected or self.thumb_is_hovered()
            else self.unhovered_thumb_color
        )
        pygame.draw.rect(
            surface=window,
            color=self.bar_color,
            rect=self._rect,
            border_radius=self.bar_border_radius,
        )
        pygame.draw.rect(
            surface=window,
            color=self.bar_border_color,
            rect=self._rect,
            width=self.bar_border_width,
            border_radius=self.bar_border_radius,
        )
        pygame.draw.rect(
            surface=window,
            color=thumb_color,
            rect=self._thumb_rect,
            border_radius=self.thumb_border_radius,
        )
