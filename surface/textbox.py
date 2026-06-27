import pygame.draw
from pygame import Color, Surface
from pygame.constants import K_BACKSPACE, KEYDOWN, MOUSEBUTTONDOWN
from pygame.event import Event
from pygame.font import Font

from surface.defaults import (
    DEFAULT_BORDER_COLOR,
    DEFAULT_BORDER_RADIUS,
    DEFAULT_BORDER_WIDTH,
    DEFAULT_HOVERED_BACKGROUND_COLOR,
    DEFAULT_SELECTED_BACKGROUND_COLOR,
    DEFAULT_TEXT_ANTIALIAS,
    DEFAULT_TEXT_COLOR,
    DEFAULT_TEXT_PADDING,
    DEFAULT_UNHOVERED_BACKGROUND_COLOR,
)

from .component import ClickableComponent
from .types import Position, Size


class Textbox(ClickableComponent):
    def __init__(
        self,
        position: Position,
        size: Size,
        font: Font,
        text_color: Color = DEFAULT_TEXT_COLOR,
        text_antialias: bool = DEFAULT_TEXT_ANTIALIAS,
        unhovered_color: Color = DEFAULT_UNHOVERED_BACKGROUND_COLOR,
        hovered_color: Color = DEFAULT_HOVERED_BACKGROUND_COLOR,
        selected_color: Color = DEFAULT_SELECTED_BACKGROUND_COLOR,
        border_color: Color = DEFAULT_BORDER_COLOR,
        border_width: int = DEFAULT_BORDER_WIDTH,
        border_radius: int = DEFAULT_BORDER_RADIUS,
        text_padding: int = DEFAULT_TEXT_PADDING,
        valid_chars: set[str] | None = None,
    ) -> None:
        super().__init__(position, size)
        self.font = font
        self.text_color = text_color
        self.text_antialias = text_antialias
        self.unhovered_color = unhovered_color
        self.hovered_color = hovered_color
        self.selected_color = selected_color
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius
        self.text_padding = text_padding
        self.valid_chars = valid_chars
        self.is_selected = False
        self.text = ""

    def _is_valid_char(self, char: str) -> bool:
        return self.valid_chars is None or char in self.valid_chars

    def _handle_key_press_event(self, event: Event) -> None:
        if event.key == K_BACKSPACE:
            self.text = self.text[:-1]
        elif not event.unicode:
            return
        elif self._is_valid_char(event.unicode):
            text_width, _ = self.font.size(self.text + event.unicode)
            if text_width < self._rect.width - 2 * self.text_padding:
                self.text += event.unicode

    def update(self, events: list[Event]) -> None:
        super().update(events)
        for event in events:
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                self.is_selected = self.is_hovered()
            elif event.type == KEYDOWN and self.is_selected:
                self._handle_key_press_event(event)

    def render(self, window: Surface) -> None:
        if self.is_selected:
            background_color = self.selected_color
        elif self.is_hovered():
            background_color = self.hovered_color
        else:
            background_color = self.unhovered_color

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

        text_surface = self.font.render(self.text, self.text_antialias, self.text_color)
        text_position = (
            self.position[0] + self.text_padding,
            self.position[1] + (self._rect.height - text_surface.get_height()) // 2,
        )
        window.blit(text_surface, text_position)
