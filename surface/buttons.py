import pygame.draw
import pygame.image
from pygame import Color, Surface
from pygame.font import Font

from .component import ClickableComponent
from .defaults import (
    DEFAULT_BORDER_COLOR,
    DEFAULT_BORDER_RADIUS,
    DEFAULT_BORDER_WIDTH,
    DEFAULT_HOVERED_BACKGROUND_COLOR,
    DEFAULT_TEXT_ANTIALIAS,
    DEFAULT_TEXT_COLOR,
    DEFAULT_TEXT_PADDING,
    DEFAULT_UNHOVERED_BACKGROUND_COLOR,
)
from .types import Position, Size


class TextButton(ClickableComponent):
    def __init__(
        self,
        text: str,
        font: Font,
        position: Position,
        size: Size | None = None,
        text_color: Color = DEFAULT_TEXT_COLOR,
        unhovered_background_color: Color = DEFAULT_UNHOVERED_BACKGROUND_COLOR,
        hovered_background_color: Color = DEFAULT_HOVERED_BACKGROUND_COLOR,
        border_color: Color = DEFAULT_BORDER_COLOR,
        border_width: int = DEFAULT_BORDER_WIDTH,
        border_radius: int = DEFAULT_BORDER_RADIUS,
        text_padding: int = DEFAULT_TEXT_PADDING,
        text_antialias: bool = DEFAULT_TEXT_ANTIALIAS,
    ) -> None:
        text_width, text_height = font.size(text)
        text_size_with_padding = (
            text_width + text_padding * 2,
            text_height + text_padding * 2,
        )
        rect_size = size if size is not None else text_size_with_padding
        super().__init__(position, rect_size)

        self._font = font
        self._text = text

        self.text_color = text_color
        self.unhovered_background_color = unhovered_background_color
        self.hovered_background_color = hovered_background_color
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius
        self.text_padding = text_padding
        self.text_antialias = text_antialias
        self.has_fixed_size = size is not None

    @property
    def font(self) -> Font:
        return self._font

    @font.setter
    def font(self, new_font: Font) -> None:
        self._font = new_font
        if not self.has_fixed_size:
            self._update_rect_size()

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, new_text: str) -> None:
        self._text = new_text
        if not self.has_fixed_size:
            self._update_rect_size()

    def render(self, window: Surface) -> None:
        background_color = (
            self.hovered_background_color
            if self.is_hovered()
            else self.unhovered_background_color
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
        text_surface = self._font.render(
            self._text, self.text_antialias, self.text_color
        )
        text_position = (
            self._rect.x + (self._rect.width - text_surface.get_width()) // 2,
            self._rect.y + (self._rect.height - text_surface.get_height()) // 2,
        )
        window.blit(text_surface, text_position)

    def _update_rect_size(self) -> None:
        text_width, text_height = self.font.size(self.text)
        self._rect.size = (
            text_width + self.text_padding * 2,
            text_height + self.text_padding * 2,
        )


class ImageButton(ClickableComponent):
    def __init__(
        self, unhovered_image_path: str, hovered_image_path: str, position: Position
    ) -> None:
        self._unhovered_image = pygame.image.load(unhovered_image_path)
        self._hovered_image = pygame.image.load(hovered_image_path)

        hovered_width, hovered_height = self._hovered_image.get_size()
        unhovered_width, unhovered_height = self._unhovered_image.get_size()
        rect_size = (
            max(hovered_width, unhovered_width),
            max(hovered_height, unhovered_height),
        )
        super().__init__(position, rect_size)

    def render(self, window: Surface) -> None:
        window.blit(
            self._hovered_image if self.is_hovered() else self._unhovered_image,
            self.position,
        )
